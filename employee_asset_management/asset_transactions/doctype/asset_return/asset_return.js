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
    asset_assignment: function (frm) {
        if (frm.doc.asset_assignment) {
            frappe.db.get_value("Asset Assignment", frm.doc.asset_assignment, ["employee", "company_asset"], (r) => {
                if (r) {
                    frm.set_value("employee", r.employee);
                    frm.set_value("company_asset", r.company_asset);
                }
            });
        }
    }
});
