# Troubleshooting Runbook: Windows Service Failure
**Incident ID:** INC-W005  
**Category:** Windows Support / Operating System  
**Target Systems:** Windows 11 / Windows 10  

---

### 1. Reported Symptom
User reports: *"When I try to start our inventory client application, an error message pops up stating 'Error 1068: The dependency service or group failed to start', or 'Error 1053: The service did not respond to the start or control request in a timely fashion'."*

### 2. User Impact
Workstation cannot connect to internal services or run local database clients. Single-user productivity blocked. Priority: P3.

### 3. Initial Questions
1. Which specific application or feature is failing to launch?
2. Did this error appear after a recent reboot, Windows update, or password change?
3. What is the exact error code or dialog message displayed?

### 4. Investigation Sequence
1. Open the Services management console (`services.msc`).
2. Locate the failed service and inspect its **Status** (*Stopped*, *Starting*, or *Running*) and **Startup Type** (*Automatic*, *Manual*, *Disabled*).
3. Right-click the service > **Properties** > **Dependencies** tab to identify parent services required for operation.
4. Check the **Log On** tab to verify account credentials (e.g., `Local System`, `Network Service`, or a service account).
5. Open Event Viewer > Windows Logs > **System** and filter for Event Sources: `Service Control Manager` (Event IDs 7000, 7001, 7009, 7024).

### 5. Tools Required
- Services Management Console (`services.msc`)
- Event Viewer (`eventvwr.msc`)
- PowerShell (`Get-Service`, `Start-Service`, `Set-Service`)
- Command Prompt (`sc.exe`, `net.exe`)

### 6. Commands & Output Interpretation
Inspect service status and startup type using PowerShell:
```powershell
Get-Service -Name "Spooler" | Select-Object Name, DisplayName, Status, StartType
```
*Interpretation:* If `Status` is `Stopped` and `StartType` is `Disabled`, the service was intentionally or accidentally deactivated.

Check service dependencies:
```powershell
(Get-Service -Name "Spooler").RequiredServices
(Get-Service -Name "Spooler").DependentServices
```
*Interpretation:* `RequiredServices` lists services that MUST be running before this service can start. If any required service is stopped, Error 1068 will trigger.

Inspect Service Control Manager errors in Event Viewer:
```powershell
Get-WinEvent -FilterHashtable @{LogName='System'; ProviderName='Service Control Manager'; Level=2} -MaxEvents 5 | Select-Object TimeCreated, Id, Message
```
*Interpretation:* Event ID 7000 indicates a timeout or access denied; Event ID 7001 indicates a dependency failure.

### 7. Expected Observations
- Normal: Required background services show Status = `Running` and StartType = `Automatic`.
- Failure: Service status is blank (stopped) or stuck in `Starting`. Event Viewer logs explicit exit codes.

### 8. Possible Root Causes
1. **Dependency Service Stopped or Disabled:** One of the prerequisite services in the dependency chain is offline.
2. **Expired Service Account Credentials (Logon Failure):** The service is configured to run under a user/service account whose password expired (Event ID 7038 / Error 1069).
3. **Corrupted Binary Path or Missing DLL:** The executable path in the registry has been moved or corrupted.
4. **Permissions / Access Denied (Error 5):** The service account lacks "Log on as a service" user rights assignment.

### 9. Corrective Action
1. **Resolve Dependencies First:** Trace the dependency list and ensure all prerequisite services are set to *Automatic* and started.
2. **Update Logon Credentials:** If running under a specific account, go to Properties > **Log On**, re-enter the correct password, and click Apply.
3. **Configure Automatic Recovery:**
   - Go to Properties > **Recovery** tab.
   - Set *First failure* to **Restart the Service**.
   - Set *Second failure* to **Restart the Service**.
   - Reset fail count after: 1 day.
4. **Start Service via PowerShell:**
   ```powershell
   Set-Service -Name "<ServiceName>" -StartupType Automatic
   Start-Service -Name "<ServiceName>"
   ```

### 10. Verification Procedure
- In `services.msc`, confirm Status displays `Running`.
- Restart the machine and verify the service starts automatically without manual intervention.
- Launch the dependent client application and confirm successful operation with zero error popups.

### 11. Escalation Conditions
- Escalate to **L2 Application Support** or **L3 Infrastructure** if a custom line-of-business service fails to start due to internal database corruption or if code-level debugging is required.

### 12. Ticket Resolution Notes
> *"Investigated Error 1068 when user attempted to start line-of-business printing service. Discovered prerequisite RPC Endpoint Mapper dependency was intact, but HTTP service dependency had been set to Disabled. Re-enabled HTTP dependency to Automatic, started the service chain, and configured Service Control Manager recovery rules to restart on failure. Tested application launch; confirmed fully operational."*

### 13. Interview Questions & Defensible Answers
- **Q: What does 'Error 1068: The dependency service or group failed to start' mean, and how do you troubleshoot it?**  
  *A: "Error 1068 means the service you are trying to start relies on one or more prerequisite services that are currently stopped or disabled. To troubleshoot, I open services.msc, right-click the failing service, go to Properties, and look at the Dependencies tab. I then check each listed service in that tree to find which one is stopped, set its startup type to Automatic, start it, and then start the primary service."*
