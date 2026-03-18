import frappe
from frappe.model.document import Document

class AssetRequest(Document):
    def validate(self):
        self.check_limits()

    def check_limits(self):
        """Check if employee already has maximum allowed assets for the category"""
        max_allowed = frappe.db.get_value("Asset Category", self.asset_category, "max_per_employee")
        if max_allowed:
            # Count active assignments
            count = frappe.db.count("Asset Assignment", filters={
                "employee": self.employee,
                "docstatus": 1,
                "company_asset": ["in", frappe.get_all("Company Asset", 
                    filters={"asset_category": self.asset_category, "current_status": "Assigned"}, 
                    pluck="name")]
            })
            if count >= max_allowed:
                frappe.throw(f"Employee already has maximum allowed {self.asset_category}. Limit: {max_allowed}")

    def on_submit(self):
        # Implementation of approval logic or notifications if needed
        pass

@frappe.whitelist()
def approve_request(docname):
    doc = frappe.get_doc("Asset Request", docname)
    doc.status = "Approved"
    doc.approved_by = frappe.session.user
    doc.save()
    return doc
