# Copyright (c) 2025, IndusWorks and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now, nowdate
from datetime import datetime, timedelta


class Telemetry(Document):
	def after_insert(self):
		pass

	def get_in_progress_job(self):
		pass

	def start_job(self):
		pass

	def complete_job(self):
		pass

	def create_output_log(self):
		pass


	def downtime_record_checker(self):
		"""Check for existing open downtime logs."""
		print("Downtime Record Checker Called")
		downtime_logs = frappe.get_all(
			"Downtime Log",
			filters={"workstation": self.workstation, "status": "Open"},
			fields=["name"],
		)
		return downtime_logs[0].name if downtime_logs else None

	def create_downtime_log(self):
		"""Create a new downtime log entry."""
		try:
			downtime_log = frappe.new_doc("Downtime Log")
			downtime_log.workstation = self.workstation
			downtime_log.created_date = nowdate()
			downtime_log.start_date_time = self.timestamp
			downtime_log.status = "Open"
			downtime_log.save()
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), "Create Downtime Log Error")

	def close_downtime_log(self, downtime_record):
		"""Close an existing downtime log entry."""
		try:
			downtime_log = frappe.get_doc("Downtime Log", downtime_record)
			downtime_log.end_date_time = now()
			downtime_log.status = "Closed"
			downtime_log.save()
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), "Close Downtime Log Error")