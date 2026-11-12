# Standard Knowledge Base Article: Resolving Microsoft OneDrive Synchronization Failures
**KB ID:** KB0009  
**Category:** Microsoft 365 / OneDrive  
**Author:** Sameer Kulkarni (L1 Support)  
**Last Reviewed:** 2024-11-12  

---

### Symptoms
- OneDrive cloud icon in taskbar displays a red circle with an X or gray paused status.
- Files in File Explorer have red X status icon or are permanently stuck on blue syncing arrows.
- Error message displays: "OneDrive is full" or "A file with this name already exists in this location".

### Applicable Systems
- Microsoft OneDrive for Business desktop client on Windows 10/11 Enterprise.

### Prerequisites
- Standard user access.

### Troubleshooting Steps
1. **Inspect Cloud Storage Quota:**
   - Click the OneDrive cloud icon in the taskbar > click the gear icon (Settings) > Settings.
   - Look at the storage bar in the bottom-left corner (e.g., 850 GB used of 1024 GB).
   - If quota is 100% full, user must delete old files or request a storage expansion.
2. **Identify Problematic Files:**
   - Click OneDrive icon in taskbar; view the active banner at the top detailing specific failed filenames.
   - Look for prohibited characters in filenames: `" * : < > ? / \ |`
   - Look for file path length exceeding 400 characters.
3. **Verify File Lock Status:**
   - If an Office document is open in background memory (`excel.exe`), OneDrive cannot obtain a read lock. Close the application via Task Manager.

### Resolution
- **Official OneDrive Sync Reset Sequence:**
  Execute via Command Prompt or Run dialog:
  ```cmd
  :: Step 1: Execute Microsoft reset utility
  "%LOCALAPPDATA%\Microsoft\OneDrive\onedrive.exe" /reset

  :: Step 2: If OneDrive does not relaunch automatically after 2 minutes:
  "%LOCALAPPDATA%\Microsoft\OneDrive\onedrive.exe"
  ```
  *(Note: This forces OneDrive to perform a full cloud catalog re-hash. No local user files are deleted).*

### Verification
- OneDrive taskbar icon returns to solid blue cloud.
- Hovering over icon displays: "OneDrive is up to date".
- Save a new test text document into `C:\Users\<user>\OneDrive - Nexora Technologies\`; verify green checkmark appears within 10 seconds.

### Escalation Instructions
- Escalate to **L2 Application / SharePoint Administrator** if tenant-wide SharePoint library sync policies block specific document libraries.

### Related Incidents
- M365-OD-001, INC-W004
