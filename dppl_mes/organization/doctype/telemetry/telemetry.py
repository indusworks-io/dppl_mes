# Copyright (c) 2025, IndusWorks and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now, nowdate, nowtime
from datetime import datetime, timedelta, time
import json

"""
Everytime a new Telemetery is saved we need to do the folloing:
1. if data Json has output key then extract output value
2. run create_output_log function

create_output_log function will do the following:
1. run get_job_details function
2. 


from machine get enable_output_logging && output_type
if enable_output_logging == 1 then 


"""

class Telemetry(Document):
	def before_save(self):
		print('Running Before Save Function')
		timestamp = self.timestamp
		machine = self.machine
		data_str = self.data
		# Parse string into dictionary
		
		try:
			data = json.loads(data_str)
		except json.JSONDecodeError as e:
			frappe.throw(f"Invalid JSON in 'data': {e}")

		if "output" in data:
			print('output key exists')
			try:
				output_value = int(data["output"])
				self.create_output_log(output_value, timestamp, machine)
			except ValueError:
				frappe.throw("Output value must be an integer.")

	def create_output_log(self, output_value, timestamp, machine):
		try:
			job_card = self.get_job_details(machine, output_value)
			if job_card:
				output_log = frappe.new_doc("Output Log")
				output_log.job_card = job_card
				output_log.output = output_value
				output_log.timestamp = timestamp
				output_log.save()
				print('Output Log Created')
				print('Updating Job Card Now')
				job_card_doc = frappe.get_doc("Job Card", job_card)
				machine_output_type = frappe.db.get_value("Machine", machine, "output_type")
				if machine_output_type == 'Absolute Values':
					job_card_doc.completed_quantity = output_value
					job_card_doc.save()
				if machine_output_type == 'Relative Values':
					job_card_doc.completed_quantity = job_card_doc.completed_quantity + output_value
					job_card_doc.save()
				print('Job Card Updated')
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), "Create Output Log Error")

	def get_job_details(self, machine, output_value):
		"""
		1. run get_active_job Function
		2. if active_job exisits then return active_job else
		3. run start_job function and return active_job

		"""
		try:
			active_job = self.get_active_job(machine)
			print(active_job)
			if active_job:
				print('Active Job Found')
				machine_output_type = frappe.db.get_value("Machine", machine, "output_type")
				if machine_output_type == 'Absolute Values':
					print('Entered Absolute Value Checker Block')
					if active_job.completed_quantity >= output_value:
						print('Output Value Reached, Updating Job Status')
						active_job.status = "Completed"
						active_job.save()
						active_job = self.start_job(machine)
						return active_job
					else:
						return active_job
			else:
				print('Active Job Not Found, Starting New Job')
				active_job = self.start_job(machine)
				return active_job
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), "Get Job Details Error")

	def get_active_job(self, machine):
		try:
			active_job_list = frappe.get_all('Job Card', filters={"machine": machine, "status": "In Progress"}, fields=["name"])
			print(active_job_list)
			if active_job_list:
				active_job = active_job_list[0].name
				return active_job
			else:
				return None
		except Exception as e:
			frappe.log_error(f"{frappe.get_traceback()}\nError: {str(e)}", "Get Active Job Error")
	
	def start_job(self, machine):
		"""
		0. In a Try Block do the following
		1. Get current_date
		2. Get current_time
		3. From Machine Get Factory
		4. Based on current_time get shift as current_shift from shift_timings table in Factory Doctype
		5. Based on machine, current_date, current_shift get scheduled_jobs from Job Card Doctype in ascedning order of job_sequence_number
		6. First check status of scheduled_job where job_sequence_number == 1. if the status is 'Not Started' then return then change the status as 'In Progress' and return the job'
		7. If the status of scheduled_job where job_sequence_number == 1 is not 'Not Started' then check for scheduled_job where job_sequence_number == 2. if such job exists then change the status as 'In Progress' and return the job' else return None

		"""
		try:
			current_date = nowdate()
			current_time = datetime.strptime(nowtime(), "%H:%M:%S.%f").time()

			machine_doc = frappe.get_doc("Machine", machine)
			factory = machine_doc.factory
			print(factory)

			# Get current shift
			current_shift = None
			factory_doc = frappe.get_doc("Factory", factory)
			for shift in factory_doc.get("shift_timings"):
				shift_start_time = to_time(shift.start_time)
				print(f'Shift Start Time: {shift_start_time}')
				shift_end_time = to_time(shift.end_time)
				print(f'Shift End Time: {shift_end_time}')

				# Handle overnight shifts
				if shift_start_time <= shift_end_time:
					if shift_start_time <= current_time <= shift_end_time:
						current_shift = shift.shift_name
						print(f'Current Shift: {current_shift}')
						break
				else:  # Overnight shift
					if current_time >= shift_start_time or current_time <= shift_end_time:
						current_shift = shift.shift_name
						print(f'Current Shift: {current_shift}')
						break
			if not current_shift:
				frappe.throw("No active shift found for the current time.")

			# Get scheduled jobs
			scheduled_jobs = frappe.get_all(
				"Job Card",
				filters={
					"machine": machine,
					"date": current_date,
					"shift": current_shift,
				},
				order_by="job_sequence_number asc",
				fields=["name", "status", "job_sequence_number"],
			)

			if not scheduled_jobs:
				return None

			# Check job with sequence number 1
			job_seq_1 = next((job for job in scheduled_jobs if job.job_sequence_number == 1), None)

			if job_seq_1 and job_seq_1.status == "Not Started":
				job_card = frappe.get_doc("Job Card", job_seq_1.name)
				job_card.status = "In Progress"
				job_card.save()
				return job_card.name
			else:
				# Check for job with sequence number 2
				job_seq_2 = next((job for job in scheduled_jobs if job.job_sequence_number == 2), None)
				if job_seq_2:
					job_card = frappe.get_doc("Job Card", job_seq_2.name)
					job_card.status = "In Progress"
					job_card.save()
					return job_card.name
				else:
					return None

		except Exception as e:
			frappe.log_error(frappe.get_traceback(), "Start Job Error")
				


				
	


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
	

def to_time(val):
    if isinstance(val, time):
        return val
    if isinstance(val, timedelta):
        total_seconds = int(val.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return time(hour=hours, minute=minutes, second=seconds)
    return datetime.strptime(str(val), "%H:%M:%S").time()