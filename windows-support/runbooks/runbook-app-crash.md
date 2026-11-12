# Troubleshooting Runbook: Application Crash
**Incident ID:** INC-W008  
**Category:** Windows Support / Software  
**Target Systems:** Windows 11 / Windows 10  

---

### 1. Reported Symptom
User reports: *"Every time I launch our accounting software or open a specific Excel workbook, the window flashes for a second and then vanishes completely with an error message saying 'The application has stopped working'."*

### 2. User Impact
User unable to process daily billing or financial entries. Single user blocked. Priority: P3.

### 3. Initial Questions
1. Does the application crash immediately upon launch or only when opening a specific file?
2. Has this application ever worked properly on this machine, or is this a recent development?
3. Did any Windows updates, antivirus definitions, or other software installs occur just prior to this behavior?
4. Do any error codes or dialog boxes appear (e.g., `0xc0000005`, `Runtime Error`)?

### 4. Investigation Sequence
1. Attempt to launch the application in **Safe Mode** (if Office app, run `excel.exe /safe` or `outlook.exe /safe`) to rule out misbehaving add-ins.
2. Open Windows Event Viewer (`eventvwr.msc`) > Windows Logs > **Application**.
3. Filter for Event ID **1000 (Application Error)** and Event ID **1001 (Windows Error Reporting)**.
4. Note the critical diagnostic fields:
   - **Faulting application name** (e.g., `EXCEL.EXE`)
   - **Faulting module name** (e.g., `VCRUNTIME140.dll`, `KERNELBASE.dll`, `MSO.dll`, or a third-party add-in `.dll`)
   - **Exception code** (e.g., `0xc0000005` = Access Violation / Memory corruption).
5. Check if the faulting module belongs to Microsoft Visual C++ Redistributable or .NET Framework.

### 5. Tools Required
- Windows Event Viewer (`eventvwr.msc`)
- Command Prompt / PowerShell
- Control Panel (`appwiz.cpl`)
- Reliability Monitor (`perfmon /rel`)

### 6. Commands & Output Interpretation
Query recent application crash events via PowerShell:
```powershell
Get-WinEvent -FilterHashtable @{LogName='Application'; ProviderName='Application Error'; Id=1000} -MaxEvents 3 | Format-List TimeCreated, Message
```
*Interpretation:* Review the message. If the faulting module is an add-in DLL (e.g., `AdobePDF.dll` or an internal COM add-in), disabling that add-in will resolve the crash. If it is `VCRUNTIME140.dll`, the C++ runtime requires repair.

Open Windows Reliability Monitor:
```powershell
perfmon /rel
```
*Interpretation:* Provides an interactive timeline showing exact crash events lined up with software installations and updates.

### 7. Expected Observations
- Healthy: Application launches cleanly into memory, loads required DLL dependencies, renders UI.
- Fault: Event Viewer logs Event ID 1000 with detailed exception offset; process terminates immediately.

### 8. Possible Root Causes
1. **Corrupted Application Add-in / Plugin:** Third-party plugin (e.g., PDF printer, CRM plugin) crashing during host app initialization.
2. **Corrupted Visual C++ Redistributable or .NET Framework:** Required runtime libraries damaged or mismatched.
3. **Corrupted User Configuration Profile / Cache:** App preferences or local cache files in `AppData\Local` corrupted.
4. **Antivirus False Positive / Hooking Conflict:** Security agent terminating the process during DLL injection.
5. **Corrupted Application Binaries:** Missing or altered files in `Program Files`.

### 9. Corrective Action
1. **Test in Safe Mode / Without Add-ins:**
   - Run `excel.exe /safe`. If Excel launches without crashing, go to File > Options > Add-ins > Manage **COM Add-ins** > Go > Uncheck all add-ins > Re-enable one by one to isolate the culprit.
2. **Repair Application via Control Panel:**
   - Open `appwiz.cpl` > Select application (e.g., Microsoft 365 Apps) > Click **Change** > Select **Quick Repair** (or **Online Repair**).
3. **Repair Microsoft Visual C++ Runtimes:**
   - In `appwiz.cpl`, locate Microsoft Visual C++ 2015-2022 Redistributable > Click Change > **Repair**.
4. **Reset Application User Cache:**
   - Rename user configuration folder: `C:\Users\<user>\AppData\Roaming\<AppName>` to `<AppName>.old` to generate fresh defaults upon next launch.

### 10. Verification Procedure
- Launch the application normally from the Start Menu.
- Open test documents and execute typical user workflows (saving, exporting).
- Confirm zero crashes occur and Event Viewer logs no new Event ID 1000 entries.

### 11. Escalation Conditions
- Escalate to **L2 Application Support** if the proprietary line-of-business application has an unhandled code bug or requires database schema updates from the vendor.

### 12. Ticket Resolution Notes
> *"Troubleshot repeated crash of Microsoft Excel on user PC. Event Viewer Application log revealed Event ID 1000 pointing to faulting module AdobePDF.dll (COM Add-in). Tested Excel in Safe Mode successfully. Disabled the corrupted third-party PDF add-in from COM Add-ins list and updated Acrobat Reader to the latest build. Verified Excel opens normally and stable during testing."*

### 13. Interview Questions & Defensible Answers
- **Q: If an application is crashing and gives no error message on screen, how do you find out why it crashed?**  
  *A: "I open the Windows Event Viewer (`eventvwr.msc`) and navigate to the Application log. I look for Event ID 1000 with source 'Application Error'. In the event details, I examine two critical fields: the 'Faulting application name' and the 'Faulting module name'. The faulting module tells me whether the crash happened inside the app's own code or was caused by a specific DLL, such as a corrupted Visual C++ runtime, a graphics driver DLL, or a third-party add-in."*
