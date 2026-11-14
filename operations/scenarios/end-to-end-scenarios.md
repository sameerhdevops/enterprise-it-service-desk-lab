# End-to-End Enterprise Support Scenarios & Operational Validation
**Document ID:** OPS-E2E-001  
**Organization:** Nexora Technologies IT Service Desk  
**Target Roles:** IT Support Engineer L1 / Service Desk Analyst / Desktop Support  
**Environment:** Live Operational IT Service Desk (`itsm/portal/app.py`), Samba 4 AD DC (`NEXORA.TEST`), Wireshark Capture Engine (`evidence/packet-captures/`), Windows 11 Diagnostics  

---

## Overview

This document demonstrates the practical execution of six core IT support operational scenarios. Each scenario follows the full ITIL v4 lifecycle: **Logging $\rightarrow$ Triage & Prioritization $\rightarrow$ Investigation $\rightarrow$ Remediation $\rightarrow$ Verification $\rightarrow$ Closure $\rightarrow$ Documentation**.

---

## Scenario 1: Domain Account Lockout & Password Recovery
- **Ticket Identifier:** `NEX-101`
- **Request Type:** `Password Reset / Account Unlock`
- **Caller:** Kavitha Murthy (HR Specialist)
- **Reported Issue:** *"Cannot log into workstation after weekend password reset. Account reports: 'The referenced account is currently locked out and may not be logged on to'."*
- **Triage & Priority:** Impact: Medium (Single user, HR blocked) | Urgency: High (Payroll deadline) $\rightarrow$ **Priority: P2 (Target: 8 Elapsed Hours)**

### Step-by-Step Resolution:
1. **Identity Verification:**
   - Analyst calls Kavitha back on registered mobile number. Confirms Employee ID (`NXT-EMP-004`) and manager name (`Rajesh Bhat`).
2. **Domain Controller Investigation (Samba AD):**
   ```bash
   samba-tool user getpasswordusagestats kavitha.murthy
   # Observed: Bad password count exceeded threshold (5 attempts)
   ```
3. **Forensic Event Correlation:**
   - Event ID 4740 identified caller device NetBIOS `NXT-W10-004` (Caller Workstation) and mobile device attempting ActiveSync connection with expired cached credentials.
4. **Account Unlock & Temporary Password Reset:**
   ```bash
   samba-tool user setpassword kavitha.murthy --newpassword='NexoraTemp@2026!' --must-change-at-next-login
   ```
5. **Client-Side Remediation:**
   - Instructed user to update corporate Wi-Fi and Outlook password on smartphone to prevent recurring lockout.
6. **Ticket Activity Logged:**
   - Work note added in Service Desk portal; ticket transitioned from `In Progress` to `Resolved`.

---

## Scenario 2: Network Connectivity & Port Reachability Failure
- **Ticket Identifier:** `NEX-103`
- **Request Type:** `Network Connectivity`
- **Caller:** Deepak Rao (Financial Controller)
- **Reported Issue:** *"Cannot access the shared finance volume (\\nexfs01\finance) or browse intranet services. Getting 'Network path was not found'."*
- **Triage & Priority:** Impact: High (Finance team shared volume) | Urgency: High (Month-end close) $\rightarrow$ **Priority: P1 (Target: 4 Elapsed Hours)**

### Step-by-Step Resolution:
1. **Layer 1 through Layer 3 Bottom-Up Triage:**
   - Physical check: Link light solid green on RJ-45 jack.
   - Run `ipconfig /all`: Client has valid IP `192.168.10.45` on VLAN 10. Default gateway `192.168.10.1` replies in <1ms.
2. **Layer 4 & Layer 7 Protocol Diagnostics:**
   - Run PowerShell port test to Domain Controller / File Server:
     ```powershell
     Test-NetConnection -ComputerName "192.168.20.10" -Port 445
     Test-NetConnection -ComputerName "192.168.20.10" -Port 389
     ```
   - Both TCP handshakes succeeded (`TcpTestSucceeded: True`).
3. **Kerberos Security Token Inspection:**
   - User was recently added to `SG-Finance-Access`, but their active Kerberos TGT lacked the new Group SID.
   - Ran `klist` on workstation; observed TGT issued prior to group modification.
4. **Remediation:**
   - Flushed stale Kerberos tickets:
     ```cmd
     klist purge
     gpupdate /force
     ```
5. **Packet Inspection Verification:**
   - Inspected Wireshark capture [`evidence/packet-captures/nexora-lab-traffic.pcap`](../../evidence/packet-captures/nexora-lab-traffic.pcap) using filter `tcp.port == 445` to verify SMB Negotiate and Tree Connect responses (`STATUS_SUCCESS`).
6. **Ticket Closure:** Resolved within 1.25 hours (well within 4h P1 SLA).

---

## Scenario 3: Print Spooler Queue Stall & Service Recovery
- **Ticket Identifier:** `NEX-107`
- **Request Type:** `Printer Issue`
- **Caller:** Kavitha Murthy (HR)
- **Reported Issue:** *"Floor 2 HR printer (HP LaserJet Enterprise) is showing 'Offline'. Multiple print jobs are stuck in queue and cannot be deleted."*
- **Triage & Priority:** Impact: Medium | Urgency: Medium $\rightarrow$ **Priority: P3 (Target: 72 Elapsed Hours)**

### Step-by-Step Resolution:
1. **Printer Reachability Check:**
   - Ran `ping 192.168.10.25` (Printer IP); confirmed network hardware is online with 0% packet loss.
   - Tested raw port 9100 listening state: `Test-NetConnection 192.168.10.25 -Port 9100`.
2. **Windows Print Spooler Triage on Client / Print Server:**
   - Inspected Print Spooler service state via PowerShell:
     ```powershell
     Get-Service -Name Spooler
     ```
   - Observed corrupt print job (`.SHD` / `.SPL`) blocking the spooler thread.
3. **Remediation Procedure (Automated L1 Runbook):**
   ```powershell
   Stop-Service -Name Spooler -Force
   Remove-Item -Path "$env:SystemRoot\System32\spool\PRINTERS\*" -Force
   Start-Service -Name Spooler
   Get-Service -Name Spooler
   ```
4. **Verification:**
   - Sent Windows test print page; confirmed page printed immediately.
   - Referenced self-help KB article `KB0010` (Printer Offline Troubleshooting) in ticket comments to caller.

---

## Scenario 4: Laptop Performance Degradation & Thermal Throttling
- **Ticket Identifier:** `NEX-108`
- **Request Type:** `Laptop Performance Issue`
- **Caller:** Arun Nair (Operations Manager)
- **Reported Issue:** *"Laptop fan running continuously at high speed. Excel freezes when switching worksheets, and mouse cursor stutters across screen."*
- **Triage & Priority:** Impact: Medium | Urgency: Medium $\rightarrow$ **Priority: P3 (Target: 72 Elapsed Hours)**

### Step-by-Step Resolution:
1. **Uptime & Fast Startup Investigation:**
   - Checked system uptime in PowerShell:
     ```powershell
     Get-CimInstance Win32_OperatingSystem | Select-Object LastBootUpTime
     ```
   - Discovered **34 days of continuous uptime**. The user shut down their laptop each evening, but Windows Fast Startup hibernated the kernel session and driver pool across shutdowns.
2. **Resource Consumption Analysis:**
   - Sorted top CPU consumers via PowerShell:
     ```powershell
     Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 ProcessName, Id, CPU, Handles
     ```
   - Identified runaway browser renderer process (`chrome.exe` PID 14220) consuming 94% of CPU cycles due to an infinite JavaScript loop in an unclosed intranet reporting tab.
3. **Wait Chain Analysis:**
   - Opened Resource Monitor (`resmon.exe`) $\rightarrow$ CPU tab $\rightarrow$ Analyzed Wait Chain. Confirmed single process hung on socket I/O.
4. **Corrective Action:**
   - Terminated runaway process tree cleanly: `Stop-Process -Id 14220 -Force`.
   - Executed a complete cold reboot bypassing Fast Startup: `shutdown /r /t 0`.
5. **Verification:**
   - Upon reboot, CPU idle utilization dropped to 4%, fan returned to whisper-quiet operation, and Excel opened in <2 seconds.

---

## Scenario 5: Microsoft 365 Client Outlook & Teams Glitch
- **Ticket Identifier:** `NEX-102`
- **Request Type:** `Microsoft 365 Client Issue`
- **Caller:** Deepak Rao (Finance)
- **Reported Issue:** *"Outlook is permanently stuck on the splash screen saying 'Loading Profile...'. Microsoft Teams is also not displaying updated channel messages."*
- **Triage & Priority:** Impact: Medium | Urgency: Medium $\rightarrow$ **Priority: P3 (Target: 72 Elapsed Hours)**

### Step-by-Step Resolution:
1. **Outlook Safe Mode Test:**
   - Executed `outlook.exe /safe` $\rightarrow$ Outlook launched successfully, confirming a third-party COM Add-in or corrupted profile was the root cause.
2. **Endpoint Connectivity Verification:**
   - Verified M365 cloud endpoints using `scripts/m365-client-diag.ps1`:
     - `login.microsoftonline.com:443` $\rightarrow$ SUCCESS
     - `outlook.office.com:443` $\rightarrow$ SUCCESS
     - `teams.microsoft.com:443` $\rightarrow$ SUCCESS
3. **Teams Client Cache Reset:**
   - Terminated Teams processes and purged the local MSIX package cache:
     ```powershell
     Stop-Process -Name "ms-teams" -Force -ErrorAction SilentlyContinue
     Remove-Item -Path "$env:LOCALAPPDATA\Packages\MSTeams_8wekyb3d8bbwe\LocalCache\*" -Recurse -Force
     ```
4. **Outlook OST Reconstruction:**
   - Closed Outlook, navigated to `%LOCALAPPDATA%\Microsoft\Outlook`, renamed corrupt `deepak.rao@nexora.com.ost` to `.old`, and launched Outlook.
   - Outlook re-synced the full mailbox cleanly from Exchange Online in under 10 minutes.

---

## Scenario 6: New Employee IT Onboarding & Access Provisioning
- **Ticket Identifier:** `NEX-110`
- **Request Type:** `New User Access`
- **Requester:** Rajesh Bhat (Head of IT Operations)
- **Employee Details:** Vikram Seth (Full-Stack Engineer, Engineering Dept)
- **Triage & Priority:** Impact: Low (Single new hire) | Urgency: High (Starting Monday) $\rightarrow$ **Priority: P3 (Target: 72 Elapsed Hours)**

### Step-by-Step Provisioning:
1. **Domain User Provisioning (Samba AD DC):**
   ```bash
   samba-tool user create vikram.seth 'NexoraTemp@2026!' \
       --given-name="Vikram" \
       --surname="Seth" \
       --job-title="Full-Stack Engineer" \
       --userou="OU=Engineering"
   ```
2. **Security Group Assignment (AGDLP Framework):**
   ```bash
   # Add to Corporate Baseline & Engineering Groups
   samba-tool group addmembers SG-All-Staff vikram.seth
   samba-tool group addmembers SG-VPN-Users vikram.seth
   ```
3. **Hardware Asset Allocation:**
   - Allocated spare laptop `NXT-AST-015` (Dell Latitude 5420, Serial: `DELL-5420-99015`) from asset inventory.
   - Updated `asset-management/asset-inventory.csv`: Set `AssignedTo: Vikram Seth`, `Status: Deployed`.
4. **Welcome Communication:**
   - Sent automated welcome email containing temporary credentials, workstation setup steps, and SSPR registration instructions using Email Template 8 (`communication/email-templates.md`).
5. **Ticket Closure:** Marked resolved upon confirmed employee first-day logon.
