# Troubleshooting Runbook: High Memory Consumption
**Incident ID:** INC-W003  
**Category:** Windows Support / Performance  
**Target Systems:** Windows 11 / Windows 10  

---

### 1. Reported Symptom
User reports: *"Windows gave me a warning message saying 'Your computer is low on memory'. Apps are closing automatically and Chrome tabs keep showing an 'Aw, Snap! Out of Memory' screen."*

### 2. User Impact
High individual impact. Unsaved work in active applications is lost when Windows aggressively terminates processes to prevent OS kernel crash. Priority: P2/P3.

### 3. Initial Questions
1. How many browser tabs and open applications do you typically keep running?
2. Did a specific program crash immediately before or during the warning dialog?
3. What is the total RAM installed on this laptop (e.g., 8 GB vs 16 GB)?

### 4. Investigation Sequence
1. Open Task Manager > **Performance** tab > **Memory**.
2. Note the metrics: **In use**, **Available**, **Committed** (e.g., 15.2 / 18.0 GB), and **Paged / Non-paged pool**.
3. Switch to **Processes** tab and sort by **Memory** descending to locate consumer processes.
4. If process RAM usage does not add up to physical memory usage, check for a kernel memory leak in **Non-paged pool** (often caused by faulty network/graphics drivers).

### 5. Tools Required
- Task Manager (`taskmgr`)
- Resource Monitor (`resmon`)
- PowerShell (`Get-Process`, `Get-CimInstance`)
- RAMMap (Sysinternals - optional/reference)

### 6. Commands & Output Interpretation
Inspect top memory-consuming processes:
```powershell
Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 10 ProcessName, Id, @{N="WorkingSetMB";E={[math]::Round($_.WorkingSet64/1MB,2)}}
```
*Interpretation:* `WorkingSet64` represents physical RAM currently allocated to the process. If a single process (e.g., `Teams.exe` or `java.exe`) is holding > 4 GB, it may have an unconstrained memory leak.

Inspect kernel pool memory:
```powershell
Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize, FreePhysicalMemory, @{N="NonPagedPoolMB";E={[math]::Round($_.TotalVisibleMemorySize - $_.FreePhysicalMemory,2)}}
```
*Interpretation:* In Task Manager > Performance > Memory, if "Non-paged pool" is over 500 MB–1 GB, a kernel-level driver leak is holding memory that cannot be paged to disk.

### 7. Expected Observations
- Healthy: Memory usage stable at 40%–70% under standard productivity workload.
- Fault state: Memory committed reaches 95%–100%, pagefile is exhausted, and `svchost.exe` or third-party apps exhibit linear upward RAM growth.

### 8. Possible Root Causes
1. **Application Memory Leak:** Software bug where memory requested by an application is never freed after use.
2. **Excessive Browser Workload:** 40+ active tabs with rich media/web applications in Chromium browsers.
3. **Driver Non-Paged Pool Leak:** Outdated network card driver (e.g., Killer Network or older Intel Wi-Fi drivers).
4. **Paging File Disabled or Too Small:** User or script disabled `pagefile.sys`, preventing Windows from offloading cold memory pages.

### 9. Corrective Action
1. Close unnecessary browser tabs and restart heavy productivity apps (Teams, Outlook).
2. Check Windows Virtual Memory (Paging File) settings:
   - Run `sysdm.cpl` > Advanced > Performance Settings > Advanced > Virtual Memory.
   - Ensure **"Automatically manage paging file size for all drives"** is checked.
3. If Non-paged pool is bloated, update the host Wi-Fi and chipset drivers via Device Manager or vendor updater.
4. Perform a clean restart to flush physical RAM and reset the pagefile.

### 10. Verification Procedure
- In Task Manager, verify memory utilization drops to baseline (30%–50%).
- Confirm available physical RAM exceeds 8 GB (on a 16 GB system).
- Reopen normal working applications; verify no low memory warnings recur.

### 11. Escalation Conditions
- Escalate to **L2 Desktop Support** if hardware RAM upgrade (from 8 GB to 16 GB) is required for the user's workload, or if diagnostic tests indicate faulty physical RAM modules.

### 12. Ticket Resolution Notes
> *"Investigated low memory warnings on user workstation. Observed memory usage at 96% with MS Teams holding 3.8 GB due to a known caching memory leak, combined with 45 open Chrome tabs. Enabled automatic paging file management which had been restricted to 1024 MB. Cleared Teams client cache and performed system reboot. Memory utilization stabilized at 38% at idle."*

### 13. Interview Questions & Defensible Answers
- **Q: What is the difference between physical RAM and virtual memory?**  
  *A: "Physical RAM is the high-speed hardware memory installed on the motherboard where active programs and data reside. Virtual memory is an OS memory management technique that combines physical RAM with temporary disk space (the Windows paging file, pagefile.sys). When physical RAM becomes full, Windows moves inactive memory pages to the paging file to free up physical RAM for active processes."*
