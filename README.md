# Enterprise IT Service Desk Lab

[![Repository](https://img.shields.io/badge/GitHub-sameerhdevops%2Fenterprise--it--service--desk--lab-blue?logo=github)](https://github.com/sameerhdevops/enterprise-it-service-desk-lab)
[![Validation Tests](https://img.shields.io/badge/Unit%20Tests-13%2F13%20Passing-brightgreen)](reporting/tests/test_validation.py)
[![Service Desk Tests](https://img.shields.io/badge/ITSM%20Tests-15%2F15%20Passing-brightgreen)](scripts/test_service_desk_platform.py)
[![Data Integrity](https://img.shields.io/badge/Datasets-Validated-brightgreen)](scripts/validate-data.py)
[![Role](https://img.shields.io/badge/Target%20Role-IT%20Support%20Engineer%20L1-orange)]()

A hands-on learning lab simulating L1 IT support operations for a small fictional company called **Nexora Technologies**. Built from scratch to develop and demonstrate the practical competencies, diagnostic workflows, and tools utilized by an entry-level IT Support Engineer — ticketing, Active Directory, networking, Windows troubleshooting, and metrics analysis.

**Repository URL:** [https://github.com/sameerhdevops/enterprise-it-service-desk-lab](https://github.com/sameerhdevops/enterprise-it-service-desk-lab)  
**Project Creator / Lab Administrator:** Sameer H ([@sameerhdevops](https://github.com/sameerhdevops))  
**Target Roles:** IT Support Engineer L1, Technical Support Engineer, Service Desk Analyst, Desktop Support Engineer

---

## What This Is (and Isn't)

This is a **self-directed, hands-on learning portfolio**, not commercial employment. Nexora Technologies is a fictional organization (~25 employees) used to model realistic operational scenarios. The lab executes entirely on local hardware (Windows 11 host with WSL2 Ubuntu) under a strict **₹0 budget constraint** (zero paid cloud subscriptions, zero trial billing, and zero external API dependencies).

- **Deployed & Verified locally:** Custom native IT Service Desk web app, Samba 4 Active Directory Domain Controller with AGDLP group nesting, native packet capture (`.pcap`) and TShark protocol analysis, and Microsoft 365 client-side diagnostic scripts.
- **Documented Reference Blueprints:** SaaS platform architectures (ServiceNow PDI and Jira Service Management Cloud) and Cisco Packet Tracer network simulation designs are fully documented as enterprise standard operating procedures and reference blueprints.

---

## Security & Credential Transparency Notice

> [!CAUTION]
> **Credential Rotation & Git Provenance:**
> Earlier experimental commits in this repository's public Git history contain static laboratory credentials used during initial drafting. In accordance with standard security hygiene, **all historical credentials have been invalidated and rotated**.
> Current active credentials are generated dynamically on first run and stored strictly in git-ignored local secret stores (`itsm/portal/.local_credentials.json` and `evidence/active-directory/.ad_credentials.json`). No active passwords, keys, or authentication tokens are committed to source control.

---

## Lab Architecture & Modules

```text
enterprise-it-service-desk-lab/
├── itsm/                    # ITSM platform architectures
│   └── portal/              # Deployed Python Service Desk Web App (Customer Portal & Agent Console)
├── active-directory/        # Active Directory architecture, OUs, and AGDLP group nesting
├── networking/              # Network fundamentals, troubleshooting, and Cisco IOS configs
│   └── packet-tracer/       # Cisco 2911 ISR router & Catalyst 2960 switch running configurations
├── windows-support/         # Windows 11 troubleshooting, Event Viewer, Fast Startup, and 15 runbooks
├── microsoft-365/           # Client-side diagnostics, Click-to-Run builds, and Teams/OneDrive guides
├── incidents/               # Historical sample registers: 20 incidents, 8 requests, 3 problems, 3 changes
├── knowledge-base/          # 12 standardized enterprise KB articles (Windows, Net, M365, Access)
├── asset-management/        # CSV-based hardware/software inventory (25 assets) and ITAM guide
├── operations/              # Operational checklists, shift handover SOPs, and 6 end-to-end scenarios
├── itil-processes/          # ITIL v4 incident, problem, change, and continuous SLA policies
├── reporting/               # Python MIS reporting engine, SLA calculators, and unit tests
├── career-assets/           # Resume bullets, Naukri/LinkedIn copy, and interview pitches
├── interview-preparation/   # 12-minute live interview demo runbook and technical study notes
├── evidence/                # Auditable artifacts: TShark pcap analysis, Samba AD logs, M365 diagnostics
└── scripts/                 # Platform test suites, Samba AD manager, packet capture, and validators
```

| Module | What It Covers | Standard Status |
|--------|---------------|-----------------|
| **itsm/portal/** | **Operational Service Desk Platform** — Native web application (`app.py`, Python stdlib + SQLite): Customer Portal, L1 Operator Console, 10 operational queues, PBKDF2 authentication, CSRF/same-origin protection, customer access token security, dynamic SLA clock tracking, stored XSS defense. | **DEPLOYED & VERIFIED** |
| **itsm/** | ITSM platform architecture & comparison blueprints — ServiceNow (PDI) and Jira Service Management setup, ticket workflows, SLA definitions. | **DOCUMENTED / REFERENCE** |
| **incidents/** | Fictional incident scenarios with full lifecycle documentation: logging, categorization, troubleshooting, and resolution notes. | **SIMULATED & VERIFIED** |
| **knowledge-base/** | 12 standardized enterprise KB articles for common support scenarios: password resets, VPN, printers, M365 issues. | **DOCUMENTED / REFERENCE** |
| **active-directory/** | Active Directory architecture, OUs, textbook AGDLP group nesting (`GG-*` -> `DL-*`), and Samba 4 AD DC deployment (`scripts/deploy_samba_ad.py`). | **DEPLOYED & VERIFIED** |
| **networking/** | Network fundamentals: Cisco 2911 router and 2960 switch IOS configs (`rtr01`, `sw01`), VLANs, 802.1Q subinterfaces, router DHCP, NAT, lab guide. | **IMPLEMENTED & VERIFIED** (Configs) / **DOCUMENTED / REFERENCE** (Sim Guide) |
| **windows-support/** | Windows 11 troubleshooting: Fast Startup vs memory leaks, Event Viewer (ID 4740), Print Spooler, remote support, 15 authored runbooks. | **IMPLEMENTED & VERIFIED** |
| **microsoft-365/** | M365 client diagnostics (`scripts/m365-client-diag.ps1`), Click-to-Run builds, Teams LocalCache, measured TCP 443 connect latency. | **DEPLOYED & VERIFIED** (Client Diag) / **OUT OF FINAL SCOPE** (Tenant Admin) |
| **asset-management/** | Hardware/software inventory tracking using CSV-based records (25 assets). | **SIMULATED & VERIFIED** |
| **operations/** | Operational procedures: 6 end-to-end support scenarios, shift handover templates, daily checklists, escalation procedures. | **IMPLEMENTED & VERIFIED** |
| **reporting/** | Python scripts (stdlib only) for generating reports from incident and asset data; 13/13 passing unit tests. | **IMPLEMENTED & VERIFIED** |
| **communication/** | Email templates, user communication guides, phone scripts for support scenarios. | **DOCUMENTED / REFERENCE** |
| **itil-processes/** | ITIL v4 foundations applied: incident management, problem management, change management, continuous elapsed-clock-hour SLA. | **IMPLEMENTED & VERIFIED** |
| **interview-preparation/** | Study notes, 12-minute live interview demonstration runbook (`live-demo-runbook.md`), and scenario practice. | **IMPLEMENTED & VERIFIED** |
| **career-assets/** | Interview-ready portfolio descriptions: Resume bullets, Naukri/LinkedIn copy, 60s/3m pitches (`portfolio-descriptions.md`). | **IMPLEMENTED & VERIFIED** |
| **evidence/** | Verified command outputs, clean loopback `.pcap` capture & TShark analysis, Samba AD DC verification logs, M365 diagnostics. | **DEPLOYED & VERIFIED** |
| **scripts/** | Administration, deployment, packet capture, and test scripts (all standard library, zero external pip packages). | **IMPLEMENTED & VERIFIED** |

---

## Quick Start & Local Verification

Clone and test the entire lab environment locally. All scripts use standard library components with **zero pip dependencies**:

```bash
# Clone the repository
git clone https://github.com/sameerhdevops/enterprise-it-service-desk-lab.git
cd enterprise-it-service-desk-lab

# 1. Run the Service Desk test suite (17/17 tests passing)
python scripts/test_service_desk_platform.py

# 2. Launch the interactive Service Desk Platform (Customer Portal & Agent Console)
python itsm/portal/app.py
# -> Customer Portal:       http://127.0.0.1:8080/portal
# -> L1 Agent Queue:        http://127.0.0.1:8080/agent

# 3. Validate dataset integrity across all CSV registers (0 errors, 0 warnings)
python scripts/validate-data.py

# 4. Run automated validation and calculation unit test suite (13/13 passing)
python -m unittest discover -s reporting/tests -v

# 5. Generate Service Desk MIS and SLA reports
python reporting/report-generator.py --save all
```

---

## Auditable Lab Evidence

- **Wireshark / TShark Packet Capture:** Open `evidence/packet-captures/nexora-lab-traffic.pcap` (3,776 bytes) in Wireshark or inspect with TShark. Read the companion [packet analysis report](evidence/packet-captures/packet-analysis-report.md) with verified display filters for ICMP, DNS SRV/NXDOMAIN, and TCP 3-way handshakes.
- **Active Directory Verification:** Inspect `evidence/active-directory/samba-ad-dc-verification.txt` for real Kerberos ticket granting (`kinit`), DNS SRV lookups, and authenticated SMB share read/write and access denial assertions.
- **Microsoft 365 Diagnostics:** Inspect `evidence/microsoft-365/m365-client-diagnostics-output.txt` for host Click-to-Run builds, New Teams LocalCache checks, OneDrive process state, and live TCP port 443 socket connect latencies to Microsoft cloud endpoints.
- **Live Interview Demo:** Follow the step-by-step 12-minute script in [interview-preparation/live-demo-runbook.md](interview-preparation/live-demo-runbook.md).

---

## Disclaimer

This is an **independent learning project**. Nexora Technologies is a fictional organization created for practical technical training. The incidents, users, and organizational structure are simulated for hands-on practice.
