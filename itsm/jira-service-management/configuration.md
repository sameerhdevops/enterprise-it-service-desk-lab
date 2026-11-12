# Jira Service Management Configuration Runbook
**Document ID:** ITSM-JSM-002  
**Platform:** Jira Service Management (Cloud Free Tier)

---

## 1. Request Types & Field Mapping
In **Project Settings > Request Types**, map customer-facing portal items to underlying Jira Issue Types:

| Portal Request Name | Issue Type | Description | Key Fields Collected |
|---|---|---|---|
| **Report a system problem** | Incident | Something is broken or malfunctioning | Summary, Description, Urgency, Affected System, Attachment |
| **Request a new account or access** | Service Request | Permission or new employee account | Target System, Justification, Manager Approval |
| **Request new software or hardware** | Service Request | Software license or hardware peripheral | Item Requested, Business Reason, Laptop Asset Tag |
| **Report broken computer hardware** | Incident | Physical damage or hardware failure | Device Type, Serial Number, Symptom Details |

---

## 2. Priority & SLA Configuration
Jira uses standard priority tiers: *Highest, High, Medium, Low, Lowest*. In JSM, map these to ITIL P1–P4:

- **Highest (P1):** Time to first response: 15m | Time to resolution: 4h
- **High (P2):** Time to first response: 1h | Time to resolution: 8h
- **Medium (P3):** Time to first response: 4h | Time to resolution: 24h (3 business days)
- **Low (P4):** Time to first response: 8h | Time to resolution: 40h (5 business days)

**SLA Goals Definition (Project Settings > SLAs):**
- **Time to resolution:**
  - Start condition: Issue Created
  - Pause condition: Status = *Waiting for customer* OR *Waiting for support*
  - Stop condition: Status = *Resolved* OR *Closed*
