# Standard Knowledge Base Article: Resolving Windows Update Failures
**KB ID:** KB0011  
**Category:** Windows / Operating System  
**Author:** Nexora IT Service Desk (L1 Support)  
**Last Reviewed:** 2024-11-12  

---

### Symptoms
- Windows Update fails with error code `0x80070002`, `0x80070003`, `0x80240034`, or `0x800f081f`.
- Updates hang indefinitely at "Downloading 0%" or "Installing 100%".
- System repeatedly attempts to install updates and rolls back upon restart.

### Applicable Systems
- Windows 11 Enterprise / Windows 10 Pro endpoints managed by Windows Server Update Services (WSUS) or Intune.

### Prerequisites
- Administrative command prompt or PowerShell.

### Troubleshooting Steps
1. **Check Disk Space:** Ensure drive C: has at least 15 GB of free space available.
2. **Run Built-in Windows Troubleshooter:**
   - Settings > System > Troubleshoot > Other troubleshooters > **Windows Update** > click **Run**.
3. **Verify Date and Time:** Ensure computer clock is synchronized within 5 minutes of internet time (SSL certificate validation fails if clock skews).

### Resolution: Reset Windows Update Components
Execute the full reset script in an elevated command prompt:
```cmd
:: 1. Stop background update services
net stop wuauserv
net stop cryptSvc
net stop bits
net stop msiserver

:: 2. Rename corrupted cache directories
ren C:\Windows\SoftwareDistribution SoftwareDistribution.old
ren C:\Windows\System32\catroot2 catroot2.old

:: 3. Restart update services
net start wuauserv
net start cryptSvc
net start bits
net start msiserver

:: 4. Force immediate update check
usoclient StartScan
```

If error `0x800f081f` persists, execute component store repair:
```cmd
DISM.exe /Online /Cleanup-image /Restorehealth
sfc /scannow
```

### Verification
- Open Settings > Windows Update > click **Check for updates**.
- Verify updates download and install cleanly to completion without error codes.

### Escalation Instructions
- Escalate to **L2 Desktop / Endpoint Management** if a specific cumulative update has a known vendor incompatibility requiring exclusion via GPO/Intune.

### Related Incidents
- INC-W004, INC-W009, WIN-OS-001
