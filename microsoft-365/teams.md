# Microsoft Teams Troubleshooting Guide for L1 Support
**Document ID:** M365-TMS-001  
**Audience:** L1 Service Desk Analysts  
**Scope:** Microsoft Teams Desktop Client (Classic & New Teams), Audio/Video Devices, Cache Clearing

---

## 1. Microsoft Teams Architecture & Editions
- **New Teams (v2):** Built on WebView2 and React, packaged as an MSIX Windows App (`ms-teams.exe`). Significantly lower memory and CPU footprint compared to classic Electron-based Teams.
- **Classic Teams (v1):** Packaged under `%LOCALAPPDATA%\Microsoft\Teams`.

---

## 2. Common Scenarios & L1 Troubleshooting Workflows

### Scenario A: Microphone / Headset Not Working in Meetings
1. **In-App Device Settings:**
   - In Teams, click three dots `...` next to profile picture > **Settings > Devices**.
   - Verify correct **Audio devices**, **Speaker**, and **Microphone** are selected (not "Default Communication Device" if switching between laptop mic and USB headset).
   - Click **Make a test call**. Listen for playback verification.
2. **Windows Privacy & Microphone Permissions:**
   - Open Settings > Privacy & security > **Microphone**.
   - Ensure **"Microphone access"** is toggled ON.
   - Ensure **"Let apps access your microphone"** and **"Let desktop apps access your microphone"** are both toggled ON.
3. **Exclusive Mode Conflict:**
   - Open `mmsys.cpl` (Sound Control Panel) > **Recording** tab > select microphone > **Properties > Advanced**.
   - Uncheck **"Allow applications to take exclusive control of this device"** (prevents Zoom or other apps from locking the audio driver).

---

### Scenario B: Clearing Microsoft Teams Cache (The #1 L1 Fix)
Corrupted local caching causes persistent glitches: status stuck on "Away", inability to send messages, white screen on launch, or meeting connection timeouts.

#### For New Teams (MSIX):
```powershell
# Reset app via Windows Settings / PowerShell
Get-AppxPackage *MSTeams* | Reset-AppxPackage
```
*Or manual cache folder purge:*
```cmd
taskkill /F /IM ms-teams.exe
rmdir /S /Q "%LOCALAPPDATA%\Packages\MSTeams_8wekyb3d8bbwe\LocalCache"
```

#### For Classic Teams:
```cmd
taskkill /F /IM teams.exe
rmdir /S /Q "%APPDATA%\Microsoft\Teams"
```
*Verification:* Relaunch Teams. User will be prompted to sign in with modern authentication; all chat history and channels are retained in the cloud.

---

### Scenario C: Sign-In Loops & Credential Conflicts
When Teams is stuck on "Signing in..." or repeatedly prompts for credentials:
1. Open Windows Credential Manager (`control keymgr.dll`).
2. Navigate to **Windows Credentials**.
3. Under Generic Credentials, locate and delete all entries beginning with:
   - `msteams_authtoken`
   - `MicrosoftAccount:user=`
   - `MicrosoftOffice16_Data:ADAL:`
4. In Windows Settings > Accounts > **Access work or school**, verify company account is listed without connection error alerts.
