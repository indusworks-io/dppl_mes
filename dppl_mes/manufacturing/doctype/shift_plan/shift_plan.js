// Copyright (c) 2025, IndusWorks and contributors
// For license information, please see license.txt

/*
To Do:
When a new form loads
1. Check Organization Settings DocType and Look for default_factory field.
2. If there is value in default_factory field then use the value and insert in factory field.
3. Put today's date in date field in the form
4. Using the factory fetch list of all machines where is_active is true and insert them in job_plan_details.
5. if the user changes factory field option then empty the table.

When the form is not new:
1. If the frm.doc.status === 'Draft' show Button called 'Confirm'
*/

frappe.ui.form.on("Shift Plan", {
    refresh(frm) {
        if (frm.is_new()) {
            console.log("New form loaded");

            // Set today's date
            frm.set_value("date", frappe.datetime.get_today());

            // Fetch and set default factory
            frappe.db.get_single_value("Organization Settings", "default_factory")
                .then(value => {
                    if (value) {
                        frm.set_value("factory", value);
                    }
                });
        } else {
            // If document is in Draft status, show Confirm button
            if (frm.doc.status === "Draft") {
                frm.add_custom_button(__('Confirm Shift Plan'), () => {
                    frappe.confirm(
                        "On submission, Job Cards will be created.",
                        () => {
                            frappe.call({
                                method: "dppl_mes.manufacturing.doctype.shift_plan.shift_plan.create_job_cards",
                                args: {
                                    docname: frm.doc.name
                                },
                                freeze: true,
                                callback: function (r) {
                                    if (!r.exc) {
                                        frappe.msgprint("Job Cards Created Successfully.");
                                        frm.reload_doc();
                                    }
                                }
                            });
                        },
                        () => {
                            // Cancelled
                        }
                    );
                });
                frm.add_custom_button(__('Cancel Shift Plan'), () => {
                    frm.set_value("status", "Cancelled");
                    frm.save();
                })
            }
        }
    },

    factory(frm) {
    if (frm.doc.factory) {
        // Clear existing table entries
        frm.clear_table("job_plan_details");

        // Fetch active machines linked to selected factory
        frappe.db.get_list("Machine", {
            filters: {
                factory: frm.doc.factory,
                is_active: 1
            },
            fields: ["machine_name", "sequence_number"],
            limit: 1000
        }).then(machines => {
            if (machines.length) {
                // Sort machines by ascending sequence_number
                machines.sort((a, b) => (a.sequence_number || 0) - (b.sequence_number || 0));

                machines.forEach(machine => {
                    frm.add_child("job_plan_details", {
                        machine_name: machine.machine_name
                    });
                });

                frm.refresh_field("job_plan_details");
            } else {
                frappe.msgprint("No active machines found for the selected factory.");
            }
        });
    } else {
        // If factory field is cleared manually, also clear table
        frm.clear_table("job_plan_details");
        frm.refresh_field("job_plan_details");
        }
    
    }

});
