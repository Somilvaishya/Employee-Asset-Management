import frappe
from frappe import _
from frappe.model.document import Document

class AssetAssignment(Document):
    def validate(self):
        self.validate_availability()
        self.check_category_limit()
        self.check_overlap()

    def validate_availability(self):
        status = frappe.db.get_value("Company Asset", self.company_asset, "current_status")
        if status != "Available":
            current_holder = frappe.db.get_value("Company Asset", self.company_asset, "current_holder")
            if current_holder:
                frappe.throw(_("This asset is already assigned to {0}").format(current_holder))
            else:
                frappe.throw(_("Asset status is '{0}'. Only 'Available' assets can be assigned.").format(status))

    def check_category_limit(self):
        category = frappe.db.get_value("Company Asset", self.company_asset, "asset_category")
        max_allowed = frappe.db.get_value("Asset Category", category, "max_per_employee")
        if max_allowed:
            count = frappe.db.count("Asset Assignment", filters={
                "employee": self.employee,
                "docstatus": 1,
                "company_asset": ["in", frappe.get_all("Company Asset", 
                    filters={"asset_category": category, "current_status": "Assigned"}, 
                    pluck="name")]
            })
            if count >= max_allowed:
                frappe.throw(_("Employee already has maximum allowed {0}. Limit: {1}").format(category, max_allowed))

    def check_overlap(self):
        """Ensure no overlapping assignments for the same asset"""
        overlap = frappe.db.exists("Asset Assignment", {
            "company_asset": self.company_asset,
            "name": ["!=", self.name],
            "docstatus": 1,
            "assigned_date": ["<=", self.expected_return_date or "9999-12-31"],
            "expected_return_date": [">=", self.assigned_date]
        })
        if overlap:
            frappe.throw(_("Asset {0} is already assigned during this period.").format(self.company_asset))

    def on_submit(self):
        # A. On Asset Assignment Submit: Update Company Asset
        frappe.db.set_value("Company Asset", self.company_asset, {
            "current_status": "Assigned",
            "current_holder": self.employee
        })
        
        # If there's an asset request, mark it as fulfilled
        if self.asset_request:
            frappe.db.set_value("Asset Request", self.asset_request, "status", "Fulfilled")

        # Notify Employee
        self.notify_employee()

    def notify_employee(self):
        """Notify Employee via Email using user_id field"""
        employee_user_id = frappe.db.get_value("Employee", self.employee, "user_id")
        if not employee_user_id:
            return

        subject = _("Asset Assigned: {0}").format(self.company_asset)
        message = _("A {0} ({1}) has been assigned to you.").format(
            frappe.db.get_value("Company Asset", self.company_asset, "asset_category"),
            self.company_asset
        )

        frappe.sendmail(recipients=employee_user_id, subject=subject, message=message)
