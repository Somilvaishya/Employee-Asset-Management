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
            "fieldtype": "Link",
            "options": "Department",
            "width": 120
        },
        {
            "label": _("Asset Category"),
            "fieldname": "asset_category",
            "fieldtype": "Link",
            "options": "Asset Category",
            "width": 120
        },
        {
            "label": _("Asset Name"),
            "fieldname": "asset_name",
            "fieldtype": "Link",
            "options": "Company Asset",
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
            "label": _("Condition"),
            "fieldname": "condition",
            "fieldtype": "Data",
            "width": 100
        }
    ]

def get_data(filters):
    conditions = []
    if filters.get("employee"):
        conditions.append(f"aa.employee = '{filters.get('employee')}'")
    if filters.get("department"):
        conditions.append(f"e.department = '{filters.get('department')}'")
    if filters.get("asset_category"):
        conditions.append(f"ca.asset_category = '{filters.get('asset_category')}'")
    
    status_filter = filters.get("status")
    if status_filter == "Assigned":
        conditions.append("ca.current_status = 'Assigned'")
    elif status_filter == "Returned":
        conditions.append("ca.current_status = 'Available'")

    where_clause = " AND ".join(conditions)
    if where_clause:
        where_clause = " AND " + where_clause

    # Base query joining Assignment, Employee, and Asset
    data = frappe.db.sql(f"""
        SELECT 
            e.employee_name,
            e.department,
            ca.asset_category,
            ca.asset_name,
            ca.serial_number,
            aa.assigned_date,
            aa.condition_at_issue as `condition`
        FROM 
            `tabAsset Assignment` aa
        JOIN 
            `tabEmployee` e ON aa.employee = e.name
        JOIN 
            `tabCompany Asset` ca ON aa.company_asset = ca.name
        WHERE 
            aa.docstatus = 1 {where_clause}
        ORDER BY 
            aa.assigned_date DESC
    """, as_dict=1)
    
    return data
