# Project Overview

## Background & Objective

This project is an independent practical learning laboratory built to develop and demonstrate core competencies required for entry-level IT Support Engineer (L1), Service Desk Analyst, Desktop Support, and Application Support positions.

Entry-level IT support roles require practical familiarity with tools, processes, and systematic troubleshooting methodologies that are difficult to learn from theory alone:
- Logging, triaging, and managing tickets through an ITSM lifecycle.
- Diagnosing Windows endpoint, network connectivity, printing, and account access issues.
- Administering Active Directory user accounts, security groups, and permissions.
- Understanding ITIL v4 operational frameworks (incident, request, problem, change, and SLA governance).
- Writing clear, actionable knowledge base articles and professional user communications.

This laboratory provides an end-to-end simulated environment to practice these workflows hands-on.

---

## What This Project Is

The lab is modeled around **Nexora Technologies**, a fictional company with approximately 25 employees across 4 operational departments (Engineering, Finance, HR, Operations).

The fictional company provides authentic business context:
- Instead of abstract exercises, support tasks involve specific users and realistic constraints (e.g., "Finance user cannot access the monthly cheque printer", "Engineering developer needs Python environment deployed", "Executive locked out of domain account").
- Incidents, service requests, problem investigations, and standard maintenance changes are tracked with realistic timestamps, priority calculations, and resolution histories.

---

## Core Competencies & Modules

### 1. IT Service Desk Operations (`itsm/portal/app.py`)
A self-contained Python web application with SQLite backend providing:
- **Customer Portal (`/portal`):** Submit support requests, track status via unique ticket keys and customer tokens.
- **Agent Console (`/agent`):** Role-based access control (Admin, L1, L2, ReadOnly), queue filtering, status transitions, internal work notes, customer comments, and audit logging.
- **Priority & SLA Engine:** Dynamic priority calculation (Impact × Urgency matrix) and continuous elapsed-time SLA target tracking.

### 2. Active Directory Administration (`active-directory/`)
- User lifecycle management: onboarding, offboarding, account lockout resets, and password resets.
- Textbook AGDLP group nesting: Accounts $\rightarrow$ Global Groups (`GG-*`) $\rightarrow$ Domain Local Groups (`DL-*`) $\rightarrow$ Permissions.
- Isolated local Samba 4 Active Directory Domain Controller (`nexora.test`) deployed in WSL2 with Kerberos authentication and SMB share permissions testing.

### 3. Incident, Problem & Change Datasets (`incidents/`)
Canonical CSV registers tracking realistic organizational support volume:
- **Incident Register (20 records):** Break/fix events across hardware, software, network, printing, and access categories.
- **Service Request Register (8 records):** Standard fulfilled requests (software deployment, equipment requests, password resets).
- **Problem Records (3 records):** Root-cause investigations linking recurring incidents (VPN drops, license gaps, network instability).
- **Change Records (3 records):** Standard, normal, and emergency changes with risk assessments and backout plans.

### 4. Windows Endpoint Support & Runbooks (`windows-support/`)
Standard Operating Procedures (SOPs) and troubleshooting guides for common L1 desktop scenarios:
- Blue Screen (BSOD) crash triage and Event Viewer log inspection.
- Print spooler crashes and network printer offline troubleshooting.
- High CPU/RAM utilization triage and process management.
- Network adapter resets, DHCP renewals, and DNS cache flushes.

### 5. Network Fundamentals & Packet Inspection (`networking/`, `evidence/packet-captures/`)
- Office network topology design and subnet planning (VLAN 10 Corporate Users, VLAN 20 Server Farm, VLAN 99 Management).
- Cisco IOS router-on-a-stick and switch configuration reference drafts.
- Local loopback packet capture (`nexora-lab-traffic.pcap`) and forensic TShark CLI analysis covering DNS, ICMP, TCP 3-way handshakes, and HTTP transactions.

### 6. ITIL v4 Operational Policies (`itil-processes/`)
- Practical definitions for Incident, Request, Problem, and Change Management.
- Clear Escalation Matrix (L1 Service Desk $\rightarrow$ L2 Network / Desktop $\rightarrow$ L3 Systems / External Vendors).
- Continuous elapsed-time SLA policy with clear priority targets.

### 7. Reporting & Analytics (`reporting/`)
- Python reporting engine (`reporting/report-generator.py`) computing key support metrics (Mean Time to Resolve - MTTR, L1 Resolution Rate [Non-Escalated: 85.0%], resolved-ticket SLA attainment [100.0%], portfolio snapshot attainment [85.0%], category breakdown).
- Automated unit test suite (`reporting/tests/`) verifying mathematical accuracy and edge-case data handling.

---

## Live Demonstrable vs. Reference Components

To maintain strict truth-in-advertising:
- **Live Demonstrable:** Python Service Desk web application and SQLite database, automated test suites (17 platform tests, 13 reporting unit tests, 5 CSV dataset validators), reporting engine, Samba 4 AD DC in WSL2, and TShark packet analysis.
- **Documented Reference:** Enterprise SaaS mappings (ServiceNow, Jira Service Management), Cisco IOS configuration drafts, and Microsoft 365 client troubleshooting guides.
