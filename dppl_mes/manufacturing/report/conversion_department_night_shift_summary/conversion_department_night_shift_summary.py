# Copyright (c) 2025, IndusWorks and contributors
# For license information, please see license.txt

import frappe
import datetime

def execute(filters=None):
    try:
        today = frappe.utils.today()
        date = frappe.utils.add_to_date(today, days=-1)
        print(date)
        columns = get_columns()
        data = get_data(date)
        return columns, data
    
    except Exception as e:
        frappe.log_error(f"Error in Job Report: {str(e)}", "Job Report")


def get_columns():
    
    # Final order as requested:
    return [
        {'fieldname': 'machine', 'label': 'Machine', 'fieldtype': 'Link', 'options': 'Machine', 'width': 150},
        {'fieldname': 'operator', 'label': 'Operator', 'fieldtype': 'Data', 'width': 150},
        {'fieldname': 'job_name_one', 'label': 'Job Name', 'fieldtype': 'Link', 'options': 'Job', 'width': 200},
        {'fieldname': 'job_number_one', 'label': 'Job No.', 'fieldtype': 'Data', 'width': 150},
        {'fieldname': 'target_quantity_one', 'label': 'Target Quantity', 'fieldtype': 'Int', 'width': 150},
        {'fieldname': 'completed_quantity_one_default_uom', 'label': 'Completed Quantity In Default Units', 'fieldtype': 'Int', 'width': 150},
        {'fieldname': 'completed_quantity_one_alternate_uom', 'label': 'Completed Quantity In Alternate Units', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'efficiency_one_percent', 'label': 'Efficiency (%)', 'fieldtype': 'Percent', 'width': 150},
        {'fieldname': 'machine_wastage_one', 'label': 'Machine Wastage', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'job_setting_wastage_one', 'label': 'Job Setting Wastage', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'roll_wastage_one', 'label': 'Roll Wastage', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'printing_wastage_one', 'label': 'Printing Wastage', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'barcode_wastage_one', 'label': 'Barcode Wastage', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'total_wastage_one', 'label': 'Total Wastage', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'job_name_two', 'label': 'Job Name', 'fieldtype': 'Link', 'options': 'Job', 'width': 200},
        {'fieldname': 'job_number_two', 'label': 'Job No.', 'fieldtype': 'Data', 'width': 150},
        {'fieldname': 'target_quantity_two', 'label': 'Target Quantity', 'fieldtype': 'Int', 'width': 150},
        {'fieldname': 'completed_quantity_two_default_uom', 'label': 'Completed Quantity In Default Units', 'fieldtype': 'Int', 'width': 150},
        {'fieldname': 'completed_quantity_two_alternate_uom', 'label': 'Completed Quantity In Alternate Units', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'efficiency_two_percent', 'label': 'Efficiency (%)', 'fieldtype': 'Percent', 'width': 150},
        {'fieldname': 'machine_wastage_two', 'label': 'Machine Wastage', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'job_setting_wastage_two', 'label': 'Job Setting Wastage', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'roll_wastage_two', 'label': 'Roll Wastage', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'printing_wastage_two', 'label': 'Printing Wastage', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'barcode_wastage_two', 'label': 'Barcode Wastage', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'total_wastage_two', 'label': 'Total Wastage', 'fieldtype': 'Float', 'width': 150},
    ]


def get_data(date):
    # Active machines
    machines = frappe.get_all("Machine", filters={"is_active": "1", "area": "Conversion Department"}, fields=["name", "sequence_number"], order_by="sequence_number asc")

    # Fetch job cards with specific fields
    job_cards = frappe.get_all(
        "Job Card",
        filters={
            "date": date,
            "shift": "Night Shift"
        },
        fields=[
            "machine", "date", "shift", "operator",
            "job_name", "job_number", "job_sequence_number",
            "target_quantity", "completed_quantity",
            "machine_wastage", "job_setting_wastage", "roll_wastage",
            "printing_wastage", "barcode_wastage", "total_wastage"
        ]
    )

    # Get conversion factors for all jobs
    job_names = list(set(job.get("job_name") for job in job_cards if job.get("job_name")))
    conversion_factors = {}
    if job_names:
        jobs = frappe.get_all("Job", filters={"name": ["in", job_names]}, fields=["name", "conversion_factor"])
        conversion_factors = {job.name: job.conversion_factor for job in jobs}

    # Add conversion factor to job cards
    for job in job_cards:
        job.conversion_factor = conversion_factors.get(job.get("job_name"), 1)

    # Group by (machine, date_str, shift) and by sequence number
    grouped = {}
    for job in job_cards:
        # normalize strings (strip) and date to ISO string
        machine_name = str(job.get("machine") or "").strip()
        shift_name = str(job.get("shift") or "").strip()
        job_date = job.get("date")
        date_str = job_date.isoformat() if hasattr(job_date, "isoformat") else str(job_date)

        key = (machine_name, date_str, shift_name)
        if key not in grouped:
            grouped[key] = {}

        # store under string sequence key for consistency
        seq = job.get("job_sequence_number")
        try:
            seq_key = str(int(seq))
        except Exception:
            seq_key = str(seq) if seq is not None else "1"

        grouped[key][seq_key] = job

    # Build rows for today's Day Shift for each machine
    data = []
    date_str = str(date)
    shift_name = 'Night Shift'

    for m in machines:
        machine_name = m['name']
        key = (machine_name, date_str, shift_name)
        jobs = grouped.get(key, {})

        # job_sequence 1 and 2 (if available)
        job1 = jobs.get("1") or jobs.get(1)
        job2 = jobs.get("2") or jobs.get(2)

        # operator: prefer job1.operator, else job2.operator, else 'Off'
        operator = "Off"
        if job1 and job1.get("operator"):
            operator = job1.get("operator")
        elif job2 and job2.get("operator"):
            operator = job2.get("operator")

        # Calculate alternate UOM quantities
        # Get conversion factors, default to 1 if not available
        conv_factor_1 = job1.get("conversion_factor") if job1 and job1.get("conversion_factor") else 1
        conv_factor_2 = job2.get("conversion_factor") if job2 and job2.get("conversion_factor") else 1

        # Calculate completed quantities in alternate UOM
        completed_qty_one_alt = 0
        if job1 and job1.get("completed_quantity") is not None:
            completed_qty_one_alt = job1.get("completed_quantity") / conv_factor_1

        completed_qty_two_alt = 0
        if job2 and job2.get("completed_quantity") is not None:
            completed_qty_two_alt = job2.get("completed_quantity") / conv_factor_2

        row = {
            "machine": machine_name,
            "operator": operator,
            "job_name_one": job1.get("job_name") if job1 else "",
            "job_number_one": job1.get("job_number") if job1 else "",
            "target_quantity_one": job1.get("target_quantity") if job1 and job1.get("target_quantity") is not None else "",
            "completed_quantity_one_default_uom": job1.get("completed_quantity") if job1 and job1.get("completed_quantity") is not None else "",
            "completed_quantity_one_alternate_uom": completed_qty_one_alt if job1 else 0,
            "efficiency_one_percent": (
                (job1.get("completed_quantity") / job1.get("target_quantity") * 100) if job1 and job1.get("target_quantity") else 0
            ) if job1 else 0,
            "machine_wastage_one": job1.get("machine_wastage") or 0 if job1 else 0,
            "job_setting_wastage_one": job1.get("job_setting_wastage") or 0 if job1 else 0,
            "roll_wastage_one": job1.get("roll_wastage") or 0 if job1 else 0,
            "printing_wastage_one": job1.get("printing_wastage") or 0 if job1 else 0,
            "barcode_wastage_one": job1.get("barcode_wastage") or 0 if job1 else 0,
            "total_wastage_one": job1.get("total_wastage") or 0 if job1 else 0,
            "job_name_two": job2.get("job_name") if job2 else "",
            "job_number_two": job2.get("job_number") if job2 else "",
            "target_quantity_two": job2.get("target_quantity") if job2 and job2.get("target_quantity") is not None else "",
            "completed_quantity_two_default_uom": job2.get("completed_quantity") if job2 and job2.get("completed_quantity") is not None else "",
            "completed_quantity_two_alternate_uom": completed_qty_two_alt if job2 else 0,
            "efficiency_two_percent": (
                (job2.get("completed_quantity") / job2.get("target_quantity") * 100) if job2 and job2.get("target_quantity") else 0
            ) if job2 else 0,
            "machine_wastage_two": job2.get("machine_wastage") or 0 if job2 else 0,
            "job_setting_wastage_two": job2.get("job_setting_wastage") or 0 if job2 else 0,
            "roll_wastage_two": job2.get("roll_wastage") or 0 if job2 else 0,
            "printing_wastage_two": job2.get("printing_wastage") or 0 if job2 else 0,
            "barcode_wastage_two": job2.get("barcode_wastage") or 0 if job2 else 0,
            "total_wastage_two": job2.get("total_wastage") or 0 if job2 else 0,
        }
        data.append(row)

    return data
