# Copyright (c) 2026, IndusWorks and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class MissingBarcode(Document):
	def on_update(self):
		"""
		Calculate and update the total number of missing barcodes
		This is called when the document is saved
		"""
		# Count the number of records in the child table
		total_count = len(self.missing_barcode_list) if self.missing_barcode_list else 0

		# Update the total_missing_barcodes field
		self.total_missing_barcodes = total_count

		# Update the database directly to ensure the value is persisted
		# (since on_update is called after the main document save)
		self.db_set("total_missing_barcodes", total_count)
