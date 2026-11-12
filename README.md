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
| **itsm/** | ITSM platform configuration — ServiceNow (PDI) and Jira Service Management setup, ticket workflows, SLA definitions |
| **incidents/** | Simulated incident scenarios with full lifecycle documentation: logging, categorization, troubleshooting, resolution |
| **knowledge-base/** | KB articles written for common issues: password resets, VPN, printer problems, M365 troubleshooting |
| **active-directory/** | User provisioning, group policies, account management exercises using local simulation |
| **networking/** | Network fundamentals practiced in Cisco Packet Tracer: VLANs, DNS, DHCP, basic topology design |
| **windows-support/** | Windows 11 troubleshooting: OS issues, driver problems, software installation, remote support, printers |
| **microsoft-365/** | M365 admin and troubleshooting: Outlook, Teams, OneDrive, license management |
| **asset-management/** | Hardware/software inventory tracking using CSV-based records |
| **operations/** | Operational procedures: shift handover templates, daily checklists, escalation procedures |
| **reporting/** | Python scripts (stdlib only) for generating reports from incident and asset data |
| **communication/** | Email templates, user communication guides, professional writing for support scenarios |
| **itil-processes/** | ITIL v4 foundations applied: incident management, problem management, change management, SLA management |
| **scripts/** | Utility scripts for common admin tasks |
| **interview-preparation/** | Study notes and scenario practice for IT support interviews |

## Tech Stack

| Tool | Purpose | Why This One |
|------|---------|-------------|
| **ServiceNow PDI** | Primary ITSM platform | Industry standard; free Personal Developer Instance |
| **Jira Service Management** | Secondary ITSM platform | Widely used; free tier available |
| **Cisco Packet Tracer** | Network simulation | Standard for learning networking; free |
| **Python 3.14** | Reporting scripts | Stdlib only — no dependencies to manage |
| **PowerShell 5.1** | Windows automation & admin | Built into Windows, essential for IT support |
| **Git** | Version control | Track everything, show progression |
| **Windows 11** | Primary OS / lab environment | What most offices actually run |

See [docs/design-decisions.md](docs/design-decisions.md) for the reasoning behind each choice.

## Navigating the Repo

```
enterprise-it-service-desk-lab/
├── docs/                    # Project documentation, architecture, design decisions
├── architecture/            # Standalone Mermaid diagram files
├── itsm/                    # ServiceNow + Jira configuration and evidence
│   ├── servicenow/
│   └── jira-service-management/
├── incidents/               # Simulated incident scenarios and resolutions
├── knowledge-base/          # KB articles by category
│   ├── windows/
│   ├── networking/
│   ├── microsoft-365/
│   └── user-access/
├── active-directory/        # AD lab exercises and documentation
├── networking/              # Packet Tracer labs and network documentation
│   └── packet-tracer/
├── windows-support/         # Windows troubleshooting by category
│   ├── operating-system/
│   ├── hardware/
│   ├── software/
│   ├── printers/
│   ├── remote-support/
│   └── runbooks/
├── microsoft-365/           # M365 troubleshooting scenarios
├── asset-management/        # Inventory and tracking
├── operations/              # Shift handovers, checklists, procedures
├── reporting/               # Python report generation scripts
├── communication/           # Email/comms templates
├── itil-processes/          # ITIL framework documentation
├── scripts/                 # Admin utility scripts
├── interview-preparation/   # Interview prep materials
├── evidence/                # Screenshots, command output, validation records
│   ├── command-output/
│   ├── network-diagrams/
│   ├── platform-screenshots/
│   └── validation/
└── tests/                   # Script tests
```

Start with [docs/project-overview.md](docs/project-overview.md) for the full picture, then explore whichever module interests you.

## Environment

This lab runs on a single Windows 11 machine — no cloud VMs, no complex infrastructure. The specifics are in [docs/environment-details.md](docs/environment-details.md), but the short version: a laptop with an i5 and 16GB RAM, running everything locally. That's a deliberate choice — it mirrors the kind of hardware you'd actually troubleshoot in a small office.

## Implementation Status & Defensibility

To ensure transparency during technical interviews, all modules follow four standardized status classifications:
- **IMPLEMENTED & VERIFIED:** Actually configured, executed, and tested locally (Windows 11 diagnostics, Python reporting utility, unit tests, dataset validators, command evidence).
- **DOCUMENTED:** Standard operating procedures, runbooks, and configurations are fully authored and defensible.
- **SIMULATED:** Modeled through realistic fictional datasets (20 incidents, 8 service requests, 3 problems, 3 changes, 25 assets) and illustrative vector diagrams.
- **MANUAL ACTION REQUIRED:** Requires individual candidate cloud credentials (ServiceNow PDI registration, Atlassian Cloud free tier).

See [docs/implementation-status.md](docs/implementation-status.md) and [PROJECT_STATUS.md](PROJECT_STATUS.md) for the complete compliance audit.

## Quick Start & Verification

Clone and verify the lab datasets and reporting engine locally (requires Python 3.8+; standard library only, zero external pip packages):

```bash
git clone https://github.com/sameerhdevops/enterprise-it-service-desk-lab.git
cd enterprise-it-service-desk-lab

# 1. Validate dataset integrity across all CSV registers
python scripts/validate-data.py

# 2. Run automated validation and calculation unit test suite
python -m unittest discover -s reporting/tests

# 3. Generate Service Desk MIS and SLA reports
python reporting/report-generator.py --save all
```

## Disclaimer

This is a **learning project**. Nexora Technologies is fictional. The incidents, users, and org structure are all made up for practice purposes. Nothing here should be treated as production-ready configuration or deployed in a real environment. Credentials, if any appear in examples, are for lab instances only.
