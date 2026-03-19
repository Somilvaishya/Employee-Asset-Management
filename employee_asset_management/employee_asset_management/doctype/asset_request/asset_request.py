import frappe
from frappe import _
from frappe.model.document import Document

class AssetRequest(Document):
    def validate(self):
        self.check_limits()
        self.handle_approval_requirement()

    def handle_approval_requirement(self):
        """If Asset Category doesn't require approval, auto-approve the request"""
        requires_approval = frappe.db.get_value("Asset Category", self.asset_category, "requires_approval")
        if not requires_approval and self.status == "Pending":
            self.status = "Approved"
            self.remarks = _("Auto-approved as per category policy.")

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
                frappe.throw(_("Employee already has maximum allowed {0}. Limit: {1}").format(self.asset_category, max_allowed))

    def after_insert(self):
        # Notify Reporting Manager
        self.notify_reporting_manager()

    def on_update(self):
        if self.has_value_changed("status"):
            if self.status in ["Approved", "Rejected"]:
                self.notify_employee()

    def notify_reporting_manager(self):
        """Notify Expense Approver via Email + System"""
        expense_approver = frappe.db.get_value("Employee", self.employee, "expense_approver")
        if not expense_approver:
            # Fallback to Reporting Manager if expense_approver is not set
            expense_approver = frappe.db.get_value("Employee", self.employee, "reports_to")
            
        if not expense_approver:
            return

        # If expense_approver is a User ID (email), use it directly. 
        # If it's another Employee name, get their user_id.
        if "@" in expense_approver:
            manager_email = expense_approver
        else:
            manager_email = frappe.db.get_value("Employee", expense_approver, "user_id")
            
        if not manager_email:
            return

        subject = _("New Asset Request: {0}").format(self.name)
        message = _("Employee {0} has requested a {1}. Please approve.").format(self.employee, self.asset_category)

        # Email
        frappe.sendmail(recipients=manager_email, subject=subject, message=message)
        
        # System Notification (Notification Log)
        frappe.get_doc({
            "doctype": "Notification Log",
            "subject": subject,
            "for_user": manager_email,
            "type": "Alert",
            "document_type": self.doctype,
            "document_name": self.name
        }).insert(ignore_permissions=True)

    def notify_employee(self):
        """Notify Employee via Email + System using user_id field"""
        employee_user_id = frappe.db.get_value("Employee", self.employee, "user_id")
        if not employee_user_id:
            return

        subject = _("Asset Request {0}: {1}").format(self.status, self.name)
        message = _("Your request for {0} has been {1}.").format(self.asset_category, self.status)

        if self.remarks:
            message += _("<br>Remarks: {0}").format(self.remarks)

        # Email
        frappe.sendmail(recipients=employee_user_id, subject=subject, message=message)

        # System Notification
        frappe.get_doc({
            "doctype": "Notification Log",
            "subject": subject,
            "for_user": employee_user_id,
            "type": "Alert",
            "document_type": self.doctype,
            "document_name": self.name
        }).insert(ignore_permissions=True)

@frappe.whitelist()
def approve_request(docname):
    doc = frappe.get_doc("Asset Request", docname)
    doc.status = "Approved"
    doc.approved_by = frappe.session.user
    doc.save()
    return doc
