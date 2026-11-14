# IT Support & Service Desk Lab

A hands-on practical learning project simulating entry-level IT Support and Service Desk operations for **Nexora Technologies**, a fictional company with ~25 employees.

> ℹ️ **Notice:** Nexora Technologies is a fictional organization created for educational and skills-demonstration purposes. This repository represents an independent technical learning project, not commercial employment.

---

## What This Project Is

This repository demonstrates the foundational competencies and operational workflows required for **IT Support Engineer (L1)**, **Service Desk Analyst**, **Desktop Support Technician**, and **Application Support Associate** roles:

- Logging, prioritizing, and managing tickets across their lifecycle.
- Diagnosing Windows desktop, printing, network, and account access issues.
- Administering Active Directory user accounts, security groups, and share permissions.
- Understanding ITIL v4 operational processes (Incident, Request, Problem, Change, and SLA governance).
- Automating support metric calculations (MTTR, FCR, SLA compliance) and validating dataset integrity.

---

## What Was Actually Built

### 1. Operational Service Desk Web Application (`itsm/portal/app.py`)
A self-contained web portal and REST API built with the Python standard library (`http.server`) and SQLite:
- **Customer Portal (`/portal`):** Submit support requests and track real-time progress using a unique ticket key and customer access token.
- **Agent Console (`/agent`):** Role-based access (Admin, L1 Agent, L2 Support, Read-Only), queue management, status progression, work notes, and customer communication.
- **Priority & SLA Engine:** Calculates priority from an Impact × Urgency matrix and evaluates continuous 24x7 elapsed-time resolution targets.
- **Security Controls:** PBKDF2-HMAC-SHA256 password hashing with salt, `HttpOnly` and `SameSite=Strict` cookies, Content Security Policy (CSP), origin validation, and stored-XSS mitigation.

### 2. Active Directory Domain Services Lab (`active-directory/`)
- Isolated **Samba 4 Active Directory Domain Controller** for realm `nexora.test` deployed on Linux/WSL2 via `scripts/deploy_samba_ad.py`.
- Departmental Organizational Units (OUs), domain users, and textbook **AGDLP** group nesting (`Accounts` $\rightarrow$ `Global Groups` $\rightarrow$ `Domain Local Groups` $\rightarrow$ `Permissions`).
- Kerberos ticket acquisition (`kinit`/`klist`) and verified SMB file share access control (`CompanyShared`, `HR-Private`, `Finance-Private`, `IT-Admin`).

### 3. Loopback Packet Capture & TShark Protocol Analysis (`evidence/packet-captures/`)
- Native 20-frame `.pcap` capture of isolated loopback traffic generated via `tcpdump`.
- Forensic protocol inspection using the `tshark` CLI to verify TCP 3-way handshakes (SYN, SYN-ACK, ACK), DNS SRV lookups, DNS NXDOMAIN responses, and HTTP transactions.

### 4. Metrics Reporting & CSV Validation Engine (`reporting/`, `scripts/`)
- Python reporting script (`reporting/report-generator.py`) computing Mean Time to Resolve (MTTR: 15.75h), First Contact Resolution (FCR: 85%), and SLA compliance (85%).
- Automated test suite (`reporting/tests/`) verifying report calculations and edge cases.
- Dataset validator (`scripts/validate-data.py`) verifying schema, chronology, and relational integrity.

---

## What Is Documented or Simulated

To maintain complete transparency during technical interviews, several components serve as operational reference guides and learning exercises rather than live cloud vendor deployments:

- **ServiceNow & Jira Service Management:** Field mapping architectures, queue designs, and standard operating procedures (`itsm/servicenow/`, `itsm/jira-service-management/`).
- **Cisco IOS Configurations:** Syntax-accurate running configuration drafts for Cisco 2911 router and Catalyst 2960 switch implementing a 2-VLAN office design (`networking/packet-tracer/`).
- **Windows Support Runbooks:** 14 practical Standard Operating Procedures for desktop issues including BSOD triage, print spooler crashes, high CPU/RAM, and network adapter resets (`windows-support/runbooks/`).
- **Microsoft 365 Support Guides:** Client-side troubleshooting procedures and a PowerShell diagnostic script (`scripts/m365-client-diag.ps1`) for Office C2R, Teams cache, and OneDrive status (`microsoft-365/`).
- **Sample Datasets:** Canonical CSV records tracking 20 incidents, 8 service requests, 3 problem investigations, 3 change records, and 25 hardware/software assets (`incidents/`, `asset-management/`).

---

## Technologies Used

- **Languages & Core:** Python 3 (standard library: `http.server`, `sqlite3`, `csv`, `json`, `hashlib`, `urllib`), PowerShell 5.1+, Bash
- **Operating Systems:** Windows 11 host, Ubuntu Linux under WSL2
- **Directory Services:** Samba 4 (Active Directory Domain Controller, Kerberos KDC, SMB/CIFS, DNS)
- **Networking & Packet Analysis:** `tcpdump`, `tshark` (Wireshark CLI), Cisco IOS syntax
- **Testing:** Python `unittest`, Playwright (headless browser UI / XSS verification gate)

---

## Quickstart & Local Verification

### Prerequisites
- Python 3.10+ (core portal, reports, and validation require zero external pip packages).
- Optional test dependencies: `pip install -r requirements-test.txt` and `python -m playwright install chromium` (for browser UI test in Module 14).

### 1. Run the Service Desk Application
```powershell
python itsm/portal/app.py
```
- Customer Portal: `http://127.0.0.1:8080/portal`
- Agent Console: `http://127.0.0.1:8080/agent`
*(Dynamic agent credentials are generated on first run and stored in the local `.local_credentials.json` file).*

### 2. Validate CSV Datasets
```powershell
python scripts/validate-data.py
```

### 3. Run Reporting Engine & Tests
```powershell
# Run unit tests
python -m unittest discover -s reporting/tests -v

# Generate summary reports to reporting/reports/
python reporting/report-generator.py --save all
```

### 4. Run Service Desk Automated Test Suite
```powershell
python scripts/test_service_desk_platform.py
```

---

## Project Structure

```text
enterprise-it-service-desk-lab/
├── itsm/                    # ITSM platform documentation & local portal code
│   └── portal/              # Python Service Desk Web App (Customer & Agent portals)
├── active-directory/        # Active Directory guides, user lifecycle, and AGDLP policies
├── networking/              # Network fundamentals, troubleshooting, and Cisco IOS configs
├── windows-support/         # Windows 10/11 troubleshooting guides and 14 support runbooks
├── microsoft-365/           # Client-side troubleshooting guides and diagnostic script
├── incidents/               # Canonical CSV datasets: incidents, requests, problems, changes
├── knowledge-base/          # Standardized KB articles (Windows, Network, M365, User Access)
├── asset-management/        # CSV hardware/software inventory (25 assets) and ITAM guide
├── operations/              # Daily checklists, shift handover SOPs, and support scenarios
├── itil-processes/          # ITIL v4 incident, problem, change, and continuous SLA policies
├── reporting/               # Python reporting engine, summary reports, and unit tests
├── evidence/                # Verifiable artifacts: TShark pcap analysis, Samba AD logs
├── docs/                    # Architecture, environment setup, and technical walkthrough
└── scripts/                 # Platform test suite, Samba deployment, and data validators
```

---

## Project Limitations

- **Fictional Enterprise:** Nexora Technologies and all associated ticket records are simulated for practice.
- **No Live SaaS Subscriptions:** ServiceNow and Jira Service Management materials are operational documentation and architecture guides.
- **Client-Side M365 Scope:** Microsoft 365 work focuses on desktop endpoint triage and diagnostic scripts, not global tenant administration.
- **Reference Network Configs:** Cisco IOS running configs are syntax-checked reference drafts; the repository does not include a compiled `.pkt` simulator file.
- **Loopback Packet Capture:** The PCAP file captures local Linux loopback traffic (`lo`) generated during lab testing, not a physical corporate switch fabric.
- **Educational Scope:** The custom Python service desk application is an educational learning project, not commercial enterprise software.
