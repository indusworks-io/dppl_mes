You are an expert Frappe and Python developer. 
Your task is to generate/update a complete and correct `downtime_log_notification()` function in Utils.py 
for a Frappe application that sends Web Push notifications using `pywebpush`.

Before writing any code, do the following:

1. **Inspect DocType JSON definitions**:
   - Check the following DocType JSON files in the app to confirm actual fieldnames, fieldtypes, and options:
     - `downtime_settings.json` (Single Doctype)
     - `downtime_log.json`
     - `area.json`
     - `push_subscription.json`
   - Confirm exact fieldnames like `enable_downtime_notification_to_supervisors`, `when_to_notify`, `minor_stop_threshold`, `vapid_public_key`, `vapid_private_key`, `contact_email`, `status`, `notified`, `start_datetime`, `machine`, and `area`.
   - Confirm how supervisors are linked in the `Area` DocType (single Link, child table, or comma-separated list).

2. **Design the function** so it does the following:
   - Retrieve `Downtime Settings` using `frappe.get_single("Downtime Settings")`.
   - If `enable_downtime_notification_to_supervisors` is unchecked or false, exit early.
   - Query `Downtime Log` for all records with:
     - `status = "Open"`
     - `notified = 0` or `False`
   - If no records found, return.
   - Retrieve from settings:
     - `when_to_notify`
     - `minor_stop_threshold`
     - `vapid_public_key`
     - `vapid_private_key`
     - `contact_email`
   - If `when_to_notify == "After Minor Stop Threshold"`:
     - Get current datetime (`frappe.utils.now_datetime()`).
     - Calculate duration between current time and `start_datetime` for each downtime log.
     - Filter only logs whose duration (in minutes) >= `minor_stop_threshold`.
     - If filtered list empty, return.
   - If `when_to_notify == "Immediately"`:
     - Use all open downtime logs directly.
   - For each qualifying downtime log:
     - Determine supervisors for the downtime’s `area` (based on Area DocType structure).
     - For each supervisor:
       - Fetch all active push subscriptions from `Push Subscription` (where `user=supervisor` and `enabled=1`).
       - For each subscription:
         - Send push notification using `pywebpush.webpush()` with payload containing:
           ```
           {
             "title": f"Open Downtime: {machine}",
             "body": f"Started at {start_datetime} — Reason: {reason}",
             "url": f"/downtime/{downtime_log_name}", (This URL should Be Compatible with The Frontend Vue JS Application)
             "downtime_log": downtime_log_name
           }
           ```
         - Use `vapid_private_key` and `contact_email` from settings for `vapid_claims`.
         - Catch and log any exceptions (e.g., invalid subscription) but continue loop.
     - After successfully processing all supervisors for that log:
       - Update `Downtime Log.notified = 1`
       - Call `frappe.db.commit()` to persist (important for scheduler jobs).
   - Log any summary info with `frappe.log_error` or `frappe.logger()` if needed.

3. **Code quality expectations**:
   - The function must be safe to run in a Frappe scheduler.
   - It must handle missing or malformed fields gracefully (no crash).
   - Include meaningful comments for each logical step.
   - Use helper functions if needed, e.g.:
     - `get_supervisors_from_area(area_name)`
     - `get_push_subscriptions(user)`
     - `send_push_notification(subscription, payload, settings)`
   - Use Frappe utility functions for datetime handling: `frappe.utils.now_datetime()` and `frappe.utils.get_datetime()`.
   - Always commit after DB updates inside scheduler context.

4. **Output format**:
   - Provide a single Python file snippet containing the full `downtime_log_notification()` implementation with helper functions.
   - Include `import` statements and a brief docstring explaining purpose and usage.
   - Assume the function will be registered in `hooks.py` under `scheduler_events`.

After inspecting the JSON files and confirming actual fieldnames, write the final code following these requirements.
