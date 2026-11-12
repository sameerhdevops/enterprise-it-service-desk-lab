# Professional Service Desk Email Templates
**Document ID:** COM-EML-001  
**Audience:** L1 Service Desk Analysts  
**Tone:** Professional, Clear, Helpful, Actionable

---

## Template 1: Incident Acknowledgment
**Subject:** [Ticket #{IncidentID}] Acknowledged: {Title}

Dear {CallerName},

Thank you for contacting the Nexora Technologies IT Service Desk. We have received your report regarding "{Title}" and logged it under ticket reference **{IncidentID}**.

**Ticket Details:**
- **Incident ID:** {IncidentID}
- **Priority:** {Priority}
- **Assigned Group:** L1 Service Desk
- **Target Resolution Time:** {TargetHours}

An IT Support Engineer has been assigned to your ticket and is actively reviewing the details. We will contact you shortly if additional diagnostic information or remote access is required.

You may reply directly to this email to add notes or screenshots to your ticket.

Kind regards,  
**IT Service Desk Team**  
Nexora Technologies | Extension: 4100 | servicedesk@nexora.local

---

## Template 2: Requesting Additional Diagnostic Information
**Subject:** [Ticket #{IncidentID}] Information Needed: {Title}

Dear {CallerName},

We are actively investigating ticket **{IncidentID}** regarding your report that {ReportedSymptom}.

To help us isolate the exact cause and resolve this quickly, could you please provide a few additional details:
1. Are you currently connected to the office network (Ethernet/Wi-Fi) or working remotely from home via VPN?
2. If an error dialog or code appears, could you reply with a screenshot or the exact text of the message?
3. What is the Asset Tag number printed on the silver barcode label on your laptop (e.g., `NXT-AST-0XX`)?

Once we receive this information, we will proceed with the appropriate corrective steps. Thank you for your cooperation!

Best regards,  
**Sameer Kulkarni** | L1 IT Support Engineer  
Nexora Technologies Service Desk

---

## Template 3: Progress & Status Update
**Subject:** [Ticket #{IncidentID}] Update: {Title}

Dear {CallerName},

We wanted to provide you with a quick progress update on ticket **{IncidentID}** ({Title}).

Our team has completed initial hardware diagnostics on your laptop. We determined that the internal motherboard power controller requires replacement. We have logged an official warranty service request with the hardware vendor (HP Case Ref: #HP-99214).

An authorized HP service technician is scheduled to visit our Bengaluru office tomorrow morning between 10:00 AM and 1:00 PM IST with the replacement part.

In the meantime, we have prepared a temporary loaner laptop (`NXT-AST-015`) pre-configured with all your standard business applications. You may collect this laptop from the IT Operations Room on Floor 2 whenever convenient.

We will provide another update as soon as the technician completes the repair.

Best regards,  
**Sameer Kulkarni** | L1 IT Support Engineer  
Nexora Technologies Service Desk

---

## Template 4: Escalation Notification
**Subject:** [Ticket #{IncidentID}] Escalation Update: {Title}

Dear {CallerName},

Following our initial troubleshooting session regarding your VPN disconnection issue, we have escalated ticket **{IncidentID}** to our **L2 Network Support Team**.

Our investigation confirmed that your local client software and home broadband connection are operating normally. The intermittent drops appear to be related to a firewall gateway MTU configuration that requires specialized network engineering adjustments.

**Escalation Details:**
- **Escalated To:** Arvind Rao (Senior Network Engineer - L2)
- **Current Status:** In Investigation (Scheduled under Change CHG0002)
- **Next Update By:** Today at 4:30 PM IST

In the interim, we have enabled the TCP protocol fallback mode in your GlobalProtect client so you can maintain a stable connection for your daily work. 

Thank you for your patience while our network team addresses this permanent fix.

Best regards,  
**IT Service Desk** | Nexora Technologies

---

## Template 5: Resolution Confirmation
**Subject:** [Ticket #{IncidentID}] Resolved: {Title}

Dear {CallerName},

Your IT support ticket **{IncidentID}** ({Title}) has been marked as **Resolved**.

**Resolution Summary:**
- **Root Cause:** Corrupted Microsoft Teams local cache caused application freezing and audio device conflicts.
- **Action Taken:** Executed cache reset on the New Teams client and updated audio device permissions in Windows Sound settings. Verified audio test call completed successfully.

Please test your applications and confirm that everything is functioning to your satisfaction. If you are still experiencing issues, simply reply directly to this email within 3 business days to automatically reopen your ticket.

Thank you for working with the IT Service Desk!

Kind regards,  
**Sameer Kulkarni** | L1 IT Support Engineer  
Nexora Technologies Service Desk

---

## Template 6: Ticket Closure Notice
**Subject:** [Ticket #{IncidentID}] Closed: {Title}

Dear {CallerName},

Ticket **{IncidentID}** regarding "{Title}" is now formally **Closed**.

We have closed this ticket following your confirmation that normal service has been restored. If you encounter any new technical issues, please submit a new ticket via the IT Help Portal at [https://helpdesk.nexora.local](https://helpdesk.nexora.local) or call Extension 4100.

**Rate Your Experience:**  
Please take 10 seconds to let us know how we did by clicking one of the options below:  
[ Excellent (5) ]  [ Good (4) ]  [ Average (3) ]  [ Poor (1) ]

Thank you for helping us improve our IT services!

Best regards,  
**IT Service Management** | Nexora Technologies

---

## Template 7: Scheduled Maintenance Notification
**Subject:** [IT NOTIFICATION] Scheduled Maintenance: Server OS Patching - Saturday, Nov 16

Dear Nexora Team,

Please be advised that the IT Infrastructure Team will perform routine monthly security patching and server maintenance this weekend.

**Maintenance Window:**
- **Start Time:** Saturday, 16 November 2024 at 23:00 IST
- **End Time:** Sunday, 17 November 2024 at 03:00 IST
- **Change Reference:** CHG0001 (Approved Standard Maintenance)

**Expected Service Impact:**
- During this 4-hour window, the primary file server (`\\nexfs01`) and corporate intranet portal will experience intermittent downtime lasting approximately 15–20 minutes as servers reboot.
- Cloud services, including Microsoft 365, Exchange Email, and Teams, will remain 100% available and unaffected.

**Action Required:**  
Please ensure all open files on shared drives (`\\nexfs01`) are saved and closed before 22:30 IST on Saturday.

If you have any questions or urgent business requirements during this period, please contact the IT Service Desk.

Kind regards,  
**IT Infrastructure & Operations Team**  
Nexora Technologies

---

## Template 8: New Employee IT Welcome & Setup Guide
**Subject:** Welcome to Nexora Technologies! Your IT Setup and Credentials

Dear {NewEmployeeName},

Welcome to the Nexora Technologies team! We are excited to have you join the {Department} department.

The IT Service Desk has prepared your corporate workstation and user account. Below are the essential details to help you get started on your first day.

**1. Your IT Equipment:**
- **Assigned Laptop:** {LaptopModel} (Asset Tag: `NXT-AST-0XX`)
- **Accessories:** USB-C Power Adapter, Laptop Sleeve, Wireless Mouse, Security Cable.

**2. Your Login Credentials:**
- **Domain Username:** `{Username}` (or `{Username}@nexora.local`)
- **Corporate Email:** `{Username}@nexora.com`
- **Temporary Password:** Provided separately via secure SMS / in-person handover.

**3. First-Time Setup Instructions:**
1. Connect your laptop to power and press the Power button.
2. At the Windows logon screen, enter your username and temporary password.
3. Windows will immediately prompt you to set your new private password (minimum 12 characters, including uppercase, lowercase, number, and symbol).
4. Launch the **Microsoft Authenticator** app on your mobile phone to complete Multi-Factor Authentication (MFA) registration when prompted.
5. Open Outlook and Teams; your email and profile will synchronize automatically.

**Need Help?**  
The IT Service Desk is located on Floor 2 (IT Operations Room). You can reach us at Extension **4100** or via email at `servicedesk@nexora.local`.

Wishing you a fantastic start at Nexora!

Warm regards,  
**Sameer Kulkarni** | L1 IT Support Engineer  
Nexora Technologies Service Desk
