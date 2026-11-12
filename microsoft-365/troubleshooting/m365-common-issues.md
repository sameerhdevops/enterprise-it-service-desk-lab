# Top 10 Microsoft 365 Client Troubleshooting Runbooks
**Document ID:** M365-RUN-001  
**Audience:** L1 Service Desk Analysts  
**Scope:** Microsoft 365 Apps for Enterprise (Word, Excel, PowerPoint, Outlook, Teams)

---

## Issue 1: "Product Deactivated" or "Unlicensed Product" Error Bar
- **Symptom:** Yellow or red warning bar in Word/Excel saying *"Product Deactivated: Most features have been disabled because your account does not have an active license."*
- **L1 Troubleshooting:**
  1. Verify user's assigned license in M365 Admin Center (ensure M365 E3 / Business Standard is active).
  2. Check computer clock and date (SSL handshake fails if system time differs by > 5 minutes).
  3. Clear cached Office licenses: Run Command Prompt as administrator:
     ```cmd
     cd "C:\Program Files\Microsoft Office\Office16"
     cscript ospp.vbs /dstatus
     ```
     Locate last 5 characters of installed product key (e.g., `XXXXX`), then remove it:
     ```cmd
     cscript ospp.vbs /unpkey:XXXXX
     ```
  4. Relaunch Word and sign in with the employee's corporate email.

---

## Issue 2: Office Application Crashes on File > Open / File > Save As
- **Symptom:** Word or Excel crashes as soon as the user tries to browse files.
- **Root Cause:** Corrupted default printer driver or inaccessible mapped network drive in Windows Recent files.
- **Resolution:** Change Windows default printer to "Microsoft Print to PDF" or "OneNote". Disconnect dead mapped network drives using `net use * /delete /y`.

---

## Issue 3: Excel Freezes with "Calculating... (4 Processors)"
- **Symptom:** Large spreadsheet freezes during formula recalculation.
- **Resolution:**
  - Launch Excel in Safe Mode: `excel.exe /safe`.
  - Go to File > Options > Formulas > change Calculation Options from **Automatic** to **Manual**.
  - Open spreadsheet, locate circular references (Formulas > Error Checking > Circular References).

---

## Issue 4: Outlook Prompting for Password Repeatedly (Authentication Loop)
- **Symptom:** Modern authentication pop-up appears, disappears, and reappears endlessly.
- **Resolution:**
  - Clear Windows Credentials: `control keymgr.dll` > delete all `ADAL` and `Office16` credentials.
  - Delete broker plugin cache:
    ```powershell
    Get-AppxPackage Microsoft.AAD.BrokerPlugin | Reset-AppxPackage
    ```
  - Disconnect and reconnect corporate account in Windows Settings > Accounts > Access work or school.

---

## Issue 5: Cannot Open Attachment in Outlook ("Access Denied")
- **Symptom:** User clicks attachment; Outlook says *"Cannot create file: filename. Right-click the folder you want to create the file in and check permissions."*
- **Root Cause:** The hidden Outlook Secure Temp folder has reached its maximum file limit (99+ duplicate files with the same name).
- **Resolution:**
  - Locate Outlook Secure Temp folder path in registry:
    `HKEY_CURRENT_USER\Software\Microsoft\Office\16.0\Outlook\Security\OutlookSecureTempFolder`
  - Open folder in File Explorer and delete all cached temporary attachments.

---

## Issue 6: Teams Shows Blank / White Screen on Startup
- **Resolution:** Enable GPU hardware acceleration disable flag or purge Teams cache folder (see `microsoft-365/teams.md`).

---

## Issue 7: Co-Authoring and AutoSave Disabled in Word/Excel
- **Symptom:** AutoSave toggle in top-left corner is disabled; user cannot collaborate live with colleagues.
- **Root Cause:** File is saved locally or in an older file format (`.doc` / `.xls` instead of `.docx` / `.xlsx`), or stored on an on-premises SMB share rather than SharePoint/OneDrive.
- **Resolution:** Ensure file is saved directly into the company OneDrive or SharePoint document library in modern XML format.

---

## Issue 8: Outlook Search Returns No Results or "Search results may be incomplete"
- **Resolution:**
  - Check Windows Search service: `Get-Service wsearch`.
  - Rebuild Search Catalog: Control Panel > **Indexing Options** > **Advanced** > click **Rebuild**.
  - Temporary workaround: Configure Outlook to use built-in search engine instead of Windows Desktop Search.

---

## Issue 9: Shared Mailbox Not Appearing in Outlook
- **Symptom:** User granted access to `invoices@nexora.com`, but it does not show in the left-hand folder pane.
- **Resolution:**
  - In Exchange Online, auto-mapping takes up to 60 minutes to propagate.
  - Manual add: File > Account Settings > Account Settings > select user account > Change > More Settings > **Advanced** tab > click **Add...** > type mailbox name > OK.

---

## Issue 10: "Your account is not allowed to sign in from this device" (Conditional Access)
- **Symptom:** User blocked from M365 apps when working from home.
- **Root Cause:** Microsoft Entra Conditional Access policy enforcing compliant device status or trusted IP ranges.
- **Resolution:** Instruct user to connect to company GlobalProtect VPN first to enter trusted corporate egress IP, or initiate device compliance check in Company Portal app.
