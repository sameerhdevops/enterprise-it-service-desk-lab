# ServiceNow Configuration Runbook: Nexora Technologies
**Document ID:** ITSM-SN-002  
**Platform:** ServiceNow PDI  
**Scope:** Assignment Groups, Categories, Priority Matrix, SLA Definitions

---

## 1. Assignment Groups & Roles Configuration

In ServiceNow, navigate to **User Administration > Groups** (`sys_user_group.list`) and configure the organizational support hierarchy for Nexora Technologies:

| Group Name | Group Email | Roles | Description & Scope |
|---|---|---|---|
| **L1 Service Desk** | `servicedesk@nexora.test` | `itil` | First-line intake, triage, initial diagnosis, password resets, basic software support. |
| **L2 Desktop Support** | `desktop-support@nexora.test` | `itil` | Onsite hardware repair, OS reimaging, advanced client crashes, physical peripherals. |
| **L2 Network Support** | `network-support@nexora.test` | `itil`, `network` | Switch ports, Wi-Fi APs, VPN gateway policies, firewall rules, DHCP/DNS infrastructure. |
| **L2 Application Support** | `app-support@nexora.test` | `itil` | Enterprise applications (SAP GUI, accounting software, custom internal tools). |
| **L3 Infrastructure** | `infra-team@nexora.test` | `itil`, `admin` | Domain controllers, hypervisors, SAN/NAS storage, cloud infrastructure. |

---

## 2. Incident Categorization & Subcategories

Navigate to **System Definition > Choice Lists** (`sys_choice.list`) filtering on Table: `incident`:

```
Category: Hardware
  ├── Subcategories: Laptop, Desktop, Monitor, Keyboard/Mouse, Docking Station, Peripherals
Category: Software
  ├── Subcategories: Operating System, Office 365, Outlook, Teams, ERP/SAP, Browser, Specialized App
Category: Network
  ├── Subcategories: Wi-Fi, Wired LAN, VPN, Internet Access, DNS/DHCP, Shared Drive
Category: Access/Security
  ├── Subcategories: Password Reset, Account Lockout, MFA Token, Folder Permissions, New Account
Category: Printing
  ├── Subcategories: Network Printer, Print Spooler, Physical Paper Jam, Toner/Supplies
```

---

## 3. Impact, Urgency, and Priority Data Lookup Rules

ServiceNow automatically computes the **Priority** (`priority`) field via the `dl_u_priority` lookup table based on **Impact** and **Urgency**:

| Impact (`impact`) | Urgency (`urgency`) | Resulting Priority (`priority`) | Nexora SLA Resolution Target |
|---|---|---|---|
| **1 - High** (Entire department / critical service down) | **1 - High** (Work halted completely) | **1 - Critical** | **4 hours** (Response: 15 min) |
| **1 - High** | **2 - Medium** (Work degraded with workaround) | **2 - High** | **8 business hours** (Response: 1 hr) |
| **2 - Medium** (Multiple users / single core system degraded) | **1 - High** | **2 - High** | **8 business hours** (Response: 1 hr) |
| **2 - Medium** | **2 - Medium** | **3 - Moderate** | **3 business days** (Response: 4 hrs) |
| **3 - Low** (Single user / minor cosmetic issue) | **1 - High** | **3 - Moderate** | **3 business days** (Response: 4 hrs) |
| **2 - Medium** | **3 - Low** | **4 - Low** | **5 business days** (Response: 1 day) |
| **3 - Low** | **2 - Medium** / **3 - Low** | **4 - Low** | **5 business days** (Response: 1 day) |

---

## 4. SLA Definitions (Service Level Management)

Navigate to **Service Level Management > SLA > SLA Definitions** (`contract_sla.list`):

### A. P1 Resolution SLA
- **Target Table:** Incident (`incident`)
- **Start Condition:** `[Active is true] AND [Priority is 1 - Critical]`
- **Pause Condition:** `[Incident State is On Hold] AND [On Hold Reason is Awaiting Caller OR Awaiting Vendor]`
- **Stop Condition:** `[Incident State is Resolved] OR [Incident State is Closed]`
- **Duration:** 4 Hours (24x7 Schedule)

### B. P2 Resolution SLA
- **Target Table:** Incident (`incident`)
- **Start Condition:** `[Active is true] AND [Priority is 2 - High]`
- **Pause Condition:** `[Incident State is On Hold]`
- **Stop Condition:** `[Incident State is Resolved] OR [Incident State is Closed]`
- **Duration:** 8 Business Hours (Nexora Business Hours: Mon-Fri 09:00 - 18:00 IST)

### C. First Response SLA (All Priorities)
- **Start Condition:** `[Active is true]`
- **Stop Condition:** `[Assigned To is not empty] OR [First Call Resolution is true] OR [Work Notes is updated]`
- **Target:** P1 = 15 mins, P2 = 60 mins, P3 = 4 business hours, P4 = 8 business hours.
