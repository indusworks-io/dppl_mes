import frappe
import json
from frappe import _
from datetime import datetime

@frappe.whitelist()
def create_telemetry():
    """
    POST API endpoint to create Telemetry documents
    Expected payload: {
        "timestamp": "2025-06-27 10:30:00",  # ISO format or frappe datetime format
        "device": "device_name",              # Must exist in Device doctype
        "machine": "machine_name",            # Must exist in Machine doctype  
        "message": "data or JSON object"      # Will be stored in data field
    }
    """
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
                # Try to parse timestamp to ensure it's valid
                datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            frappe.throw(_("Invalid timestamp format. Use ISO format (YYYY-MM-DD HH:MM:SS)"))
        
        # Validate that Device and Machine exist (optional but recommended)
        if not frappe.db.exists("Device", device):
            frappe.throw(_("Device '{}' does not exist").format(device))
            
        if not frappe.db.exists("Machine", machine):
            frappe.throw(_("Machine '{}' does not exist").format(machine))
        
        # Create new Telemetry document
        telemetry = frappe.new_doc("Telemetry")
        telemetry.timestamp = timestamp
        telemetry.device = device
        telemetry.machine = machine
        telemetry.data = message  # This will handle both strings and JSON objects
        
        # Insert with proper error handling
        telemetry.insert(ignore_permissions=True)
        frappe.db.commit()

        # Add Logic To Provide Job Metrics In Return
        
        return {
            "status": "success",
            "message": "Telemetry record created successfully",
            "telemetry_id": telemetry.name,
            "data": {
                "name": telemetry.name,
                "timestamp": telemetry.timestamp,
                "device": telemetry.device,
                "machine": telemetry.machine
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
def get_job_metrics(machine):
    """
    Fetch latest 'In Progress' Job Card for a machine and return key metrics.
    If no job is found, return default values (all zeros and empty strings).
    """
    if frappe.request.method != "GET":
        frappe.throw(_("Only GET requests are allowed"), frappe.PermissionError)
    
    try:
        # Parse the JSON data from request body
        if not frappe.request.data:
            frappe.throw(_("Request body is empty"))
        
        data = json.loads(frappe.request.data)
        
        machine = data.get("machine")

        # Check if machine exists
        if not frappe.db.exists("Machine", machine):
            return {
                "status": "error",
                "message": f"Machine '{machine}' does not exist",
                "data": {
                    "job_name": "",
                    "job_number": "",
                    "target_quantity": 0,
                    "completed_quantity": 0,
                    "run_rate_indicator": 0
                }
            }
    except Exception:
        frappe.log_error(frappe.get_traceback(), f"Error in get_job_metrics for machine {machine}")
    try:
        # Get latest job card directly
        job_card = frappe.get_value(
            "Job Card",
            filters={"machine": machine, "status": "In Progress"},
            fieldname=[
                "job_name",
                "job_number",
                "target_quantity",
                "completed_quantity",
                "target_run_rate",
                "actual_run_rate"
            ],
            order_by="creation desc",
            as_dict=True
        )

        # Default values if no job card exists
        if not job_card:
            return {
                "status": "success",
                "message": f"No job in progress for machine {machine}, returning defaults",
                "data": {
                    "job_name": "",
                    "job_number": "",
                    "target_quantity": 0,
                    "completed_quantity": 0,
                    "run_rate_indicator": 0
                }
            }

        # Compute run_rate_indicator safely
        target_rate = job_card.target_run_rate or 0
        actual_rate = job_card.actual_run_rate or 0
        run_rate_indicator = 1 if actual_rate >= target_rate else 0

        return {
            "status": "success",
            "message": "Job metrics retrieved successfully",
            "data": {
                "job_name": job_card.job_name or "",
                "job_number": job_card.job_number or "",
                "target_quantity": job_card.target_quantity or 0,
                "completed_quantity": job_card.completed_quantity or 0,
                "run_rate_indicator": run_rate_indicator
            }
        }

    except Exception:
        frappe.log_error(frappe.get_traceback(), f"Error in get_job_metrics for machine {machine}")
        return {
            "status": "error",
            "message": "Internal server error occurred while fetching job metrics",
            "data": {
                "job_name": "",
                "job_number": "",
                "target_quantity": 0,
                "completed_quantity": 0,
                "run_rate_indicator": 0
            }
        }

        
    

# Optional: Bulk create endpoint for multiple telemetry records
@frappe.whitelist(allow_guest=True)
def create_telemetry_bulk():
    """
    POST API endpoint to create multiple Telemetry documents in bulk
    Expected payload: {
        "records": [
            {
                "timestamp": "2025-06-27 10:30:00",
                "device": "device_name", 
                "machine": "machine_name",
                "message": "data"
            },
            // ... more records
        ]
    }
    """
    if frappe.request.method != "POST":
        frappe.throw(_("Only POST requests are allowed"), frappe.PermissionError)
    
    try:
        data = json.loads(frappe.request.data)
        records = data.get("records", [])
        
        if not records:
            frappe.throw(_("No records provided"))
        
        if len(records) > 1000:  # Limit bulk operations
            frappe.throw(_("Cannot process more than 1000 records at once"))
        
        created_records = []
        errors = []
        
        for i, record in enumerate(records):
            try:
                timestamp = record.get("timestamp")
                device = record.get("device")
                machine = record.get("machine")
                message = record.get("message")
                
                if not all([timestamp, device, machine, message]):
                    errors.append(f"Record {i+1}: Missing required fields")
                    continue
                
                telemetry = frappe.new_doc("Telemetry")
                telemetry.timestamp = timestamp
                telemetry.device = device
                telemetry.machine = machine
                telemetry.data = message
                
                telemetry.insert(ignore_permissions=True)
                created_records.append(telemetry.name)
                
            except Exception as e:
                errors.append(f"Record {i+1}: {str(e)}")
        
        frappe.db.commit()
        
        return {
            "status": "success" if not errors else "partial_success",
            "message": f"Created {len(created_records)} records",
            "created_count": len(created_records),
            "error_count": len(errors),
            "created_records": created_records,
            "errors": errors if errors else None
        }
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Bulk Create Telemetry Error")
        frappe.response["http_status_code"] = 500
        return {
            "status": "error",
            "message": str(e)
        }