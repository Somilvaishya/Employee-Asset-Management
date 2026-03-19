import frappe
from frappe import _
from frappe.model.document import Document

class AssetReturn(Document):
    def on_submit(self):
        # B. On Asset Return Submit: Update Company Asset
        frappe.db.set_value("Company Asset", self.company_asset, {
            "current_status": "Available",
            "current_holder": None
        })
        
        # Notify Admin if damaged
        if self.condition_at_return == "Damaged":
            self.notify_admin_of_damage()

    def notify_admin_of_damage(self):
        """Send email and system notification to System Manager when an asset is returned as Damaged"""
        admin_users = frappe.get_all("Has Role", 
            filters={"role": "System Manager", "parenttype": "User"}, 
            pluck="parent")
            
        if not admin_users:
            return

        subject = _("Asset Returned Damaged: {0}").format(self.company_asset)
        message = _("""
            <p>An asset has been returned in <b>Damaged</b> condition.</p>
            <ul>
                <li><b>Asset:</b> {0}</li>
                <li><b>Employee:</b> {1}</li>
                <li><b>Return Date:</b> {2}</li>
                <li><b>Notes:</b> {3}</li>
                <li><b>Penalty Amount:</b> {4}</li>
            </ul>
        """).format(self.company_asset, self.employee, self.return_date, self.damage_notes or "No notes provided", self.penalty_amount or 0)

        # Email
        frappe.sendmail(
            recipients=admin_users,
            subject=subject,
            message=message
        )

        # System Notification
        for user in admin_users:
            frappe.get_doc({
                "doctype": "Notification Log",
                "subject": subject,
                "for_user": user,
                "type": "Alert",
                "document_type": self.doctype,
                "document_name": self.name
            }).insert(ignore_permissions=True)
