# IT Service Desk & Infrastructure Support Lab

A hands-on project I built to practise the day-to-day work of an **L1 IT Support Engineer / Service Desk Analyst**. It brings together ticket handling, Windows troubleshooting, identity and access management, basic network diagnostics, and service desk reporting in a fictional company environment.

**Built with:** Python · SQLite · Samba 4 · PowerShell · WSL2 · TShark

---

## What I Built

| Area | Implementation |
|---|---|
| **Service Desk Application** | A local Python and SQLite web app with customer and agent portals, ticket assignment and status updates, 10 support queues, internal work notes, customer comments, priority mapping, and elapsed-time SLA tracking. |
| **Identity & Access** | A Samba 4 Active Directory lab in Ubuntu on WSL2, with fictional domain users, departmental OUs, AGDLP group nesting, Kerberos authentication, and SMB share access tests. |
| **Windows Support** | 15 troubleshooting runbooks covering application issues, login problems, high CPU/memory, low disk space, drivers, network adapters, printers, Windows services, shared folders, software installation, and USB devices. |
| **Microsoft 365 Client Checks** | A PowerShell script that checks local Office installation details, Outlook profile registry entries, Teams process/cache presence, OneDrive process/folder presence, and TCP port 443 reachability to selected Microsoft endpoints. |
| **Networking & Reporting** | A 20-frame Linux loopback PCAP analysed with TShark, Cisco three-VLAN reference configuration drafts, a Python service desk metrics report, and validation for five CSV registers. |

## Service Desk Metrics

The reporting script calculates metrics from the project's **simulated incident dataset**:

| Metric | Sample result |
|---|---:|
| Mean Time to Resolve (17 resolved incidents) | **15.75 hours** |
| Non-escalated incident rate | **85% (17 of 20)** |
| SLA attainment for resolved incidents | **100% (17 of 17)** |
| SLA attainment at the portfolio snapshot | **85% (17 of 20)** |

The non-escalated rate is **not First Contact Resolution (FCR)**. These figures describe the sample data in this lab, not results from a real employer or production service desk.

## Run the Service Desk App

### Prerequisites
- Python 3.10 or later.
- Windows, Linux, or WSL2.
- Optional browser-test dependencies: install from `requirements-test.txt` and install the Playwright Chromium browser.

### Start the application

```powershell
python itsm/portal/app.py
```

Open:
- Customer portal: http://127.0.0.1:8080/portal
- Agent console: http://127.0.0.1:8080/agent

On first run, the app creates a local bootstrap credential file named `.local_credentials.json`. The file is excluded from Git. Read it locally with a trusted text editor when setting up the agent login; **do not share it or commit it**.

### Validate the sample data and run tests

```powershell
python scripts/validate-data.py
python -m unittest discover -s reporting/tests -v
python scripts/test_service_desk_platform.py
python reporting/report-generator.py --save all
```

### Run the Active Directory lab

The Samba lab requires Ubuntu on WSL2:

```powershell
python scripts/deploy_samba_ad.py
```

See the project documentation for setup details and environment requirements.

## Verification

The repository records these results from local lab runs:

| Check | Recorded result |
|---|---:|
| CSV register validation | **5 of 5 passed** |
| Reporting unit tests | **13 of 13 passed** |
| Service desk platform tests | **17 of 17 passed** |
| Samba AD / AGDLP checks | **5 of 5 passed** |
| Loopback packet-capture analysis | **Verified with TShark** |

These are local project checks; they are not results from a hosted production environment or a continuous-integration pipeline.

## Project Scope

This is a **self-directed learning project**, not a production ITSM deployment. The environment and records are fictional.

- **Active Directory:** The domain controller is Samba 4 running in WSL2, not Windows Server Active Directory Domain Services.
- **Microsoft 365:** The PowerShell script performs local client checks. It does not verify Outlook mailbox access, OneDrive file synchronisation, or Microsoft 365 tenant configuration.
- **ServiceNow and Jira:** The repository contains workflow and field-mapping documentation; it does not connect to live ServiceNow or Jira tenants.
- **Cisco networking:** The three-VLAN IOS files are reference configuration drafts. They have not been deployed on physical Cisco devices or validated in Packet Tracer.
- **Packet capture:** The included PCAP contains local Linux loopback traffic, not traffic captured from a physical office network.
- **Application:** The Python web app is intended for local demonstration and learning, not commercial or production use.

## Repository Structure

```text
itsm/                 Python service desk application
active-directory/     Samba AD design, setup and access-control material
windows-support/      Windows troubleshooting guides and 15 runbooks
microsoft-365/        Client-side Microsoft 365 support notes
networking/           Network notes and Cisco reference configurations
incidents/            Simulated incidents, requests, problems and changes
knowledge-base/       Support knowledge articles
asset-management/     Sample asset inventory and ITAM notes
reporting/            Python metrics generator and unit tests
evidence/             Test outputs and packet-capture evidence
docs/                 Architecture, setup, scope and walkthrough guides
scripts/              Deployment, validation and diagnostic scripts
```

For a deeper technical explanation, see the [project walkthrough](docs/project-walkthrough.md) and [project scope](docs/project-scope.md).
