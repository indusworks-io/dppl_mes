# Copyright (c) 2026, IndusWorks and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class MissingBarcode(Document):
	def on_update(self):
		"""
		Calculate and update total_barcodes and total_missing_barcodes
		This is called when the document is saved
		"""
		# Count the number of records in the child table
		total_count = len(self.missing_barcode_list) if self.missing_barcode_list else 0

		# Update the total_missing_barcodes field
		self.total_missing_barcodes = total_count
		self.db_set("total_missing_barcodes", total_count)

		# Calculate and update total_barcodes
		# Formula: total_barcodes = ending_barcode_number - starting_barcode_number - total_missing_barcodes
		self.total_barcodes = self.ending_barcode_number - self.starting_barcode_number - self.total_missing_barcodes
		self.db_set("total_barcodes", self.total_barcodes)
