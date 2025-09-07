# Copyright (c) 2025, IndusWorks and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now, time_diff_in_seconds, flt


class JobCard(Document):
	def before_save(self):
		try:
			if self.planned_end_date_time and self.planned_start_date_time:
				self.planned_duration = abs(time_diff_in_seconds(self.planned_end_date_time, self.planned_start_date_time))
			if self.actual_duration == "":
				self.actual_duration = None
			if self.actual_start_date_time:
				self.actual_duration = 0
				if self.actual_end_date_time:
					self.actual_duration = time_diff_in_seconds(self.actual_end_date_time, self.actual_start_date_time)
					duration_in_minutes = self.actual_duration / 60
					if duration_in_minutes > 0:
						self.actual_run_rate = self.completed_quantity / duration_in_minutes
				else:
					print("Job Card: No actual end time, calculating duration from start time to now")
					self.actual_duration = time_diff_in_seconds(now(), self.actual_start_date_time)
					duration_in_minutes = self.actual_duration / 60
					if duration_in_minutes > 0:
						self.actual_run_rate = self.completed_quantity / duration_in_minutes
			self.calculate_total_wastage()
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), "Job Card Error")

	def calculate_total_wastage(self):
		"""Calculate total wastage by summing all individual wastage components"""
		# Sum all individual wastage fields, treating None/empty values as 0
		machine_wastage = flt(self.machine_wastage or 0)
		job_setting_wastage = flt(self.job_setting_wastage or 0)
		roll_wastage = flt(self.roll_wastage or 0)
		printing_wastage = flt(self.printing_wastage or 0)
		barcode_wastage = flt(self.barcode_wastage or 0)
		
		# Calculate total and round to 2 decimal places
		self.total_wastage = flt(
			machine_wastage + job_setting_wastage + roll_wastage + printing_wastage + barcode_wastage,
			precision=2
		)

# class JobCard(Document):
#     def before_save(self):
#         if self.start_date_time:
#             end_time = self.end_date_time or now()
#             self.duration = time_diff_in_seconds(end_time, self.start_date_time)
#             if self.duration > 0:
#                 duration_in_minutes = self.duration / 60
#                 self.actual_run_rate = self.completed_quantity / duration_in_minutes if duration_in_minutes > 0 else 0
#             else:
#                 self.actual_run_rate = 0