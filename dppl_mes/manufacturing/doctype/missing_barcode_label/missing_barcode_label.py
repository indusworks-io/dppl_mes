# Copyright (c) 2026, IndusWorks and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re


class MissingBarcodeLabel(Document):
	def validate(self):
		"""
		Validate that scanned barcodes are within the pack's range.
		This is called before the document is saved.
		"""
		# Check if starting and ending barcode numbers are set
		if not self.starting_barcode_number or not self.ending_barcode_number:
			return

		# Validate each barcode in the child table is within the valid range
		if self.missing_barcode_list:
			invalid_barcodes = []
			for row in self.missing_barcode_list:
				if row.barcode_number:
					barcode_number = int(row.barcode_number)
					if barcode_number < self.starting_barcode_number or barcode_number > self.ending_barcode_number:
						invalid_barcodes.append(str(barcode_number))

			if invalid_barcodes:
				frappe.throw(
					f"The following barcode numbers are outside the valid range "
					f"({self.starting_barcode_number} to {self.ending_barcode_number}): "
					f"{', '.join(invalid_barcodes)}"
				)

	def on_update(self):
		"""
		Calculate and update total_barcodes and total_missing_barcodes.
		This is called when the document is saved.
		"""
		# Count the number of records in the child table
		total_count = len(self.missing_barcode_list) if self.missing_barcode_list else 0

		# Update the total_missing_barcodes field
		self.total_missing_barcodes = total_count
		self.db_set("total_missing_barcodes", total_count)

		# Calculate and update total_barcodes
		# Formula: total_barcodes = (ending_barcode_number - starting_barcode_number + 1) - total_missing_barcodes
		if self.ending_barcode_number and self.starting_barcode_number:
			self.total_barcodes = self.ending_barcode_number - self.starting_barcode_number + 1 - self.total_missing_barcodes
			self.db_set("total_barcodes", self.total_barcodes)


@frappe.whitelist()
def bulk_add_missing_barcode_label_range(start_barcode, end_barcode, starting_barcode_number, ending_barcode_number, existing_barcodes):
	"""
	Generate and validate missing barcodes in a range for Missing Barcode Label.

	Args:
		start_barcode: Starting barcode of missing range
		end_barcode: Ending barcode of missing range
		starting_barcode_number: Label's starting barcode number (for validation)
		ending_barcode_number: Label's ending barcode number (for validation)
		existing_barcodes: List of barcodes already in missing_barcode_list

	Returns:
		dict: {
			'success': True/False,
			'barcodes': [{'barcode_number': bc}, ...],
			'message': 'Success/Error message'
		}
	"""
	# Convert string parameters to integers (passed as strings from frappe.call)
	starting_barcode_number = int(starting_barcode_number) if starting_barcode_number else 0
	ending_barcode_number = int(ending_barcode_number) if ending_barcode_number else 0

	# Validate starting and ending barcode numbers are provided
	if not starting_barcode_number or not ending_barcode_number:
		return {
			"success": False,
			"message": "Please set Starting Barcode Number and Ending Barcode Number first"
		}

	# Parse the barcode formats
	start_format = _parse_barcode_format(start_barcode)
	end_format = _parse_barcode_format(end_barcode)

	if not start_format or not end_format:
		return {
			"success": False,
			"message": "Invalid barcode format. No numeric portion found."
		}

	# Validate formats match (same prefix and suffix)
	if start_format["prefix"] != end_format["prefix"] or start_format["suffix"] != end_format["suffix"]:
		return {
			"success": False,
			"message": "Barcode formats do not match. Ensure prefix and suffix are the same."
		}

	# Validate order (start number should be <= end number)
	if start_format["number"] > end_format["number"]:
		return {
			"success": False,
			"message": "Starting missing barcode cannot be greater than ending missing barcode."
		}

	# Validate the range is within label bounds
	if start_format["number"] < starting_barcode_number or end_format["number"] > ending_barcode_number:
		return {
			"success": False,
			"message": f"Missing barcode range is outside the valid range ({starting_barcode_number} to {ending_barcode_number})."
		}

	# Check range size limit to prevent timeout
	MAX_RANGE_SIZE = 50000
	range_size = end_format["number"] - start_format["number"] + 1
	if range_size > MAX_RANGE_SIZE:
		return {
			"success": False,
			"message": f"Range exceeds maximum limit of {MAX_RANGE_SIZE} barcodes. Please split into smaller ranges."
		}

	# Get existing barcodes for duplicate check
	existing_barcodes_set = set(existing_barcodes) if existing_barcodes else set()

	# Generate the barcode range
	barcodes_to_add = []
	duplicate_count = 0

	for i in range(range_size):
		barcode_number = start_format["number"] + i

		# Check for duplicates
		if barcode_number in existing_barcodes_set:
			duplicate_count += 1
			continue

		barcodes_to_add.append({
			"barcode_number": barcode_number
		})

	# Prepare result message
	if not barcodes_to_add:
		if duplicate_count > 0:
			message = f"All {duplicate_count} barcodes in this range already exist in the missing list."
		else:
			message = "No barcodes to add."
	else:
		if duplicate_count > 0:
			message = f"Added {len(barcodes_to_add)} barcodes. {duplicate_count} duplicates were skipped."
		else:
			message = f"Added {len(barcodes_to_add)} barcodes successfully."

	return {
		"success": True if barcodes_to_add else False,
		"barcodes": barcodes_to_add,
		"message": message
	}


def _parse_barcode_format(barcode):
	"""
	Parse barcode into prefix, numeric portion, and suffix.
	Uses the same logic as the client-side extract_barcode_number.

	Args:
		barcode: The barcode string to parse

	Returns:
		dict: {'prefix': str, 'number': int, 'suffix': str} or None if invalid
	"""
	if not barcode or not isinstance(barcode, str):
		return None

	barcode = barcode.strip()

	# Find all sequences of digits in the barcode
	matches = re.findall(r'\d+', barcode)

	if not matches:
		return None

	# Take the last (rightmost) sequence of digits
	last_sequence = matches[-1]
	last_match_pos = barcode.rfind(last_sequence)

	return {
		"prefix": barcode[:last_match_pos],
		"number": int(last_sequence),
		"suffix": barcode[last_match_pos + len(last_sequence):]
	}
