import frappe

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
    else:
        print("Workflow 'Asset Request Workflow' already exists.")
