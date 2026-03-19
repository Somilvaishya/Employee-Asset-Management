import frappe
import json

def check():
    try:
        meta = frappe.get_meta("Employee")
        results = {
            "expense_approver": bool(meta.get_field("expense_approver")),
            "user_id": bool(meta.get_field("user_id")),
            "reports_to": bool(meta.get_field("reports_to"))
        }
        print(json.dumps(results, indent=4))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check()
