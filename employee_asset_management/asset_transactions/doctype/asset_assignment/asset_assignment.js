frappe.ui.form.on("Asset Assignment", {
    setup: function (frm) {
        // Filter Company Asset to show only 'Available' ones
        frm.set_query("company_asset", function () {
            return {
                filters: {
                    "current_status": "Available"
                }
            };
        });
    },
    asset_request: function (frm) {
        if (frm.doc.asset_request) {
            frappe.db.get_value("Asset Request", frm.doc.asset_request, "asset_category", (r) => {
                if (r && r.asset_category) {
                    frm.set_query("company_asset", function () {
                        return {
                            filters: {
                                "current_status": "Available",
                                "asset_category": r.asset_category
                            }
                        };
                    });
                }
            });

            // Also fetch employee if not set
            frappe.db.get_value("Asset Request", frm.doc.asset_request, "employee", (r) => {
                if (r && r.employee && !frm.doc.employee) {
                    frm.set_value("employee", r.employee);
                }
            });
        }
    }
});
