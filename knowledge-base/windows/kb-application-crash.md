# Standard Knowledge Base Article: Investigating & Resolving Application Crashes
**KB ID:** KB0012  
**Category:** Windows / Applications  
**Author:** Sameer Kulkarni (L1 Support)  
**Last Reviewed:** 2024-11-12  

---

### Symptoms
- Application (e.g., Excel, Outlook, SAP GUI, internal billing software) abruptly closes without warning.
- Windows pop-up dialog says: "The application has stopped working and needs to close."
- Application crashes consistently when performing a specific action (e.g., File > Open, Export to PDF).

### Applicable Systems
- Windows 11 Enterprise / Windows 10 Pro desktop client software.

### Prerequisites
- Event Viewer inspection rights; standard user credentials for testing.

### Troubleshooting Steps
1. **Test Application in Safe Mode:**
   - For Microsoft Office: Run `excel.exe /safe` or `outlook.exe /safe`.
   - If the application runs stably in Safe Mode, a third-party COM Add-in is the root cause.
2. **Examine Event Viewer Application Log:**
   - Launch `eventvwr.msc` > Windows Logs > **Application**.
   - Filter for Event ID **1000** (Application Error).
   - Identify:
     - **Faulting application name:** (e.g., `EXCEL.EXE`)
     - **Faulting module name:** (e.g., `VCRUNTIME140.dll`, `KERNELBASE.dll`, or a vendor `.dll`)
     - **Exception code:** (e.g., `0xc0000005` = memory access violation).

### Resolution
- **If Add-In is Responsible:**
  - Launch app > File > Options > Add-ins > Manage: **COM Add-ins** > click Go > uncheck suspicious add-ins.
- **If Microsoft Office Suite Corrupted:**
  - Control Panel > Programs and Features > select Microsoft 365 Apps > click **Change** > select **Quick Repair** (3-minute local binary scan).
- **If Visual C++ Runtime Corrupted:**
  - Control Panel > Programs and Features > select Microsoft Visual C++ 2015-2022 Redistributable > Change > **Repair**.

### Verification
- Launch application from Start Menu; verify UI opens smoothly.
- Perform the exact action that previously crashed the app (e.g., opening large report); confirm zero crashes.
- Inspect Event Viewer; verify no new Event ID 1000 entries are generated.

### Escalation Instructions
- Escalate to **L2 Application Support** if the proprietary software crashes with an unhandled database exception requiring vendor code patch.

### Related Incidents
- INC0003, INC-W008, WIN-SW-001
