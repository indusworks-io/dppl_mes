// Copyright (c) 2025, IndusWorks and contributors
// For license information, please see license.txt

frappe.query_reports["Job Report"] = {
    // Existing filters are preserved
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_days(frappe.datetime.get_today(), -31),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_days(frappe.datetime.get_today(), -1),
            "reqd": 1
        }
    ],
};