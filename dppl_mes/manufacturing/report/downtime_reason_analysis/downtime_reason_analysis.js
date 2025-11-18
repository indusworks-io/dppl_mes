// Copyright (c) 2025, IndusWorks and contributors
// For license information, please see license.txt

frappe.query_reports["Downtime Reason Analysis"] = {
	"filters": [
		{
			"fieldname": "factory",
			"label": __("Factory"),
			"fieldtype": "MultiSelectList",
			"get_data": function(txt) {return frappe.db.get_link_options("Factory", txt);},
			"reqd": 1,
			"on_change": function() {
				let selected_sites = frappe.query_report.get_filter_value("factory");
				if (!selected_sites || selected_sites.length === 0) {
					frappe.query_report.set_filter_value("factory", []);
					frappe.query_report.set_filter_value("machines", []);
				}
			}
		},
		{
			"fieldname": "machine",
			"label": __("Machines"),
			"fieldtype": "MultiSelectList",
			"get_data": function(txt) {
				let selected_sites = frappe.query_report.get_filter_value("factory");
                if (!selected_sites || selected_sites.length === 0) {
                    return [];
                }
                return frappe.db.get_link_options("Machine", txt, {
                    factory: ["in", selected_sites]
                });
			
			},
			"reqd": 1
		},
		{
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_days(frappe.datetime.get_today(), -30),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        }
	]
};
