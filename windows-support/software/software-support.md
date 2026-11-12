# Enterprise Software Support & Application Management
**Document ID:** WIN-SW-001  
**Audience:** L1 Service Desk Analysts  
**Scope:** Application Lifecycle, Repair, Clean Uninstallation, Compatibility

---

## 1. Application Management Principles for L1

Enterprise endpoints run a combination of standardized business tools (Microsoft 365, Teams, Edge/Chrome, GlobalProtect VPN) and department-specific line-of-business applications.

### Standard User Privileges vs. Administrative Elevation
In a secured enterprise environment (like Nexora Technologies):
- End users have **Standard User** accounts to prevent malware persistence and unauthorized software installations.
- All installation tasks requiring writes to `C:\Program Files` or `HKLM` require elevation using an authorized L1 Service Desk admin account or automated deployment via Endpoint Management (Intune/MECM).

---

## 2. Silent & Scripted Application Installation

For standardized deployments and remote assistance, L1 technicians utilize silent command-line flags to avoid user prompts:

### MSI Installers (Windows Installer)
```cmd
msiexec /i "\\nexfs01\deploy\ZoomClient.msi" /qn /norestart ALLUSERS=1
```
- `/i`: Install package
- `/qn`: Quiet mode, no user interface
- `/norestart`: Suppresses unexpected client reboot
- `ALLUSERS=1`: Installs for all users on the machine

### EXE Installers
Common vendor flags:
- Inno Setup: `/VERYSILENT /SUPPRESSMSGBOXES /NORESTART`
- InstallShield: `/s /v"/qn"`
- Nullsoft (NSIS): `/S` (case-sensitive uppercase)

---

## 3. Repairing Broken Applications

Before performing a time-consuming uninstall and reinstall:
1. **Windows Settings Repair:**
   - Open Settings > Apps > Installed apps > Click three dots next to app > **Advanced options** > click **Repair** (preserves user data) or **Reset** (clears local app data).
2. **Microsoft 365 Repair:**
   - Control Panel > Programs and Features > select Microsoft 365 Apps > click **Change**.
   - **Quick Repair:** Fixes most issues within 3 minutes by verifying local binaries (offline).
   - **Online Repair:** Complete re-download and reinstall of Office suite without touching user emails or files (requires 15–20 minutes and active internet).

---

## 4. Completely Removing Stubborn Software

When standard uninstallation fails with error popups or leaves behind locked files:
1. Boot into **Safe Mode** (`msconfig` > Boot > Safe boot > Minimal) and run the uninstaller.
2. Manually clean remaining user profile fragments:
   - `C:\Users\<user>\AppData\Local\<Vendor>`
   - `C:\Users\<user>\AppData\Roaming\<Vendor>`
   - `C:\ProgramData\<Vendor>`
