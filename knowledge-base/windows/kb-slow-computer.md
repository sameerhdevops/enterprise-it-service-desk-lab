# Standard Knowledge Base Article: Troubleshooting Slow Windows Workstation
**KB ID:** KB0001  
**Category:** Windows / Performance  
**Author:** Nexora IT Service Desk (L1 Support)  
**Last Reviewed:** 2024-11-12  

---

### Symptoms
- Workstation takes > 3 minutes to boot or launch basic applications (Outlook, Chrome, Excel).
- Mouse cursor freezes intermittently; fan continuously spins at high speed.
- Task Manager reflects sustained 90%+ CPU, Memory, or Disk utilization.

### Applicable Systems
- Windows 11 Enterprise (22H2 / 23H2 / 24H2)
- Windows 10 Pro / Enterprise (21H2 / 22H2)
- Dell Latitude, HP EliteBook, Lenovo ThinkPad standard corporate models

### Prerequisites
- Standard local user access for initial diagnostics.
- Administrative credentials for temp folder cleanup, SFC/DISM, or services restart.

### Troubleshooting Steps
1. **Check System Uptime:**
   - Open Task Manager (`Ctrl + Shift + Esc`) > **Performance** tab > **CPU**.
   - Note the **Up time** counter (Days:Hours:Minutes).
   - If uptime exceeds 7 days, Fast Startup has preserved accumulated memory fragmentation.
2. **Identify Resource Consumers:**
   - On **Processes** tab, click **CPU**, **Memory**, and **Disk** column headers to sort by top consumers.
   - If a third-party application (e.g., Chrome, Teams) is consuming > 80% CPU or > 4 GB RAM, terminate it via **End task**.
3. **Check Free Disk Space:**
   - Open File Explorer > This PC. Ensure drive `C:` has at least 15% free capacity.
4. **Inspect Startup Items:**
   - In Task Manager > **Startup apps**, disable non-essential startup utilities (Spotify, personal updaters).
5. **Run Disk & Component Cleanup:**
   - Run `cleanmgr.exe /d c:` to remove temporary files and cached Windows Update files.

### Resolution
- Execute a clean operating system restart via Command Prompt: `shutdown /r /t 0`.
- If system corruption is suspected, execute elevated repair:
  ```cmd
  sfc /scannow
  ```

### Verification
- Reopen Task Manager; confirm CPU idle baseline settles below 10% and RAM below 65%.
- Launch Outlook and Excel; verify applications open within 5 seconds.
- User verbally confirms workstation is responsive.

### Escalation Instructions
- If SSD/HDD disk activity remains pegged at 100% with read/write speeds below 1 MB/s, escalate to **L2 Desktop Support** for SMART hardware diagnostic scan (failing drive).

### Related Incidents
- INC0001, INC-W001, INC-W002, INC-W003
