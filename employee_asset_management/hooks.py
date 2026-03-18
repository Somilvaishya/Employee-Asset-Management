app_name = "employee_asset_management"
app_title = "Employee Asset Management"
app_publisher = "Antigravity"
app_description = "Asset Management System"
app_email = "admin@example.com"
app_license = "mit"

# DocEvents
# Assignment and Return logic is already in their respective controllers.
# Request logic is in its controller.

# Fixtures for sample data
fixtures = [
    {"dt": "Asset Category", "filters": [["name", "in", ["Laptop", "Mobile Phone", "ID Card"]]]},
    {"dt": "Company Asset", "filters": [["name", "in", ["Dell Laptop #001", "Dell Laptop #002", "iPhone 14 #001"]]]}
]
