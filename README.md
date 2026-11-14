# Enterprise IT Service Desk Lab

[![Repository](https://img.shields.io/badge/GitHub-sameerhdevops%2Fenterprise--it--service--desk--lab-blue?logo=github)](https://github.com/sameerhdevops/enterprise-it-service-desk-lab)
[![Validation Tests](https://img.shields.io/badge/Tests-13%2F13%20Passing-brightgreen)](reporting/tests/test_validation.py)
[![Data Integrity](https://img.shields.io/badge/Datasets-Validated-brightgreen)](scripts/validate-data.py)
[![Role](https://img.shields.io/badge/Target%20Role-IT%20Support%20Engineer%20L1-orange)]()

A hands-on learning lab simulating L1 IT support operations for a small fictional company called **Nexora Technologies**. I built this to teach myself the day-to-day workflows, tools, and troubleshooting that an entry-level IT Support Engineer actually deals with — ticketing, Active Directory, networking, hardware issues, the whole stack.

**Repository URL:** [https://github.com/sameerhdevops/enterprise-it-service-desk-lab](https://github.com/sameerhdevops/enterprise-it-service-desk-lab)  
**Author:** Sameer H ([@sameerhdevops](https://github.com/sameerhdevops))

## What This Is (and Isn't)

This is a **personal learning lab**, not a production setup. The "company" is made up, the tickets are scenarios I create and work through, and the environment runs on my personal laptop. The goal is practical skill-building: configuring real tools (ServiceNow, Jira), working through realistic incident scenarios, writing knowledge base articles, and building the muscle memory for L1 support work.

It's not meant to be a polished product or a template for real deployments. It's meant to be evidence that I can do this work.

## The Fictional Company: Nexora Technologies

Nexora Technologies is a small tech consulting firm with roughly 25 employees spread across four departments: HR, Finance, Operations, and IT. They run a pretty standard small-business stack — Microsoft 365 for productivity, Windows 11 workstations, a basic office network. The IT team is small (3 people), so the L1 support engineer handles a wide range of issues.

See [docs/support-model.md](docs/support-model.md) for the full org structure and support model.

## Modules

| Module | What It Covers |
|--------|---------------|
| **itsm/portal/** | **Operational Service Desk Platform** — Native interactive web application (`app.py`, Python stdlib + SQLite): Customer Portal, L1 Operator Console, 10 operational queues, PBKDF2 authentication, Impact x Urgency priority matrix, dynamic SLA clock tracking, stored XSS defense |
| **itsm/** | ITSM platform architecture & comparison blueprints — ServiceNow (PDI) and Jira Service Management setup, ticket workflows, SLA definitions (SaaS deployment Out of Final Scope) |
| **incidents/** | Simulated incident scenarios with full lifecycle documentation: logging, categorization, troubleshooting, resolution |
| **knowledge-base/** | KB articles written for common issues: password resets, VPN, printer problems, M365 troubleshooting |
| **active-directory/** | Active Directory architecture, OUs, textbook AGDLP group nesting (`GG-*` -> `DL-*`), and non-destructive Samba 4 AD DC deployment script (`scripts/deploy_samba_ad.py`) |
| **networking/** | Network fundamentals: Cisco Packet Tracer running configs (`rtr01`, `sw01`), VLANs, 802.1Q subinterfaces, DHCP pools, NAT, lab guide |
| **windows-support/** | Windows 11 troubleshooting: Fast Startup vs memory leaks, Event Viewer (ID 4740), Print Spooler, remote support, runbooks |
| **microsoft-365/** | M365 client diagnostics (`scripts/m365-client-diag.ps1`), Click-to-Run builds, Teams LocalCache, measured TCP 443 connect latency, runbooks |
| **asset-management/** | Hardware/software inventory tracking using CSV-based records |
| **operations/** | Operational procedures: 6 end-to-end support scenarios, shift handover templates, daily checklists, escalation procedures |
| **reporting/** | Python scripts (stdlib only) for generating reports from incident and asset data |
| **communication/** | Email templates, user communication guides, professional writing for support scenarios |
| **itil-processes/** | ITIL v4 foundations applied: incident management, problem management, change management, SLA management |
| **interview-preparation/** | Study notes, 12-minute live interview demonstration runbook (`live-demo-runbook.md`), and scenario practice |
| **career-assets/** | Interview-ready portfolio descriptions: Resume bullets, Naukri/LinkedIn copy, 60s/3m pitches (`portfolio-descriptions.md`) |
| **evidence/** | Verified command outputs, clean Wireshark `.pcap` capture & TShark analysis, Samba AD DC verification logs, M365 diagnostics |
| **scripts/** | Administration, deployment, testing, and packet capture utility scripts |

## Tech Stack

| Tool / Technology | Purpose in Portfolio | Technical Classification | Why This One |
|---|---|---|---|
| **Nexora IT Service Desk** | Primary ITSM Platform | **DEPLOYED & VERIFIED** | Self-hosted Python HTTP + SQLite application with real queues, PBKDF2 auth, and dynamic SLA timers |
| **Samba 4 Active Directory** | Directory & Identity | **DEPLOYED & VERIFIED** | Runs in WSL2 Ubuntu; real Kerberos KDC, DNS SRV resolution, AGDLP nesting, and SMB share controls |
| **Wireshark & TShark** | Packet Capture & Analysis | **DEPLOYED & VERIFIED** | Clean loopback trace analyzed via `tshark 4.2.2` verifying ICMP, DNS SRV/NXDOMAIN, and TCP 3-way handshake |
| **PowerShell 5.1 / 7+** | Windows 11 Diagnostics | **DEPLOYED & VERIFIED** | Native Windows automation for Event Viewer ID 4740, Uptime/Fast Startup, and M365 endpoint TCP socket latency |
| **Python 3.12+ (stdlib)** | MIS Reporting & Portal | **IMPLEMENTED & VERIFIED** | Zero-dependency reporting engine and web portal; 13/13 passing unit tests |
| **Cisco Packet Tracer** | Network Simulation | **IMPLEMENTED & VERIFIED** | Realistic Cisco 2911 router and Catalyst 2960 switch running configurations for 802.1Q inter-VLAN routing |
| **ServiceNow & Jira Blueprints**| Enterprise ITSM Comparison | **DOCUMENTED / REFERENCE** | Complete field dictionaries and workflows; external SaaS provisioning is Out of Final Scope |

See [docs/design-decisions.md](docs/design-decisions.md) for the reasoning behind each choice.

## Navigating the Repo

```
enterprise-it-service-desk-lab/
├── docs/                    # Architecture, support model, design decisions, implementation audit
├── architecture/            # Standalone Mermaid diagrams (ITIL workflows, network topology, AD OU)
├── itsm/                    # Service Desk implementations
│   ├── portal/              # Operational web platform (app.py: Customer Portal & L1 Console)
│   ├── servicenow/          # ServiceNow PDI configuration runbooks & XML definitions
│   └── jira-service-management/ # Jira Service Management free-tier configuration
├── incidents/               # 20 incidents, 8 service requests, 3 problems, 3 changes (CSV registers)
├── knowledge-base/          # 8 polished standard operating KB articles
├── active-directory/        # OU structures, AGDLP security model, and verification runbooks
├── networking/              # Network architecture & Cisco Packet Tracer lab
│   └── packet-tracer/       # Running configs (rtr01, sw01) & hands-on lab guide
├── windows-support/         # OS, Fast Startup, Event Viewer 4740, Spooler, remote support runbooks
├── microsoft-365/           # M365 client troubleshooting runbooks & architecture
├── asset-management/        # 25-device hardware/software inventory (CSV register)
├── operations/              # Operational checklists, shift handover, 6 end-to-end scenarios
│   └── scenarios/           # Detailed walkthrough of common L1 support cases
├── reporting/               # Python MIS and SLA reporting engine (zero pip dependencies)
│   └── tests/               # 13 automated unit tests for validation & calculations
├── communication/           # Professional user communication & notification templates
├── itil-processes/          # ITIL v4 Incident, Problem, Change, and SLA management frameworks
├── interview-preparation/   # Study notes, FAQ, and 12-minute Live Interview Demonstration Runbook
├── career-assets/           # Portfolio copy: Resume bullets, Naukri/LinkedIn, 60s/3m pitches
├── evidence/                # Auditable proof: Wireshark .pcap, Samba logs, M365 diagnostics
│   ├── active-directory/    # Real Samba AD DC verification logs (Kerberos, DNS SRV, SMB ACL)
│   ├── packet-captures/     # Native pcap capture file & forensic packet analysis report
│   ├── itsm/                # Live Service Desk test execution evidence & JSON export
│   ├── microsoft-365/       # Real host PowerShell diagnostic output (Click-to-Run, endpoints)
│   └── command-output/      # Host PowerShell verification command outputs
└── scripts/                 # Automation, deployment, packet capture, and test scripts
```

Start with [docs/project-overview.md](docs/project-overview.md) for the full picture, or consult [interview-preparation/live-demo-runbook.md](interview-preparation/live-demo-runbook.md) for an interactive interview walkthrough.

## Environment

This lab runs on a single Windows 11 Enterprise machine (HP 348 G7, Intel Core i5-10210U, 16GB RAM) utilizing native tools, PowerShell 5.1/7+, Python 3.12+, and an embedded Ubuntu 24.04 WSL2 environment for Linux/Samba services. See [docs/environment-details.md](docs/environment-details.md) for hardware and platform specifications.

## Implementation Status & Defensibility

To ensure 100% transparency during technical interviews, all modules follow standardized status classifications:
- **DEPLOYED & VERIFIED:** Fully deployed, executed, and tested with real artifacts saved in `evidence/` (Samba 4 AD DC with Kerberos and DNS, native clean Wireshark `.pcap` capture with TShark filter verification, operational Python Service Desk web platform with 10 queues and PBKDF2 auth, host M365 diagnostic scripts with measured TCP connect latencies).
- **IMPLEMENTED & VERIFIED:** Actually configured, executed, and validated locally (Python reporting engine, 13/13 passing unit tests, dataset validators, Cisco Packet Tracer router/switch running configs).
- **SIMULATED & VERIFIED:** Modeled through realistic datasets (20 incidents, 8 service requests, 3 problems, 3 changes, 25 assets) with 0 validation errors.
- **DOCUMENTED / REFERENCE:** Standard operating procedures, enterprise runbooks, and ITIL practices fully authored and interview-defensible.
- **OUT OF FINAL SCOPE:** External vendor SaaS instances (ServiceNow PDI, Jira Cloud) and tenant-level M365 administration requiring commercial cloud subscriptions; verified zero-cost local alternatives deployed and demonstrated instead.

See [PROJECT_STATUS.md](PROJECT_STATUS.md) and [docs/implementation-status.md](docs/implementation-status.md) for the comprehensive compliance matrix.

## Quick Start & Verification

Clone and test the entire lab environment locally. All scripts use standard library components with **zero pip dependencies**:

```bash
# Clone the repository
git clone https://github.com/sameerhdevops/enterprise-it-service-desk-lab.git
cd enterprise-it-service-desk-lab

# 1. Launch the interactive Service Desk Platform (Customer Portal & Agent Console)
python itsm/portal/app.py
# -> Customer Portal:       http://127.0.0.1:8080/portal
# -> L1 Agent Queue:        http://127.0.0.1:8080/agent

# 2. Run the Service Desk test suite (tests priority matrix, lifecycle transitions, audit trail)
python scripts/test_service_desk_platform.py

# 3. Validate dataset integrity across all CSV registers (0 errors, 0 warnings)
python scripts/validate-data.py

# 4. Run automated validation and calculation unit test suite (13/13 passing)
python -m unittest discover -s reporting/tests -v

# 5. Generate Service Desk MIS and SLA reports
python reporting/report-generator.py --save all
```

### Inspecting Lab Evidence

- **Wireshark Packet Capture:** Open `evidence/packet-captures/nexora-lab-traffic.pcap` in Wireshark to inspect live ICMP, DNS SRV/NXDOMAIN, and TCP 3-way handshakes. Read the companion [packet analysis report](evidence/packet-captures/packet-analysis-report.md).
- **Active Directory Verification:** Inspect `evidence/active-directory/samba-ad-dc-verification.txt` for real Kerberos ticket granting (`kinit`), DNS SRV lookups, and SMB share access denials.
- **Microsoft 365 Diagnostics:** Inspect `evidence/microsoft-365/m365-client-diagnostics-output.txt` for real host Click-to-Run builds, New Teams LocalCache checks, and TCP 443 connectivity to Microsoft cloud endpoints.
- **Live Interview Demo:** Follow the step-by-step 12-minute script in [interview-preparation/live-demo-runbook.md](interview-preparation/live-demo-runbook.md).

## Disclaimer

This is a **learning project**. Nexora Technologies is fictional. The incidents, users, and org structure are all made up for practice purposes. Nothing here should be treated as production-ready configuration or deployed in a real environment. Credentials, if any appear in examples, are for lab instances only.
