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
   - **Explain to interviewer:** *"First, I check `ipconfig /all`. I look at three critical fields: Is the IPv4 address a valid private IP like `192.168.10.45`, or did it fall back to an APIPA address like `169.254.x.x`? If it's APIPA, I know immediately the DHCP server or switch port is down. Next, I check if the Default Gateway is present."*
2. **Loopback Stack Verification:**
   ```cmd
   ping 127.0.0.1
   ```
   - **Explain to interviewer:** *"I ping the loopback address to ensure the operating system's TCP/IP protocol stack is working and the network card driver hasn't crashed."*
3. **Gateway Reachability (Local LAN Check):**
   ```cmd
   ping 192.168.10.1
   ```
   - **Explain to interviewer:** *"Next, I ping our local Default Gateway router. If this succeeds, it proves the physical Ethernet cable, local switch port, and local LAN are 100% operational."*
4. **Public IP Routing (WAN Check):**
   ```cmd
   ping 8.8.8.8
   ```
   - **Explain to interviewer:** *"Then I ping a public IP address like Google's 8.8.8.8. If this replies, our ISP WAN uplink and router NAT are working."*
5. **DNS Name Resolution Check:**
   ```cmd
   nslookup www.google.com
   ```
   - **Explain to interviewer:** *"Finally, I test DNS resolution. If pinging 8.8.8.8 works but `nslookup` or pinging google.com fails, the problem is strictly DNS. I would run `ipconfig /flushdns` and verify the adapter points to our corporate DNS server `192.168.20.10`."*

---

## Demonstration 2: Investigating a Slow Windows Computer
**Interviewer Prompt:** *"An employee complains their laptop is sluggish and freezing. How do you investigate without guessing?"*

### Live Execution Script:
1. **System Uptime & Resource Triage:**
   - Press `Ctrl + Shift + Esc` to open Task Manager.
   - Click **Performance > CPU** tab.
   - **Explain to interviewer:** *"First, I look at the 'Up time' clock. If it shows 25 days, I know Fast Startup has preserved memory leaks across shutdowns. Next, I look at the top graphs: is CPU at 100%, Memory at 95%, or Disk pinned at 100%? That immediately narrows my investigation."*
2. **Locate Resource Hogging Process:**
   - Switch to **Processes** tab and sort by CPU and Memory.
   - **Explain to interviewer:** *"If a user application like Chrome has 30 sub-processes or Teams is holding 4 GB of RAM, I can terminate that specific thread. If high CPU is caused by 'System Interrupts', I know it's a hardware driver or bad USB peripheral firing excessive interrupts."*
3. **Analyze Wait Chain in Resource Monitor:**
   - Run `resmon.exe` > CPU tab > right-click unresponsive process > **Analyze Wait Chain**.
   - **Explain to interviewer:** *"Rather than killing an unresponsive application and losing unsaved work, I check the Wait Chain. Often the app is just blocked waiting for an offline network printer or stuck antivirus hook. If I terminate only that blocking sub-thread, the application unfreezes immediately."*
4. **Disk Cleanup & Clean Reboot:**
   ```powershell
   cleanmgr.exe /d c:
   shutdown /r /t 0
   ```
   - **Explain to interviewer:** *"I clear temporary caches to ensure the virtual memory paging file can expand, and perform a full reboot."*

---

## Demonstration 3: Handling a Password Lockout & Access Incident
**Interviewer Prompt:** *"A user calls in saying their account is locked out and they need access immediately. Walk me through what you do."*

### Live Execution Script:
1. **Mandatory Identity Verification:**
   - **Explain to interviewer:** *"Before touching Active Directory, I must verify the caller's identity to prevent social engineering. I ask for their Employee ID number and manager's name and cross-reference our HR directory, or call them back on their registered corporate phone number."*
2. **Inspect and Unlock Account via PowerShell / ADUC:**
   ```powershell
   Get-ADUser -Identity "kmurthy" -Properties LockedOut, BadLogonCount
   Unlock-ADAccount -Identity "kmurthy"
   ```
   - **Explain to interviewer:** *"In Active Directory Users and Computers or via PowerShell, I inspect the BadLogonCount. I unlock the account. If they forgot their password, I set a temporary compliant password and enforce 'User must change password at next logon'."*
3. **Investigate Recurrent Lockouts:**
   - **Explain to interviewer:** *"If the account locks out again within 15 minutes, I know a mobile phone, tablet, or mapped network drive is continually transmitting an old cached password. I have the user disconnect Wi-Fi on their phone, check Event ID 4740 on the Domain Controller to find the Caller Computer Name, and update the stored credentials."*

---

## Demonstration 4: ServiceNow Incident Lifecycle Walkthrough
**Interviewer Prompt:** *"Walk me through the complete lifecycle of a ticket in ServiceNow from creation to closure."*

### Walkthrough Script:
1. **Intake & Logging (State: New [1]):**
   - *"The ticket enters ServiceNow via user portal, email, or direct L1 call logging. I enter the Caller, which auto-populates their department, location, and assigned asset CIs."*
2. **Categorization & Priority Matrix:**
   - *"I select Category: Software, Subcategory: Outlook. I select Impact: 2-Medium and Urgency: 2-Medium. The platform's Data Lookup rules automatically calculate Priority: 3-Moderate, which sets our resolution SLA timer to 3 business days."*
3. **Investigation & Work (State: In Progress [2]):**
   - *"I assign the ticket to `L1 Service Desk` and set `Assigned to: Sameer Kulkarni`. As I troubleshoot, I log technical logs in **Work Notes** (visible only to ITIL staff) and communicate with the user via **Additional Comments** (visible to the user)."*
4. **Resolution (State: Resolved [6]):**
   - *"Once verified, I select Resolution Code: 'Solved (Permanently)' and document detailed resolution steps in Resolution Notes. An automated resolution email is dispatched to the user."*
5. **Closure (State: Closed [7]):**
   - *"If the user confirms resolution or 5 business days elapse with no response, the system transitions the incident to Closed, making it read-only for audit compliance."*

---

## Demonstration 5: Diagnosing a "Printer Offline" Incident
**Interviewer Prompt:** *"A user says their network printer is offline and nothing prints. How do you solve this?"*

### Live Execution Script:
1. **Physical & Network Reachability Check:**
   ```powershell
   Test-NetConnection -ComputerName 192.168.10.25 -Port 9100
   ```
   - **Explain to interviewer:** *"First, I check if the printer is pingable and whether RAW port 9100 is listening. If port 9100 responds, the physical printer and network switch port are healthy; the issue is on the Windows client side."*
2. **Inspect Windows Queue Settings:**
   - Open `control printers` > double-click printer queue.
   - **Explain to interviewer:** *"In the Printer menu, I verify that 'Use Printer Offline' and 'Pause Printing' are both unchecked."*
3. **Inspect Port Configuration (WSD vs TCP/IP):**
   - In Printer Properties > Ports tab.
   - **Explain to interviewer:** *"If Windows configured the printer on a WSD (Web Services for Devices) port, it often goes offline when the printer sleeps. I switch the port to a Standard TCP/IP Port bound to static IP `192.168.10.25`."*
4. **Restart Print Spooler & Send Test Page:**
   ```powershell
   Restart-Service -Name Spooler -Force
   ```
   - Print Windows Test page; verify job clears and physically prints.
