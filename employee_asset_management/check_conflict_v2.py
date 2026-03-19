import frappe
import json

def check():
    doctypes = ["Asset Assignment", "Asset Return"]
    results = {}
    for dt in doctypes:
        try:
            module = frappe.db.get_value("DocType", dt, "module")
            results[dt] = module
        except Exception as e:
            results[dt] = f"Error: {e}"
    print(json.dumps(results, indent=4))

if __name__ == "__main__":
    check()
