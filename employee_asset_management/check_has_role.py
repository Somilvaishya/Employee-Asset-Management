import frappe
import json

def check():
    try:
        roles = frappe.get_all("Has Role", 
            filters={"role": "System Manager"}, 
            fields=["parent", "parenttype"])
        print(json.dumps(roles, indent=4))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check()
