import frappe
from frappe.utils import add_days, now
from pywebpush import webpush
import json


def delete_old_telemetry_records(days=60, batch_size=1000):
	"""
	Delete Telemetry records older than the specified number of days.

	Args:
		days (int): Number of days to retain. Records older than this will be deleted. Default is 60.
		batch_size (int): Number of records to delete in each batch. Default is 1000.

	Returns:
		dict: Dictionary containing success status, total deleted count, and message.

	Example:
		# Delete records older than 60 days
		result = delete_old_telemetry_records()

		# Delete records older than 30 days
		result = delete_old_telemetry_records(days=30)
	"""
	try:
		# Calculate cutoff date
		cutoff_date = add_days(now(), -days)

		frappe.logger().info(f"Starting deletion of Telemetry records older than {cutoff_date}")

		# Get count of records to be deleted
		total_records = frappe.db.count(
			"Telemetry",
			filters={"timestamp": ["<", cutoff_date]}
		)

		if total_records == 0:
			message = f"No Telemetry records found older than {days} days"
			frappe.logger().info(message)
			return {
				"success": True,
				"deleted_count": 0,
				"message": message
			}

		frappe.logger().info(f"Found {total_records} records to delete")

		deleted_count = 0

		# Delete records in batches
		while True:
			# Get batch of old records
			old_records = frappe.get_all(
				"Telemetry",
				filters={"timestamp": ["<", cutoff_date]},
				fields=["name"],
				limit=batch_size
			)

			if not old_records:
				break

			# Delete each record in the batch
			for record in old_records:
				try:
					frappe.delete_doc("Telemetry", record.name, force=1, ignore_permissions=True)
					deleted_count += 1
				except Exception as e:
					frappe.log_error(
						f"Error deleting Telemetry record {record.name}: {str(e)}",
						"Telemetry Deletion Error"
					)

			# Commit after each batch to avoid large transactions
			frappe.db.commit()

			frappe.logger().info(f"Deleted {deleted_count} of {total_records} records")

		message = f"Successfully deleted {deleted_count} Telemetry records older than {days} days"
		frappe.logger().info(message)

		return {
			"success": True,
			"deleted_count": deleted_count,
			"message": message
		}

	except Exception as e:
		error_message = f"Error deleting old Telemetry records: {str(e)}"
		frappe.log_error(frappe.get_traceback(), "Delete Old Telemetry Records Error")
		frappe.logger().error(error_message)

		return {
			"success": False,
			"deleted_count": 0,
			"message": error_message
		}

