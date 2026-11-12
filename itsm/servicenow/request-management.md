# ServiceNow Service Request Management & Catalog Fulfillment
**Document ID:** ITSM-SN-004  
**Audience:** L1 Service Desk Analysts  
**Data Hierarchy:** Request (`sc_request`) > Requested Item (`sc_req_item` / RITM) > Catalog Task (`sc_task`)

---

## 1. Incidents vs. Service Requests

| Dimension | Incident Management | Service Request Management |
|---|---|---|
| **Definition** | Unplanned interruption or reduction in quality of an IT service. | Formal request from a user for something to be provided (hardware, software, access). |
| **Philosophy** | **"Something is broken"** — goal is rapid restoration of normal service. | **"I need something new"** — standard, planned fulfillment following defined approval workflows. |
| **Examples** | Laptop blue screens; VPN won't connect; printer is offline. | New hire setup; dual monitor request; SAP access grant; software license request. |
| **ITIL Process** | Incident Management | Service Request Management (Request Fulfillment) |

---

## 2. ServiceNow Request Data Structure (REQ > RITM > TASK)

When a user submits an order via the Service Catalog:
1. **REQ (Request):** The shopping cart parent record (e.g., `REQ0010045`). Contains billing and delivery details.
2. **RITM (Requested Item):** The specific catalog item ordered (e.g., `RITM0010082 - Standard Developer Laptop`). Holds approvals (e.g., Manager Approval: Approved).
3. **SCTASK (Catalog Task):** The actual technical work assignments routed to fulfiller teams (e.g., `SCTASK0010190 - Image laptop with Nexora Windows 11 Enterprise`).

---

## 3. Nexora Service Catalog Items Supported by L1

| Catalog Item | Required Approvals | L1 Fulfillment Tasks |
|---|---|---|
| **New Employee IT Onboarding** | HR Manager + Department Head | 1. Create Active Directory account & mailbox.<br>2. Image and assign laptop from inventory.<br>3. Hand over hardware & initial credentials. |
| **Standard Software Installation** | Immediate (Pre-approved) | 1. Verify system compatibility.<br>2. Deploy via SCCM/Intune or install manually via shared installer repository. |
| **Shared Drive Access Permission** | Data Owner / Department Head | 1. Add user account to designated AD security group.<br>2. Instruct user to sign out and back in to refresh Kerberos token. |
| **Hardware Replacement / Peripherals** | Reporting Manager | 1. Check stock in asset inventory.<br>2. Issue equipment, register serial number, update CMDB status to *In Use*. |
