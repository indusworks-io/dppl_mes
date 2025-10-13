# Copyright (c) 2025, IndusWorks and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now, nowdate, nowtime
from datetime import datetime, timedelta, time
import json

class Telemetry(Document):
	def before_save(self):
		timestamp = self.timestamp
		machine = self.machine
		data_str = self.data
		
		try:
			data = json.loads(data_str)
		except json.JSONDecodeError as e:
			frappe.log_error(frappe.get_traceback(), "JSON Decoding Error")
			return

		if "output" in data:
			try:
				output_raw = data["output"]
				if output_raw is None or output_raw == '' or str(output_raw).strip() == '':
					print('Empty or invalid output value detected, skipping output processing')
					return
				output_value = int(output_raw)
				run_rate_value = float(data["run_rate"])
				if output_value == 0:
					print('Output is zero. Do Nothing')
				if output_value != 0:
					print('Output is not zero. Running handle_output function')
					self.handle_output(output_value, run_rate_value, timestamp, machine)
			except Exception as e:
				frappe.log_error(frappe.get_traceback(), "Output Parsing Error")
		
		if "status" in data:
			print('Machine Status Exists')
			try:
				machine_status = data["status"]
				self.downtime_checker(machine_status)
			except Exception as e:
				frappe.log_error(frappe.get_traceback(), "Status Parsing Error")

	def handle_output(self, output_value, run_rate_value, timestamp, machine):
		try:
			active_job = self.get_active_job(machine)
			if active_job:
				print(f'Active Job Found: {active_job}')
				active_job_doc = frappe.get_doc("Job Card", active_job)
				job_completed_qty = active_job_doc.completed_quantity
				
				if output_value > job_completed_qty:
					active_job_doc.completed_quantity = output_value
					active_job_doc.save()
					output_log = frappe.new_doc("Output Log")
					output_log.machine = machine
					output_log.job_card = active_job
					output_log.output = output_value
					output_log.run_rate = run_rate_value
					output_log.timestamp = timestamp
					output_log.save()
					print('Output Log Created')
				
				elif output_value < job_completed_qty:
					# Complete Existing Job
					active_job_doc.status = 'Completed'
					active_job_doc.actual_end_date_time = now()
					active_job_doc.save()

					# Try To Start New Job
					new_job = self.start_job(machine)
					if new_job:
						# if New Job Started
						print(f'New Job Started: {new_job}')
						new_job_doc = frappe.get_doc("Job Card", new_job)
						new_job_doc.completed_quantity = output_value
						new_job_doc.save()
						# Creating output log for new job
						output_log = frappe.new_doc("Output Log")
						output_log.machine = machine
						output_log.job_card = new_job
						output_log.output = output_value
						output_log.run_rate = run_rate_value
						output_log.timestamp = timestamp
						output_log.save()
						print('Output Log Created for New Job')
			else:
				print('No Active Job Found, Starting New Job')
				if output_value > 0:
					new_job = self.start_job(machine)	
					if new_job:
						print(f'New Job Started: {new_job}')
						new_job_doc = frappe.get_doc("Job Card", new_job)
						new_job_doc.completed_quantity = output_value
						new_job_doc.save()
						
						# Creating output log for new job
						output_log = frappe.new_doc("Output Log")
						output_log.machine = machine
						output_log.job_card = new_job
						output_log.output = output_value
						output_log.run_rate = run_rate_value
						output_log.timestamp = timestamp
						output_log.save()
						print('Output Log Created for New Job')
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), "Handle Output Error")

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
			return None
	
	def start_job(self, machine):
		"""
		Simple approach: Get all jobs for current date and shift, then start by sequence priority
		"""
		try:
			current_datetime = now()
			current_time = datetime.strptime(nowtime(), "%H:%M:%S.%f").time()

			machine_doc = frappe.get_doc("Machine", machine)
			factory = machine_doc.factory
			print(f"Factory: {factory}")

			# Get current shift
			current_shift = None
			factory_doc = frappe.get_doc("Factory", factory)
			for shift in factory_doc.get("shift_timings"):
				shift_start_time = to_time(shift.start_time)
				shift_end_time = to_time(shift.end_time)
				print(f"Checking shift: {shift.shift_name}, Start: {shift_start_time}, End: {shift_end_time}")

				# Handle overnight shifts
				if shift_start_time <= shift_end_time:
					# Regular shift (e.g., 8 AM to 8 PM)
					if shift_start_time <= current_time <= shift_end_time:
						current_shift = shift.shift_name
						print(f"Current Shift: {current_shift}")
						break
				else:  
					# Overnight shift (e.g., 8 PM to 8 AM)
					if current_time >= shift_start_time or current_time <= shift_end_time:
						current_shift = shift.shift_name
						print(f"Current Shift: {current_shift}")
						break
			
			if not current_shift:
				print("No active shift found for the current time")
				return None

			# Determine which date to check for overnight shifts
			# If we're in an overnight shift and current time is before shift end (morning hours),
			# we need to check the previous date's jobs
			search_date = nowdate()
			
			# For overnight shifts, if current time is in morning hours (before noon),
			# check previous date as well
			for shift in factory_doc.get("shift_timings"):
				if shift.shift_name == current_shift:
					shift_start_time = to_time(shift.start_time)
					shift_end_time = to_time(shift.end_time)
					
					if shift_start_time > shift_end_time:  # Overnight shift
						if current_time <= shift_end_time:  # We're in the morning part
							search_date = frappe.utils.add_days(nowdate(), -1)
							print(f"Overnight shift detected, searching for jobs from: {search_date}")
					break

			# Get all jobs for this machine, date, and shift
			scheduled_jobs = frappe.get_all(
				"Job Card",
				filters={
					"machine": machine,
					"date": search_date,
					"shift": current_shift,
				},
				order_by="job_sequence_number asc",
				fields=["name", "status", "job_sequence_number"],
			)

			if not scheduled_jobs:
				print(f"No jobs found for machine: {machine}, date: {search_date}, shift: {current_shift}")
				return None

			print(f"Found {len(scheduled_jobs)} jobs for date: {search_date}, shift: {current_shift}")

			# Check job with sequence number 1
			job_seq_1 = next((job for job in scheduled_jobs if job.job_sequence_number == 1), None)

			if job_seq_1 and job_seq_1.status == "Not Started":
				job_card = frappe.get_doc("Job Card", job_seq_1.name)
				job_card.status = "In Progress"
				job_card.actual_start_date_time = current_datetime
				job_card.save()
				print(f"Started job sequence 1: {job_card.name}")
				return job_card.name
			else:
				# Check for job with sequence number 2
				job_seq_2 = next((job for job in scheduled_jobs if job.job_sequence_number == 2), None)
				if job_seq_2 and job_seq_2.status == "Not Started":
					job_card = frappe.get_doc("Job Card", job_seq_2.name)
					job_card.status = "In Progress"
					job_card.actual_start_date_time = current_datetime
					job_card.save()
					print(f"Started job sequence 2: {job_card.name}")
					return job_card.name
				else:
					print("No available jobs to start (sequence 1 and 2 either don't exist or are not 'Not Started')")
					return None

		except Exception as e:
			frappe.log_error(frappe.get_traceback(), "Start Job Error")
			return None
	
	
	def start_job_old(self, machine):
		"""
		0. In a Try Block do the following
		1. Get current_date
		2. Get current_time
		3. From Machine Get Factory
		4. Based on current_time get shift as current_shift from shift_timings table in Factory Doctype
		5. Based on machine, current_date, current_shift get scheduled_jobs from Job Card Doctype in ascending order of job_sequence_number
		6. First check status of scheduled_job where job_sequence_number == 1. if the status is 'Not Started' then change the status as 'In Progress' and return the job
		7. If the status of scheduled_job where job_sequence_number == 1 is not 'Not Started' then check for scheduled_job where job_sequence_number == 2. if such job exists then change the status as 'In Progress' and return the job else return None
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
				job_card.actual_start_date_time = now()
				job_card.save()
				return job_card.name
			else:
				# Check for job with sequence number 2
				job_seq_2 = next((job for job in scheduled_jobs if job.job_sequence_number == 2), None)
				if job_seq_2 and job_seq_2.status == "Not Started":
					job_card = frappe.get_doc("Job Card", job_seq_2.name)
					job_card.status = "In Progress"
					job_card.actual_start_date_time = now()
					job_card.save()
					return job_card.name
				else:
					return None

		except Exception as e:
			frappe.log_error(frappe.get_traceback(), "Start Job Error")
			return None
				

	def downtime_checker(self, machine_status):
		try:
			existing_downtime_log = self.downtime_record_checker()
			if machine_status == 'running':
				if existing_downtime_log:
					print('Existing Downtime Log Found, Closing Downtime Log')
					self.close_downtime_log(existing_downtime_log)
					print('Downtime Log Closed')
				else:
					print('No Existing Downtime Log Found, No Action Needed')
			elif machine_status == 'stopped':
				if not existing_downtime_log:
					print('No Existing Downtime Log Found, Creating New Downtime Log')
					self.create_downtime_log()
					print('Downtime Log Created')
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), "Downtime Checker Error")
	
	def downtime_record_checker(self):
		"""Check for existing open downtime logs."""
		try:
			print("Downtime Record Checker Called")
			downtime_logs = frappe.get_all(
				"Downtime Log",
				filters={"machine": self.machine, "status": "Open"},
				fields=["name"],
			)
			return downtime_logs[0].name if downtime_logs else None
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), "Downtime Record Checker Error")
			return None

	def create_downtime_log(self):
		"""Create a new downtime log entry."""
		try:
			downtime_log = frappe.new_doc("Downtime Log")
			downtime_log.machine = self.machine
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

def previous_job_counter_reset_function(machine, output_value):
	"""
	requirements:
	1. Get the job card document previous to the active job
	2. Check if the previous job completed quantity is same as output_value
	3. if yes then return False else return True
	"""
	try:
		print(f'Checking Previous Job for Machine: {machine}, Output Value: {output_value}')
		previous_job = frappe.get_all(
			"Job Card",
			filters={"machine": machine, "status": "Completed"},
			order_by="actual_end_date_time desc",
			fields=["completed_quantity"],
			limit=1
		)
		if previous_job:
			print(f'Previous Job Found: {previous_job}')
			if previous_job[0].completed_quantity == output_value:
				print('Previous Job Completed Quantity Matches Output Value')
				return False
			else:
				print('Previous Job Completed Quantity Does Not Match Output Value')
				return True
		else:
			print('No Previous Job Found')
			return True
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Previous Job Counter Reset Function Error")
		return True
	


	# def handle_output_old(self, output_value, run_rate_value, timestamp, machine):
	# 	try:
	# 		active_job = self.get_active_job(machine)

	# 		if active_job:
	# 			print(f'Active Job Found: {active_job}')
	# 			active_job_doc = frappe.get_doc("Job Card", active_job)
	# 			job_completed_qty = active_job_doc.completed_quantity
	# 			if output_value > job_completed_qty:
	# 				pass

	# 			elif output_value < job_completed_qty:
	# 				pass


	# 			if job_completed_qty > 0 and output_value < job_completed_qty:

	# 				# Output dropped - check if we have a stored checker value
	# 				if active_job_doc.completed_quantity_checker is None or active_job_doc.completed_quantity_checker == 0:

	# 					# First time seeing a drop - store the current value for verification
	# 					print(f'First drop detected: {job_completed_qty} -> {output_value}. Storing checker value.')
	# 					active_job_doc.completed_quantity_checker = job_completed_qty
	# 					active_job_doc.save()
						
	# 					# Creating output log
	# 					output_log = frappe.new_doc("Output Log")
	# 					output_log.machine = machine
	# 					output_log.job_card = active_job
	# 					output_log.output = output_value
	# 					output_log.run_rate = run_rate_value
	# 					output_log.timestamp = timestamp
	# 					output_log.save()
	# 					print('Output Log Created')
					
	# 				else:
	# 					# We have a previous checker value - analyze the pattern
	# 					checker_value = active_job_doc.completed_quantity_checker
						
	# 					if output_value >= checker_value:
	# 						# Output recovered to previous level or higher - false drop confirmed
	# 						print(f'False drop confirmed. Output recovered: {output_value} >= {checker_value}')
	# 						active_job_doc.completed_quantity = output_value
	# 						active_job_doc.completed_quantity_checker = 0
	# 						active_job_doc.save()

	# 						# Creating output log
	# 						output_log = frappe.new_doc("Output Log")
	# 						output_log.machine = machine
	# 						output_log.job_card = active_job
	# 						output_log.output = output_value
	# 						output_log.run_rate = run_rate_value
	# 						output_log.timestamp = timestamp
	# 						output_log.save()
	# 						print('Output Log Created')
						
	# 					else:
	# 						# Output still below checker value - genuine reset confirmed
	# 						print(f'Genuine reset confirmed: {output_value} < {checker_value}. Completing job.')
	# 						active_job_doc.completed_quantity = checker_value
	# 						active_job_doc.completed_quantity_checker = 0
	# 						active_job_doc.status = 'Completed'
	# 						active_job_doc.actual_end_date_time = now()
	# 						active_job_doc.save()
	# 						if output_value > 0:
	# 							print('Output Value Detected, Checking Previous Job Completion')
	# 							previous_job_counter_reset = previous_job_counter_reset_function(machine, output_value)
	# 							if previous_job_counter_reset == False:
	# 								print('Counter of Previous Job Still Coming. Not Starting New Job')
	# 							else:
	# 								new_job = self.start_job(machine)
	# 								if new_job:
	# 									print(f'New Job Started: {new_job}')
	# 									new_job_doc = frappe.get_doc("Job Card", new_job)
	# 									new_job_doc.completed_quantity = output_value
	# 									new_job_doc.save()
	# 									# Creating output log for new job
	# 									output_log = frappe.new_doc("Output Log")
	# 									output_log.machine = machine
	# 									output_log.job_card = new_job
	# 									output_log.output = output_value
	# 									output_log.run_rate = run_rate_value
	# 									output_log.timestamp = timestamp
	# 									output_log.save()
	# 									print('Output Log Created for New Job')
	# 								else:
	# 									print('No New Job Started')
	# 			elif job_completed_qty > 0 and output_value >= job_completed_qty:
	# 				if active_job_doc.completed_quantity_checker:
	# 					active_job_doc.completed_quantity_checker = 0 
	# 				active_job_doc.completed_quantity = output_value
	# 				active_job_doc.save()

	# 				# Creating output log
	# 				output_log = frappe.new_doc("Output Log")
	# 				output_log.machine = machine
	# 				output_log.job_card = active_job
	# 				output_log.output = output_value
	# 				output_log.run_rate = run_rate_value
	# 				output_log.timestamp = timestamp
	# 				output_log.save()
	# 				print('Output Log Created')
	# 		else:
	# 			print('No Active Job Found, Starting New Job')
	# 			if output_value > 0:
	# 				print('Output Value Detected, Checking Previous Job Completion')
	# 				previous_job_counter_reset = previous_job_counter_reset_function(machine, output_value)
	# 				if previous_job_counter_reset == False:
	# 					print('Counter of Previous Job Still Coming. Not Starting New Job')
	# 				else:
	# 					new_job = self.start_job(machine)
						
	# 					if new_job:
	# 						print(f'New Job Started: {new_job}')
	# 						new_job_doc = frappe.get_doc("Job Card", new_job)
	# 						new_job_doc.completed_quantity = output_value
	# 						new_job_doc.save()
	# 						# Creating output log for new job
	# 						output_log = frappe.new_doc("Output Log")
	# 						output_log.machine = machine
	# 						output_log.job_card = new_job
	# 						output_log.output = output_value
	# 						output_log.run_rate = run_rate_value
	# 						output_log.timestamp = timestamp
	# 						output_log.save()
	# 						print('Output Log Created for New Job')
	# 					else:
	# 						print('No New Job Started')
	# 			else:
	# 				print('No Output Value Detected, Not Starting New Job')
	# 				return None
	# 	except Exception as e:
	# 		frappe.log_error(frappe.get_traceback(), "Handle Output Error")