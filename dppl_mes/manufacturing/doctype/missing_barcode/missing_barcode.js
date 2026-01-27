// Copyright (c) 2026, IndusWorks and contributors
// For license information, please see license.txt

frappe.ui.form.on("Missing Barcode", {
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
		add_missing_barcode(frm, barcode_value);
		show_message(frm, "Missing Barcode Added Successfully", false);
		frm.set_value("scan_missing_barcode", "");
	}
});

/**
 * Extract numeric portion from barcode string using regex
 * @param {string} barcode - The barcode string (e.g., "FSBU00002928659")
 * @returns {number|null} - Extracted number as integer, or null if not found
 */
function extract_barcode_number(barcode) {
	if (!barcode || typeof barcode !== "string") {
		return null;
	}

	// Regex to match trailing digits (handles leading zeros in the number portion)
	const match = barcode.match(/[0-9]+$/);

	if (match) {
		return parseInt(match[0], 10);
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
function add_missing_barcode(frm, barcode_value) {
	frm.add_child("missing_barcode_list", {
		barcode: barcode_value
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
