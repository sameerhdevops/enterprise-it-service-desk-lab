# Troubleshooting Runbook: Print Spooler Problem
**Incident ID:** INC-W007  
**Category:** Windows Support / Printers  
**Target Systems:** Windows 11 / Windows 10  

---

### 1. Reported Symptom
User reports: *"When I click print, nothing happens. When I try to open Printers & Scanners, it freezes or gives an error saying 'The local print spooler service is not running. Please restart the spooler'."*

### 2. User Impact
User cannot print any documents from any application on the workstation. Priority: P3.

### 3. Initial Questions
1. Did a specific document (e.g., large PDF or complex diagram) get sent to the printer right before the issue began?
2. Did you receive a popup message saying the print spooler has stopped?
3. Have you tried restarting your computer?

### 4. Investigation Sequence
1. Check the status of the `Spooler` service in `services.msc` or via PowerShell.
2. If the service is stopped or continuously crashes upon starting, inspect the spool directory: `C:\Windows\System32\spool\PRINTERS`.
3. Check Windows Event Viewer: Application log for `spoolsv.exe` crashes (Event ID 1000) and System log for Service Control Manager events (Event ID 7031/7034).
4. Identify if a corrupted `.SPL` (spool file) or `.SHD` (shadow file) is causing the spooler process to crash immediately upon initialization.

### 5. Tools Required
- Services Management Console (`services.msc`)
- Windows Event Viewer (`eventvwr.msc`)
- Administrative PowerShell or Command Prompt

### 6. Commands & Output Interpretation
Check spooler service status:
```powershell
Get-Service -Name Spooler
```
*Interpretation:* If Status is `Stopped`, attempt to start it. If it starts and then immediately stops within 2 seconds, a corrupted print file or bad driver is crashing `spoolsv.exe`.

Check for stuck spool files in the spool directory:
```powershell
Get-ChildItem -Path "C:\Windows\System32\spool\PRINTERS"
```
*Interpretation:* Any files with extensions `.SHD` or `.SPL` represent unprocessed jobs stuck in the queue.

### 7. Expected Observations
- Healthy: `Spooler` service is `Running`, startup type is `Automatic`, spool directory is completely empty when no print jobs are active.
- Fault: `spoolsv.exe` crashes repeatedly; old `.SPL` files dated days ago remain locked in `PRINTERS` folder.

### 8. Possible Root Causes
1. **Corrupted Print Job:** A malformed PDF or postscript document generated an invalid spool file that causes `spoolsv.exe` to trigger an access violation exception whenever it parses it.
2. **Corrupted Printer Driver:** A newly installed third-party print driver running in the spooler process has a memory fault.
3. **Spooler Service Disabled:** Service was stopped by an administrator or conflicting software.
4. **Insufficient Disk Space:** Drive C: has zero bytes available to write spool files.

### 9. Corrective Action (The Standard Spooler Purge Procedure)
> **Safety Notice:** Inform the user prior to execution that all currently queued, unprinted documents will be discarded and must be re-sent after service restoration. Never delete spool files while the `Spooler` service is active.

Execute the standard 4-step L1 Print Spooler reset script in an elevated PowerShell session:
```powershell
# Step 1: Stop the print spooler service (releases file locks on .SPL/.SHD files)
Stop-Service -Name Spooler -Force

# Step 2: Delete all stuck print spool (.SPL raw data) and shadow (.SHD metadata) files
Remove-Item -Path "C:\Windows\System32\spool\PRINTERS\*" -Force

# Step 3: Start the print spooler service
Start-Service -Name Spooler

# Step 4: Verify status
Get-Service -Name Spooler
```

If the spooler continues crashing after purging files:
- Open `printmanagement.msc` > Custom Filters > **All Drivers**.
- Remove recently added or non-essential print drivers.
- Reinstall clean PCL6 drivers directly from the manufacturer (avoid uncertified generic drivers).

### 10. Verification Procedure
- Verify `Get-Service Spooler` reports `Running`.
- Open Printers & Scanners in Windows Settings; confirm all configured printers display properly without freezing.
- Print a standard Windows test page; verify it spools, prints, and clears cleanly.

### 11. Escalation Conditions
- Escalate to **L2 Desktop Support** if `spoolsv.exe` crashes due to corrupted Windows system binaries (requires SFC/DISM or OS repair).

### 12. Ticket Resolution Notes
> *"Addressed Print Spooler service failure. Spooler was terminating due to a corrupted 450 MB print job stuck in the spool directory. Stopped Spooler service, cleared orphaned .SPL and .SHD files from C:\Windows\System32\spool\PRINTERS, and restarted service. Verified spooler remains in Running state. Sent test print successfully."*

### 13. Interview Questions & Defensible Answers
- **Q: Walk me through the exact steps to clear a stuck print job in Windows when you cannot cancel it through the GUI.**  
  *A: "When a print job is locked in the GUI, clicking 'Cancel' often hangs on 'Deleting...'. The standard procedure is: First, notify the user that pending print jobs will be cleared. Second, open an elevated command prompt or PowerShell and stop the Print Spooler service with `Stop-Service Spooler -Force`—this releases file locks and prevents spooler crashes. Third, navigate to `C:\Windows\System32\spool\PRINTERS` and delete all temporary `.SPL` (raw print data) and `.SHD` (shadow job header) files. Fourth, restart the service with `Start-Service Spooler`. Finally, verify that the queue is clear and print a test page."*
