# Professional Ticket Documentation & Comment Standards
**Document ID:** COM-CMT-001  
**Audience:** L1 Service Desk Analysts  
**Scope:** Customer-Facing Comments vs. Internal Technical Work Notes

---

## 1. Documentation Quality Standard

Every update logged on a service ticket must answer four standard questions:
1. **What was investigated or observed?**
2. **What technical diagnostic steps were executed?**
3. **What was the outcome?**
4. **What is the next planned step or customer expectation?**

---

## 2. 10 Representative Ticket Comment Pairs (Customer vs. Internal)

### Ticket 1: Laptop Not Powering On (INC0001)
- **Additional Comments (Customer Visible):**  
  *"Hello Kavitha, I have inspected your laptop in the IT room. The motherboard power controller has failed. We have requested an on-site warranty replacement from HP (Case #HP-99214). In the meantime, I have issued you spare laptop NXT-AST-015 so your work is not interrupted. I will notify you as soon as your primary laptop is repaired."*
- **Work Notes (Internal ITIL Only):**  
  *"Tested with known-good 65W HP Smart AC adapter. Power LED unresponsive. Executed 60-second static capacitor drain—no POST or fan spin. Inspected DC jack for physical damage; intact. Checked warranty in asset inventory: active until 2025-03-15. Contacted HP enterprise support; logged dispatch case #HP-99214 for motherboard replacement. Issued spare loaner NXT-AST-015. Updated asset register."*

---

### Ticket 2: Shared Folder Access Denied (INC0002)
- **Additional Comments (Customer Visible):**  
  *"Hello Meena, your permissions for the Finance shared folder have been verified and restored per approval from Rajesh Bhat. Please log off your computer and sign back in to apply the updated permissions."*
- **Work Notes (Internal ITIL Only):**  
  *"Checked `whoami /groups` via remote session; confirmed user lacked FIN-SharedDrive-RW SID following quarterly security group clean-up. Verified manager approval in HR portal. Executed: `Add-ADGroupMember -Identity 'SHARE-Finance-ReadWrite' -Members 'miyer'`. Ran `klist purge`. Instructed user to sign out and log back in to refresh Kerberos token."*

---

### Ticket 3: Outlook Repeated Crashes (INC0003)
- **Additional Comments (Customer Visible):**  
  *"Hi Akash, we identified an incompatible PDF add-in that was causing Outlook to crash on launch. We have disabled the add-in and repaired your Outlook profile. You should now be able to open Outlook normally."*
- **Work Notes (Internal ITIL Only):**  
  *"Event Viewer Application log showed Event ID 1000 with faulting module AdobePDF.dll. Launched `outlook.exe /safe` successfully. Navigated to File > Options > Add-ins > COM Add-ins; disabled Adobe PDF Maker plugin. Restarted Outlook normally. Confirmed 0 crashes over 10 minutes of active use."*

---

### Ticket 4: VPN Intermittent Drops (INC0004)
- **Additional Comments (Customer Visible):**  
  *"Hello Divya, we have temporarily updated your VPN connection protocol to TCP mode to stabilize your connection while our network team implements a firewall configuration update scheduled for this Saturday."*
- **Work Notes (Internal ITIL Only):**  
  *"User experiencing tunnel disconnects every 10–12 minutes on home ACT Fibernet broadband. Pings to gateway show packet fragmentation at 1500 bytes. Workaround applied: Changed GlobalProtect client protocol to SSL/TCP mode and set MTU to 1400. Connection stable for 45 minutes. Escalated ticket to L2 Network (Arvind Rao) referencing PRB0001 / CHG0002."*

---

### Ticket 5: Floor Printer Offline (INC0006)
- **Additional Comments (Customer Visible):**  
  *"Hi Arun, the Floor 2 HP printer connection has been refreshed. A test document was sent through and printed cleanly. You can now release your pending print jobs."*
- **Work Notes (Internal ITIL Only):**  
  *"Checked `Get-Printer`; printer status showed Offline on dynamic WSD port. Ping to 192.168.10.25 was responding. Re-bound printer to Standard TCP/IP Port (IP_192.168.10.25) on raw port 9100. Restarted Spooler service via PowerShell. Sent Windows test page; printed and cleared cleanly."*

---

### Ticket 6: Stuck Print Spooler (INC0007)
- **Additional Comments (Customer Visible):**  
  *"Hello Pooja, a corrupted 400 MB PDF document was blocking your print queue. We have cleared the stuck job and restarted the printer service. Printing is now fully functional."*
- **Work Notes (Internal ITIL Only):**  
  *"Spoolsv.exe crashing repeatedly due to damaged spool file. Stopped spooler service (`net stop spooler`), navigated to `C:\Windows\System32\spool\PRINTERS` and purged orphaned .SPL and .SHD files. Restarted spooler service. Verified queue empty and service running stably."*

---

### Ticket 7: Excel 'Not Responding' Hang (INC0008)
- **Additional Comments (Customer Visible):**  
  *"Hi Siddharth, your Excel workbook became unresponsive because it was waiting on a disconnected network printer. We cleared the blocked process and restored your spreadsheet without losing your open calculations."*
- **Work Notes (Internal ITIL Only):**  
  *"Opened Resource Monitor > CPU > Analyze Wait Chain on EXCEL.EXE (PID 8820). Excel was deadlocked waiting for 32-bit print driver component splwow64.exe. Terminated splwow64.exe thread. Excel window unfroze immediately; user saved file successfully."*

---

### Ticket 8: Slow PC with High Memory (INC0014)
- **Additional Comments (Customer Visible):**  
  *"Hello Ananya, we cleared accumulated background update temporary files and optimized your virtual memory settings. Your laptop has been restarted and should now perform smoothly."*
- **Work Notes (Internal ITIL Only):**  
  *"System uptime was 31 days with RAM committed at 96%. Fast Startup disabled. Ran cleanmgr to purge 9.2 GB of temp files from %temp% and SoftwareDistribution. Configured virtual memory paging file to System Managed. Executed shutdown /r /t 0. Verified idle RAM usage dropped to 41%."*

---

### Ticket 9: Account Lockout Reset (SR0004)
- **Additional Comments (Customer Visible):**  
  *"Hello Akash, your account has been unlocked and a temporary password has been provided to you securely via phone. You will be prompted to choose your new private password upon signing in."*
- **Work Notes (Internal ITIL Only):**  
  *"Caller identity verified via Employee ID NXT-1088 and manager Rajesh Bhat. Checked ADUC; BadLogonCount was 6. Executed Unlock-ADAccount and Set-ADAccountPassword with -ChangePasswordAtLogon $true. Advised user to update Wi-Fi credentials on personal mobile device to prevent recurrent lockouts."*

---

### Ticket 10: New Software Install Request (SR0002)
- **Additional Comments (Customer Visible):**  
  *"Hello Kavitha, Microsoft Visio Professional has been successfully installed and activated on your laptop. You can launch it directly from the Windows Start Menu."*
- **Work Notes (Internal ITIL Only):**  
  *"Procurement approval verified for Visio license #VIS-8812. Deployed package via administrative silent install: `msiexec /i \\nexfs01\deploy\Visio2021.msi /qn ALLUSERS=1`. Verified application opens cleanly and license activated via M365 subscription."*
