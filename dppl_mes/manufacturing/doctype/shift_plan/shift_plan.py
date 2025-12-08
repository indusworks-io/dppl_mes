# Copyright (c) 2025, IndusWorks and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now, get_time_str
import datetime


class ShiftPlan(Document):
    pass

@frappe.whitelist()
def create_job_cards(docname):
    """
    Row Validation Requirement:
    If in Job Plan Details Table the no_job checkbox is unchecked and if any of the following fields are empty:
       - operator_name
       - job_one_name
       - job_one_quantity
    Then throw an error message indicating that for the row with machine {machine_name}, operator {operator_name}, job one {job_one_name}, job one quantity {job_one_quantity} is required.
    """

    doc = frappe.get_doc("Shift Plan", docname)
    for item in doc.job_plan_details:
        if not item.no_job:
            if not item.operator_name or not item.job_one_name or not item.job_one_quantity:
                frappe.throw(
                    f"For machine {item.machine_name}, Operator Name, Job 1 Name, Job 1 Target Quantity is required. If no job is to be done, please check the No Job checkbox."
                )

    """
    Shift start & end time requirements:
    From the Factory Doctype, fetch the Shift Timing for the  doc.factory and doc.shift.

    """
        # Shift start & end time requirements:
    # From the Factory Doctype, fetch the Shift Timing for the doc.factory and doc.shift.

    factory_doc = frappe.get_doc("Factory", doc.factory)
    shift_start = None
    shift_end = None

    for timing in factory_doc.shift_timings:
        if timing.shift_name == doc.shift:
            shift_start = timing.start_time
            shift_end = timing.end_time
            break

    # Combine date and time to get full datetime objects
    if isinstance(doc.date, str):
        shift_date = datetime.datetime.strptime(doc.date, "%Y-%m-%d").date()
    else:
        shift_date = doc.date

    shift_start_str = get_time_str(shift_start)
    shift_end_str = get_time_str(shift_end)

    today_shift_start_date_time = datetime.datetime.combine(
        shift_date,
        datetime.datetime.strptime(shift_start_str, "%H:%M:%S").time()
    )
    today_shift_end_date_time = datetime.datetime.combine(
        shift_date,
        datetime.datetime.strptime(shift_end_str, "%H:%M:%S").time()
    )

    if today_shift_end_date_time <= today_shift_start_date_time:
        today_shift_end_date_time += datetime.timedelta(days=1)

    print(f"Shift Start: {today_shift_start_date_time}, Shift End: {today_shift_end_date_time}")

    created_count = 0

    for row in doc.job_plan_details:
        if row.no_job:
            continue

        base_fields = {
            "date": doc.date,
            "shift": doc.shift,
            "shift_plan": docname,
            "operator": row.operator_name,
            "machine": row.machine_name,
        }

        # Define job fields mapping
        job_fields = [
            {"name_field": "job_one_name", "quantity_field": "job_one_quantity", "sequence": 1},
            {"name_field": "job_two_name", "quantity_field": "job_two_quantity", "sequence": 2},
            {"name_field": "job_three_name", "quantity_field": "job_three_target_quantity", "sequence": 3},
            {"name_field": "job_four_name", "quantity_field": "job_four_target_quantity", "sequence": 4},
            {"name_field": "job_five_name", "quantity_field": "job_five_target_quantity", "sequence": 5},
        ]

        # Track the previous job's end time
        previous_job_end_time = today_shift_start_date_time

        # Create job cards for each job
        for job_info in job_fields:
            job_name = getattr(row, job_info["name_field"], None)
            job_quantity = getattr(row, job_info["quantity_field"], None)

            # Skip if job name or quantity is not provided
            if not job_name or not job_quantity:
                continue

            # Fetch ideal_run_rate from Job DocType
            job_doc = frappe.get_doc("Job", job_name)
            # ideal_run_rate is output per minute (units per minute)
            # Calculate how many minutes needed for the job quantity
            minutes_needed = job_quantity / job_doc.ideal_run_rate
            # Convert to seconds
            planned_duration = minutes_needed * 60

            # Calculate start and end times
            planned_start_date_time = previous_job_end_time
            planned_end_date_time = planned_start_date_time + datetime.timedelta(seconds=planned_duration)

            # Create job card
            job_card = frappe.new_doc("Job Card")
            job_card.update(base_fields)
            job_card.update({
                "job_name": job_name,
                "target_quantity": job_quantity,
                "job_sequence_number": job_info["sequence"],
                "planned_start_date_time": planned_start_date_time,
                "planned_end_date_time": planned_end_date_time,
                "planned_duration": int(planned_duration)
            })
            job_card.save()
            created_count += 1

            # Update previous job end time for next iteration
            previous_job_end_time = planned_end_date_time

    doc.status = "Confirmed"
    doc.save()
    return {"status": "success", "created": created_count}