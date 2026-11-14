# Project Walkthrough & Technical Interview Guide
## Enterprise IT Service Desk & End-User Support Operations Lab

---

## 1. Why the Project Was Created
This project was built to gain practical, hands-on experience with the day-to-day tools, workflows, and troubleshooting methodologies expected of an entry-level IT Support Engineer (L1), Service Desk Analyst, or Desktop Support Associate. Rather than only memorizing ITIL definitions or reading documentation, this lab implements real, functional software and configurations to practice ticket handling, Active Directory administration, Windows troubleshooting, network diagnostics, and metric reporting.

---

## 2. What the Fictional Company Represents
The lab is centered around **Nexora Technologies**, a fictional company of approximately 25 employees operating across four core departments:
- **Human Resources (HR):** User onboarding, offboarding, policy distribution.
- **Finance:** Accounting systems, ERP access, shared billing directories, payroll printing.
- **Operations:** Facilities, inventory, process flowcharting, meeting room technology.
- **Engineering:** Software developers, automation scripting, workstation build environments.

Using a consistent fictional organization provides realistic business context for every ticket, change request, and incident scenario.

---

## 3. What the Service Desk Application Does
The operational ticketing application is located in `itsm/portal/app.py`. It is a lightweight web server and REST API built entirely using the Python standard library (`http.server`) and SQLite:
- **Customer Portal (`/portal`):** Allows employees to submit incidents or service requests and track real-time progress using their unique ticket key and customer access token.
- **Agent Console (`/agent`):** Provides service desk technicians with authenticated queue visibility, ticket assignment, status progression, internal work note logging, customer communications, and resolution documentation.
- **Security & Integrity:** Implements PBKDF2 password hashing, HTTP-only session cookies with `SameSite=Strict`, Content Security Policy (CSP), Origin/Referer same-origin request validation (checking scheme, hostname, and port), and stored XSS defense.

---

## 4. How the SQLite Database Is Used
The application stores its operational data in an isolated SQLite database (`nexora_servicedesk.db`).
- **Tables:** `tickets`, `ticket_activity`, `users`, and `assets`.
- **Relational Integrity:** Foreign key constraints link tickets to assets and users.
- **Audit History:** Every status change, assignment update, internal note, or customer message is written to the `ticket_activity` ledger with timestamps and user attribution.
- **Fail-Closed Security:** Local bootstrap credentials and database user migrations are handled transactionally so that user accounts can be safely rotated without corrupting existing ticket records.

---

## 5. What Happens When a User Creates a Ticket
1. **Intake & Validation:** The user submits a form on `/portal`. The backend validates mandatory fields (`title`, `caller_name`, `caller_email`, `department`, `impact`, `urgency`, `description`) and validates email syntax via regex.
2. **Key & Token Generation:** The system assigns a unique ticket key (e.g., `NEX-101`) and cryptographically generates a 32-character urlsafe `customer_access_token`.
3. **Priority & Target Assignment:** Priority is calculated based on impact and urgency, and the corresponding SLA target hours are assigned.
4. **Initial Activity Logging:** The initial submission is logged in `ticket_activity` as a `CUSTOMER_SUBMIT` event.
5. **Customer Confirmation:** The portal returns the ticket key and customer access token, allowing the caller to track their ticket without requiring an internal agent login.

---

## 6. How Impact and Urgency Determine Priority
Priority is calculated using a standard 3×3 ITIL Priority Matrix:

| | Urgency 1 (High - Work Blocked) | Urgency 2 (Medium - Impaired) | Urgency 3 (Low - Inconvenience) |
|---|---|---|---|
| **Impact 1 (High - Enterprise / Multi-User)** | **P1 — Critical** | **P2 — High** | **P3 — Medium** |
| **Impact 2 (Medium - Group / Department)** | **P2 — High** | **P3 — Medium** | **P4 — Low** |
| **Impact 3 (Low - Single User)** | **P3 — Medium** | **P4 — Low** | **P4 — Low** |

- **Impact:** How broadly the business or team is affected.
- **Urgency:** How quickly the affected user or business requires resolution.

---

## 7. How the SLA Is Calculated
In this learning lab, SLA resolution targets are calculated using **continuous elapsed clock hours**:
- **P1 (Critical):** 4 elapsed hours
- **P2 (High):** 8 elapsed hours
- **P3 (Medium):** 72 elapsed hours
- **P4 (Low):** 120 elapsed hours

**Measurement Formula:**
- While open: $\text{Elapsed Hours} = \text{Current Time} - \text{Created Time}$
- When resolved: $\text{Elapsed Hours} = \text{Resolved Time} - \text{Created Time}$
- $\text{Remaining Hours} = \max(0.0, \text{Target Hours} - \text{Elapsed Hours})$
- If $\text{Elapsed Hours} > \text{Target Hours}$, the ticket is flagged as **Breached** (`sla_breached = 1`).

**Continuous Clock on Reopening:**
If a resolved ticket is reopened (moved back to *In Progress*), the resolution timestamp is cleared to `NULL`, and elapsed time continues accumulating from the original ticket creation timestamp (`created_at`). Reopening does not reset the clock to zero.

---

## 8. How Internal Notes Differ from Customer Comments
To maintain proper confidentiality and technical clarity, comments are divided into two distinct visibility streams:
- **Work Notes (`WORK_NOTE`):** Visible exclusively to authenticated Service Desk agents and administrators. Used for internal technical diagnostics, escalation transmittals, root-cause notes, and hardware serial numbers. The public API explicitly strips work notes when accessed via a customer access token.
- **Customer Comments (`CUSTOMER_COMMENT`):** Visible on both the agent console and the customer tracking portal. Used for communicating troubleshooting steps, scheduling remote sessions, and notifying users of resolution.

---

## 9. How Samba AD Users and Groups Work
Active Directory provides centralized identity management and access control across the enterprise:
- **Domain Controller:** An isolated Samba 4 AD DC (`nexora.test`) deployed on Linux/WSL2.
- **Directory Structure:** Fictional users are organized into departmental Organizational Units (OUs: `IT`, `HR`, `Finance`, `Operations`, `Engineering`).
- **Security Policies:** Fine-grained password complexity policies, account lockout thresholds (5 failed attempts), and login restriction rules.
- **DNS Integration:** Integrated DNS service resolving domain SRV records (`_ldap._tcp.nexora.test`, `_kerberos._tcp.nexora.test`) and host A records.

---

## 10. What AGDLP Means
**AGDLP** is the Microsoft best-practice role-based access control architecture for managing permissions:
- **A (Accounts):** User accounts (e.g., `alex.chen`, `kavitha.murthy`).
- **G (Global Groups):** Groupings based on organizational function or department (e.g., `GG-HR-Users`, `GG-Finance-Users`).
- **DL (Domain Local Groups):** Groupings representing specific resource permissions on a file share or server (e.g., `DL-HR-Private-RW`, `DL-Finance-ReadWrite`).
- **P (Permissions):** NTFS / share permissions assigned to the Domain Local group (e.g., Modify, Read & Execute).

**Nesting Flow:** User $\rightarrow$ Global Group $\rightarrow$ Domain Local Group $\rightarrow$ Granted NTFS Permission. Users are never assigned directly to resource permissions or Domain Local groups.

---

## 11. What Kerberos Authentication Does
Kerberos is the default network authentication protocol in Active Directory:
1. **Ticket-Granting Ticket (TGT):** When a user logs in, their workstation authenticates against the Key Distribution Center (KDC on the Domain Controller) using their password hash and receives a Ticket-Granting Ticket (`krbtgt`).
2. **Service Ticket (TGS):** When the user accesses a network resource (like an SMB file share `\\nexfs01\finance`), the client presents its TGT to request a service ticket for that specific service principal name (SPN).
3. **No Password over the Wire:** Kerberos uses mutual cryptographic timestamps and symmetric encryption keys, ensuring plain passwords are never transmitted across the network.
4. **Logon Token Refresh:** Because a user's Windows access token is generated at logon, adding a user to a new AD group typically requires the user to **sign out and sign back in** so that Windows builds a fresh security access token containing the new group SID.

---

## 12. How SMB Share Permissions Were Tested
SMB network shares on the domain controller were tested for authenticated access and least privilege:
- `CompanyShared`: All authenticated domain users have read/write access.
- `HR-Private`: Accessible only to members of `GG-HR-Users` through Domain Local group permissions.
- `Finance-Private`: Accessible only to members of `GG-Finance-Users`.
- `IT-Admin`: Restricted strictly to IT administrators.
- **Verification:** Tests demonstrated successful authenticated file creation on authorized shares, and confirmed `NT_STATUS_ACCESS_DENIED` blocks when unauthorized users (e.g., Finance user attempting to access `HR-Private`) attempted connection.

---

## 13. What the PCAP File Demonstrates
The capture file (`evidence/packet-captures/nexora-lab-traffic.pcap`) contains 20 frames of local loopback traffic captured using `tcpdump` and analyzed using the `tshark` CLI:
- **ICMP Echo:** Request and reply sequence demonstrating Layer 3 network reachability.
- **DNS Protocol:** Standard SRV query lookups and an intentional NXDOMAIN error response showing query rejection behavior.
- **TCP 3-Way Handshake:** Explicit SYN, SYN-ACK, and ACK frame sequence on port 8085 demonstrating connection establishment.
- **HTTP Payload:** Full HTTP GET request and HTTP 200 OK server response sequence.
- **Analysis Scope:** Validates protocol syntax, TCP flag behavior, and command-line packet filtering using standard Wireshark display filters.

---

## 14. How the Python Reporting Script Calculates Metrics
The reporting generator (`reporting/report-generator.py`) processes the canonical incident CSV register and produces key operational metrics:
- **Total Ticket Volume:** Count of all incidents and requests.
- **Mean Time to Resolve (MTTR):** Total elapsed resolution hours divided by the number of resolved incidents ($\frac{267.75\text{ h}}{17\text{ tickets}} = 15.75\text{ hours}$).
- **L1 Resolution Rate (Non-Escalated):** Percentage of sample incidents resolved by the L1 Service Desk without functional escalation to L2/L3 ($\frac{17}{20} = 85.0\%$). This metric measures tickets handled entirely within L1; it does not measure First Contact Resolution (FCR), which requires multi-touch interaction logs.
- **SLA Attainment:**
  - **Resolved-Ticket SLA Attainment:** 100.0% (all 17 resolved incidents completed within their target elapsed resolution window).
  - **Portfolio Snapshot Attainment:** 85.0% ($\frac{17}{20}$ incidents compliant), taking into account the 3 escalated open backlog tickets overdue against target at the snapshot baseline.
- **Category & Priority Breakdown:** Aggregated volume tables to identify chronic problem areas (e.g., network and printing bottlenecks).

---

## 15. What Was Not Implemented (Honest Project Limitations)
To maintain complete integrity during technical interviews:
- **No Commercial SaaS Deployment:** ServiceNow and Jira Service Management are documented as operational reference guides and field-mapping architectures; no live production SaaS subscriptions are attached.
- **No Microsoft 365 Tenant Administration:** M365 work is focused on client-side desktop diagnostics (PowerShell inspection of Office C2R, Teams local cache, OneDrive process states, and cloud endpoint TCP 443 socket reachability), not global tenant administration.
- **No Compiled Cisco Packet Tracer Binary:** Cisco IOS configurations are syntax-checked reference configuration drafts implementing a 3-VLAN design (VLAN 10 Corporate Users, VLAN 20 Server Farm, VLAN 99 Management); the project does not include a verified `.pkt` binary simulator file.
- **Local Loopback Packet Capture:** The PCAP file captures traffic across the local Linux loopback interface (`lo`), not a physical corporate switch fabric or physical LAN cable.
- **Learning Lab Scope:** The custom Python service desk application is an educational learning tool and is not intended for commercial production deployment.
- **Historical Security Disclosure:** Early repository drafts contained static placeholder credentials that have been invalidated locally and replaced with dynamically generated random credentials (`.local_credentials.json` and `.ad_credentials.json`, mode 0600, git-ignored). An automated migration in `init_db()` rotates legacy database password hashes on startup. Because historical Git commits retain early drafts, users should treat all historical commit values as publicly known.

---

## Live Demonstrable vs. Reference Practice

| Category | Component | Demonstration Method |
|---|---|---|
| **What I Can Demonstrate Live** | Python Service Desk Web Portal | Run `python itsm/portal/app.py`, log in as agent or customer, submit and resolve tickets live in the browser. |
| **What I Can Demonstrate Live** | Automated Platform Test Suite | Run `python scripts/test_service_desk_platform.py` (all 17 security and integration test modules execute). |
| **What I Can Demonstrate Live** | Python Reporting Engine & Unit Tests | Run `python reporting/report-generator.py --save all` and `python -m unittest discover -s reporting/tests -v`. |
| **What I Can Demonstrate Live** | CSV Data Integrity Validation | Run `python scripts/validate-data.py` (validates all 5 datasets with zero errors). |
| **What I Can Demonstrate Live** | Samba 4 Active Directory DC | Demonstrate running Samba DC in WSL2, user query, Kerberos ticket acquisition, and SMB share access. |
| **What I Can Demonstrate Live** | TShark Protocol Packet Analysis | Run TShark commands against `evidence/packet-captures/nexora-lab-traffic.pcap` showing TCP handshakes and DNS queries. |
| **What is Documentation or Reference** | ServiceNow & Jira Guides | Field mapping architectures, workflow diagrams, and configuration runbooks. |
| **What is Documentation or Reference** | Cisco IOS Running Configs | Router-on-a-stick and switch port configurations documented as reference drafts. |
| **What is Documentation or Reference** | Microsoft 365 Support Guides | Standard operating procedures for Outlook sync, OneDrive conflicts, and Teams audio triage. |
| **What is Documentation or Reference** | Fictional Incident Register | 20 realistic incidents, 8 requests, and ITIL process documentation modeling Nexora Technologies. |
