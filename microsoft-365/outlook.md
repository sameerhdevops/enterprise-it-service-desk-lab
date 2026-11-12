# Microsoft Outlook Troubleshooting Guide for L1 Support
**Document ID:** M365-OUT-001  
**Audience:** L1 Service Desk Analysts  
**Scope:** Outlook 365 Desktop Client, Exchange Online, Cached Mode, Mailbox Synchronization

---

## 1. Outlook Architecture: Cached Exchange Mode vs. Online Mode

In enterprise environments using Microsoft 365, Outlook operates by default in **Cached Exchange Mode**:
- An offline local copy of the user's Exchange mailbox is stored in an Offline Storage Table file (`.ost`) located at:  
  `C:\Users\<username>\AppData\Local\Microsoft\Outlook\<email>.ost`.
- Changes made offline sync bidirectionally when connected to the internet.
- **Online Mode:** Connects directly to Exchange Online servers with zero local caching. Useful for shared kiosk PCs or RDS/virtual desktop servers where local disk space is constrained.

---

## 2. Common Scenarios & L1 Troubleshooting Workflows

### Scenario A: Outlook Won't Open / Freezes on "Processing" or "Loading Profile"
1. **Launch in Safe Mode:**
   - Press `Windows Key + R` > type `outlook.exe /safe` > press Enter.
   - *If Outlook opens in Safe Mode:* A third-party COM Add-in is crashing the client.
   - *Resolution:* Go to File > Options > Add-ins > Manage **COM Add-ins** > Go > uncheck suspicious add-ins (e.g., outdated Adobe PDF Maker, CRM add-in, anti-spam toolbar) > restart Outlook normally.
2. **Reset Navigation Pane:**
   - If profile gets stuck loading views: Run `outlook.exe /resetnavpane` (clears and regenerates corrupted navigation pane settings).
3. **Clean Free/Busy View:**
   - Run `outlook.exe /cleanfreebusy`.

---

### Scenario B: Mailbox Not Synchronizing / Disconnected Status
1. Check the bottom right status bar of Outlook:
   - `Connected to: Microsoft Exchange` — Working normally.
   - `Disconnected` or `Trying to connect...` — Network loss or authentication token expired.
   - `Need Password` — Modern authentication prompt blocked behind another window.
2. **Verify Web Access (OWA First Rule):**
   - Direct the user to log into Outlook on the Web ([https://outlook.office.com](https://outlook.office.com)).
   - *If email works in OWA:* The user's account, license, and Exchange server are 100% operational. The issue is isolated to the local desktop client or local network connection.
   - *If email fails in OWA:* Account is locked, license is expired, or Exchange Online service outage is ongoing.

---

### Scenario C: Corrupted Outlook Profile (Recreating the Profile)
When an existing profile is corrupted beyond repair:
1. Close Outlook completely.
2. Open Windows Control Panel (`control.exe`) > search for **Mail** > click **Mail (Microsoft Outlook)**.
3. In the Mail Setup window, click **Show Profiles...**
4. Click **Add...** > enter a new profile name (e.g., `Nexora-New`).
5. Complete the auto-account setup wizard using the employee's corporate email and password.
6. Set **"Always use this profile"** to the newly created profile.
7. Open Outlook; Exchange will create a fresh local `.ost` file and download emails from the cloud.

---

### Scenario D: Repairing or Rebuilding the Local OST File
```cmd
:: 1. Close Outlook completely
taskkill /F /IM outlook.exe

:: 2. Rename existing OST file to force Outlook to regenerate it upon launch
ren "%LOCALAPPDATA%\Microsoft\Outlook\*.ost" "*.ost.old"
```
*Note:* In modern Outlook 365, do not waste hours running the legacy `scanpst.exe` utility on `.ost` files. Because Exchange Online stores the master copy in the cloud, deleting or renaming the damaged `.ost` file allows Outlook to cleanly re-download an exact server copy.
