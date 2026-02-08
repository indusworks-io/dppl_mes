// Copyright (c) 2026, IndusWorks and contributors
// For license information, please see license.txt

frappe.ui.form.on("Missing Barcode", {
	onload: function(frm) {
		if (
			frm.doc.missing_barcode_list &&
			frm.doc.missing_barcode_list.length === 1
		) {
			const row = frm.doc.missing_barcode_list[0];

			// Check if barcode field is empty
			if (!row.barcode) {
				frm.clear_table('missing_barcode_list');
				frm.refresh_field('missing_barcode_list');
			}
		}
	},
	refresh: function(frm) {
		// Message persists until next scan - don't clear here
	},

	starting_barcode: function(frm) {
		// Extract and set starting barcode number
		const barcode = frm.doc.starting_barcode;
		if (barcode) {
			const number = extract_barcode_number(barcode);
			console.log(number)
			frm.set_value("starting_barcode_number", number);
		}
	},

	ending_barcode: function(frm) {
		// Extract and set ending barcode number
		const barcode = frm.doc.ending_barcode;
		if (barcode) {
			const number = extract_barcode_number(barcode);
			console.log(number)
			frm.set_value("ending_barcode_number", number);
		}
	},

	scan_missing_barcode: function(frm) {
		const scanned_barcode = frm.doc.scan_missing_barcode;

		// Exit if no value
		if (!scanned_barcode || !scanned_barcode.trim()) {
			return;
		}

		// Trim whitespace
		const barcode_value = scanned_barcode.trim();

		// Check for duplicate
		if (is_duplicate_barcode(frm, barcode_value)) {
			show_message(frm, `Barcode: ${barcode_value} already Exist`, true);
			frm.set_value("scan_missing_barcode", "");
			return;
		}

		// Extract number and check range
		const barcode_number = extract_barcode_number(barcode_value);
		console.log(barcode_number)

		if (barcode_number === null) {
			show_message(frm, `Barcode: ${barcode_value} is invalid. No numeric portion found.`, true);
			frm.set_value("scan_missing_barcode", "");
			return;
		}

		if (is_out_of_range(frm, barcode_number)) {
			show_message(frm, `Barcode: ${barcode_value} is outside starting & ending barcodes`, true);
			frm.set_value("scan_missing_barcode", "");
			return;
		}

		// All validations passed - add to list
		add_missing_barcode(frm, barcode_value, barcode_number);
		show_message(frm, "Missing Barcode Added Successfully", false);
		frm.set_value("scan_missing_barcode", "");
	},

	bulk_add_missing_barcodes: function(frm) {
		// Check if document has starting and ending barcodes set
		if (!frm.doc.starting_barcode || !frm.doc.ending_barcode) {
			show_message(frm, "Please set Starting Barcode and Ending Barcode first", true);
			return;
		}

		// Show dialog for bulk add
		frappe.prompt(
			[
				{
					fieldname: "starting_missing_barcode",
					label: __("Starting Missing Barcode"),
					fieldtype: "Data",
					reqd: 1,
					description: __("Enter the first barcode of the missing range")
				},
				{
					fieldname: "ending_missing_barcode",
					label: __("Ending Missing Barcode"),
					fieldtype: "Data",
					reqd: 1,
					description: __("Enter the last barcode of the missing range")
				}
			],
			function(values) {
				// Extract existing barcodes for duplicate check
				const existing_barcodes = (frm.doc.missing_barcode_list || [])
					.map(function(row) { return row.barcode; });

				// Call server-side method
				frappe.call({
					method: "dppl_mes.manufacturing.doctype.missing_barcode.missing_barcode.bulk_add_missing_barcode_range",
					args: {
						start_barcode: values.starting_missing_barcode,
						end_barcode: values.ending_missing_barcode,
						starting_barcode_number: frm.doc.starting_barcode_number,
						ending_barcode_number: frm.doc.ending_barcode_number,
						existing_barcodes: existing_barcodes
					},
					callback: function(r) {
						if (r.message) {
							if (r.message.success && r.message.barcodes && r.message.barcodes.length > 0) {
								// Add barcodes to child table
								add_barcodes_to_table(frm, r.message.barcodes);
								show_message(frm, r.message.message, false);
							} else {
								// Show error or info message
								show_message(frm, r.message.message, true);
							}
						}
					},
					freeze: true,
					freeze_message: __("Processing barcode range...")
				});
			},
			__("Bulk Add Missing Barcodes"),
			__("Add Barcodes")
		);
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
 * @param {string} barcode - The barcode string (e.g., "FSBU00002928659")
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
		// This handles cases like "AB000XX12345" where we want "12345"
		const lastSequence = matches[matches.length - 1];
		return parseInt(lastSequence, 10);
	}

	return null;
}

/**
 * Check if barcode already exists in missing_barcode_list
 * @param {object} frm - The form object
 * @param {string} barcode_value - The barcode value to check
 * @returns {boolean} - True if duplicate found
 */
function is_duplicate_barcode(frm, barcode_value) {
	if (!frm.doc.missing_barcode_list || frm.doc.missing_barcode_list.length === 0) {
		return false;
	}

	return frm.doc.missing_barcode_list.some(function(row) {
		return row.barcode === barcode_value;
	});
}

/**
 * Check if barcode number is outside the starting/ending range
 * @param {object} frm - The form object
 * @param {number} barcode_number - The numeric portion of barcode to validate
 * @returns {boolean} - True if out of range
 */
function is_out_of_range(frm, barcode_number) {
	const starting_number = frm.doc.starting_barcode_number;
	const ending_number = frm.doc.ending_barcode_number;

	// If starting or ending numbers are not set, cannot validate range
	if (starting_number === null || starting_number === undefined ||
		ending_number === null || ending_number === undefined) {
		return false;
	}

	// Check if barcode is outside the range
	return barcode_number < starting_number || barcode_number > ending_number;
}

/**
 * Add a new barcode to the missing_barcode_list child table
 * @param {object} frm - The form object
 * @param {string} barcode_value - The barcode value to add
 */
function add_missing_barcode(frm, barcode_value, barcode_number) {
	frm.add_child("missing_barcode_list", {
		barcode: barcode_value,
		barcode_number: barcode_number
	});
	frm.refresh_field("missing_barcode_list");
}

/**
 * Add multiple barcodes to the missing_barcode_list child table
 * @param {object} frm - The form object
 * @param {array} barcodes - Array of barcode objects with barcode and barcode_number properties
 */
function add_barcodes_to_table(frm, barcodes) {
	barcodes.forEach(function(item) {
		frm.add_child("missing_barcode_list", {
			barcode: item.barcode,
			barcode_number: item.barcode_number
		});
	});
	frm.refresh_field("missing_barcode_list");
}

/**
 * Display message in the message field with appropriate color
 * @param {object} frm - The form object
 * @param {string} text - The message text to display
 * @param {boolean} is_error - True for error (red), False for success (green)
 */
// function show_message(frm, text, is_error) {
// 	const color = is_error ? "#dc3545" : "#198754"; // Red for error, Green for success
// 	const html = `
// 		<div style="
// 			padding: 12px;
// 			border-radius: 4px;
// 			background-color: ${is_error ? "#f8d7da" : "#d1e7dd"};
// 			border: 1px solid ${color};
// 			color: ${color};
// 			font-weight: 500;
// 			text-align: center;
// 		">
// 			${text}
// 		</div>
// 	`;
// 	frm.set_value("message", html);
// 	frm.refresh_field("message");
// }

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
