# Copyright (c) 2026, IndusWorks and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class MissingBarcodeLog(Document):
	def validate(self):
		"""
		Called before save. Calculate ending_barcode_number and ending_barcode.
		"""
		self.calculate_ending_barcode()

	def on_update(self):
		"""
		Called after save. Calculate and update total_barcodes and total_missing_barcodes.
		"""
		self.calculate_totals()

	def calculate_ending_barcode(self):
		"""
		Calculate ending_barcode_number and reconstruct ending_barcode
		based on starting_barcode_number and pack_size.
		"""
		if self.starting_barcode_number and self.pack_size:
			self.ending_barcode_number = self.starting_barcode_number + self.pack_size - 1

			# Reconstruct ending_barcode from starting_barcode format
			if self.starting_barcode:
				self.ending_barcode = self.reconstruct_barcode(
					self.starting_barcode,
					self.ending_barcode_number
				)

	def reconstruct_barcode(self, starting_barcode, new_number):
		"""
		Reconstruct barcode by replacing the numeric portion with new_number.
		Preserves prefix, zeros padding, and suffix from starting_barcode.

		Examples:
			- reconstruct_barcode("00012345XX", 12500) -> "00012500XX"
			- reconstruct_barcode("AB00012345XX", 12500) -> "AB00012500XX"
			- reconstruct_barcode("AB000XX12345", 12500) -> "AB000XX12500"

		Args:
			starting_barcode (str): The original barcode string
			new_number (int): The new numeric value to insert

		Returns:
			str: Reconstructed barcode string
		"""
		import re

		if not starting_barcode or not isinstance(starting_barcode, str):
			return ""

		# Find all sequences of digits and their positions
		matches = []
		for match in re.finditer(r'\d+', starting_barcode):
			matches.append({
				'value': match.group(),
				'index': match.start(),
				'length': len(match.group())
			})

		if not matches:
			return starting_barcode

		# Get the last (rightmost) numeric sequence
		last_match = matches[-1]

		# Extract prefix and suffix
		prefix = starting_barcode[:last_match['index']]
		suffix = starting_barcode[last_match['index'] + last_match['length']:]

		# Pad the new number with leading zeros to match original length
		padded_number = str(new_number).zfill(last_match['length'])

		return prefix + padded_number + suffix

	def calculate_totals(self):
		"""
		Calculate total_barcodes and total_missing_barcodes.
		Update the values in the database using db_set.
		"""
		# Calculate total_barcodes
		if self.ending_barcode_number and self.starting_barcode_number:
			self.total_barcodes = self.ending_barcode_number - self.starting_barcode_number + 1
		else:
			self.total_barcodes = 0

		# Calculate total_missing_barcodes
		self.total_missing_barcodes = len(self.missing_barcode_list) if self.missing_barcode_list else 0

		# Update in database
		self.db_set({
			'total_barcodes': self.total_barcodes,
			'total_missing_barcodes': self.total_missing_barcodes
		})


import frappe


@frappe.whitelist()
def bulk_add_missing_barcode_range(start_barcode, end_barcode, existing_barcodes=None):
	"""
	Generate a range of barcodes for bulk adding to missing_barcode_list.

	Args:
		start_barcode (str): Starting barcode (e.g., "AB10000XX")
		end_barcode (str): Ending barcode (e.g., "AB10500XX")
		existing_barcodes (list): List of barcodes already in missing_barcode_list

	Returns:
		dict: {
			'success': bool,
			'message': str,
			'barcodes': [{'barcode': str, 'barcode_number': int}, ...]
		}
	"""
	import re

	# Parse input
	if existing_barcodes is None:
		existing_barcodes = []
	elif isinstance(existing_barcodes, str):
		existing_barcodes = frappe.parse_json(existing_barcodes)

	# Validate inputs
	if not start_barcode or not end_barcode:
		return {
			'success': False,
			'message': 'Please provide both starting and ending barcodes',
			'barcodes': []
		}

	# Extract numeric portion from start_barcode
	start_matches = list(re.finditer(r'\d+', start_barcode))
	if not start_matches:
		return {
			'success': False,
			'message': f'Invalid starting barcode format: {start_barcode}',
			'barcodes': []
		}

	# Extract numeric portion from end_barcode
	end_matches = list(re.finditer(r'\d+', end_barcode))
	if not end_matches:
		return {
			'success': False,
			'message': f'Invalid ending barcode format: {end_barcode}',
			'barcodes': []
		}

	# Get the last (rightmost) numeric sequence from each
	start_last_match = start_matches[-1]
	end_last_match = end_matches[-1]

	# Extract prefix and suffix from start_barcode for reconstruction
	start_prefix = start_barcode[:start_last_match.start()]
	start_suffix = start_barcode[start_last_match.end():]
	start_number_length = len(start_last_match.group())

	# Extract prefix and suffix from end_barcode
	end_prefix = end_barcode[:end_last_match.start()]
	end_suffix = end_barcode[end_last_match.end():]

	# Validate that prefix and suffix match
	if start_prefix != end_prefix or start_suffix != end_suffix:
		return {
			'success': False,
			'message': 'Starting and ending barcodes must have the same format (prefix and suffix)',
			'barcodes': []
		}

	# Get numeric values
	start_number = int(start_last_match.group())
	end_number = int(end_last_match.group())

	# Validate that start <= end
	if start_number > end_number:
		return {
			'success': False,
			'message': 'Starting barcode number must be less than or equal to ending barcode number',
			'barcodes': []
		}

	# Generate barcode range
	barcodes = []
	duplicate_count = 0

	for num in range(start_number, end_number + 1):
		# Reconstruct barcode with proper padding
		padded_number = str(num).zfill(start_number_length)
		barcode = start_prefix + padded_number + start_suffix

		# Skip if already exists
		if barcode in existing_barcodes:
			duplicate_count += 1
			continue

		barcodes.append({
			'barcode': barcode,
			'barcode_number': num
		})

	# Build response message
	total_in_range = end_number - start_number + 1
	added_count = len(barcodes)

	if added_count == 0:
		message = f'All {total_in_range} barcodes already exist in the missing barcode list'
	else:
		message = f'Added {added_count} missing barcode'
		if added_count > 1:
			message += 's'
		if duplicate_count > 0:
			message += f' ({duplicate_count} duplicate{"" if duplicate_count == 1 else "s"} skipped)'

	return {
		'success': True,
		'message': message,
		'barcodes': barcodes
	}
