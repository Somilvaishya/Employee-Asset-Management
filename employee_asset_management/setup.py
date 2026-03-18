import frappe
from frappe.utils import today

def run_setup():
    create_workflow()
    insert_sample_data()
    frappe.db.commit()

def create_workflow():
    # Create States
    states = ["Draft", "Pending Approval", "Approved", "Rejected", "Fulfilled"]
    for state in states:
        if not frappe.db.exists("Workflow State", state):
            frappe.get_doc({"doctype": "Workflow State", "workflow_state_name": state}).insert()

    # Create Actions
    actions = ["Submit", "Approve", "Reject"]
    for action in actions:
        if not frappe.db.exists("Workflow Action Master", action):
            frappe.get_doc({"doctype": "Workflow Action Master", "workflow_action_name": action}).insert()

    if not frappe.db.exists("Workflow", "Asset Request Workflow"):
        workflow = frappe.get_doc({
            "doctype": "Workflow",
            "workflow_name": "Asset Request Workflow",
            "document_type": "Asset Request",
            "is_active": 1,
            "states": [
                {"state": "Draft", "allow_edit": "System Manager", "doc_status": 0},
                {"state": "Pending Approval", "allow_edit": "System Manager", "doc_status": 1},
                {"state": "Approved", "allow_edit": "System Manager", "doc_status": 1},
                {"state": "Rejected", "allow_edit": "System Manager", "doc_status": 2},
                {"state": "Fulfilled", "allow_edit": "System Manager", "doc_status": 1}
            ],
            "transitions": [
                {
                    "state": "Draft",
                    "action": "Submit",
                    "next_state": "Pending Approval",
                    "allowed": "System Manager"
                },
                {
                    "state": "Pending Approval",
                    "action": "Approve",
                    "next_state": "Approved",
                    "allowed": "System Manager"
                },
                {
                    "state": "Pending Approval",
                    "action": "Reject",
                    "next_state": "Rejected",
                    "allowed": "System Manager"
                }
            ]
        })
        workflow.insert(ignore_permissions=True)
        print("Workflow 'Asset Request Workflow' created.")

def insert_sample_data():
    # 1. Asset Categories
    categories = [
        {"category_name": "Laptop", "max_per_employee": 1, "requires_approval": 1},
        {"category_name": "Mobile Phone", "max_per_employee": 1, "requires_approval": 1},
        {"category_name": "ID Card", "max_per_employee": 1, "requires_approval": 0},
        {"category_name": "Headset", "max_per_employee": 2, "requires_approval": 0}
    ]
    
    for cat in categories:
        if not frappe.db.exists("Asset Category", cat["category_name"]):
            frappe.get_doc({"doctype": "Asset Category", **cat}).insert()
            print(f"Category {cat['category_name']} created.")

    # 2. Company Assets
    assets = [
        {"asset_name": "MacBook Pro #001", "asset_category": "Laptop", "serial_number": "SN-MBP-001", "current_status": "Available"},
        {"asset_name": "MacBook Pro #002", "asset_category": "Laptop", "serial_number": "SN-MBP-002", "current_status": "Available"},
        {"asset_name": "iPhone 15 #001", "asset_category": "Mobile Phone", "serial_number": "SN-IP15-001", "current_status": "Available"},
        {"asset_name": "Logitech H390 #001", "asset_category": "Headset", "serial_number": "SN-H390-001", "current_status": "Available"}
    ]
    
    for asset in assets:
        if not frappe.db.exists("Company Asset", asset["asset_name"]):
            frappe.get_doc({"doctype": "Company Asset", **asset}).insert()
            print(f"Asset {asset['asset_name']} created.")
