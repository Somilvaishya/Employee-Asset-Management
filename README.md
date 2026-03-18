# Employee Asset Management

A comprehensive asset management system for Frappe/ERPNext v16.

## Features

- **Asset Category Master**: Define categories with maximum limits per employee and approval requirements.
- **Company Asset Master**: Track individual assets, their current status (Available, Assigned, Maintenance, Retired), and current holder.
- **Asset Request**: Employee portal for requesting assets with urgency and approval workflow.
- **Asset Assignment**: Formalize asset issuance with automated status updates.
- **Asset Return**: Track returns with condition monitoring and automated damage notifications.
- **Reporting**: "Employee Asset Register" for an overview of all issued assets.

## Installation

1. Get the app:
   ```bash
   bench get-app employee_asset_management
   ```
2. Install the app on your site:
   ```bash
   bench --site yourcurrentsite install-app employee_asset_management
   ```

## Workflow

The **Asset Request** DocType follows a formal workflow:
`Draft` -> `Pending Approval` -> `Approved` / `Rejected` -> `Fulfilled` (automatically updated on Assignment).

## Notifications

Administrators are automatically notified via email when an asset is returned in **Damaged** condition.
