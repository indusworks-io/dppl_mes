# Copyright (c) 2025, IndusWorks and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class OutputLog(Document):
	def before_save(self):
		print('Running Before Save Function')
		"""
		1. From Job Card Get Machine Name
		2. From Machine Get 
		"""

