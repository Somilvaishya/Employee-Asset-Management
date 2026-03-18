import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "label": _("Employee Name"),
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Department"),
            "fieldname": "department",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Asset Category"),
            "fieldname": "asset_category",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Asset Name"),
            "fieldname": "asset_name",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Serial No"),
            "fieldname": "serial_number",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Assigned Date"),
            "fieldname": "assigned_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": _("Expected Return"),
            "fieldname": "expected_return_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": _("Condition"),
            "fieldname": "condition",
            "fieldtype": "Data",
            "width": 100
        }
    ]

def get_data(filters):
    conditions = ""
    if filters.get("employee"):
        conditions += f" AND aa.employee = '{filters.get('employee')}'"
    if filters.get("asset_category"):
        conditions += f" AND ca.asset_category = '{filters.get('asset_category')}'"
    
    # Base query joining Assignment, Employee, and Asset
    data = frappe.db.sql(f"""
        SELECT 
            e.employee_name,
            e.department,
            ca.asset_category,
            ca.asset_name,
            ca.serial_number,
            aa.assigned_date,
            aa.expected_return_date,
            aa.condition_at_issue as condition
        FROM 
            `tabAsset Assignment` aa
        JOIN 
            `tabEmployee` e ON aa.employee = e.name
        JOIN 
            `tabCompany Asset` ca ON aa.company_asset = ca.name
        WHERE 
            aa.docstatus = 1 {conditions}
    """, as_dict=1)
    
    return data
