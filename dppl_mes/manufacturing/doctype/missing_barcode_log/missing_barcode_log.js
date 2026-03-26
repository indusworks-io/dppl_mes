// Copyright (c) 2026, IndusWorks and contributors
// For license information, please see license.txt

frappe.ui.form.on("Missing Barcode Log", {
	onload: function(frm) {
		// Initialize form state
	},
	refresh: function(frm) {
		// Remove existing button to avoid duplicates
		frm.remove_custom_button(__('Add Multiple Missing Barcodes'));

		// Add custom button for bulk add
		frm.add_custom_button(__('Add Multiple Missing Barcodes'), () => {
			show_bulk_add_dialog(frm);
		});
	},

	// Calculate ending_barcode when starting_barcode changes
	starting_barcode: function(frm) {
		if (frm.doc.starting_barcode) {
			const number = extract_barcode_number(frm.doc.starting_barcode);
			if (number !== null) {
				frm.set_value("starting_barcode_number", number);
				calculate_ending_barcode(frm);
				frm.save();
			}
		}
	},

	// Recalculate ending_barcode when pack_size changes
	pack_size: function(frm) {
		if (frm.doc.starting_barcode_number && frm.doc.pack_size) {
			calculate_ending_barcode(frm);
			frm.save();
		}
	},

	// Handle barcode scanning
	scan_missing_barcode: function(frm) {
		const barcode = frm.doc.scan_missing_barcode ? frm.doc.scan_missing_barcode.trim() : "";

		// Exit if no value
		if (!barcode) {
			return;
		}

		// Extract barcode number
		const barcode_number = extract_barcode_number(barcode);

		if (barcode_number === null) {
			show_message(frm, `Invalid barcode: ${barcode}`, true);
			frm.set_value("scan_missing_barcode", "");
			return;
		}

		// Check if barcode already exists
		if (is_duplicate_barcode(frm, barcode)) {
			show_message(frm, `${barcode} already exists in missing barcode list`, true);
		} else {
			add_missing_barcode(frm, barcode, barcode_number);
			show_message(frm, `${barcode} Added In Missing Barcode List`, false);
		}

		// Clear the scan field
		frm.set_value("scan_missing_barcode", "");
		frm.save();

		// Return focus to scan field for continuous scanning
		setTimeout(() => {
			if (frm.fields_dict.scan_missing_barcode) {
				frm.fields_dict.scan_missing_barcode.set_focus();
			}
		}, 500);
	}
});

/**
 * Extract numeric portion from barcode string using regex
 * Handles various barcode formats:
 * - Trailing numbers: "XX00012345" -> 12345
 * - Leading numbers: "00012345XX" -> 12345
 * - Mixed: "AB00012345XX" -> 12345
 * - X in middle: "AB000XX12345" -> 12345
 *
 * @param {string} barcode - The barcode string
 * @returns {number|null} - Extracted number as integer, or null if not found
 */
function extract_barcode_number(barcode) {
	if (!barcode || typeof barcode !== "string") {
		return null;
	}

	// Find all sequences of digits in the barcode
	const matches = barcode.match(/\d+/g);

	if (matches && matches.length > 0) {
		// Take the last (rightmost) sequence of digits
		const lastSequence = matches[matches.length - 1];
		return parseInt(lastSequence, 10);
	}

	return null;
}

/**
 * Reconstruct barcode by replacing the numeric portion with new_number
 * Preserves prefix, zeros padding, and suffix from starting_barcode
 *
 * Examples:
 * - reconstruct_barcode("00012345XX", 12500) -> "00012500XX"
 * - reconstruct_barcode("AB00012345XX", 12500) -> "AB00012500XX"
 * - reconstruct_barcode("AB000XX12345", 12500) -> "AB000XX12500"
 *
 * @param {string} starting_barcode - The original barcode string
 * @param {number} new_number - The new numeric value to insert
 * @returns {string} - Reconstructed barcode string
 */
function reconstruct_barcode(starting_barcode, new_number) {
	if (!starting_barcode || typeof starting_barcode !== "string") {
		return "";
	}

	// Find all sequences of digits and their positions
	const regex = /\d+/g;
	const matches = [];
	let match;

	while ((match = regex.exec(starting_barcode)) !== null) {
		matches.push({
			value: match[0],
			index: match.index,
			length: match[0].length
		});
	}

	if (matches.length === 0) {
		return starting_barcode;
	}

	// Get the last (rightmost) numeric sequence
	const lastMatch = matches[matches.length - 1];

	// Extract prefix and suffix
	const prefix = starting_barcode.substring(0, lastMatch.index);
	const suffix = starting_barcode.substring(lastMatch.index + lastMatch.length);

	// Pad the new number with leading zeros to match original length
	const paddedNumber = String(new_number).padStart(lastMatch.length, '0');

	return prefix + paddedNumber + suffix;
}

/**
 * Calculate ending_barcode and ending_barcode_number based on
 * starting_barcode_number and pack_size
 *
 * @param {object} frm - The form object
 */
function calculate_ending_barcode(frm) {
	const starting_barcode_number = parseInt(frm.doc.starting_barcode_number) || 0;
	const pack_size = parseInt(frm.doc.pack_size) || 0;

	if (starting_barcode_number > 0 && pack_size > 0) {
		const ending_number = starting_barcode_number + pack_size - 1;
		frm.set_value("ending_barcode_number", ending_number);

		if (frm.doc.starting_barcode) {
			const ending_barcode = reconstruct_barcode(frm.doc.starting_barcode, ending_number);
			frm.set_value("ending_barcode", ending_barcode);
		}
	} else {
		frm.set_value("ending_barcode_number", 0);
		frm.set_value("ending_barcode", "");
	}
}

/**
 * Check if barcode already exists in missing_barcode_list
 *
 * @param {object} frm - The form object
 * @param {string} barcode - The barcode string to check
 * @returns {boolean} - True if duplicate found
 */
function is_duplicate_barcode(frm, barcode) {
	if (!frm.doc.missing_barcode_list || frm.doc.missing_barcode_list.length === 0) {
		return false;
	}

	return frm.doc.missing_barcode_list.some(function(row) {
		return row.barcode === barcode;
	});
}

/**
 * Add a new barcode to the missing_barcode_list child table
 *
 * @param {object} frm - The form object
 * @param {string} barcode - The full barcode string
 * @param {number} barcode_number - The extracted numeric portion
 */
function add_missing_barcode(frm, barcode, barcode_number) {
	frm.add_child("missing_barcode_list", {
		barcode: barcode,
		barcode_number: barcode_number
	});
	frm.refresh_field("missing_barcode_list");
}

/**
 * Display message in the message field with appropriate color
 *
 * @param {object} frm - The form object
 * @param {string} text - The message text to display
 * @param {boolean} is_error - True for error (red), False for success (green)
 */
function show_message(frm, text, is_error) {
	const color = is_error ? "#dc3545" : "#198754"; // red / green

	const html = `
		<div style="
			padding: 12px;
			border-radius: 4px;
			background-color: ${is_error ? "#f8d7da" : "#d1e7dd"};
			border: 1px solid ${color};
			color: ${color};
			font-weight: 600;
			text-align: center;
		">
			${text}
		</div>
	`;

	if (frm.fields_dict.message) {
		frm.fields_dict.message.$wrapper.html(html);
	}
}

/**
 * Show dialog for adding multiple missing barcodes in a range
 *
 * @param {object} frm - The form object
 */
function show_bulk_add_dialog(frm) {
	frappe.prompt([
		{
			fieldname: "starting_missing_barcode",
			label: __("Starting Missing Barcode"),
			fieldtype: "Data",
			reqd: 1,
			description: __("Enter or scan the first barcode of the missing range")
		},
		{
			fieldname: "ending_missing_barcode",
			label: __("Ending Missing Barcode"),
			fieldtype: "Data",
			reqd: 1,
			description: __("Enter or scan the last barcode of the missing range")
		}
	],
	function(values) {
		bulk_add_missing_barcodes(frm, values.starting_missing_barcode, values.ending_missing_barcode);
	},
	__("Add Multiple Missing Barcodes"),
	__("Add Barcodes")
	);
}

/**
 * Bulk add missing barcodes by calling server-side method
 *
 * @param {object} frm - The form object
 * @param {string} start_barcode - Starting barcode of the range
 * @param {string} end_barcode - Ending barcode of the range
 */
function bulk_add_missing_barcodes(frm, start_barcode, end_barcode) {
	// Get existing barcodes for duplicate check
	const existing_barcodes = (frm.doc.missing_barcode_list || [])
		.map(row => row.barcode);

	// Call server-side method
	frappe.call({
		method: "dppl_mes.manufacturing.doctype.missing_barcode_log.missing_barcode_log.bulk_add_missing_barcode_range",
		args: {
			start_barcode: start_barcode,
			end_barcode: end_barcode,
			existing_barcodes: existing_barcodes
		},
		callback: function(r) {
			if (r.message) {
				if (r.message.success && r.message.barcodes && r.message.barcodes.length > 0) {
					// Add all barcodes to child table
					r.message.barcodes.forEach(item => {
						frm.add_child("missing_barcode_list", {
							barcode: item.barcode,
							barcode_number: item.barcode_number
						});
					});
					frm.refresh_field("missing_barcode_list");
					frm.save();

					show_message(frm, r.message.message, false);

					// Return focus to scan field
					setTimeout(() => {
						if (frm.fields_dict.scan_missing_barcode) {
							frm.fields_dict.scan_missing_barcode.set_focus();
						}
					}, 500);
				} else {
					show_message(frm, r.message.message, true);
				}
			}
		},
		freeze: true,
		freeze_message: __("Processing barcode range...")
	});
}
