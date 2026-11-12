# Troubleshooting Runbook: Software Installation Failure
**Incident ID:** INC-W009  
**Category:** Windows Support / Software  
**Target Systems:** Windows 11 / Windows 10  

---

### 1. Reported Symptom
User reports: *"I am trying to install the approved video conferencing tool / VPN client, but the installer stops midway and fails with an error: 'Error 1603: A fatal error occurred during installation', or 'The system administrator has set policies to prevent this installation'."*

### 2. User Impact
User cannot access virtual meetings or required business software. Priority: P3 (or Service Request fulfillment).

### 3. Initial Questions
1. Is this application on the approved enterprise software list?
2. Are you running the installer using standard user privileges or administrative elevation?
3. Was an older version of this software previously installed on the workstation?

### 4. Investigation Sequence
1. Check User Account Control (UAC) and local administrator rights (standard domain users cannot install MSI packages that write to `Program Files` or `HKLM`).
2. If Windows Installer (`msiexec.exe`) fails with Error 1603, generate an MSI installation verbose log file.
3. Check if the Windows Installer service (`msiserver`) is running or stuck.
4. Verify whether pending Windows updates or a reboot flag (`PendingFileRenameOperations`) is blocking installation.
5. Check AppLocker or Software Restriction Policies in Event Viewer (`Microsoft-Windows-AppLocker/EXE and DLL`).

### 5. Tools Required
- Command Prompt / PowerShell (Run as Administrator)
- Services Management Console (`services.msc`)
- Event Viewer (`eventvwr.msc`)
- Windows Registry (`regedit` - read-only inspection)

### 6. Commands & Output Interpretation
Generate a verbose MSI installation log to capture the exact failure point:
```cmd
msiexec /i "C:\Installers\ClientApp.msi" /l*v "C:\Temp\install_debug.log"
```
*Interpretation:* Open `C:\Temp\install_debug.log` in Notepad and search for the string `"Return value 3"` (the standard Windows Installer code indicating an unrecoverable action failure). The lines immediately preceding `"Return value 3"` reveal the exact cause (e.g., access denied to registry key, missing prerequisite, locked file).

Check for pending reboot flags:
```powershell
Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager" -Name "PendingFileRenameOperations" -ErrorAction SilentlyContinue
```
*Interpretation:* If `PendingFileRenameOperations` exists, an earlier update or software removal requires a computer restart before new packages can be safely written.

### 7. Expected Observations
- Normal: Installer requests UAC elevation, writes binaries to `Program Files`, registers DLLs, creates Start Menu shortcuts, returns exit code 0.
- Fault: Installer rolls back actions midway, displays generic 1603 dialog, or UAC prompt is blocked.

### 8. Possible Root Causes
1. **Lack of Administrative Privileges:** Standard user attempting to run per-machine installer without elevation.
2. **Pending System Reboot:** Windows has pending file operations locked in memory from previous update.
3. **Leftover Registry Keys from Previous Installation:** Incomplete uninstall left orphaned GUID keys in `HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall`.
4. **Missing Prerequisites:** Application requires specific .NET Framework or Visual C++ runtime build not yet installed.
5. **Antivirus / Endpoint Protection Blocking:** Security software flagging unknown executable.

### 9. Corrective Action
1. **Reboot the Computer:** Clears `PendingFileRenameOperations` and restarts the `msiserver` service.
2. **Elevate Installer:** Right-click installer > **Run as administrator** (or run command prompt as admin and invoke installer).
3. **Install Prerequisites Manually:** Download and install required Visual C++ Redistributable or .NET runtime.
4. **Clean Previous Corrupted Installation:** Use the official Microsoft Program Install and Uninstall Troubleshooter tool (`msicuu2` equivalent) or manually clear orphaned registry GUID keys.
5. **Re-register Windows Installer Service:**
   ```cmd
   msiexec /unregister
   msiexec /regserver
   ```

### 10. Verification Procedure
- Run installer with administrator credentials; observe installation completes to 100%.
- Launch installed application from Start Menu; verify it opens and operates properly.
- Verify entry appears under Settings > Installed apps (`appwiz.cpl`).

### 11. Escalation Conditions
- Escalate to **L2 Desktop / Endpoint Management** if domain Group Policy (AppLocker) has explicitly blacklisted the package hash or if deployment via Microsoft Intune / SCCM is failing across multiple machines.

### 12. Ticket Resolution Notes
> *"Assisted user with failed installation of approved software package (Error 1603). Diagnostic MSI log revealed failure was due to pending reboot lock and missing Visual C++ 2019 x64 runtime prerequisite. Installed required C++ runtime package, rebooted workstation, and executed installation with elevated L1 support credentials. Installation completed successfully."*

### 13. Interview Questions & Defensible Answers
- **Q: What is Windows Installer Error 1603 and how do you find the root cause?**  
  *A: "Error 1603 is a generic fatal error code returned by Windows Installer (msiexec). Because the dialog does not give specifics, the professional way to diagnose it is to launch the installer from command line with verbose logging enabled: `msiexec /i package.msi /l*v C:\temp\install.log`. Inside the log, I search for 'Return value 3', which marks the exact custom action or script that failed right before the installer rolled back."*
