# Lab Environment Setup & Prerequisites

This document outlines the system requirements, software prerequisites, and architectural design choices for running and testing the IT Support & Service Desk Lab.

---

## 1. System Requirements

The lab is designed to run efficiently on standard consumer or office hardware without requiring dedicated enterprise servers or paid cloud subscriptions:

- **Host Operating System:** Windows 10 / 11 (64-bit). Linux and macOS can also run the core Python web application, reporting engine, and CSV validation scripts.
- **Memory (RAM):** 8 GB minimum recommended (16 GB provides ample headroom when running WSL2 and browser sessions simultaneously).
- **Storage:** ~1 GB of available disk space for the repository, SQLite databases, and virtual environment dependencies.
- **Privileges:** Standard user access is sufficient for running the core web portal and reporting scripts. Administrator privileges are required only when testing certain local Windows diagnostic runbooks or managing local firewall rules.

---

## 2. Software Prerequisites

### Core Application & Reporting (Zero External Dependencies)
- **Python 3.10 or higher:** Used for the Service Desk web application (`itsm/portal/app.py`), the reporting generator (`reporting/report-generator.py`), and dataset validation (`scripts/validate-data.py`).
- **Standard Library Only:** The production application and reporting engine use built-in Python standard library modules (`http.server`, `sqlite3`, `csv`, `json`, `datetime`, `urllib`, `hashlib`, `hmac`, `secrets`). No external `pip` packages are needed to run the service desk portal or generate reports.

### Automated Testing Suite (Optional Test Dependencies)
- **Playwright:** The browser UI integration test and stored-XSS verification gate (Module 14 in `scripts/test_service_desk_platform.py`) uses Playwright with headless Chromium.
- **Installation:**
  ```powershell
  pip install -r requirements-test.txt
  python -m playwright install chromium
  ```

### Active Directory & Packet Capture (WSL2 Prerequisites)
- **Windows Subsystem for Linux (WSL2):** Ubuntu 22.04 LTS or 24.04 LTS.
- **Samba 4 & Kerberos:** Used to host the isolated local Active Directory Domain Controller (`nexora.test`) via `scripts/deploy_samba_ad.py`.
- **Packet Analysis Tools:** `tcpdump` and `tshark` (Wireshark CLI) on Linux/WSL2 for capturing and analyzing local loopback protocol traffic.

### Windows Support & Troubleshooting
- **PowerShell 5.1 or PowerShell 7+:** Used for Windows endpoint support runbooks, local SAM user management labs, and client diagnostic scripts.

---

## 3. Architecture & Design Choices

### Why Lightweight Local Components Instead of Heavy Server VMs
In commercial enterprise environments, Active Directory runs on dedicated Windows Server virtual machines, and Service Desk platforms run on dedicated cloud SaaS instances (such as ServiceNow or Jira Service Management). For an independent learning lab, this project utilizes intentional, resource-conscious alternatives:

1. **Self-Contained Python Service Desk:** Built using native Python `http.server` and SQLite. This delivers a working, testable L1 ticket management platform with customer and agent portals, RBAC, SLA timers, and REST APIs without needing Docker containers or enterprise database servers.
2. **Samba 4 AD DC in WSL2:** Provides an authentic, standards-compliant Active Directory Domain Controller (`nexora.test`) supporting Kerberos authentication, LDAP queries, AGDLP group nesting, and SMB network shares while consuming a fraction of the RAM and CPU required by a full Windows Server VM.
3. **Reference Blueprints for Enterprise Platforms:** Workflows for enterprise platforms (ServiceNow, Jira Service Management, Cisco IOS router/switch configurations, Microsoft 365) are documented as comprehensive reference architectures and standard operating procedures.

---

## 4. Verification & Testing Quickstart

```powershell
# 1. Validate sample datasets (incidents, service requests, assets)
python scripts/validate-data.py

# 2. Run reporting calculation tests
python -m unittest discover -s reporting/tests -v

# 3. Generate Service Desk KPI summary reports
python reporting/report-generator.py --save all

# 4. Run automated platform integration tests
python scripts/test_service_desk_platform.py
```
