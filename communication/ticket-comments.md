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

## 2. Representative Ticket Comment Pairs (Customer vs. Internal)

### Ticket 1: Laptop Not Powering On (INC0001)
- **Additional Comments (Customer Visible):**  
  *"Hello Kavitha, I have inspected your laptop in the IT room. The motherboard power controller has failed. We have requested an on-site warranty replacement from HP. In the meantime, I have issued you a spare laptop so your work is not interrupted. I will notify you as soon as your primary laptop is repaired."*
- **Work Notes (Internal ITIL Only):**  
  *"Tested with known-good 65W HP AC adapter. Power LED unresponsive. Executed 60-second static capacitor drain—no POST or fan spin. Inspected DC jack for physical damage; intact. Checked warranty in asset inventory: active. Logged vendor RMA case for motherboard replacement. Issued spare loaner unit. Updated asset register."*

---

### Ticket 2: Shared Folder Access Denied (INC0002)
- **Additional Comments (Customer Visible):**  
  *"Hello Meena, your permissions for the Finance shared folder have been verified and restored. Please sign out of your computer and log back in to apply the updated permissions."*
- **Work Notes (Internal ITIL Only):**  
  *"Checked `whoami /groups` via remote session; confirmed user lacked FIN-SharedDrive security group membership following quarterly access review. Re-added user to FIN-SharedDrive security group. Ran `klist purge`. Advised user to sign out and log back in so the Windows security access token refreshes with the new group SID."*

---

### Ticket 3: Outlook Repeated Crashes (INC0003)
- **Additional Comments (Customer Visible):**  
  *"Hi Akash, we identified an incompatible add-in that was causing Outlook to crash on launch. We have disabled the add-in and refreshed your local profile. Outlook is now operating normally."*
- **Work Notes (Internal ITIL Only):**  
  *"Event Viewer Application log showed Event ID 1000 with faulting add-in module. Launched `outlook.exe /safe` successfully. Navigated to File > Options > Add-ins > COM Add-ins; disabled conflicting plugin. Re-created local OST synchronization. Confirmed stable operation over 10 minutes of active use."*

---

### Ticket 4: VPN Intermittent Drops (INC0004)
- **Additional Comments (Customer Visible):**  
  *"Hello Divya, we have temporarily updated your VPN connection protocol to TCP mode to stabilize your connection while our network team implements a firewall configuration update scheduled for this maintenance window."*
- **Work Notes (Internal ITIL Only):**  
  *"User experiencing tunnel disconnects every 10–12 minutes on home broadband. Pings to gateway show packet fragmentation at 1500 bytes. Workaround applied: Changed GlobalProtect client protocol to TCP mode and set MTU to 1400. Connection stable for 45 minutes. Escalated ticket to L2 Network (Arvind Rao) referencing PRB0001 / CHG0002."*

---

### Ticket 5: 3rd Floor Printer Not Printing (INC0005)
- **Additional Comments (Customer Visible):**  
  *"Hello Neha, the Print Spooler service on the print server was unresponsive and has been restarted. Pending jobs have been cleared and the printer is now processing new documents normally."*
- **Work Notes (Internal ITIL Only):**  
  *"HP LaserJet Pro M404 on 3rd floor showed jobs queuing without printing. Printer self-test page printed cleanly. Checked print server NEXPRINT01; Print Spooler service was hung. Stopped spooler service, purged stuck jobs, restarted service. Verified print queue resumed processing."*

---

### Ticket 6: New Joiner Cannot Log In to Domain (INC0006)
- **Additional Comments (Customer Visible):**  
  *"Hello Ranjitha, Anil's Active Directory account has been activated and a temporary password has been set. He can now log in at his workstation and set his permanent password."*
- **Work Notes (Internal ITIL Only):**  
  *"New employee Anil Shetty (HR) joining today could not log in. Inspected ADUC; account was created under SR0001 but left disabled (missed onboarding step). Enabled account in AD, set temporary password, enabled 'User must change password at next logon'. Verified successful sign-in."*

---

### Ticket 7: Blue Screen During Presentation (INC0007)
- **Additional Comments (Customer Visible):**  
  *"Hello Vikram, your desktop experienced a critical storage drive hardware failure. We have installed a new solid-state drive, restored your user profile from last night's backup, and verified system stability."*
- **Work Notes (Internal ITIL Only):**  
  *"Workstation crashed with BSOD KERNEL_DATA_INPAGE_ERROR. SMART storage diagnostics confirmed failing SSD with bad reallocated sectors. Swapped SSD with new unit from stock. Restored profile and verified zero further crashes. Old SSD marked for secure disposal per policy."*

---

### Ticket 8: Cannot Send Emails - Mailbox Full (INC0008)
- **Additional Comments (Customer Visible):**  
  *"Hello Sunitha, your mailbox had reached its 50 GB storage threshold. We have archived emails older than one year to a local archive, reducing your mailbox size to 31 GB. Sending and receiving has been restored."*
- **Work Notes (Internal ITIL Only):**  
  *"Mailbox quota exceeded at 49.8 GB / 50 GB. Assisted user with archiving messages older than 12 months to local archive PST. Configured auto-archive policy. Mailbox usage reduced to 31 GB. Verified test email outbound delivery."*

---

### Ticket 9: Password Reset & Account Lockout (SR0004)
- **Additional Comments (Customer Visible):**  
  *"Hello Sunitha, your account has been unlocked and a temporary password has been provided to you securely. You will be prompted to choose your permanent private password upon sign-in."*
- **Work Notes (Internal ITIL Only):**  
  *"Caller identity verified via Employee ID NEX-FIN-003 and manager Rajesh Bhat. Unlocked account in AD and set temporary password `<TEMPORARY_PASSWORD>`. Enabled 'User must change password at next logon'. User successfully authenticated and set new password."*

---

### Ticket 10: Python Development Environment Setup (SR0002)
- **Additional Comments (Customer Visible):**  
  *"Hello Karthik, Python 3.12 has been deployed to your engineering workstation with pip and virtualenv configured. You can access it directly from your terminal."*
- **Work Notes (Internal ITIL Only):**  
  *"Software request approved by manager Arun Venkatesh. Deployed standard Python 3.12 package to workstation NEXWS-ENG04. Verified installation via `python --version` and `pip --version`. Added environment variables to system PATH."*
