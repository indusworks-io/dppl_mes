# Copyright (c) 2025, IndusWorks and contributors
# For license information, please see license.txt

import frappe
import datetime

def execute(filters=None):
    try:
        date = frappe.utils.today()
        columns = get_columns()
        data = get_data(date)
        return columns, data
    
    except Exception as e:
        frappe.log_error(f"Error in Job Report: {str(e)}", "Job Report")


def get_columns():

    # Simplified columns as requested:
    return [
        {'fieldname': 'machine', 'label': 'Machine', 'fieldtype': 'Link', 'options': 'Machine', 'width': 150},
        {'fieldname': 'operator', 'label': 'Operator', 'fieldtype': 'Data', 'width': 150},
        {'fieldname': 'job_name', 'label': 'Job Name', 'fieldtype': 'Link', 'options': 'Job', 'width': 200},
        {'fieldname': 'job_number', 'label': 'Job No.', 'fieldtype': 'Data', 'width': 150},
        {'fieldname': 'job_sequence', 'label': 'Job Sequence', 'fieldtype': 'Int', 'width': 50},
        {'fieldname': 'target_quantity', 'label': 'Target Quantity', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'completed_quantity_one_default_uom', 'label': 'Completed Quantity', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'completed_quantity_one_alternate_uom', 'label': 'Completed Quantity In Alternate Units', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'efficiency_percent', 'label': 'Efficiency (%)', 'fieldtype': 'Percent', 'width': 150},
        {'fieldname': 'machine_wastage', 'label': 'Machine Wastage', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'job_setting_wastage', 'label': 'Job Setting Wastage', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'roll_wastage', 'label': 'Roll Wastage', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'printing_wastage', 'label': 'Printing Wastage', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'barcode_wastage', 'label': 'Barcode Wastage', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'total_wastage', 'label': 'Total Wastage', 'fieldtype': 'Float', 'width': 150},
    ]


def get_data(date):
    # Active machines
    machines = frappe.get_all("Machine", filters={"is_active": "1", "area": "Extrusion Department"}, fields=["name", "sequence_number"], order_by="sequence_number asc")

    # Fetch job cards with specific fields
    job_cards = frappe.get_all(
        "Job Card",
        filters={
            "date": date,
            "shift": "Day Shift"
        },
        fields=[
            "machine", "date", "shift", "operator",
            "job_name", "job_number", "job_sequence_number",
            "target_quantity", "completed_quantity",
            "machine_wastage", "job_setting_wastage", "roll_wastage",
            "printing_wastage", "barcode_wastage", "total_wastage"
        ]
    )
    print(f"Date: {date}")
    print(f"Found {len(job_cards)} job cards for Day Shift")

    # Get conversion factors for all jobs
    job_names = list(set(job.get("job_name") for job in job_cards if job.get("job_name")))
    conversion_factors = {}
    if job_names:
        jobs = frappe.get_all("Job", filters={"name": ["in", job_names]}, fields=["name", "conversion_factor"])
        conversion_factors = {job.name: job.conversion_factor for job in jobs}
        print(f"Conversion factors: {conversion_factors}")

    # Create a lookup dictionary for job cards by machine
    job_cards_by_machine = {}
    for job in job_cards:
        machine_name = job.get("machine")
        if machine_name not in job_cards_by_machine:
            job_cards_by_machine[machine_name] = []
        job_cards_by_machine[machine_name].append(job)

    # Sort job cards within each machine by job_sequence_number
    for machine_name in job_cards_by_machine:
        job_cards_by_machine[machine_name].sort(key=lambda x: x.get("job_sequence_number", 0))

    data = []

    # Iterate through machines in sequence order
    for machine in machines:
        machine_name = machine['name']
        machine_jobs = job_cards_by_machine.get(machine_name, [])

        if machine_jobs:
            # Create rows for each job in sequence
            for job in machine_jobs:
                # Get conversion factor for this job
                conversion_factor = conversion_factors.get(job.get("job_name"), 1)

                # Calculate alternate UOM quantity
                completed_qty_alternate_uom = 0
                if job.get("completed_quantity") is not None and conversion_factor and conversion_factor > 0:
                    completed_qty_alternate_uom = job.get("completed_quantity") / conversion_factor

                # Calculate efficiency
                efficiency_percent = 0
                if job.get("target_quantity"):
                    efficiency_percent = (job.get("completed_quantity", 0) / job.get("target_quantity")) * 100

                row = {
                    "machine": job.get("machine"),
                    "operator": job.get("operator") or "Off",
                    "job_name": job.get("job_name"),
                    "job_number": job.get("job_number"),
                    "job_sequence": job.get("job_sequence_number"),
                    "target_quantity": job.get("target_quantity") or 0,
                    "completed_quantity_one_default_uom": job.get("completed_quantity") or 0,
                    "completed_quantity_one_alternate_uom": completed_qty_alternate_uom,
                    "efficiency_percent": efficiency_percent,
                    "machine_wastage": job.get("machine_wastage") or 0,
                    "job_setting_wastage": job.get("job_setting_wastage") or 0,
                    "roll_wastage": job.get("roll_wastage") or 0,
                    "printing_wastage": job.get("printing_wastage") or 0,
                    "barcode_wastage": job.get("barcode_wastage") or 0,
                    "total_wastage": job.get("total_wastage") or 0,
                }
                data.append(row)
        else:
            # Create "Off" row for machine with no jobs
            row = {
                "machine": machine_name,
                "operator": "Off",
                "job_name": "",
                "job_number": "",
                "job_sequence": 0,
                "target_quantity": 0,
                "completed_quantity_one_default_uom": 0,
                "completed_quantity_one_alternate_uom": 0,
                "efficiency_percent": 0,
                "machine_wastage": 0,
                "job_setting_wastage": 0,
                "roll_wastage": 0,
                "printing_wastage": 0,
                "barcode_wastage": 0,
                "total_wastage": 0,
            }
            data.append(row)

    print(f"Total data rows to return: {len(data)}")
    return data
