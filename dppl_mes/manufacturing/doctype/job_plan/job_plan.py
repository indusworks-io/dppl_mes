# Copyright (c) 2025, IndusWorks and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class JobPlan(Document):
	pass


@frappe.whitelist()
def create_job_cards(docname):
    doc = frappe.get_doc("Job Plan", docname)

    if doc.docstatus != 0:
        frappe.throw(_("Only Draft Job Plans can be processed."))

    created_count = 0

    for row in doc.job_plan_details:
        if row.no_job:
            continue  # Skip this row if No Job is checked

        # Common fields
        base_fields = {
            "machine": row.machine_name,
            "date": doc.date,
            "shift": doc.shift,
            "operator": row.operator_name,
        }

        # Job 1
        if row.job_one_name and row.job_one_number and row.job_one_quantity:
            job_card_1 = frappe.new_doc("Job Card")
            job_card_1.update(base_fields)
            job_card_1.update({
                "job_name": row.job_one_name,
                "job_number": row.job_one_number,
                "target_quantity": row.job_one_quantity,
                "job_sequence_number": 1,
            })
            job_card_1.save()
            created_count += 1

        # Job 2
        if row.job_two_name and row.job_two_number and row.job_two_quantity:
            job_card_2 = frappe.new_doc("Job Card")
            job_card_2.update(base_fields)
            job_card_2.update({
                "job_name": row.job_two_name,
                "job_number": row.job_two_number,
                "target_quantity": row.job_two_quantity,
                "job_sequence_number": 2,
            })
            job_card_2.save()
            created_count += 1

    # Optionally update Job Plan status
    doc.status = "Confirmed"
    doc.save()
    return {"status": "success", "created": created_count}