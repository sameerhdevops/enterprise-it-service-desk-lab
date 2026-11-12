# Standard Knowledge Base Article: Resolving Microsoft Outlook Sign-in Issues
**KB ID:** KB0005  
**Category:** Microsoft 365 / Outlook  
**Author:** Nexora IT Service Desk (L1 Support)  
**Last Reviewed:** 2024-11-12  

---

### Symptoms
- Outlook prompts for password continuously in an infinite modern authentication loop.
- Status bar at bottom right says "Need Password" or "Disconnected".
- Dialog box appears saying: "We can't connect you right now. Please check your network and try again."

### Applicable Systems
- Microsoft 365 Apps for Enterprise (Outlook 365 Desktop Client on Windows 10/11).

### Prerequisites
- Standard user permissions; internet connectivity.

### Troubleshooting Steps
1. **Rule out Account / Exchange Outage:**
   - Direct user to log into Outlook on the Web ([https://outlook.office.com](https://outlook.office.com)).
   - If web login succeeds, the mailbox and cloud credentials are healthy; the issue is localized to Windows Credential Manager or local OAuth tokens.
2. **Close All Office Applications:**
   - Terminate `outlook.exe`, `teams.exe`, `excel.exe`, and `winword.exe` via Task Manager.
3. **Purge Stored Windows Credentials:**
   - Press `Windows Key + R` > type `control keymgr.dll` > press Enter.
   - Click **Windows Credentials**.
   - Under Generic Credentials, locate and expand all entries containing:
     - `MicrosoftOffice16_Data:ADAL:`
     - `MicrosoftAccount:user=`
     - `MS.Outlook.15:`
   - Click **Remove** on each entry.

### Resolution
- **Reset Microsoft Entra WAM Broker Plugin:**
  Open PowerShell (as user) and run:
  ```powershell
  Get-AppxPackage Microsoft.AAD.BrokerPlugin | Reset-AppxPackage
  ```
- **Reopen Outlook:**
  - Launch Outlook. Modern authentication login prompt will appear.
  - Enter corporate email and password.
  - Complete multi-factor authentication (MFA) push notification on Microsoft Authenticator app.
  - Check "Allow my organization to manage my device" > click OK.

### Verification
- Confirm bottom-right status bar displays: `Connected to: Microsoft Exchange`.
- Send a test email to the user's own email address; verify message sends and arrives in Inbox within 30 seconds.

### Escalation Instructions
- Escalate to **L2 Application / Identity Support** if the user account has a Conditional Access block or disabled MFA hardware token.

### Related Incidents
- INC0003, INC-W013, M365-RUN-001
