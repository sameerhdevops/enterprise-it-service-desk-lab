# Troubleshooting Runbook: Slow Windows Computer
**Incident ID:** INC-W001  
**Category:** Windows Support / Performance  
**Target Systems:** Windows 11 Enterprise / Windows 10 Pro  

---

### 1. Reported Symptom
User reports: *"My laptop is running extremely slow today. Opening Excel or Outlook takes several minutes, and switching between browser tabs causes the system to freeze."*

### 2. User Impact
Productivity severely degraded. User cannot participate in video calls or complete daily accounting tasks. Single-user impact, medium urgency (Priority: P3).

### 3. Initial Questions
1. When did this slowness start? Was the computer working fine yesterday?
2. Did the computer recently restart or apply any Windows updates?
3. Are specific applications slow, or is the entire operating system sluggish?
4. Have you noticed any loud fan noise or excessive heat from the laptop chassis?

### 4. Investigation Sequence
1. Check overall system uptime (users frequently put laptops to sleep for weeks without a true reboot).
2. Open Task Manager (`Ctrl + Shift + Esc`) to inspect real-time resource utilization (CPU, Memory, Disk, Network).
3. Review Startup apps tab to see if excessive background applications were launched.
4. Check available storage on drive `C:` to ensure sufficient paging file space.
5. Review Event Viewer System log for disk I/O errors or thermal throttling events.

### 5. Tools Required
- Task Manager (`taskmgr`)
- Resource Monitor (`resmon`)
- PowerShell (Administrative)
- Windows Event Viewer (`eventvwr.msc`)

### 6. Commands & Output Interpretation
Check system uptime:
```powershell
Get-CimInstance Win32_OperatingSystem | Select-Object LastBootUpTime, @{N="UptimeDays";E={[math]::Round(((Get-Date) - $_.LastBootUpTime).TotalDays, 1)}}
```
*Interpretation:* If `UptimeDays` is > 14 days, the system has not experienced a cold restart. In Windows 10/11, Fast Startup (hybrid boot) logs off user sessions but hibernates the OS kernel session and system drivers to `hiberfil.sys`. As a result, kernel session uptime accumulates across shutdowns, and any corrupted device driver states or kernel-mode pool leaks (Paged/Non-Paged pool) persist. Note: high uptime by itself does not automatically equal a memory leak, but it indicates accumulated operational state. Furthermore, users frequently put laptops to sleep rather than shutting down, which can preserve user-mode application memory leaks. A clean restart (`shutdown /r /t 0` or Start > Restart) completely tears down both the kernel and user sessions.

Inspect top resource-consuming processes:
```powershell
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 ProcessName, Id, CPU, @{N="WorkingSetMB";E={[math]::Round($_.WorkingSet/1MB,2)}}
```
*Interpretation:* Identify whether a runaway process (e.g., antivirus scan, browser memory leak, or hung background updater) is saturating the CPU or RAM.

Check free storage on system drive:
```powershell
Get-PSDrive C | Select-Object Name, @{N="FreeGB";E={[math]::Round($_.Free/1GB,2)}}, @{N="TotalGB";E={[math]::Round(($_.Free+$_.Used)/1GB,2)}}
```
*Interpretation:* If free space is below 10%, Windows cannot efficiently expand the virtual memory paging file (`pagefile.sys`), causing severe thrashing.

### 7. Expected Observations
- Normal system: CPU idle 2–10%, Memory <70%, Disk activity <5%.
- Problem state: Disk utilization pegged at 100% with low transfer speeds (failing drive or intense background indexing), or RAM at 95%+ with heavy paging.

### 8. Possible Root Causes
1. **Prolonged Uptime / Kernel Session Degradation:** Windows Fast Startup hibernating the kernel session and device drivers across shutdowns, preserving corrupted driver states or non-paged memory pool leaks, combined with persistent sleep cycles preserving user-mode process leaks.
2. **Excessive Startup Programs:** Multiple unneeded background utilities launching upon user logon.
3. **Storage Exhaustion:** System drive C: has < 10% free space, preventing virtual memory paging file (`pagefile.sys`) expansion.
4. **Thermal Throttling:** Clogged cooling vents or degraded thermal interface forcing the CPU multiplier down (e.g. to 0.79 GHz).
5. **Background Update or Antivirus Scan:** Windows Update (`TiWorker.exe`) or Defender full scan executing during working hours.

### 9. Corrective Action
1. If uptime is high, perform a full cold reboot: `shutdown /r /t 0` (or clicking Restart in the Start Menu, which bypasses Fast Startup).
2. Disable non-essential startup items in Task Manager > Startup apps.
3. Clean temporary files: Run `cleanmgr.exe` or clear contents of `C:\Windows\Temp` and `%temp%`.
4. Run System File Checker to repair corrupted OS components:
   ```cmd
   sfc /scannow
   ```
5. Ensure vents are clear and laptop is on a hard flat surface.

### 10. Verification Procedure
- Verify Task Manager reflects normal resource thresholds (CPU < 15% at idle, RAM < 70%).
- Confirm system uptime in Task Manager has reset to 0:00:00.
- Launch Outlook and Excel; confirm launch times return to normal (< 5 seconds).
- User confirms smooth tab switching and application responsiveness.

### 11. Escalation Conditions
- Escalate to **L2 Desktop Support** if hardware diagnostics indicate failing NVMe/SSD (bad sectors / SMART errors) or persistent thermal throttling requiring fan/heatsink replacement.

### 12. Ticket Resolution Notes
> *"Diagnosed system slowness reported by user. Discovered 28 days of system uptime with memory consumption at 94% due to orphaned background processes and accumulated sleep cycles. Cleaned temporary files (freed 8.4 GB), disabled unnecessary startup utilities, and executed a clean operating system reboot (shutdown /r /t 0) to reinitialize kernel state, device drivers, and user memory. Verified CPU idle at 4% and memory at 42%. Tested application launch times with user; confirmed performance restored."*

### 13. Interview Questions & Defensible Answers
- **Q: A user calls and says their computer is very slow. What is the very first thing you check?**  
  *A: "I start by checking system uptime in Task Manager or via PowerShell. In Windows 10 and 11, Fast Startup (hybrid boot) means clicking 'Shut Down' closes user applications but hibernates the Windows kernel and drivers to hiberfil.sys. If the computer has high uptime because the user only clicks shut down or uses sleep, driver states and kernel memory pools persist without re-initialization. Clicking 'Restart' or running `shutdown /r /t 0` forces a complete teardown and reinitialization of both the kernel session and user session, resolving many slowness issues. If uptime is low, I then look at real-time resource utilization to see whether CPU, RAM, or Disk is pegged at 100%."*
- **Q: Does Fast Startup preserve running user applications like Word and Excel across shutdowns?**  
  *A: "No. Fast Startup logs off user sessions (e.g., Session 1), closing all user-mode applications and freeing user-mode RAM. It then hibernates the operating system kernel session and loaded device drivers. The reason uptime accumulates is that the kernel session was hibernated rather than cold-booted, meaning driver-level memory leaks in Non-Paged Pool or stale driver states persist, while user applications must be reopened upon next logon."*
