# Copyright (c) 2025, IndusWorks and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now, time_diff_in_seconds

class DowntimeLog(Document):
	def before_save(self):
		self.duration = 0
		if self.end_date_time:
			self.duration = time_diff_in_seconds(self.end_date_time, self.start_date_time)
		else:
			self.duration = time_diff_in_seconds(now(), self.start_date_time)
		
		if not self.job_card and self.machine:
			in_progress_job_cards = frappe.get_list(
				"Job Card",
				filters={
					"machine": self.machine,
					"status": "In Progress"
				},
				fields=["name"],
				limit=1
			)
			
			if in_progress_job_cards:
				self.job_card = in_progress_job_cards[0].name
		
		if self.status == 'Closed' and not self.reason:
			print('Checking for Minor Stops')
			downtime_settings = frappe.get_doc('Downtime Settings')
			if downtime_settings.enable_automatic_reason_update_for_minor_stops:
				minor_stop_threshold = int(downtime_settings.minor_stop_threshold)
				if self.duration <= minor_stop_threshold:
					self.reason = downtime_settings.minor_stop_downtime_reason