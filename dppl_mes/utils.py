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


def get_supervisors_from_area(area_name):
	"""
	Retrieve list of supervisor users for a given area.

	Args:
		area_name (str): Name of the Area

	Returns:
		list: List of user email addresses who are supervisors for this area
	"""
	if not area_name:
		return []

	try:
		# Get the Area document
		area = frappe.get_doc("Area", area_name)

		# Extract supervisors from the child table
		supervisors = []
		if hasattr(area, 'supervisors') and area.supervisors:
			for supervisor_row in area.supervisors:
				if hasattr(supervisor_row, 'user') and supervisor_row.user:
					supervisors.append(supervisor_row.user)

		return supervisors
	except Exception as e:
		frappe.log_error(
			f"Error fetching supervisors for area {area_name}: {str(e)}",
			"Get Supervisors Error"
		)
		return []


def get_push_subscriptions(user):
	"""
	Retrieve all active push subscriptions for a given user.

	Args:
		user (str): User email address

	Returns:
		list: List of subscription dictionaries with endpoint and keys
	"""
	if not user:
		return []

	try:
		subscriptions = frappe.get_all(
			"Push Subscription",
			filters={"user": user, "enabled": 1},
			fields=["name", "endpoint", "p256dh", "auth"]
		)

		return subscriptions
	except Exception as e:
		frappe.log_error(
			f"Error fetching push subscriptions for user {user}: {str(e)}",
			"Get Push Subscriptions Error"
		)
		return []


def send_push_notification(subscription, payload, settings):
	"""
	Send a web push notification to a single subscription endpoint.

	Args:
		subscription (dict): Subscription info with endpoint, p256dh, auth
		payload (dict): Notification payload with title, body, url, etc.
		settings: Downtime Settings document with VAPID keys

	Returns:
		bool: True if successful, False otherwise
	"""
	try:
		# Build subscription info object for pywebpush
		sub_info = {
			"endpoint": subscription.get("endpoint"),
			"keys": {
				"p256dh": subscription.get("p256dh"),
				"auth": subscription.get("auth")
			}
		}

		# Build VAPID claims
		vapid_claims = {
			"sub": f"mailto:{settings.contact_email}" if settings.contact_email else "mailto:noreply@example.com"
		}

		# Send the push notification
		webpush(
			subscription_info=sub_info,
			data=json.dumps(payload),
			vapid_private_key=settings.vapid_private_key,
			vapid_claims=vapid_claims
		)

		return True

	except Exception as e:
		error_str = str(e)
		subscription_name = subscription.get('name', 'unknown')

		# Check if this is a permanent error (subscription no longer valid)
		if '410' in error_str or 'Gone' in error_str or 'Unregistered' in error_str:
			frappe.logger().warning(
				f"Subscription {subscription_name} is no longer valid (410 Gone). Disabling it."
			)

			# Disable the invalid subscription to prevent future errors
			try:
				frappe.db.set_value("Push Subscription", subscription_name, "enabled", 0)
				frappe.db.commit()
				frappe.logger().info(f"Disabled invalid push subscription {subscription_name}")
			except Exception as db_error:
				frappe.logger().error(f"Failed to disable subscription {subscription_name}: {db_error}")

			# Only log critical errors, not routine subscription cleanup
			return False

		# For other errors, log them but keep subscription active
		frappe.log_error(
			f"Push notification failed for subscription {subscription_name}: {error_str}",
			"Push Notification Error"
		)
		return False


def downtime_log_notification():
	"""
	Send web push notifications to area supervisors for open downtime logs.

	This function is designed to run as a Frappe scheduler job. It:
	1. Checks if downtime notifications are enabled in Downtime Settings
	2. Queries for open downtime logs that haven't been notified yet
	3. Applies threshold logic based on settings (immediate or after threshold)
	4. Sends push notifications to all supervisors of the affected area
	5. Updates the notified flag after successful processing

	Configuration in Downtime Settings:
	- enable_downtime_notification_to_supervisors: Enable/disable notifications
	- when_to_notify: "Immediately" or "After Minor Stop Threshold"
	- minor_stop_threshold: Duration threshold in seconds
	- vapid_public_key, vapid_private_key: VAPID keys for web push
	- contact_email: Contact email for VAPID claims

	Usage:
		# Add to hooks.py under scheduler_events
		"cron": {
			"*/5 * * * *": [  # Every 5 minutes
				"dppl_mes.utils.downtime_log_notification"
			]
		}
	"""
	try:
		frappe.logger().info("Running downtime notification job")

		# Step 1: Get Downtime Settings
		settings = frappe.get_single("Downtime Settings")

		# Early exit if notifications are disabled
		if not settings.enable_downtime_notification_to_supervisors:
			frappe.logger().info("Downtime notifications are disabled in settings")
			return

		# Validate required settings
		if not settings.vapid_private_key:
			frappe.log_error("VAPID private key not configured in Downtime Settings", "Downtime Notification Error")
			return

		# Step 2: Query open downtime logs that haven't been notified
		open_logs = frappe.get_all(
			"Downtime Log",
			filters={"status": "Open", "notified": 0},
			fields=["name", "machine", "start_date_time", "reason", "category"]
		)

		if not open_logs:
			frappe.logger().info("No open unnotified downtime logs found")
			return

		frappe.logger().info(f"Found {len(open_logs)} open unnotified downtime logs")

		# Step 3: Apply threshold logic based on when_to_notify setting
		qualifying_logs = []
		current_time = frappe.utils.now_datetime()

		if settings.when_to_notify == "After Minor Stop Threshold":
			# Filter logs that have exceeded the threshold
			threshold_seconds = int(settings.minor_stop_threshold or 0)

			for log in open_logs:
				if not log.start_date_time:
					continue

				# Calculate duration in seconds
				start_dt = frappe.utils.get_datetime(log.start_date_time)
				duration_seconds = int((current_time - start_dt).total_seconds())

				# Only include logs that exceed threshold
				if duration_seconds >= threshold_seconds:
					qualifying_logs.append(log)

			frappe.logger().info(
				f"{len(qualifying_logs)} logs exceed threshold of {threshold_seconds} seconds"
			)
		else:
			# when_to_notify == "Immediately" - use all open logs
			qualifying_logs = open_logs

		if not qualifying_logs:
			frappe.logger().info("No downtime logs qualify for notification")
			return

		# Step 4: Process each qualifying downtime log
		for log in qualifying_logs:
			try:
				# Get the machine's area
				machine_doc = frappe.get_doc("Machine", log.machine)
				area_name = machine_doc.area

				if not area_name:
					frappe.logger().warning(f"Machine {log.machine} has no area assigned")
					continue

				# Get supervisors for this area
				supervisors = get_supervisors_from_area(area_name)

				if not supervisors:
					frappe.logger().warning(f"No supervisors found for area {area_name}")
					continue

				# Prepare notification payload
				payload = {
					"title": f"Open Downtime: {log.machine}",
					"body": f"Started at {log.start_date_time} — Reason: {log.reason or 'Not specified'}",
					"url": f"/frontend/production/downtime-logs/{log.name}",
					"downtime_log": log.name
				}

				# Send notification to each supervisor
				notification_sent = False
				for supervisor in supervisors:
					# Get all active subscriptions for this supervisor
					subscriptions = get_push_subscriptions(supervisor)

					if not subscriptions:
						frappe.logger().info(f"No active subscriptions for supervisor {supervisor}")
						continue

					# Send to each subscription
					for subscription in subscriptions:
						success = send_push_notification(subscription, payload, settings)
						if success:
							notification_sent = True
							frappe.logger().info(
								f"Notification sent to {supervisor} for downtime {log.name}"
							)

				# Step 5: Mark log as notified after processing
				if notification_sent:
					frappe.db.set_value("Downtime Log", log.name, "notified", 1)
					frappe.db.commit()
					frappe.logger().info(f"Marked downtime log {log.name} as notified")

			except Exception as log_error:
				# Log error but continue processing other logs
				frappe.log_error(
					f"Error processing downtime log {log.name}: {str(log_error)}\n{frappe.get_traceback()}",
					"Downtime Notification Processing Error"
				)
				continue

		frappe.logger().info("Downtime notification job completed successfully")

	except Exception as e:
		# Log overall errors
		frappe.log_error(
			f"Error in downtime_log_notification: {str(e)}\n{frappe.get_traceback()}",
			"Downtime Notification Job Error"
		)
		frappe.logger().error(f"Downtime notification job failed: {str(e)}")

def cleanup_invalid_push_subscriptions():
	"""
	Cleanup disabled push subscriptions that have been invalid for a long time.

	This function should be run periodically (e.g., weekly) as a scheduled job
	to remove old disabled subscriptions and keep the database clean.

	Subscriptions that have been disabled for more than 30 days will be permanently deleted.

	Usage:
		# Add to hooks.py under scheduler_events
		"cron": {
			"0 0 * * 0": [  # Every Sunday at midnight
				"dppl_mes.utils.cleanup_invalid_push_subscriptions"
			]
		}
	"""
	try:
		frappe.logger().info("Starting cleanup of invalid push subscriptions")

		# Find subscriptions that have been disabled for more than 30 days
		cutoff_date = add_days(now(), -30)

		old_disabled_subscriptions = frappe.get_all(
			"Push Subscription",
			filters={
				"enabled": 0,
				"modified": ["<", cutoff_date]
			},
			fields=["name", "user", "endpoint"]
		)

		if not old_disabled_subscriptions:
			frappe.logger().info("No old disabled subscriptions found for cleanup")
			return

		frappe.logger().info(
			f"Found {len(old_disabled_subscriptions)} old disabled subscriptions to delete"
		)

		deleted_count = 0
		for subscription in old_disabled_subscriptions:
			try:
				frappe.delete_doc(
					"Push Subscription",
					subscription.name,
					force=1,
					ignore_permissions=True
				)
				deleted_count += 1
				frappe.logger().info(
					f"Deleted old subscription {subscription.name} for user {subscription.user}"
				)
			except Exception as e:
				frappe.logger().error(
					f"Failed to delete subscription {subscription.name}: {str(e)}"
				)

		frappe.db.commit()
		frappe.logger().info(
			f"Cleanup completed: Successfully deleted {deleted_count} old push subscriptions"
		)

	except Exception as e:
		frappe.log_error(
			f"Error in cleanup_invalid_push_subscriptions: {str(e)}\n{frappe.get_traceback()}",
			"Push Subscription Cleanup Error"
		)
		frappe.logger().error(f"Push subscription cleanup job failed: {str(e)}")


def close_open_job_cards():
	"""


	"""
	pass