# Live Interview Demonstration Runbook (10–15 Minute Walkthrough)
**Document ID:** INT-DEMO-001  
**Candidate:** Sameer H  
**Target Roles:** IT Support Engineer L1 / Service Desk Analyst / Technical Support Engineer  
**Objective:** A deterministic, defensible, step-by-step technical demonstration of the Nexora IT Operations Lab for technical interviewers.

---

## Demonstration Timeline & Checklist (12 Minutes Total)

```
[0:00 - 1:30]   Phase 1: Architectural Context & Honest Project Positioning
[1:30 - 4:00]   Phase 2: Live Service Desk Portal & Ticket Lifecycle (ITIL v4)
[4:00 - 6:30]   Phase 3: Active Directory Domain Controller & Security Groups (WSL2 Samba AD)
[6:30 - 8:30]   Phase 4: Network Packet Inspection & Wireshark Forensic Analysis
[8:30 - 10:30]  Phase 5: Windows 11 Diagnostics & Host System Automation
[10:30 - 12:00] Phase 6: Service Desk MIS Reporting Engine & Transparent Q&A
```

---

## Phase 1: Architectural Context (90 Seconds)
**Talking Point:**
> *"To prepare thoroughly for an L1 IT Support Engineer role, I wanted hands-on operational practice beyond textbook theory. I built this comprehensive operations lab simulating Nexora Technologies—a fictional 25-employee tech consulting firm with HR, Finance, Operations, Sales, and IT departments. The lab contains a deployed Samba 4 Active Directory Domain Controller with Kerberos, an interactive IT Service Desk platform running standard ITIL lifecycle workflows, live Wireshark packet captures, automated Python reporting, and 15 documented Windows troubleshooting runbooks tested right on my Windows 11 host."*

---

## Phase 2: Live Service Desk Portal & Ticket Lifecycle (2.5 Minutes)
**Action:**
1. Start the Service Desk web engine:
   ```bash
   python itsm/portal/app.py
   ```
2. Open browser to **`http://localhost:8080/portal`**. Show the 10 customer-facing request types.
3. Click **"Network Connectivity"** and submit a test ticket:
   - Caller: `Deepak Rao` (Finance)
   - Title: `Cannot reach intranet finance portal`
   - Impact: `High` | Urgency: `High` $\rightarrow$ Priority dynamically calculated as **P1 Critical**.
   - SLA Target: **4 Elapsed Clock Hours (24x7)**.
4. Switch to **`http://localhost:8080/agent`** (L1 Operator Console).
5. Select the newly generated ticket (`NEX-11`):
   - Click **"Start Work (Assign to Me)"** $\rightarrow$ Transitions to `In Progress`.
   - Add Internal Work Note: *"Ping to gateway 192.168.10.1 succeeded; inspecting Kerberos TGT token."*
   - Click **"Resolve Incident"** $\rightarrow$ Enter root cause and corrective action.
   - Show how the audit trail captures all transitions with author timestamps.

---

## Phase 3: Active Directory Domain Controller & Authentication (2.5 Minutes)
**Action:**
Demonstrate real domain administration inside WSL2 Ubuntu:
1. Show Domain Controller status:
   ```bash
   wsl -u root -d Ubuntu -e samba-tool domain level show
   ```
   *Expected Output:* Domain `DC=nexora,DC=test`, Forest Function Level Windows 2008 R2.
2. Show Domain Password & Lockout Policy:
   ```bash
   wsl -u root -d Ubuntu -e samba-tool domain passwordsettings show
   ```
   *Point out:* Complexity enabled, Lockout threshold 5 attempts, lockout duration 15 minutes.
3. Show 12 provisioned domain users across department OUs:
   ```bash
   wsl -u root -d Ubuntu -e samba-tool user list
   ```
4. Demonstrate Textbook AGDLP Group Nesting:
   ```bash
   wsl -u root -d Ubuntu -e samba-tool group listmembers DL-HR-Private-RW
   ```
   *Point out:* Shows Domain Local resource group `DL-HR-Private-RW` containing Global group `GG-HR` (textbook AGDLP nesting).
5. Demonstrate Kerberos ticket acquisition:
   ```bash
   wsl -u root -d Ubuntu -e bash -c "kinit alex.chen@NEXORA.TEST && klist"
   ```
   *Point out:* Principal `alex.chen@NEXORA.TEST`, Service Principal `krbtgt/NEXORA.TEST@NEXORA.TEST`.
6. Demonstrate Access Control on SMB Shares:
   - Authorized user `alex.chen` lists `//localhost/CompanyShared` $\rightarrow$ Access Granted.
   - Unauthorized user `deepak.rao` attempts `//localhost/HR-Private` $\rightarrow$ `NT_STATUS_ACCESS_DENIED`.

---

## Phase 4: Network Packet Inspection & Wireshark Analysis (2 Minutes)
**Action:**
1. Open [`evidence/packet-captures/packet-analysis-report.md`](../evidence/packet-captures/packet-analysis-report.md) and highlight [`evidence/packet-captures/nexora-lab-traffic.pcap`](../evidence/packet-captures/nexora-lab-traffic.pcap).
2. Explain the 3-Way Handshake captured during the local test transaction:
   - `SYN` (`tcp.flags.syn == 1 && tcp.flags.ack == 0`)
   - `SYN-ACK` (`tcp.flags.syn == 1 && tcp.flags.ack == 1`)
   - `ACK` (`tcp.flags.ack == 1`)
3. Explain the DNS NXDOMAIN packet capture:
   - Filter `dns.flags.rcode != 0` isolates RFC 1035 Code 3 (`Name Error`), demonstrating how an L1 technician diagnoses whether an address failure is an unresolvable hostname vs an unresponsive DNS server.

---

## Phase 5: Windows 11 Diagnostics & Runbooks (2 Minutes)
**Action:**
Demonstrate practical PowerShell diagnostic commands on the host:
1. Uptime & Fast Startup check:
   ```powershell
   Get-CimInstance Win32_OperatingSystem | Select-Object LastBootUpTime, @{N="UptimeDays";E={[math]::Round(((Get-Date) - $_.LastBootUpTime).TotalDays, 1)}}
   ```
   *Talking Point:* Explain Fast Startup hibernating kernel session and driver pool to `hiberfil.sys`, and why cold reboots (`shutdown /r /t 0`) are necessary to resolve persistent driver latency.
2. High CPU / Top Process triage:
   ```powershell
   Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 ProcessName, Id, CPU, Handles
   ```
   *Talking Point:* Explain why technicians terminate process trees rather than individual worker threads, and how Resource Monitor's "Analyze Wait Chain" identifies deadlocks.

---

## Phase 6: Python MIS Reporting & Honest Limitations (1.5 Minutes)
**Action:**
1. Run the Python reporting engine:
   ```bash
   python reporting/report-generator.py --save all
   ```
2. Run the automated test suite:
   ```bash
   python -m unittest discover -s reporting/tests -v
   ```
   *Point out:* 13/13 unit tests passing, verifying duration math, 15.75h MTTR, and 85.0% sample SLA compliance.
3. Conclude with honest project limitations:
   - Nexora Technologies is a fictional organization created for practical skill demonstration.
   - All host commands, packet captures, Samba AD controllers, and Python utilities are real and reproducible on this machine.
   - External cloud platforms (ServiceNow, Jira) are documented with exact production-grade configuration schemas and field mappings.
