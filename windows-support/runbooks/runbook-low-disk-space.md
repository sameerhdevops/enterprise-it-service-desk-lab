# Troubleshooting Runbook: Low Disk Space on System Drive
**Incident ID:** INC-W004  
**Category:** Windows Support / Storage  
**Target Systems:** Windows 11 / Windows 10  

---

### 1. Reported Symptom
User reports: *"A red bar is showing on my C: drive in File Explorer, and Windows popped up a notification saying 'Low Disk Space: You are running out of disk space on Local Disk (C:)'."*

### 2. User Impact
User cannot download email attachments, save new files, or install required application updates. System freezes can occur when the pagefile cannot expand. Priority: P3.

### 3. Initial Questions
1. How long has the red bar been showing on your C: drive?
2. Did you recently download any large video files, ISO images, or database dumps?
3. Have you checked your personal Downloads folder or emptied the Recycle Bin?

### 4. Investigation Sequence
1. Check available free space on drive `C:` using File Explorer or PowerShell.
2. Identify whether the space is consumed by user files (`Downloads`, `Videos`, `Desktop`) or system directories (`C:\Windows\Temp`, `C:\ProgramData`, `AppData`).
3. Check for leftover Windows Update installation files (`Windows.old` or `SoftwareDistribution\Download`).
4. Review hibernation file (`hiberfil.sys`) and pagefile size.

### 5. Tools Required
- Windows Disk Cleanup (`cleanmgr.exe`)
- Windows Storage Sense (`ms-settings:storagesense`)
- PowerShell (Administrative)
- TreeSize Free or WinDirStat (optional portable utility)

### 6. Commands & Output Interpretation
Check free space and percentage on drive C:
```powershell
Get-PSDrive C | Select-Object Name, @{N="FreeGB";E={[math]::Round($_.Free/1GB,2)}}, @{N="UsedGB";E={[math]::Round($_.Used/1GB,2)}}, @{N="PercentFree";E={[math]::Round(($_.Free/($_.Free+$_.Used))*100,1)}}
```
*Interpretation:* If `PercentFree` is below 10% (or less than 15 GB), immediate cleanup is required.

Identify largest subdirectories in the user profile:
```powershell
Get-ChildItem -Path $env:USERPROFILE -Directory | ForEach-Object {
    $size = (Get-ChildItem $_.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    [PSCustomObject]@{
        Folder = $_.Name
        SizeMB = [math]::Round($size/1MB,2)
    }
} | Sort-Object SizeMB -Descending | Select-Object -First 5
```
*Interpretation:* Pinpoints whether `Downloads`, `OneDrive`, or hidden `AppData` is storing massive caches.

### 7. Expected Observations
- Healthy enterprise drive: At least 20–30 GB (or >15%) free space on system drive.
- Low space condition: Drive C has < 2 GB free, bar displays solid red in File Explorer.

### 8. Possible Root Causes
1. **Accumulated Temporary Files:** `C:\Windows\Temp` and `C:\Users\<user>\AppData\Local\Temp` holding gigabytes of uncleaned setup caches.
2. **Old Windows Update Installations:** `C:\Windows.old` retaining previous OS builds after a feature update.
3. **Bloated Downloads Folder:** User storing large installers, ISOs, and personal media in Downloads.
4. **OneDrive Sync Misconfiguration:** OneDrive downloading the entire company SharePoint document library locally rather than using "Files On-Demand".
5. **Excessive Crash Dumps / Log Files:** Application crash dumps (`.dmp`) accumulating in `C:\Windows\Minidump` or `C:\ProgramData`.

### 9. Corrective Action
1. **Run Built-in Disk Cleanup:**
   - Run `cleanmgr.exe /d c:` or enable **Storage Sense** in Settings > System > Storage.
   - Click "Clean up system files", check *Windows Update Cleanup*, *Temporary files*, and *Recycle Bin*.
2. **Clear User and System Temp Directories:**
   ```powershell
   Remove-Item -Path "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
   Remove-Item -Path "C:\Windows\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
   ```
3. **Clear SoftwareDistribution Download Cache:**
   ```cmd
   net stop wuauserv
   rd /s /q C:\Windows\SoftwareDistribution\Download
   md C:\Windows\SoftwareDistribution\Download
   net start wuauserv
   ```
4. **Enable OneDrive Files On-Demand:**
   - In OneDrive Settings > Sync and backup > Advanced settings > verify "Files On-Demand" is active so files remain in cloud until opened.

### 10. Verification Procedure
- Rerun disk check command; confirm free space on `C:` is at least 15 GB (or > 15%).
- Verify the drive icon in File Explorer returns from red to the normal blue progress bar.
- Confirm user can successfully save documents and download attachments.

### 11. Escalation Conditions
- Escalate to **L2 Desktop Support** if the physical drive capacity is fundamentally insufficient for the user's role (e.g., 128 GB SSD on a developer laptop requiring local Docker images).

### 12. Ticket Resolution Notes
> *"Resolved low disk space alert on user laptop (drive C had 1.2 GB free). Executed Windows Update cleanup and emptied Recycle Bin (freed 11.5 GB). Cleared orphaned temporary files in %temp% and SoftwareDistribution cache (freed 4.8 GB). Configured OneDrive Files On-Demand to prevent auto-downloading of shared team folders. Free space restored to 24.6 GB (22% free). Verified with user."*

### 13. Interview Questions & Defensible Answers
- **Q: What is the safest way to clear disk space on a corporate Windows machine without deleting user files?**  
  *A: "The safest method is using native Windows tools: running Disk Cleanup (cleanmgr.exe) with 'Clean up system files' to remove superseded Windows Update packages and old OS builds, clearing the %temp% and C:\Windows\Temp folders, and emptying the Recycle Bin. I also check if OneDrive Files On-Demand is enabled so users don't store offline copies of huge shared cloud libraries. I never delete files from System32 or user Document directories without explicit user authorization."*
