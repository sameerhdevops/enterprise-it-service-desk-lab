# Microsoft OneDrive for Business Troubleshooting Guide
**Document ID:** M365-OD-001  
**Audience:** L1 Service Desk Analysts  
**Scope:** OneDrive Sync Client, Files On-Demand, Sync Conflicts, Known Folder Move (KFM)

---

## 1. OneDrive Sync Client Fundamentals & Status Icons

In Windows File Explorer, OneDrive displays distinct status icons under the **Status** column:

| Icon | Name | Meaning | Local Disk Usage |
|---|---|---|---|
| ☁️ **Blue Cloud** | Online-only file | File exists only in OneDrive cloud. Double-clicking downloads it on-demand. | 0 bytes on local disk. |
| 🟢 **Green Tick (White circle)** | Locally available | File was opened and temporarily cached locally. Can be turned back into online-only. | Consumes local disk space. |
| 🟢 **Solid Green Circle (White tick)** | Always available | User right-clicked and selected "Always keep on this device" (pinned offline). | Permanently consumes local disk space. |
| 🔄 **Sync Arrows** | Syncing | File is currently uploading or downloading. | Active network transfer. |
| 🔴 **Red X Circle** | Sync Error | File cannot sync due to name invalid characters, file lock, or quota limit. | Blocked. |

---

## 2. Common Scenarios & L1 Troubleshooting Workflows

### Scenario A: File Won't Sync (Red X Error)
1. **Invalid Characters / File Name Length:**
   - OneDrive restricts file names containing: `" * : < > ? / \ |`
   - Maximum path length cannot exceed 400 characters.
2. **File Locked Open by Another Application:**
   - If an Excel file is open in another program or stuck in background memory, OneDrive cannot obtain a read lock. Close the application or kill the process in Task Manager.
3. **OneDrive Storage Limit Exceeded:**
   - Standard business license grants 1 TB. Check available quota via OneDrive Web portal > Settings > More Settings > Storage Metrics.

---

### Scenario B: Resetting the OneDrive Sync Client
When OneDrive hangs indefinitely on "Looking for changes" or "Processing changes":

```cmd
:: Step 1: Close OneDrive
taskkill /F /IM onedrive.exe

:: Step 2: Execute official Microsoft reset command
"%LOCALAPPDATA%\Microsoft\OneDrive\onedrive.exe" /reset

:: Step 3: If OneDrive does not restart automatically after 2 minutes, launch manually:
"%LOCALAPPDATA%\Microsoft\OneDrive\onedrive.exe"
```
*Note:* Running `/reset` disconnects all current sync connections, re-indexes existing local files against the cloud copy, and clears internal sync databases without deleting any personal files.

---

### Scenario C: Known Folder Move (KFM) Redirection Issues
In corporate setups, Desktop, Documents, and Pictures are redirected into OneDrive cloud storage:
- If a user reports missing desktop icons after signing in to a new laptop, ensure OneDrive is signed in and KFM is turned on:
  - In OneDrive Settings > **Sync and backup > Manage backup**.
  - Toggle ON: *Desktop*, *Documents*, *Pictures* > click **Save changes**.
