# Design Decisions

Technical choices made for this lab and why. Each decision is driven by what is realistic for L1 support, reproducible on standard hardware, and achievable with zero software licensing costs.

## ITSM Platform Strategy: Interactive Portal + Enterprise Blueprints

**Decision**: Build and run a local interactive Python Service Desk portal (`itsm/portal/app.py`), complemented by documented reference blueprints for ServiceNow and Jira Service Management.

**Why a local portal?**

- **Zero Cost & Always Available**: Cloud developer instances (like ServiceNow PDI) sleep or reset after inactivity, requiring re-registration and internet access. A local portal running on `localhost:8080` starts instantly, never expires, and costs ₹0.
- **Deep Technical Understanding**: Building the ticketing portal from scratch using Python's standard library (`http.server` + `sqlite3`) required directly implementing core ITIL concepts:
  - 3×3 priority matrix mapping Impact and Urgency to P1–P4.
  - Strict lifecycle state machine (New → Assigned → In Progress → Waiting for Customer → Resolved → Closed).
  - 10 operational queues for technician triage.
  - Dual-perspective commenting (public customer updates vs. private agent work notes).
  - Web security fundamentals: PBKDF2 password hashing, session cookies (`HttpOnly`, `SameSite=Strict`), Origin/Referer same-origin validation (scheme, hostname, and port), and stored XSS defense.

**Why document ServiceNow and Jira SM?**

Job postings for L1 support roles frequently mention ServiceNow or Jira. Documenting their field dictionaries, request types, SLA timers, and configuration steps in `itsm/` ensures familiarity with the exact terminology, choice lists, and workflows used by commercial enterprise platforms.

## Active Directory: Samba 4 AD DC in WSL2

**Decision**: Deploy an isolated Samba 4 Active Directory Domain Controller for realm `nexora.test` inside WSL2 Ubuntu, combined with practical Windows administrative runbooks.

**Why Samba 4 in WSL2 instead of a Windows Server GUI VM?**

- **Resource Efficiency**: A full Windows Server GUI virtual machine requires substantial dedicated CPU and RAM, which can slow down a workstation. WSL2 runs natively on Windows with minimal overhead.
- **Real Enterprise Protocols**: Samba 4 is a production-grade, protocol-compatible Active Directory Domain Controller. It provides:
  - Real Kerberos KDC for ticket granting ticket (TGT) acquisition and inspection via `kinit` and `klist`.
  - Real LDAP directory for user, group, and organizational unit (OU) queries.
  - Textbook AGDLP group nesting: Accounts → Global Groups (`GG-*`) → Domain Local Groups (`DL-*`) → Permissions.
  - Real SMB share permission controls (`CompanyShared`, `Finance-Private`, `HR-Private`, `IT-Admin`).
- **Standard Operating Runbooks**: For Windows-specific GUI administration (Active Directory Users and Computers, Group Policy Management Console), step-by-step administrative runbooks are maintained in `active-directory/`.

## Data Storage: SQLite for Interactive App, CSV for Datasets & Reporting

**Decision**: Use SQLite for the live Service Desk application, and canonical CSV files for sample incident registers, asset tracking, and reporting.

**Why this division?**

- **SQLite for the Web Portal (`nexora_servicedesk.db`)**: An interactive ticketing system requires relational ACID transactions, foreign keys, auto-incrementing IDs, and concurrency-safe status updates. SQLite provides all of this natively in the Python standard library with zero server installation.
- **CSV for Datasets & Reporting (`incidents/`, `asset-management/`)**:
  - Transparent & Human-Readable: Anyone viewing the GitHub repository can inspect the raw data directly in a browser or spreadsheet.
  - Git-Friendly: Text-based CSV files diff line-by-line cleanly across commits.
  - Python Standard Library Processing: The reporting script (`reporting/report-generator.py`) and validator (`scripts/validate-data.py`) process CSVs directly using Python's built-in `csv` module, demonstrating raw data handling without heavy third-party libraries.

## Python Standard Library Only (Zero Pip Dependencies)

**Decision**: The core lab functionality requires zero external pip packages. All scripts rely exclusively on the Python 3 standard library (`http.server`, `sqlite3`, `csv`, `json`, `hashlib`, `unittest`).

**Why?**

- **Zero Setup Friction**: Clone the repository and run the scripts immediately. No `pip install`, no virtual environment configuration, and no dependency breakages.
- **Demonstrates Core Competence**: Writing reporting logic, state machines, and validation scripts with standard library modules proves genuine understanding of the underlying logic rather than relying on high-level abstractions like `pandas.DataFrame`.
- **Testing Separation**: Automated browser verification uses Playwright, but this is isolated in `requirements-test.txt` and is not required for running the core lab, reports, or validation.

## Networking: Cisco IOS Config Drafts & Loopback Packet Analysis

**Decision**: Author syntax-accurate Cisco 2911 router and 2960 switch configuration drafts (`.ios`) and Packet Tracer lab guides, combined with a 20-frame loopback packet capture (`.pcap`) analyzed using TShark.

**Why?**

- **Reference Design Files**: Real enterprise Cisco hardware is impractical for a home lab. Packet Tracer topology guides and `.ios` configuration drafts allow studying VLAN trunking (802.1Q), router-on-a-stick, DHCP exclusion pools, and default gateway configurations.
- **Empirical Packet Analysis**: The 20-frame packet capture (`evidence/packet-captures/nexora-lab-traffic.pcap`) captures local loopback traffic to demonstrate real network protocol inspection (TCP 3-way handshake, DNS query/response, ICMP) using `tshark` display filters, without falsely claiming access to physical corporate switch cabling.

## Markdown for Documentation

**Decision**: All operational documentation, runbooks, and policies are authored in GitHub Flavored Markdown (`.md`).

**Why?**

- **Version Control**: Markdown diffs cleanly in Git, tracking every procedural update and technical correction.
- **Portability**: Renders cleanly in GitHub, VS Code, or any text viewer without proprietary office software.
- **Transferable Skill**: Modern IT organizations rely heavily on Markdown for internal knowledge bases, runbooks, and GitHub/GitLab documentation repositories.

## Git for Everything

**Decision**: The entire lab is managed in a single Git repository with clean commit history.

**Why?**

- **Evidence of Work**: The commit history shows real incremental development, technical corrections, and systematic verification.
- **Discipline**: Using Git branches, descriptive commit messages, and automated test checks reflects professional engineering habits expected in modern IT support roles.

## Directory Structure: By Function, Not by Tool

**Decision**: Top-level directories are organized by functional domain (`incidents/`, `knowledge-base/`, `windows-support/`, `active-directory/`, `networking/`) rather than by tool.

**Why?**

Real IT support work is organized around problems and services, not tools. When an engineer troubleshoots an issue, they diagnose the affected functional area using whatever tools are appropriate. Organizing by function makes the repository intuitive to navigate for any interviewer or support technician.
