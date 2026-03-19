# Video Showcase Script: Employee Asset Management

This script is designed for a 3-5 minute demonstration video of the **Employee Asset Management** app.

---

## Part 1: Introduction (30s)
**Action:** Show the **Employee Asset Management Workspace**.
**Script:** "Welcome to the Employee Asset Management system built on Frappe v16. Today, we'll walk through a complete lifecycle of an asset—from request to return—and see how the system handles validations and notifications automatically."

---

## Part 2: Scenario 1 - Asset Request (45s)
**Action:** Go to **Asset Request** -> Create New.
- Select Employee (e.g., Jane Doe).
- Select Asset Category: **Laptop**.
- Click **Save**.
**Script:** "Scenario 1: An employee needs a new laptop. As Jane Doe, I submit an Asset Request. Notice that upon saving, the system identifies the Reporting Manager and triggers a notification. The status is currently 'Pending'."

---

## Part 3: Scenario 2 - Manager Approval (45s)
**Action:** Open the same **Asset Request** as a Manager (or Admin).
- Change Status to **Approved**.
- Save.
**Script:** "Scenario 2: The Manager reviews the request. Once they approve it, the employee is immediately notified via email and system alert. The request status is now 'Approved', ready for the Admin to take action."

---

## Part 4: Scenario 3 - Asset Assignment (1m)
**Action:** Go to **Asset Assignment** -> Create New.
- Link the **Asset Request**.
- Select a **Company Asset** (e.g., LPT-001).
- Click **Submit**.
**Script:** "Scenario 3: The Admin now assigns a specific asset. By linking the request, all details are pulled automatically. Upon submission, the Company Asset record is updated: its status changes to 'Assigned' and the holder is set to the employee."

---

## Part 5: Scenarios 4 & 5 - Validations (1m)
**Action 4:** Try to create another **Asset Request** for the *same employee* for a *Laptop*.
- Click **Save**.
- **Expected:** Error "Employee already has maximum allowed Laptop. Limit: 1".
**Script:** "Scenario 4: The system enforces strict policies. If I try to request a second laptop for the same employee, the system blocks it, ensuring fair distribution of resources."

**Action 5:** Try to create an **Asset Assignment** for the *same laptop* to a *different employee*.
- Select the already assigned laptop.
- **Expected:** Error "This asset is already assigned to [Employee Name]".
**Script:** "Scenario 5: Multi-assignment protection. The system prevents assigning an asset that is already in use, maintaining data integrity."

---

## Part 6: Scenario 6 - Asset Return & Damage (1m)
**Action:** Go to **Asset Return** -> Create New.
- Select the **Asset Assignment**.
- Change **Condition at Return** to **Damaged**.
- Observe: **Penalty Amount** and **Damage Notes** appear.
- Fill details and **Submit**.
**Script:** "Scenario 6: Asset Return. When an asset is returned, we record its condition. If it's 'Damaged', the system prompts for a penalty amount and detailed notes. Once submitted, the Admin is instantly notified of the damage, and the asset status is reset to 'Available' for repair or re-issue."

---

## Part 7: Conclusion (30s)
**Action:** Show the **Asset Management Dashboard**.
**Script:** "With real-time dashboards, automated notifications, and robust policy enforcement, the Employee Asset Management app provides a complete, professional solution for your organization. Thank you!"
