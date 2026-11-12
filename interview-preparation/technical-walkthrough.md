# 5 End-to-End Live Interview Demonstration Scripts
**Document ID:** INT-004  
**Audience:** Candidate Practical Demonstration Script  
**Purpose:** Use when an interviewer asks: *"Show me or walk me step-by-step through how you troubleshoot..."*

---

## Demonstration 1: Live Troubleshooting of "No Internet Connectivity"
**Interviewer Prompt:** *"A user calls you and says they lost all internet access. How do you troubleshoot this on the command line?"*

### Live Execution Script:
1. **Open Command Prompt / PowerShell:**
   ```cmd
   ipconfig /all
   ```
   - **Explain to interviewer:** *"First, I check `ipconfig /all`. I look at three critical fields: Is the IPv4 address a valid private IP like `192.168.10.45`, or did it fall back to an APIPA address (`169.254.x.x`)? An APIPA address indicates the client failed to obtain a DHCP lease; it does not immediately prove the DHCP server or switch is down. I investigate whether the network adapter driver is healthy, the DHCP Client service is running, the cable/Wi-Fi has a link, or if a VLAN misconfiguration or exhausted scope is preventing lease acquisition. Next, I check if the Default Gateway is populated."*
2. **Loopback Stack Verification:**
   ```cmd
   ping 127.0.0.1
   ```
   - **Explain to interviewer:** *"I ping `127.0.0.1` to confirm the local TCP/IP protocol software stack is functioning properly. Note that loopback testing never places packets on the wire, so it does not verify physical network adapter hardware or cable integrity."*
3. **Gateway Reachability (Local LAN Check):**
   ```cmd
   ping 192.168.10.1
   ```
   - **Explain to interviewer:** *"Next, I ping our local Default Gateway router. If this replies, it confirms Layer 3 reachability to our default gateway across the immediate link, though it does not prove every LAN switch, VLAN, or network component is completely healthy."*
4. **Public IP Routing (WAN Check):**
   ```cmd
   ping 8.8.8.8
   ```
   - **Explain to interviewer:** *"Then I ping a public IP address like Google's 8.8.8.8. A reply confirms ICMP packet routing out to that specific destination, although it does not guarantee that application-level protocols like HTTP, HTTPS, or web proxies are operational."*
5. **DNS Name Resolution Check:**
   ```cmd
   nslookup www.google.com
   ```
   - **Explain to interviewer:** *"Finally, I test DNS resolution. If pinging 8.8.8.8 works but `nslookup` or pinging google.com fails, the problem is DNS. Importantly, I test using Layer 7 tools like `nslookup` or PowerShell `Resolve-DnsName`, which issue actual DNS query packets (UDP/TCP 53), rather than just `Test-NetConnection -Port 53` which only checks Layer 4 TCP port reachability. I would run `ipconfig /flushdns` and verify the adapter points to our valid corporate DNS servers."*

---

## Demonstration 2: Investigating a Slow Windows Computer
**Interviewer Prompt:** *"An employee complains their laptop is sluggish and freezing. How do you investigate without guessing?"*

### Live Execution Script:
1. **System Uptime & Resource Triage:**
   - Press `Ctrl + Shift + Esc` to open Task Manager.
   - Click **Performance > CPU** tab.
   - **Explain to interviewer:** *"First, I check the 'Up time' clock. In Windows 10 and 11, Fast Startup logs off user sessions and hibernates the Windows kernel session and device-driver state to `hiberfil.sys`. A high uptime indicates the machine has not undergone a full boot cycle. However, high uptime does not automatically prove a memory leak. I review the real-time resource meters to determine whether CPU, Memory, or Disk is experiencing genuine resource exhaustion."*
2. **Locate Resource-Consuming Process:**
   - Switch to **Processes** tab and sort by CPU and Memory.
   - **Explain to interviewer:** *"If a user application like Chrome or Teams is consuming excessive CPU or RAM, I can gracefully terminate the process or end the process tree. In standard Task Manager and Resource Monitor, technicians terminate processes rather than individual threads. Ending a process risks losing unsaved user work, so I attempt graceful application shutdown first. If high CPU is caused by 'System Interrupts', that indicates hardware interrupt or driver DPC latency issues rather than a user application, which requires driver verification or hardware escalation."*
3. **Analyze Wait Chain in Resource Monitor:**
   - Run `resmon.exe` > CPU tab > right-click unresponsive process > **Analyze Wait Chain**.
   - **Explain to interviewer:** *"Analyze Wait Chain reveals if a process is waiting on another process or thread (such as a hung background service, RPC call, or print spooler hook). While Resource Monitor does not allow terminating individual sub-threads, ending the specific blocking parent process can release the application without losing user session state."*
4. **Disk Cleanup & Controlled Cold Restart:**
   ```powershell
   cleanmgr.exe /d c:
   shutdown /r /t 0
   ```
   - **Explain to interviewer:** *"I verify available disk space to ensure the virtual memory paging file can expand, and if a full refresh is needed, execute a cold restart (`shutdown /r /t 0`), which bypasses Fast Startup hybrid hibernation and performs a complete OS boot cycle."*

---

## Demonstration 3: Handling a Password Lockout & Access Incident
**Interviewer Prompt:** *"A user calls in saying their account is locked out and they need access immediately. Walk me through what you do."*

### Live Execution Script:
1. **Mandatory Identity Verification:**
   - **Explain to interviewer:** *"Before touching Active Directory, I must verify the caller's identity to prevent social engineering. I confirm their Employee ID number and manager's name against the HR directory, or call them back on their registered corporate telephone number."*
2. **Inspect and Unlock Account via PowerShell / ADUC:**
   ```powershell
   Get-ADUser -Identity "kmurthy" -Properties LockedOut, BadLogonCount
   Unlock-ADAccount -Identity "kmurthy"
   ```
   - **Explain to interviewer:** *"In Active Directory Users and Computers or via PowerShell, I inspect the BadLogonCount and unlock the account. If they forgot their password, I set a temporary compliant password and enforce 'User must change password at next logon'."*
3. **Investigate Recurrent Lockouts:**
   - **Explain to interviewer:** *"If the account locks out repeatedly, I perform event correlation. On the Domain Controller Security log, I inspect Event ID 4740 ('A user account was locked out') to identify the 'Caller Computer Name'. (While the PDC Emulator is a common focal point, Event 4740 can be logged on any DC that processed the lockout). Once the source workstation or device is identified, I inspect Event ID 4625 ('An account failed to log on') on that source device. Logon Type 3 indicates network logon, which could stem from a mapped drive, an expired Wi-Fi credential, or a background service. Correlating the timestamp, calling process, and credential manager entries allows isolating the exact root cause."*

---

## Demonstration 4: ServiceNow Incident Lifecycle Walkthrough
**Interviewer Prompt:** *"Walk me through the complete lifecycle of a ticket in ServiceNow from creation to closure."*

### Walkthrough Script:
1. **Intake & Logging (State: New [1]):**
   - *"The ticket enters ServiceNow via user portal, email, or direct L1 call logging. I enter the Caller, which auto-populates their department, location, and assigned asset CIs."*
2. **Categorization & Priority Matrix:**
   - *"I select Category: Software, Subcategory: Outlook. I select Impact: 2-Medium and Urgency: 2-Medium. In our simulated Nexora ServiceNow configuration, Data Lookup rules calculate Priority: 3-Moderate (72 elapsed clock hours). Note that priority calculation matrices and SLA timers are company-specific configurations, not universal platform defaults."*
3. **Investigation & Work (State: In Progress [2]):**
   - *"I assign the ticket to `L1 Service Desk` and set `Assigned to: Nexora L1 Support Agent`. As I troubleshoot, I log technical logs in **Work Notes** (visible only to ITIL staff) and communicate with the user via **Additional Comments** (visible to the user)."*
4. **Resolution (State: Resolved [6]):**
   - *"Once verified, I select Resolution Code: 'Solved (Permanently)' and document detailed resolution steps in Resolution Notes. An automated resolution notification is dispatched to the user."*
5. **Closure (State: Closed [7]):**
   - *"In our simulated Nexora environment, if the user confirms resolution or 5 business days elapse without response, the system transitions the incident to Closed, making it read-only for audit compliance. (Auto-close duration and transition logic depend on individual enterprise business rules)."*

---

## Demonstration 5: Diagnosing a "Printer Offline" Incident
**Interviewer Prompt:** *"A user says their network printer is offline and nothing prints. How do you solve this?"*

### Live Execution Script:
1. **Network Reachability & Protocol Verification:**
   ```powershell
   Test-NetConnection -ComputerName 192.168.10.25 -Port 9100
   ```
   - **Explain to interviewer:** *"I test network connectivity to the printer. While TCP 9100 is standard for RAW printing, other protocols such as WSD, LPR (port 515), or IPP (port 631) may be used depending on the printer environment. A successful port test confirms Layer 4 reachability, but does not prove complete printer health (such as paper jams, depleted toner, or paused print engine). I also check whether the queue is mapped locally or hosted on a shared corporate print server (`\\NEX-PRN01`). If hosted on a print server, queue modifications require proper authorization and user coordination."*
2. **Inspect Windows Queue Settings:**
   - Open `control printers` > double-click printer queue.
   - **Explain to interviewer:** *"In the Printer menu, I verify that 'Use Printer Offline' and 'Pause Printing' are both unchecked."*
3. **Inspect Port Configuration (WSD vs TCP/IP):**
   - In Printer Properties > Ports tab.
   - **Explain to interviewer:** *"If a printer configured via WSD frequently drops offline due to network sleep states, I verify network discovery and evaluate switching to a Standard TCP/IP Port bound to the printer's static IP. However, I diagnose the root cause rather than changing ports arbitrarily."*
4. **Clear Spooler Queue Safely & Send Test Page:**
   ```powershell
   Stop-Service -Name Spooler -Force
   Remove-Item -Path "C:\Windows\System32\spool\PRINTERS\*" -Force
   Start-Service -Name Spooler
   ```
   - **Explain to interviewer:** *"If print jobs are stuck in 'Deleting...', I notify the user that pending unprinted documents will be cleared. I stop the Print Spooler service first to release locks on `.SPL` (raw print data) and `.SHD` (shadow job header) files in `C:\Windows\System32\spool\PRINTERS`, purge the directory, restart the service, and print a test page to verify end-to-end operation."*
