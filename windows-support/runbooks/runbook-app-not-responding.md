# Troubleshooting Runbook: Application Not Responding (Hung Process)
**Incident ID:** INC-W014  
**Category:** Windows Support / Software  
**Target Systems:** Windows 11 / Windows 10  

---

### 1. Reported Symptom
User reports: *"My accounting software window is frozen. It says '(Not Responding)' in the title bar, the screen has gone slightly milky white, and the spinning blue circle appears whenever I click inside it."*

### 2. User Impact
User cannot input data or save open records. Fear of losing work if forcibly closed. Priority: P3.

### 3. Initial Questions
1. How long has the application been showing '(Not Responding)'?
2. Did you just trigger a large operation (such as generating an annual ledger report or importing a massive file)?
3. Do you have any unsaved work in other applications?

### 4. Investigation Sequence
1. Distinguish between an **actively processing** thread (busy calculating or waiting for network I/O) versus a **deadlocked** thread (hung indefinitely waiting for a resource that will never release).
2. Open Resource Monitor (`resmon.exe`) > **CPU** tab > expand **Processes** and locate the frozen process.
3. Right-click the process > select **Analyze Wait Chain**.
4. Review the Wait Chain tree:
   - If the process is waiting on another process (e.g., waiting for `splwow64.exe` or a network socket), that dependency is the actual bottleneck.
   - If the process is in a circular deadlock with itself, it will never recover.

### 5. Tools Required
- Task Manager (`taskmgr`)
- Resource Monitor (`resmon.exe`)
- Command Prompt / PowerShell (`taskkill`, `Stop-Process`)

### 6. Commands & Output Interpretation
Inspect process status and thread count using PowerShell:
```powershell
Get-Process -Name "excel" | Select-Object Name, Id, Responding, CPU, Threads
```
*Interpretation:* If `Responding` is `False`, the Windows message pump is not processing window messages. If `CPU` continues to increment, the process is still working and may recover if given 2–3 minutes. If `CPU` is 0.00 and disk I/O is 0, the thread is deadlocked.

Force terminate a hung process by PID via Command Prompt:
```cmd
taskkill /PID 9144 /F /T
```
*Interpretation:* `/F` forces termination, `/T` terminates all child processes spawned by the hung tree.

### 7. Expected Observations
- Normal: Window processes GUI messages; Responding = `True`.
- Hang: Window message queue fills up; Windows Desktop Window Manager (DWM) overlays a ghost window and appends "(Not Responding)".

### 8. Possible Root Causes
1. **Long-Running Synchronous Query:** Application executing a heavy database query or file read on the main UI thread instead of an asynchronous worker thread.
2. **Hung Print Driver Call:** App waiting for a printer driver (`splwow64.exe`) that is offline.
3. **Network Share Disconnection:** App trying to read from a mapped network drive that lost connectivity.
4. **Deadlocked Thread:** Two threads waiting for mutually exclusive locks on memory structures.

### 9. Corrective Action
1. **Wait 2–3 Minutes:** If the app is processing a large report, monitor CPU and Disk I/O in Resource Monitor. If I/O is active, advise user to allow it to finish.
2. **Analyze Wait Chain in Resource Monitor:**
   - In `resmon`, right-click process > **Analyze Wait Chain**.
   - If it is waiting on a non-critical child process (like a hung print spooler or browser helper), terminate ONLY that blocking sub-process to release the main application window without losing work.
3. **Graceful Close Attempt:** In Task Manager > Right-click > **End Task** (sends `WM_CLOSE` to allow the app to prompt to save).
4. **Forced Termination (If Deadlocked):**
   - Execute `Stop-Process -Name "<process>" -Force` or `taskkill /F /IM <process.exe>`.
5. **Recover AutoSaved Documents:** Launch app again and check the AutoRecover pane (e.g., in Office apps).

### 10. Verification Procedure
- Relaunch application from Start Menu.
- Confirm application window opens with clean responsive UI (no milkiness, immediate cursor response).
- Confirm user can perform standard actions without hanging.

### 11. Escalation Conditions
- Escalate to **L2 Application Support** if the application reliably hangs on a specific business operation every time (indicates a database lock or software bug).

### 12. Ticket Resolution Notes
> *"Addressed '(Not Responding)' hang on line-of-business ERP client. Used Resource Monitor Analyze Wait Chain to discover the main ERP process was blocked waiting on a deadlocked 32-bit print driver component (splwow64.exe). Terminated the blocked print component, which immediately returned the ERP window to responsive state without terminating the application or losing unsaved invoice data. Verified with user."*

### 13. Interview Questions & Defensible Answers
- **Q: What is the 'Analyze Wait Chain' feature in Windows Resource Monitor, and when would you use it?**  
  *A: "Analyze Wait Chain is a diagnostic tool in Resource Monitor that shows which threads or processes an unresponsive application is waiting for. For example, if Word says '(Not Responding)', rather than instantly killing it and losing the user's unsaved document, I check the Wait Chain. It might reveal Word is simply waiting on a hung network printer process or an antivirus scanner. If I terminate that specific blocking sub-thread, the main application often unlocks immediately and work is saved."*
