# Copyright (c) 2026, IndusWorks and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re


class MissingBarcodeLog(Document):
	def validate(self):
		"""
		Validate and calculate ending_barcode_number based on batch_size and starting_barcode_number.
		Formula: ending_barcode_number = starting_barcode_number + batch_size - 1
		This is called before the document is saved.
		"""
		if self.batch_size and self.starting_barcode_number:
			# Calculate ending barcode number
			self.ending_barcode_number = self.starting_barcode_number + self.batch_size - 1

		# Calculate total packs
		if self.batch_size and self.pack_size:
			self.total_packs = int(self.batch_size / self.pack_size) if self.pack_size > 0 else 0

	def on_update(self):
		"""
		Calculate and update total_barcodes and total_missing_barcode_logs
		This is called when the document is saved
		"""
		# Count the number of records in the child table
		total_count = len(self.missing_barcode_list) if self.missing_barcode_list else 0

		# Update the total_missing_barcodes field
		self.total_missing_barcodes = total_count
		self.db_set("total_missing_barcodes", total_count)

		# Calculate and update total_barcodes
		# Formula: total_barcodes = ending_barcode_number - starting_barcode_number + 1 - total_missing_barcodes
		if self.ending_barcode_number and self.starting_barcode_number:
			self.total_barcodes = self.ending_barcode_number - self.starting_barcode_number + 1 - self.total_missing_barcodes
			self.db_set("total_barcodes", self.total_barcodes)


@frappe.whitelist()
def bulk_add_missing_barcode_log_range(start_barcode, end_barcode, starting_barcode_number, ending_barcode_number, existing_barcodes):
	"""
	Generate and validate missing barcodes in a range.

	Args:
		start_barcode: Starting barcode of missing range
		end_barcode: Ending barcode of missing range
		starting_barcode_number: Document's starting barcode number (for validation)
		ending_barcode_number: Document's ending barcode number (for validation)
		existing_barcodes: List of barcodes already in missing_barcode_log_list

	Returns:
		dict: {
			'success': True/False,
			'barcodes': [{'barcode': 'AB10000XX', 'barcode_number': 10000}, ...],
			'message': 'Success/Error message'
		}
	"""
	# Convert string parameters to integers (passed as strings from frappe.call)
	starting_barcode_number = int(starting_barcode_number) if starting_barcode_number else 0
	ending_barcode_number = int(ending_barcode_number) if ending_barcode_number else 0

	# Validate starting and ending barcodes are provided
	if not starting_barcode_number or not ending_barcode_number:
		return {
			"success": False,
			"message": "Please set Starting Barcode and Ending Barcode first"
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

	# Validate the range is within document bounds
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
	# existing_barcodes is passed from client as a list
	existing_barcodes_set = set(existing_barcodes) if existing_barcodes else set()

	# Generate the barcode range
	barcodes_to_add = []
	duplicate_count = 0

	for i in range(range_size):
		barcode_number = start_format["number"] + i
		barcode = f"{start_format['prefix']}{barcode_number}{start_format['suffix']}"

		# Check for duplicates
		if barcode in existing_barcodes_set:
			duplicate_count += 1
			continue

		barcodes_to_add.append({
			"barcode": barcode,
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

@frappe.whitelist()
def generate_missing_barcode_labels(docname):
    try:
        parent_doc = frappe.get_doc("Missing Barcode Log", docname)

        if parent_doc.labels_generated:
            return {
                "success": False,
                "message": "Labels have already been generated for this document."
            }

        batch_size = int(parent_doc.batch_size or 0)
        pack_size = int(parent_doc.pack_size or 0)
        starting_barcode_number = int(parent_doc.starting_barcode_number or 0)
        ending_barcode_number = int(parent_doc.ending_barcode_number or 0)
        job_name = parent_doc.job_name

        if not all([batch_size, pack_size, starting_barcode_number, ending_barcode_number]):
            return {
                "success": False,
                "message": "Missing required fields: batch_size, pack_size, starting_barcode_number, ending_barcode_number"
            }

        total_packs = batch_size // pack_size
        if total_packs == 0:
            return {
                "success": False,
                "message": "Invalid pack size calculation. Total packs is 0."
            }

        # Extract missing barcode numbers from child table
        missing_barcode_numbers = sorted([
            int(row.barcode_number)
            for row in parent_doc.missing_barcode_list
            if row.barcode_number
        ])

        labels_created = 0
        for serial_number in range(1, total_packs + 1):
            pack_start = starting_barcode_number + ((serial_number - 1) * pack_size)
            pack_end = pack_start + pack_size - 1

            # Clamp last pack to actual ending barcode
            if serial_number == total_packs:
                pack_end = ending_barcode_number

            pack_missing = [
                {"doctype": "Barcode List", "barcode_number": bc}
                for bc in missing_barcode_numbers
                if pack_start <= bc <= pack_end
            ]

            total_missing_barcodes = len(pack_missing)
            total_barcodes = (pack_end - pack_start + 1) - total_missing_barcodes

            label_doc = frappe.get_doc({
                "doctype": "Missing Barcode Label",
                "date": frappe.utils.today(),
                "job": job_name,
                "pack_size": pack_size,
                "missing_barcode_log": docname,
                "serial_number": serial_number,
                "starting_barcode_number": pack_start,
                "ending_barcode_number": pack_end,
                "total_barcodes": total_barcodes,
                "total_missing_barcodes": total_missing_barcodes,
                "missing_barcode_list": pack_missing
            })
            label_doc.insert(ignore_permissions=True)
            labels_created += 1

        parent_doc.labels_generated = 1
        parent_doc.save(ignore_permissions=True)
        frappe.db.commit()

        return {
            "success": True,
            "message": f"Successfully created {labels_created} Missing Barcode Label documents.",
            "labels_created": labels_created
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Generate Missing Barcode Labels Error")
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

@frappe.whitelist()
def generate_missing_barcode_labels_old(docname, batch_size, pack_size, starting_barcode_number, ending_barcode_number, job_name, missing_barcode_list):
	"""
	Generate Missing Barcode Label documents for each pack in the production run.

	Args:
		docname: Name of the parent Missing Barcode Log document
		batch_size: Total number of barcodes in the production run
		pack_size: Number of barcodes per pack
		starting_barcode_number: Starting barcode number of the production run
		ending_barcode_number: Ending barcode number of the production run
		job_name: Name of the Job
		missing_barcode_list: List of missing barcodes [{barcode_number: int}, ...]

	Returns:
		dict: {
			'success': True/False,
			'message': 'Success/Error message',
			'labels_created': int
		}
	"""
	try:
		# Get parent document
		parent_doc = frappe.get_doc("Missing Barcode Log", docname)

		# Check if labels already generated
		if parent_doc.labels_generated:
			return {
				"success": False,
				"message": "Labels have already been generated for this document."
			}

		# Convert to integers
		batch_size = int(batch_size) if batch_size else 0
		pack_size = int(pack_size) if pack_size else 0
		starting_barcode_number = int(starting_barcode_number) if starting_barcode_number else 0
		ending_barcode_number = int(ending_barcode_number) if ending_barcode_number else 0

		# Validate required fields
		if not batch_size or not pack_size or not starting_barcode_number or not ending_barcode_number:
			return {
				"success": False,
				"message": "Missing required fields: batch_size, pack_size, starting_barcode_number, ending_barcode_number"
			}

		# Calculate total packs
		total_packs = int(batch_size / pack_size) if pack_size > 0 else 0

		if total_packs == 0:
			return {
				"success": False,
				"message": "Invalid pack size calculation. Total packs is 0."
			}

		# Extract barcode numbers from missing_barcode_list
		missing_barcode_numbers = set()
		if missing_barcode_list:
			for item in missing_barcode_list:
				if isinstance(item, dict) and "barcode_number" in item:
					missing_barcode_numbers.add(item["barcode_number"])
				elif isinstance(item, int):
					missing_barcode_numbers.add(item)

		# Create Missing Barcode Label for each pack
		labels_created = 0
		for serial_number in range(1, total_packs + 1):
			# Calculate pack's barcode range
			pack_start = starting_barcode_number + ((serial_number - 1) * pack_size)
			pack_end = pack_start + pack_size - 1

			# Filter missing barcodes for this pack
			pack_missing_barcodes = [
				{"barcode_number": bc} for bc in sorted(missing_barcode_numbers)
				if pack_start <= bc <= pack_end
			]

			# Calculate totals for this pack
			total_missing_barcodes = len(pack_missing_barcodes)
			total_barcodes = pack_size - total_missing_barcodes

			# Create Missing Barcode Label document
			# Initialize child table data
			missing_barcode_list_data = [
				{"barcode_number": bc} for bc in sorted(missing_barcode_numbers)
				if pack_start <= bc <= pack_end
			]

			label_doc = frappe.get_doc({
				"doctype": "Missing Barcode Label",
				"date": frappe.utils.today(),
				"job": job_name,
				"pack_size": pack_size,
				"missing_barcode_log": docname,
				"serial_number": serial_number,
				"starting_barcode_number": pack_start,
				"ending_barcode_number": pack_end,
				"total_barcodes": total_barcodes,
				"total_missing_barcodes": total_missing_barcodes,
				"missing_barcode_list": missing_barcode_list_data  # Include child table data directly
			})

			label_doc.insert()
			labels_created += 1

		# Update parent document - set labels_generated flag
		parent_doc.labels_generated = 1
		parent_doc.save(ignore_permissions=True)

		return {
			"success": True,
			"message": f"Successfully created {labels_created} Missing Barcode Label documents.",
			"labels_created": labels_created
		}

	except Exception as e:
		frappe.log_error(f"Error generating missing barcode labels: {str(e)}")
		return {
			"success": False,
			"message": f"Error: {str(e)}"
		}
