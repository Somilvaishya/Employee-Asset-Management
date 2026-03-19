frappe.ui.form.on("Asset Return", {
    setup: function (frm) {
        // Filter Asset Assignment to show only submitted ones
        frm.set_query("asset_assignment", function () {
            return {
                filters: {
                    "docstatus": 1
                }
            };
        });
    },
    refresh: function (frm) {
        frm.trigger("condition_at_return");
    },
    asset_assignment: function (frm) {
        if (frm.doc.asset_assignment) {
            frappe.db.get_value("Asset Assignment", frm.doc.asset_assignment, ["employee", "company_asset"], (r) => {
                if (r) {
                    frm.set_value("employee", r.employee);
                    frm.set_value("company_asset", r.company_asset);
                }
            });
        }
    },
    condition_at_return: function (frm) {
        // Penalty field and damage notes are mandatory/visible only if damaged
        let is_damaged = frm.doc.condition_at_return === "Damaged";
        frm.set_df_property("penalty_amount", "hidden", !is_damaged);
        frm.set_df_property("damage_notes", "reqd", is_damaged);
    }
});
