import frappe
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
        """Send email notification to System Manager when an asset is returned as Damaged"""
        admin_emails = frappe.get_all("User", 
            filters={"name": ["in", frappe.get_roles("System Manager")]}, 
            pluck="email")
            
        if not admin_emails:
            return

        subject = _("Asset Damaged: {0}").format(self.company_asset)
        message = _("""
            <p>An asset has been returned in <b>Damaged</b> condition.</p>
            <ul>
                <li><b>Asset:</b> {0}</li>
                <li><b>Employee:</b> {1}</li>
                <li><b>Return Date:</b> {2}</li>
                <li><b>Notes:</b> {3}</li>
            </ul>
        """).format(self.company_asset, self.employee, self.return_date, self.damage_notes or "No notes provided")

        frappe.sendmail(
            recipients=admin_emails,
            subject=subject,
            message=message
        )
