import frappe
import json
from frappe import _
from datetime import datetime
from frappe.utils import now, now_datetime, time_diff_in_seconds


@frappe.whitelist(methods=["POST"], allow_guest=True)
def get_context_for_dev():
	return get_boot()


def get_boot():
	return frappe._dict(
		{
			"frappe_version": frappe.__version__,
			"default_route": get_default_route(),
			"site_name": frappe.local.site,
			"csrf_token": frappe.sessions.get_csrf_token(),
		}
	)

def get_default_route():
	return "/frontend"

@frappe.whitelist()
def create_telemetry():
    if frappe.request.method != "POST":
        frappe.throw(_("Only POST requests are allowed"), frappe.PermissionError)
    try:
        # Parse the JSON data from request body
        if not frappe.request.data:
            frappe.throw(_("Request body is empty"))
        data = json.loads(frappe.request.data)
        
        # Extract fields with validation
        timestamp = data.get("timestamp")
        device = data.get("device")
        machine = data.get("machine")
        message = data.get("message")
        
        # Validate required fields
        if not all([timestamp, device, machine, message]):
            frappe.throw(_("Missing required fields. Required: timestamp, device, machine, message"))
        
        # Validate timestamp format
        try:
            if isinstance(timestamp, str):
                datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            frappe.throw(_("Invalid timestamp format. Use ISO format (YYYY-MM-DD HH:MM:SS)"))
        
        # Validate that Device and Machine exist
        if not frappe.db.exists("Device", device):
            frappe.throw(_("Device '{}' does not exist").format(device))
        if not frappe.db.exists("Machine", machine):
            frappe.throw(_("Machine '{}' does not exist").format(machine))
        
        # Create new Telemetry document
        telemetry = frappe.new_doc("Telemetry")
        telemetry.timestamp = timestamp
        telemetry.device = device
        telemetry.machine = machine
        telemetry.data = message
        telemetry.insert(ignore_permissions=True)
        frappe.db.commit()

        job_metrics = get_job_metrics_internal_function(machine=machine)
        metrics_data = job_metrics.get("data", {})

        # Publish realtime update to frontend
        publish_data = {
            "machine": machine,
            "job_metrics": metrics_data
        }
        
        try:
            # Publish to all users in the 'all' room (frontend auto-joins this room)
            frappe.publish_realtime(
                event='job_metrics_update',
                message=publish_data
            )
            print(f"📡 Published job_metrics_update for machine '{machine}'")
            
        except Exception as e:
            print(f"❌ Error publishing realtime event: {e}")
            frappe.log_error(frappe.get_traceback(), "Realtime Publishing Error")

        return {
            "status": "success",
            "message": "Telemetry record created and realtime update published",
            "data": {
                "machine": machine,
                "job_metrics": metrics_data
            }
        }
        
    except frappe.ValidationError as e:
        frappe.log_error(frappe.get_traceback(), "Telemetry Validation Error")
        frappe.response["http_status_code"] = 400
        return {
            "status": "error",
            "error_type": "validation_error",
            "message": str(e)
        }
        
    except json.JSONDecodeError as e:
        frappe.log_error(frappe.get_traceback(), "Telemetry JSON Parse Error")
        frappe.response["http_status_code"] = 400
        return {
            "status": "error", 
            "error_type": "json_error",
            "message": "Invalid JSON format in request body"
        }
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Create Telemetry Error")
        frappe.response["http_status_code"] = 500
        return {
            "status": "error",
            "error_type": "server_error", 
            "message": "Internal server error occurred"
        }



@frappe.whitelist()
def get_job_metrics_internal_function(machine=None):
    try:
        job_card = frappe.get_value(
            "Job Card",
            filters={"machine": machine, "status": "In Progress"},
            fieldname=[
                "job_name",
                "job_number",
                "target_quantity",
                "completed_quantity",
                "planned_start_date_time",
                "planned_duration"
            ],
            order_by="creation desc",
            as_dict=True
        )

        if not job_card:
            return {
                "status": "failure",
                "data": {
                    "job_name": "No Job Running",
                    "job_number": "N/A",
                    "target_quantity": 0,
                    "completed_quantity": 0,
                    "balance_quantity": 0,
                    "run_rate_indicator": 0,
                    "current_time": now()
                }
            }

        planned_start_time = job_card.planned_start_date_time
        current_time = now_datetime()

        if current_time < planned_start_time:
            time_spent_in_seconds = 0
        else:
            time_spent_in_seconds = time_diff_in_seconds(current_time, planned_start_time)

        total_time = job_card.planned_duration or 0
        target_qty = job_card.target_quantity or 0
        actual_quantity = job_card.completed_quantity or 0
        balance_quantity = max(target_qty - actual_quantity, 0)

        ideal_quantity = (time_spent_in_seconds / total_time) * target_qty if total_time else 0
        ideal_quantity = min(ideal_quantity, target_qty)

        run_rate_indicator = 1 if actual_quantity >= ideal_quantity else 0
        print(f'Machine {machine}: Actual {actual_quantity}/{target_qty}, Run Rate: {run_rate_indicator}')

        return {
            "status": "success",
            "data": {
                "job_name": job_card.job_name or "",
                "job_number": job_card.job_number or "",
                "target_quantity": target_qty,
                "completed_quantity": actual_quantity,
                "balance_quantity": balance_quantity,
                "run_rate_indicator": run_rate_indicator,
                "current_time": now()
            }
        }

    except Exception:
        frappe.log_error(frappe.get_traceback(), f"Error in get_job_metrics for machine {machine}")
        return {
            "status": "error",
            "data": {
                "job_name": "",
                "job_number": "",
                "target_quantity": 0,
                "completed_quantity": 0,
                "run_rate_indicator": 0
            }
        }



# @frappe.whitelist()
# def get_job_metrics_internal_function(machine=None):
#     print(f"Fetching job metrics for machine: {machine}")
#     """
#     Fetch latest 'In Progress' Job Card for a machine and return key metrics.
#     Always returns metrics inside a 'data' key.
#     """
#     try:
#         job_card = frappe.get_value(
#             "Job Card",
#             filters={"machine": machine, "status": "In Progress"},
#             fieldname=[
#                 "job_name",
#                 "job_number",
#                 "target_quantity",
#                 "completed_quantity",
#                 "planned_start_date_time",
#                 "planned_duration"
#             ],
#             order_by="creation desc",
#             as_dict=True
#         )

#         if not job_card:
#             return {
#                 "status": "failure",
#                 "data": {
#                     "job_name": "No Job Running",
#                     "job_number": "N/A",
#                     "target_quantity": 0,
#                     "completed_quantity": 0,
#                     "balance_quantity": 0,
#                     "run_rate_indicator": 0,
#                     "current_time": now()
#                 }
#             }

#         # Calculate Time Spent as difference between now and planned start time
#         planned_start_time = job_card.planned_start_date_time
#         current_time = now_datetime()
#         time_spent_in_seconds = abs(time_diff_in_seconds(current_time, planned_start_time))
#         total_time = job_card.planned_duration
#         ideal_quantity = (time_spent_in_seconds / total_time) * job_card.target_quantity if total_time else 0
#         actual_quantity = job_card.completed_quantity or 0
#         balance_quantity = job_card.target_quantity - actual_quantity

#         print(f'Time Spent: {time_spent_in_seconds}, Total Time: {total_time}, Ideal Quantity: {ideal_quantity}, Actual Quantity: {actual_quantity}, Balance Quantity: {balance_quantity}')

#         if actual_quantity >= ideal_quantity:
#             run_rate_indicator = 1
#         else:
#             run_rate_indicator = 0

#         return {
#             "status": "success",
#             "data": {
#                 "job_name": job_card.job_name or "",
#                 "job_number": job_card.job_number or "",
#                 "target_quantity": job_card.target_quantity or 0,
#                 "completed_quantity": job_card.completed_quantity or 0,
#                 "balance_quantity": balance_quantity or 0,
#                 "run_rate_indicator": run_rate_indicator,
#                 "current_time": now()
#             }
#         }

#     except Exception:
#         frappe.log_error(frappe.get_traceback(), f"Error in get_job_metrics for machine {machine}")
#         return {
#             "status": "error",
#             "data": {
#                 "job_name": "",
#                 "job_number": "",
#                 "target_quantity": 0,
#                 "completed_quantity": 0,
#                 "run_rate_indicator": 0
#             }
#         }


@frappe.whitelist()
def get_all_machines_job_metrics():
    """
    Fetch job metrics for all active machines in one API call.
    Returns a dictionary mapping machine names to their job metrics.
    """
    try:
        # Get all active machines
        machines = frappe.get_all(
            "Machine",
            fields=["name"],
            filters={"is_active": "1"}
        )
        
        if not machines:
            return {
                "status": "success",
                "data": {}
            }
        
        # Collect job metrics for each machine
        all_metrics = {}
        
        for machine in machines:
            machine_name = machine.name
            # Use the existing job metrics function
            metrics_response = get_job_metrics_internal_function(machine=machine_name)
            
            if metrics_response.get("status") == "success":
                all_metrics[machine_name] = metrics_response.get("data", {})
            else:
                # Include failed machines with empty metrics
                all_metrics[machine_name] = {
                    "job_name": "No Job Running",
                    "job_number": "N/A",
                    "target_quantity": 0,
                    "completed_quantity": 0,
                    "balance_quantity": 0,
                    "run_rate_indicator": 0,
                    "current_time": now()
                }
        
        return {
            "status": "success",
            "data": all_metrics,
            "machines_count": len(machines)
        }
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in get_all_machines_job_metrics")
        return {
            "status": "error",
            "message": "Failed to fetch job metrics for all machines",
            "data": {}
        }



############ Energy Logs ##################
@frappe.whitelist()
def create_energy_log():
    if frappe.request.method != "POST":
        frappe.throw(_("Only POST requests are allowed"), frappe.PermissionError)
    try:
        # Parse the JSON data from request body
        if not frappe.request.data:
            frappe.throw(_("Request body is empty"))
        data = json.loads(frappe.request.data)
        
        # Extract fields with validation
        timestamp = data.get("timestamp")
        energy_meter = data.get("energy_meter")
        machine = data.get("machine")
        message = data.get("message")
        
        # Validate required fields
        if not all([timestamp, energy_meter, machine, message]):
            frappe.throw(_("Missing required fields. Required: timestamp, device, machine, message"))
        
        # Validate timestamp format
        try:
            if isinstance(timestamp, str):
                datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            frappe.throw(_("Invalid timestamp format. Use ISO format (YYYY-MM-DD HH:MM:SS)"))
        
        # Validate that Energy Meter and Machine exist
        if not frappe.db.exists("Energy Meter", energy_meter):
            frappe.throw(_("Energy Meter '{}' does not exist").format(energy_meter))
        if not frappe.db.exists("Machine", machine):
            frappe.throw(_("Machine '{}' does not exist").format(machine))
        
        # Create new Telemetry document
        telemetry = frappe.new_doc("Energy Log")
        telemetry.timestamp = timestamp
        telemetry.energy_meter = energy_meter
        telemetry.machine = machine
        telemetry.data = message
        telemetry.insert(ignore_permissions=True)
        frappe.db.commit()
    
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Create Energy Log Error")
        frappe.response["http_status_code"] = 500
        return {
            "status": "error",
            "error_type": "server_error", 
            "message": "Internal server error occurred"
        }