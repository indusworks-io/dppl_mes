# Copyright (c) 2025, IndusWorks and contributors
# For license information, please see license.txt

import frappe
import datetime

def execute(filters=None):
    try:
        if not filters:
            filters = {}
        
        from_date = filters.get("from_date")
        to_date = filters.get("to_date")
        
        if not from_date or not to_date:
            frappe.throw("From Date and To Date are required")
        
        columns = get_columns()
        data = get_data(from_date, to_date)
        return columns, data
    
    except Exception as e:
        frappe.log_error(f"Error in Job Report: {str(e)}", "Job Report")
        frappe.throw("An error occurred while generating the report. Please check the error log.")


def get_columns():

    # Simplified columns as requested:
    return [
        {'fieldname': 'machine', 'label': 'Machine', 'fieldtype': 'Link', 'options': 'Machine', 'width': 150},
        {'fieldname': 'date', 'label': 'Date', 'fieldtype': 'Date', 'width': 120},
        {'fieldname': 'shift', 'label': 'Shift', 'fieldtype': 'Data', 'width': 120},
        {'fieldname': 'operator', 'label': 'Operator', 'fieldtype': 'Data', 'width': 150},
        {'fieldname': 'job_name', 'label': 'Job Name', 'fieldtype': 'Link', 'options': 'Job', 'width': 200},
        {'fieldname': 'job_number', 'label': 'Job No.', 'fieldtype': 'Data', 'width': 150},
        {'fieldname': 'job_sequence', 'label': 'Job Sequence', 'fieldtype': 'Int', 'width': 50},
        {'fieldname': 'target_quantity', 'label': 'Target Quantity', 'fieldtype': 'Int', 'width': 150},
        {'fieldname': 'completed_quantity_one_default_uom', 'label': 'Completed Quantity', 'fieldtype': 'Int', 'width': 150},
        {'fieldname': 'completed_quantity_one_alternate_uom', 'label': 'Completed Quantity In Alternate Units', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'efficiency_percent', 'label': 'Efficiency (%)', 'fieldtype': 'Percent', 'width': 150},
        {'fieldname': 'machine_wastage', 'label': 'Machine Wastage', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'job_setting_wastage', 'label': 'Job Setting Wastage', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'roll_wastage', 'label': 'Roll Wastage', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'printing_wastage', 'label': 'Printing Wastage', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'barcode_wastage', 'label': 'Barcode Wastage', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'total_wastage', 'label': 'Total Wastage', 'fieldtype': 'Float', 'width': 150},
    ]


def get_data(from_date, to_date):
    # Active machines
    machines = frappe.get_all("Machine", filters={"is_active": "1"}, fields=["name", "sequence_number"], order_by="sequence_number asc")
    # Shifts (we'll prefer Day Shift / Night Shift ordering if present)
    shifts = frappe.get_all("Shift Type", fields=["name"])

    # Put Day Shift first, Night Shift second, others after (alphabetical)
    preferred_order = {'Day Shift': 0, 'Night Shift': 1}
    shifts_sorted = sorted(shifts, key=lambda s: (preferred_order.get(s['name'], 99), s['name']))

    # date list (inclusive)
    start = datetime.datetime.strptime(from_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(to_date, "%Y-%m-%d")
    date_list = [(start + datetime.timedelta(days=x)).strftime("%Y-%m-%d")
                 for x in range((end - start).days + 1)]

    # fetch job cards once with conversion_factor from Job DocType
    job_cards_query = """
        SELECT
            jc.machine, jc.date, jc.shift, jc.operator,
            jc.job_name, jc.job_number, jc.job_sequence_number,
            jc.target_quantity, jc.completed_quantity,
            jc.machine_wastage, jc.job_setting_wastage, jc.roll_wastage,
            jc.printing_wastage, jc.barcode_wastage, jc.total_wastage,
            j.conversion_factor
        FROM `tabJob Card` jc
        LEFT JOIN `tabJob` j ON jc.job_name = j.name
        WHERE jc.date >= %s AND jc.date <= %s
    """
    job_cards = frappe.db.sql(job_cards_query, (from_date, to_date), as_dict=True)
    print(f"Found {len(job_cards)} job cards from {from_date} to {to_date}")

    # Create a lookup dictionary for job cards by (machine, date, shift)
    job_cards_by_group = {}
    for job in job_cards:
        machine_name = str(job.get("machine") or "").strip()
        shift_name = str(job.get("shift") or "").strip()
        job_date = job.get("date")
        date_str = job_date.isoformat() if hasattr(job_date, "isoformat") else str(job_date)

        key = (machine_name, date_str, shift_name)
        if key not in job_cards_by_group:
            job_cards_by_group[key] = []
        job_cards_by_group[key].append(job)

    # Sort job cards within each group by job_sequence_number
    for key in job_cards_by_group:
        job_cards_by_group[key].sort(key=lambda x: x.get("job_sequence_number", 0))

    # Build rows in order: date -> shift -> machine
    data = []
    for date in date_list:
        for shift in shifts_sorted:
            shift_name = shift['name']
            for m in machines:
                machine_name = m['name']
                key = (machine_name, date, shift_name)
                jobs = job_cards_by_group.get(key, [])

                if jobs:
                    # Create rows for each job in sequence
                    for job in jobs:
                        # Get conversion factor for this job
                        conversion_factor = job.get("conversion_factor") or 1

                        # Calculate alternate UOM quantity
                        completed_qty_alternate_uom = 0
                        if job.get("completed_quantity") is not None and conversion_factor and conversion_factor > 0:
                            completed_qty_alternate_uom = job.get("completed_quantity") / conversion_factor

                        # Calculate efficiency
                        efficiency_percent = 0
                        if job.get("target_quantity"):
                            efficiency_percent = (job.get("completed_quantity", 0) / job.get("target_quantity")) * 100

                        row = {
                            "machine": machine_name,
                            "date": date,
                            "shift": shift_name,
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
                    # Create "Off" row for machine with no jobs on this date/shift
                    row = {
                        "machine": machine_name,
                        "date": date,
                        "shift": shift_name,
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
