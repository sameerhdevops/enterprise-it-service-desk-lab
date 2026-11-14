# Project Scope & Technical Truth Register
## IT Support & Service Desk Operations Lab

This register provides a clear and honest audit of every component in the repository, categorizing each item by its exact technical implementation status.

---

## 1. Classification Categories

- **A. Implemented & Locally Executed:** Real application code, CLI scripts, or reporting tools developed in the project and executed locally.
- **B. Deployed & Verified:** Real local system service or daemon configured, active, and verified through empirical test evidence.
- **C. Tested Local Implementation:** Code or software functionality verified through an automated test suite.
- **D. Simulated Sample Data:** Fictional organizational records (tickets, assets, users, incidents) created to model authentic enterprise support volume.
- **E. Documentation / Reference Only:** Standard operating procedures, enterprise architecture mappings, and configuration runbooks provided for study and procedural guidance without local live deployment.
- **F. Not Implemented / Honest Limitations:** Features or enterprise services intentionally excluded from the lab scope.

---

## 2. Project Truth Register

| # | Lab Component | Technical Classification | Description & Implementation Details |
|---|---|---|---|
| 1 | **Python Service Desk Portal** | **A & C** (Implemented & Tested) | Lightweight web server built in `itsm/portal/app.py` using Python standard library (`http.server`). Listens on port 8080. |
| 2 | **SQLite Database** | **A & C** (Implemented & Tested) | Relational database (`nexora_servicedesk.db`) storing tickets, assets, users, and audit activity records. |
| 3 | **Agent Console (`/agent`)** | **A & C** (Implemented & Tested) | Web interface for service desk technicians with queue filtering, status transitions, work notes, and customer communication. |
| 4 | **Authentication & Authorization** | **A & C** (Implemented & Tested) | PBKDF2 password hashing, secure random salt, session cookies (`HttpOnly`, `SameSite=Strict`), and 4 RBAC roles. |
| 5 | **Customer Access Tokens** | **A & C** (Implemented & Tested) | 32-character urlsafe tokens issued at ticket creation; authorizes customer ticket tracking without exposing agent interfaces. |
| 6 | **Ticket Lifecycle State Machine** | **A & C** (Implemented & Tested) | Strict transitions: Draft $\rightarrow$ Submitted $\rightarrow$ Assigned $\rightarrow$ In Progress $\rightarrow$ Pending Customer/Vendor $\rightarrow$ Resolved $\rightarrow$ Closed. |
| 7 | **Priority Calculation Engine** | **A & C** (Implemented & Tested) | Deterministic 3×3 ITIL matrix mapping Impact (1-3) and Urgency (1-3) to P1, P2, P3, or P4. |
| 8 | **SLA Calculation Engine** | **A & C** (Implemented & Tested) | Continuous 24x7 elapsed-hour measurement from ticket creation. Reopened tickets resume clock from original creation time. |
| 9 | **Samba 4 Active Directory** | **B** (Deployed & Verified) | Isolated Samba 4 Domain Controller for realm `nexora.test` running in WSL2 Ubuntu via `scripts/deploy_samba_ad.py`. |
| 10 | **Kerberos Authentication** | **B** (Deployed & Verified) | Functional KDC in WSL2; ticket granting ticket (TGT) acquisition and inspection verified via `kinit` and `klist`. |
| 11 | **AGDLP Group Management** | **B & D** (Verified in Lab) | Textbook nesting implemented: Accounts $\rightarrow$ Global Groups (`GG-*`) $\rightarrow$ Domain Local Groups (`DL-*`) $\rightarrow$ Permissions. |
| 12 | **SMB Share Permissions** | **B** (Deployed & Verified) | Departmental file shares (`CompanyShared`, `HR-Private`, `Finance-Private`, `IT-Admin`) with verified access and access denied blocks. |
| 13 | **Packet Capture & TShark** | **A & B** (Executed & Verified) | 20-frame loopback `.pcap` capture analyzed via `tshark` CLI with 8 standard display filters (TCP handshake, DNS, ICMP). |
| 14 | **Cisco IOS Running Configs** | **E** (Reference Drafts) | Syntax-accurate Cisco 2911 router and Catalyst 2960 switch configuration files (`.ios`) for a 2-VLAN office design. |
| 15 | **Packet Tracer Documentation** | **E** (Reference Documentation) | Office network topology design, subnet planning, and simulation instructions. No compiled `.pkt` binary in repository. |
| 16 | **Windows Troubleshooting Runbooks** | **E** (Operational SOPs) | 14 Standard Operating Procedures for L1 desktop issues (BSOD triage, printer spooler crashes, high memory, disk cleanup). |
| 17 | **M365 Client Diagnostic Script** | **A** (Executed Locally) | PowerShell script (`scripts/m365-client-diag.ps1`) checking local Office C2R build, Teams cache, OneDrive, and TCP 443 sockets. |
| 18 | **Microsoft 365 Documentation** | **E** (Support Guides) | End-user support guides for Outlook profile errors, OneDrive sync conflicts, and Teams audio configuration. |
| 19 | **ITIL v4 Framework Policies** | **E** (Process Documentation) | Practical policies for Incident, Request, Problem, and Change Management, including Escalation Matrix and SLA governance. |
| 20 | **Incident & Request Datasets** | **D** (Simulated Datasets) | Canonical CSV registers: 20 incidents (P1-P4), 8 service requests, 3 problem records, and 3 change records. |
| 21 | **Asset Inventory Dataset** | **D** (Simulated Dataset) | 25 hardware and software configuration items (laptops, monitors, printers, servers) tracked with serial numbers and models. |
| 22 | **Python Reporting Engine** | **A & C** (Implemented & Tested) | `reporting/report-generator.py` calculates MTTR (15.75h), FCR (85%), SLA compliance rate (85%), and summary breakdowns. |
| 23 | **CSV Dataset Validation** | **A & C** (Implemented & Tested) | `scripts/validate-data.py` validates all 5 CSV registers for schema conformance, unique keys, and chronological dates. |
| 24 | **Service Desk Test Suite** | **A & C** (Executed & Verified) | `scripts/test_service_desk_platform.py` executes 17 automated test modules covering API, auth, CSRF, XSS, and permissions. |
| 25 | **Interview & Walkthrough Guide** | **E** (Technical Walkthrough) | `docs/project-walkthrough.md` provides concise technical explanations of all implemented concepts for interview defense. |

---

## 3. Explicit Boundaries & Exclusions (Category F)

1. **No Live SaaS Tenants:** ServiceNow and Jira Service Management are documented as operational blueprints and field mappings; no paid vendor SaaS instances are attached.
2. **No Microsoft 365 Tenant Administration:** M365 work is restricted to client-side workstation diagnostics and standard operating procedures.
3. **No Hardware Network Simulation:** Cisco IOS configurations are reference design files; they were not executed on physical Cisco hardware or inside an attached `.pkt` simulator file.
4. **No Physical Network Packet Capture:** The capture file (`nexora-lab-traffic.pcap`) captures local Linux loopback (`lo`) traffic, not physical corporate LAN cabling.
5. **Educational Scope:** The custom Python Service Desk application is designed as a learning and demonstration project, not commercial enterprise software.
