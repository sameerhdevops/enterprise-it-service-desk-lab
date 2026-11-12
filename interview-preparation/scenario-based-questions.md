# 10 Practical Scenario-Based Interview Runbooks
**Document ID:** INT-003  
**Audience:** Candidate Technical Interview Preparation  
**Format:** Scenario > Triage Strategy > Diagnostic Checks > Resolution > Ticket Note

---

## Scenario 1: "A user calls and says: 'My internet is completely down and I cannot work.'"
- **Initial Questions:** Is the computer on wired Ethernet or Wi-Fi? Are nearby colleagues also affected? Is the network icon a globe or monitor?
- **Investigation Sequence:**
  1. Run `ipconfig /all` to check IPv4 address.
  2. If `169.254.x.x` (APIPA): Run `ipconfig /release` and `ipconfig /renew`. Check switch port link.
  3. If valid IP (e.g., `192.168.10.45`): Ping default gateway `192.168.10.1`.
  4. Ping `8.8.8.8` to test WAN routing.
  5. Ping `www.google.com` to test DNS.
- **Resolution:** If ping to 8.8.8.8 works but names fail, flush DNS (`ipconfig /flushdns`) and set adapter DNS to automatic. If cable disconnected, reseat cable.
- **Ticket Documentation:** *"User reported loss of internet. Diagnosed APIPA address 169.254.88.12 due to disconnected patch cable. Reseated RJ-45 cable; renewed DHCP lease to 192.168.10.62. Verified internet and intranet access restored."*

---

## Scenario 2: "A user calls saying: 'My laptop is extremely slow, it takes 5 minutes to open Excel.'"
- **Initial Questions:** When did this start? Did the machine reboot recently? Any loud fan noise?
- **Investigation Sequence:**
  1. Open Task Manager (`Ctrl + Shift + Esc`). Check system uptime on Performance > CPU tab.
  2. Sort Processes tab by CPU and Memory. Identify rogue background processes.
  3. Check Drive C: free space in File Explorer (ensure > 15% free).
- **Resolution:** If uptime is 25 days, execute a clean reboot (`shutdown /r /t 0`). If memory is at 95% due to runaway Chrome/Teams process, terminate the thread and clear temp files (`cleanmgr.exe`).
- **Ticket Documentation:** *"Investigated slow laptop performance. Identified 22 days uptime with unreleased memory leaks. Ran Disk Cleanup (freed 6.4 GB) and rebooted system. CPU idle dropped from 88% to 4%; confirmed Excel opens in 3 seconds."*

---

## Scenario 3: "A user says: 'I clicked print 20 minutes ago and nothing is coming out of the printer.'"
- **Initial Questions:** Is this a shared network printer or USB desktop printer? Are other people able to print to it?
- **Investigation Sequence:**
  1. Check physical printer LCD for paper jam or out of toner messages.
  2. Ping printer IP address (`ping 192.168.10.25`).
  3. Open print queue on user workstation; check if status says "Offline" or "Paused".
  4. Check if a 500 MB document is stuck at the top of the queue blocking other jobs.
- **Resolution:** If queue is locked, restart Print Spooler service (`net stop spooler`), clear files in `C:\Windows\System32\spool\PRINTERS`, and restart spooler (`net start spooler`). Uncheck "Use Printer Offline".
- **Ticket Documentation:** *"Resolved printing blockage on Floor 2 HP MFD. Cleared corrupted spool file from user queue and restarted Spooler service. Re-sent test print; confirmed functional."*

---

## Scenario 4: "An employee calls from home: 'My password expired and I can't log in to my laptop.'"
- **Initial Questions:** Verify caller identity: Employee ID, manager name, department. Confirm they are on their home Wi-Fi.
- **Investigation Sequence:**
  1. Check Active Directory for user account status (`Get-ADUser -Identity <user> -Properties LockedOut, PasswordExpired`).
  2. If user is remote and offline, explain that changing password in AD won't update their laptop until the machine communicates with the domain controller.
- **Resolution:**
  - Instruct user to log in with their **OLD** cached password.
  - Once on Windows desktop, connect to corporate GlobalProtect VPN.
  - Press `Ctrl + Alt + Del` > **Change a password** to sync with Domain Controller live over the VPN tunnel.
- **Ticket Documentation:** *"Assisted remote employee with expired domain password. Verified identity via HR records. Guided user to log in via cached credentials, connect to corporate VPN, and synchronize new password with Domain Controller. Confirmed access restored."*

---

## Scenario 5: "A user reports: 'Outlook crashes every time I open it.'"
- **Initial Questions:** Did Outlook work earlier today? Does it crash immediately or show an error dialog?
- **Investigation Sequence:**
  1. Test Outlook in Safe Mode: `outlook.exe /safe`.
  2. Check Event Viewer Application log for Event ID 1000 and faulting module.
  3. Direct user to Outlook Web App (`outlook.office.com`) to confirm mailbox health.
- **Resolution:** If safe mode opens without crashing, go to File > Options > Add-ins > COM Add-ins and disable third-party add-ins (e.g., Adobe PDF add-in). If safe mode fails, recreate profile via Control Panel > Mail.
- **Ticket Documentation:** *"Troubleshot Outlook crash on launch. Event ID 1000 identified corrupted third-party PDF COM add-in. Disabled add-in in Safe Mode. Verified Outlook opens normally and sends/receives emails."*

---

## Scenario 6: "A remote engineer says: 'My GlobalProtect VPN drops every 10 minutes.'"
- **Initial Questions:** Are you connected via Wi-Fi or home Ethernet? Are video calls outside the VPN stable?
- **Investigation Sequence:**
  1. Check user home internet latency and speed (run `ping 8.8.8.8 -t`).
  2. Inspect VPN client settings: check gateway URL (`vpn.nexora.com`).
  3. Check MTU packet fragmentation during large transfers.
- **Resolution:** Switch VPN connection transport protocol in client settings from IPsec/UDP to **SSL/TCP** mode and lower MTU to 1400.
- **Ticket Documentation:** *"Addressed intermittent VPN disconnects for remote user. Home broadband confirmed healthy. Applied TCP fallback workaround in GlobalProtect to prevent MTU fragmentation. Escalated to L2 Network referencing PRB0001."*

---

## Scenario 7: "HR submits a ticket: 'New employee starting Monday. Needs full IT setup.'"
- **Procedure:**
  1. Check HR Service Request for approved department, job title, and manager.
  2. Create user account in Active Directory under the appropriate departmental OU (`OU=Finance,OU=Nexora-Users`).
  3. Assign role-based security groups (e.g., `DEPT-Finance`, `SHARE-Finance-ReadWrite`).
  4. Assign Microsoft 365 E3 license via Admin Center.
  5. Provision and image laptop from asset inventory with Windows 11 Enterprise.
  6. Update Asset Inventory: status to `Active`, assign serial number to employee name.
- **Ticket Documentation:** *"Fulfilled new hire IT onboarding for Naveen Kumar (HR). Created AD account nkumar, assigned M365 license, provisioned laptop NXT-AST-012, and verified first-logon password change policy. Handover form staged."*

---

## Scenario 8: "A user says: 'I cannot open the Finance shared drive \\nexfs01\finance; it says Access Denied.'"
- **Investigation Sequence:**
  1. Run `whoami /groups` on user workstation.
  2. Check if user belongs to `SHARE-Finance-ReadWrite` group.
  3. Check if user recently joined Finance or transferred departments.
- **Resolution:** Verify manager approval. Add user to the AD security group via ADUC. Run `klist purge` to refresh cached Kerberos tickets, and instruct user to sign out and log back in.
- **Ticket Documentation:** *"Resolved Access Denied on \\nexfs01\finance. User lacked group membership following departmental transfer. Verified manager approval and added user to SHARE-Finance-ReadWrite. Purged Kerberos tickets; confirmed read/write access restored."*

---

## Scenario 9: "A user says: 'No one can hear me in Microsoft Teams meetings.'"
- **Investigation Sequence:**
  1. Check physical hardware mute switch on headset cable.
  2. In Teams > Settings > Devices: check if correct microphone is selected. Click **Make a test call**.
  3. In Windows Settings > Privacy > Microphone: verify "Let desktop apps access your microphone" is ON.
  4. In `mmsys.cpl` > Recording > Microphone Properties > Advanced: uncheck "Allow applications to take exclusive control".
- **Resolution:** Select USB headset as default in Teams, grant Windows privacy permissions, and test audio playback.
- **Ticket Documentation:** *"Addressed Teams microphone failure. Root cause was Windows privacy setting blocking desktop apps from accessing microphone. Enabled microphone permissions and verified via Teams test call."*

---

## Scenario 10: "A user calls saying: 'My laptop won't turn on at all. The screen is completely black.'"
- **Investigation Sequence:**
  1. Check if charging LED lights up when AC adapter is plugged in.
  2. Test with a known-good power adapter and different wall outlet to rule out bad charger.
  3. Check if power button LED or caps lock LED blinks error diagnostic codes.
- **Resolution:** Perform a **hard reset / residual power drain**: Unplug AC adapter, hold the power button down continuously for 30–60 seconds to drain motherboard capacitors, reconnect power, and turn on. If motherboard is completely dead, issue a spare loaner laptop from inventory and log a vendor warranty RMA ticket.
- **Ticket Documentation:** *"Investigated laptop failure to power on. AC adapter verified functional. Performed 60-second capacitor drain without POST. Motherboard power circuit unresponsive. Issued spare loaner NXT-AST-015 and logged HP warranty case #HP-99214."*
