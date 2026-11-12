# Troubleshooting Runbook: High CPU Usage
**Incident ID:** INC-W002  
**Category:** Windows Support / Performance  
**Target Systems:** Windows 11 / Windows 10  

---

### 1. Reported Symptom
User reports: *"The laptop fan is spinning loudly and constantly. The machine is warm to the touch and the mouse cursor stutters when moving across the screen."*

### 2. User Impact
Single user impacted. Applications lag or become temporarily unresponsive. Battery drains rapidly. Priority: P3.

### 3. Initial Questions
1. Which application were you using when the fan started running loudly?
2. Has this behavior been ongoing for days or did it start recently?
3. Did you recently open any large files (e.g., massive spreadsheet, video editing, compiling code)?

### 4. Investigation Sequence
1. Open Task Manager (`Ctrl + Shift + Esc`) and sort the **Processes** tab by the **CPU** column descending.
2. If system processes are hidden, click "More details" and ensure "Show processes from all users" is active.
3. Identify whether the culprit is a user-level process (e.g., Google Chrome, Teams) or a Windows system service (e.g., `TiWorker.exe`, `WmiPrvSE.exe`, `MsMpEng.exe`).
4. If a system process, use Resource Monitor (`resmon`) to inspect associated threads and service handles.

### 5. Tools Required
- Task Manager (`taskmgr`)
- Resource Monitor (`resmon.exe`)
- PowerShell (`Get-Process`, `Get-Service`)
- Process Explorer (Sysinternals - optional/reference)

### 6. Commands & Output Interpretation
Identify top 5 CPU consumers via PowerShell:
```powershell
Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 ProcessName, Id, CPU, Handles
```
*Interpretation:* Note the `ProcessName` and `CPU` seconds counter. A process whose CPU count ticks up rapidly every second while idle is in a tight loop.

Inspect Windows Management Instrumentation (WMI) activity if `WmiPrvSE.exe` is consuming CPU:
```powershell
Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-WMI-Activity/Operational'; ID=5858} -MaxEvents 5 | Format-List
```
*Interpretation:* Event ID 5858 logs the ClientProcessId causing WMI errors or excessive queries.

### 7. Expected Observations
- Normal: CPU utilization hovers below 10% when idle.
- Problem: CPU stays pegged at 85%–100% indefinitely, even when the user is not typing or interacting.

### 8. Possible Root Causes
1. **Runaway Browser Tab or Web App:** Heavy JavaScript loop or unclosed video stream in Edge/Chrome.
2. **Windows Update Background Worker (`TiWorker.exe` / `TrustedInstaller`):** Actively compiling .NET assemblies or installing patches.
3. **WMI Provider Host (`WmiPrvSE.exe`):** Misbehaving third-party monitoring agent or driver issuing continuous WMI queries.
4. **Antivirus Real-Time Scanner (`MsMpEng.exe`):** Stuck scanning a huge compressed archive or database folder.
5. **Corrupted OneDrive or File Indexing Loop:** Windows Search indexing corrupt files.

### 9. Corrective Action
1. **If user application (e.g., Chrome/Excel):** Save user work if possible, then select process in Task Manager and click **End Task** (or `Stop-Process -Id <PID> -Force`).
2. **If `TiWorker.exe` / Windows Update:** Allow 15–20 minutes to complete installation. If permanently stuck, restart the Windows Update service:
   ```powershell
   Restart-Service -Name wuauserv -Force
   ```
3. **If Windows Search Indexer (`SearchIndexer.exe`):** Rebuild the search index via `control.exe srchadmin.msc` > Advanced > Rebuild.
4. **If hardware fan is loud despite low CPU:** Inspect BIOS/UEFI thermal settings and clean physical vents.

### 10. Verification Procedure
- Monitor Task Manager CPU graph for 3–5 minutes.
- Confirm baseline drops below 15% at idle.
- Confirm fan speed gradually ramps down to whisper-quiet levels.

### 11. Escalation Conditions
- Escalate to **L2 Desktop Support** if hardware fan bearings have failed (loud grinding noise) or if `System` (PID 4) consumes 100% CPU due to a misbehaving hardware interrupt/driver (DPC/Deferred Procedure Call latency).

### 12. Ticket Resolution Notes
> *"Addressed high CPU utilization and fan noise. Diagnosed runaway Google Chrome renderer process (PID 14220) consuming 92% of CPU cycles due to a hung script in an intranet tab. Terminated the specific sub-process via Task Manager. CPU utilization dropped to 6% idle and chassis temperature stabilized. Verified with user."*

### 13. Interview Questions & Defensible Answers
- **Q: What do you do if `System` (PID 4) or `System Interrupts` is using 40-50% CPU?**  
  *A: "High CPU usage by 'System Interrupts' or PID 4 is almost always caused by a malfunctioning hardware device driver continuously firing hardware interrupts (Interrupt Service Routines or DPCs). As an L1 tech, I would check Device Manager for yellow exclamation marks, review recently installed drivers or connected USB docks, and disconnect external peripherals one by one. If it persists, I would escalate to L2 to run Windows Performance Analyzer."*
