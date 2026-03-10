// Copyright (c) 2026, IndusWorks and contributors
// For license information, please see license.txt

frappe.ui.form.on("Missing Barcode Label", {
	onload: function(frm) {
		// Clear empty child table if only one row exists with empty barcode_number
		if (
			frm.doc.missing_barcode_list &&
			frm.doc.missing_barcode_list.length === 1
		) {
			const row = frm.doc.missing_barcode_list[0];

			// Check if barcode_number field is empty
			if (!row.barcode_number) {
				frm.clear_table('missing_barcode_list');
				frm.refresh_field('missing_barcode_list');
			}
		}
	},

	refresh: function(frm) {
		// No "Create Missing Barcode Labels" button
		// This functionality is handled by the parent Missing Barcode Log
	},

	scan_missing_barcode: function(frm) {
		const scanned_barcode = frm.doc.scan_missing_barcode;

		// Exit if no value
		if (!scanned_barcode || !scanned_barcode.trim()) {
			return;
		}

		// Trim whitespace
		const barcode_value = scanned_barcode.trim();

		// Extract barcode number
		const barcode_number = extract_barcode_number(barcode_value);

		if (barcode_number === null) {
			show_message(frm, `Invalid barcode: No numeric portion found in ${barcode_value}`, true);
			frm.set_value("scan_missing_barcode", "");
			return;
		}

		// Validate barcode is within pack range
		if (!validate_barcode_range(frm, barcode_number)) {
			show_message(
				frm,
				`Barcode Number ${barcode_number} is outside the valid range (${frm.doc.starting_barcode_number} to ${frm.doc.ending_barcode_number})`,
				true
			);
			frm.set_value("scan_missing_barcode", "");
			return;
		}

		// Check if barcode_number already exists in the list
		if (is_duplicate_barcode_number(frm, barcode_number)) {
			show_message(frm, `Barcode Number ${barcode_number} already exists`, true);
		} else {
			// Add to list
			add_missing_barcode(frm, barcode_number);
			show_message(frm, `Barcode Number ${barcode_number} added successfully`, false);
		}

		// Clear the scan field
		frm.set_value("scan_missing_barcode", "");
	},

	bulk_add_missing_barcodes: function(frm) {
		// Check if document has starting and ending barcode numbers set
		if (!frm.doc.starting_barcode_number || !frm.doc.ending_barcode_number) {
			show_message(frm, "Please set Starting and Ending Barcode Numbers first", true);
			return;
		}

		// Show dialog for bulk add
		frappe.prompt(
			[
				{
					fieldname: "starting_missing_barcode_number",
					label: __("Starting Missing Barcode"),
					fieldtype: "Data",
					reqd: 1,
					description: __("Scan the first full barcode of the missing range")
				},
				{
					fieldname: "ending_missing_barcode_number",
					label: __("Ending Missing Barcode"),
					fieldtype: "Data",
					reqd: 1,
					description: __("Scan the last full barcode of the missing range")
				}
			],
			function(values) {
				// Extract existing barcode_numbers for duplicate check
				const existing_barcode_numbers = (frm.doc.missing_barcode_list || [])
					.map(function(row) { return row.barcode_number; });

				// Call server-side method
				frappe.call({
					method: "dppl_mes.manufacturing.doctype.missing_barcode_label.missing_barcode_label.bulk_add_missing_barcode_label_range",
					args: {
						start_barcode: values.starting_missing_barcode_number,
						end_barcode: values.ending_missing_barcode_number,
						starting_barcode_number: frm.doc.starting_barcode_number,
						ending_barcode_number: frm.doc.ending_barcode_number,
						existing_barcodes: existing_barcode_numbers
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
			__("Add Missing Barcodes")
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
 * Check if barcode_number already exists in missing_barcode_list
 * @param {object} frm - The form object
 * @param {number} barcode_number - The barcode number to check
 * @returns {boolean} - True if duplicate found
 */
function is_duplicate_barcode_number(frm, barcode_number) {
	if (!frm.doc.missing_barcode_list || frm.doc.missing_barcode_list.length === 0) {
		return false;
	}

	return frm.doc.missing_barcode_list.some(function(row) {
		return row.barcode_number === barcode_number;
	});
}

/**
 * Validate that barcode_number is within starting_barcode_number to ending_barcode_number
 * @param {object} frm - The form object
 * @param {number} barcode_number - The barcode number to validate
 * @returns {boolean} - True if valid, false otherwise
 */
function validate_barcode_range(frm, barcode_number) {
	const starting_barcode_number = parseInt(frm.doc.starting_barcode_number) || 0;
	const ending_barcode_number = parseInt(frm.doc.ending_barcode_number) || 0;

	if (starting_barcode_number === 0 || ending_barcode_number === 0) {
		return false;
	}

	return barcode_number >= starting_barcode_number && barcode_number <= ending_barcode_number;
}

/**
 * Add a new barcode_number to the missing_barcode_list child table
 * @param {object} frm - The form object
 * @param {number} barcode_number - The barcode number to add
 */
function add_missing_barcode(frm, barcode_number) {
	frm.add_child("missing_barcode_list", {
		barcode_number: barcode_number
	});
	frm.refresh_field("missing_barcode_list");
}

/**
 * Add multiple barcodes to the missing_barcode_list child table
 * @param {object} frm - The form object
 * @param {array} barcodes - Array of barcode objects with barcode_number property
 */
function add_barcodes_to_table(frm, barcodes) {
	barcodes.forEach(function(item) {
		frm.add_child("missing_barcode_list", {
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
