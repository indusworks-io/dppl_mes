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
    # Final order as requested:
    return [
        {'fieldname': 'machine', 'label': 'Machine', 'fieldtype': 'Link', 'options': 'Machine', 'width': 150},
        {'fieldname': 'date', 'label': 'Date', 'fieldtype': 'Date', 'width': 120},
        {'fieldname': 'shift', 'label': 'Shift', 'fieldtype': 'Data', 'width': 120},
        {'fieldname': 'operator', 'label': 'Operator', 'fieldtype': 'Data', 'width': 150},
        {'fieldname': 'job_name_one', 'label': 'Job Name', 'fieldtype': 'Link', 'options': 'Job', 'width': 200},
        {'fieldname': 'job_number_one', 'label': 'Job No.', 'fieldtype': 'Data', 'width': 150},
        {'fieldname': 'target_quantity_one', 'label': 'Target Quantity', 'fieldtype': 'Int', 'width': 150},
        {'fieldname': 'completed_quantity_one', 'label': 'Completed Quantity', 'fieldtype': 'Int', 'width': 150},
        {'fieldname': 'efficiency_one_percent', 'label': 'Efficiency (%)', 'fieldtype': 'Percent', 'width': 150},
        {'fieldname': 'job_name_two', 'label': 'Job Name', 'fieldtype': 'Link', 'options': 'Job', 'width': 200},
        {'fieldname': 'job_number_two', 'label': 'Job No.', 'fieldtype': 'Data', 'width': 150},
        {'fieldname': 'target_quantity_two', 'label': 'Target Quantity', 'fieldtype': 'Int', 'width': 150},
        {'fieldname': 'completed_quantity_two', 'label': 'Completed Quantity', 'fieldtype': 'Int', 'width': 150},
        {'fieldname': 'efficiency_two_percent', 'label': 'Efficiency (%)', 'fieldtype': 'Percent', 'width': 150},
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

    # fetch job cards once
    job_cards = frappe.get_all(
        "Job Card",
        filters=[
            ["date", ">=", from_date],
            ["date", "<=", to_date]
        ],
        fields=[
            "machine", "date", "shift", "operator",
            "job_name", "job_number", "job_sequence_number",
            "target_quantity", "completed_quantity"
        ]
    )

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

    # Build rows in order: date -> shift -> machine
    data = []
    for date in date_list:
        for shift in shifts_sorted:
            shift_name = shift['name']
            for m in machines:
                machine_name = m['name']
                key = (machine_name, date, shift_name)
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

                row = {
                    "machine": machine_name,
                    "date": date,
                    "shift": shift_name,
                    "operator": operator,
                    "job_name_one": job1.get("job_name") if job1 else "",
                    "job_number_one": job1.get("job_number") if job1 else "",
                    "target_quantity_one": job1.get("target_quantity") if job1 and job1.get("target_quantity") is not None else "",
                    "completed_quantity_one": job1.get("completed_quantity") if job1 and job1.get("completed_quantity") is not None else "",
                    "efficiency_one_percent": (
                        (job1.get("completed_quantity") / job1.get("target_quantity") * 100) if job1 and job1.get("target_quantity") else 0
                    ) if job1 else 0,
                    "job_name_two": job2.get("job_name") if job2 else "",
                    "job_number_two": job2.get("job_number") if job2 else "",
                    "target_quantity_two": job2.get("target_quantity") if job2 and job2.get("target_quantity") is not None else "",
                    "completed_quantity_two": job2.get("completed_quantity") if job2 and job2.get("completed_quantity") is not None else "",
                    "efficiency_two_percent": (
                        (job2.get("completed_quantity") / job2.get("target_quantity") * 100) if job2 and job2.get("target_quantity") else 0
                    ) if job2 else 0,
                }
                data.append(row)

    return data
