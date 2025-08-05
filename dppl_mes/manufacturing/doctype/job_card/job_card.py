# Copyright (c) 2025, IndusWorks and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now, time_diff_in_seconds


class JobCard(Document):
	def before_save(self):
		if self.start_date_time:
			self.duration = 0
			if self.end_date_time:
				self.duration = time_diff_in_seconds(self.end_date_time, self.start_date_time)
			else:
				self.duration = time_diff_in_seconds(now(), self.start_date_time)