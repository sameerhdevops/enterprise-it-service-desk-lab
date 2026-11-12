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
4. If a process appears hung or locked, open Resource Monitor (`resmon.exe`), go to the CPU tab, right-click the suspect process, and select **Analyze Wait Chain** to identify whether it is waiting on another process, I/O handle, or deadlock. Note: Resource Monitor displays associated worker threads, but an L1 technician terminates the *process* or *process tree*, not individual threads.

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
1. **If user application (e.g., Chrome/Excel):** Save user work if possible, then select the process in Task Manager and click **End Task** (or in Resource Monitor / Task Manager, select **End Process Tree**; in PowerShell: `Stop-Process -Id <PID> -Force`). Note: Never attempt to terminate individual worker threads directly, as this risks kernel instability or application deadlocks—always terminate the parent process or process tree cleanly.
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
- Escalate to **L2 Desktop Support** if hardware fan bearings have failed (loud grinding noise) or if `System` (PID 4) / `System Interrupts` consumes excessive CPU due to a misbehaving hardware interrupt/driver (Deferred Procedure Call / DPC latency) requiring Windows Performance Toolkit (WPT) trace analysis.

### 12. Ticket Resolution Notes
> *"Addressed high CPU utilization and fan noise. Diagnosed runaway Google Chrome renderer process (PID 14220) consuming 92% of CPU cycles due to a hung script in an intranet tab. Verified thread wait chain in Resource Monitor, then terminated the runaway process tree cleanly via Task Manager. CPU utilization dropped to 6% idle and chassis temperature stabilized. Verified application responsiveness with user."*

### 13. Interview Questions & Defensible Answers
- **Q: What do you do if `System` (PID 4) or `System Interrupts` is using 40-50% CPU?**  
  *A: "'System Interrupts' is not a normal user process—it represents the CPU time spent servicing hardware interrupts (Interrupt Service Routines / ISRs) and Deferred Procedure Calls (DPCs). High CPU usage here is almost always caused by a malfunctioning hardware device driver or faulty peripheral continuously firing interrupts. As an L1 tech, I would check Device Manager for yellow exclamation marks, review recently installed drivers or connected USB docks, and disconnect external peripherals one by one to see if the interrupt storm clears. If it persists, I would escalate to L2/L3 to capture an ETL trace using Windows Performance Recorder (WPR) and analyze DPC/ISR execution times in Windows Performance Analyzer (WPA)."*
- **Q: Can you terminate an individual thread that is causing high CPU in Resource Monitor?**  
  *A: "No, L1 technicians terminate the process or process tree, not individual threads. While Resource Monitor and Process Explorer allow you to inspect individual thread activity and CPU cycles, terminating a thread directly inside a running process leaves shared memory structures, locks, and handles in an inconsistent state, typically crashing the entire process or corrupting data. The correct procedure is to use 'Analyze Wait Chain' to determine why the thread is blocked, and if runaway, terminate the process cleanly via End Task or Stop-Process."*
