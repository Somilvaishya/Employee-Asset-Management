import frappe
import json

def check():
    try:
        # Use existing context if available, or just get all
        res = frappe.get_all("Workspace", filters={"label": "Employee Asset Management"}, fields=["name", "is_standard", "public"])
        print("Workspaces found:")
        print(json.dumps(res, indent=4))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check()
