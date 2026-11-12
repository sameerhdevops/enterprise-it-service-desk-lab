# Troubleshooting Runbook: Hardware Device Driver Issue
**Incident ID:** INC-W010  
**Category:** Windows Support / Hardware & Drivers  
**Target Systems:** Windows 11 / Windows 10  

---

### 1. Reported Symptom
User reports: *"My laptop's built-in webcam / audio / Wi-Fi stopped working after a recent update. In Device Manager, there is a yellow exclamation mark next to the device."*

### 2. User Impact
User cannot participate in video meetings or connect wirelessly. Moderate urgency. Priority: P3.

### 3. Initial Questions
1. When did the device stop functioning?
2. Did Windows run any updates just before this happened?
3. Did any external software or driver update utility get installed?

### 4. Investigation Sequence
1. Open Device Manager (`devmgmt.msc`).
2. Locate the device with the yellow exclamation mark (or check under 'Other devices' for 'Unknown device').
3. Right-click device > **Properties** > **General** tab to read the **Device status** error code (e.g., Code 10, Code 28, Code 43).
4. Review **Events** tab to see recent driver installation timestamps and errors.
5. Check the **Details** tab > select **Hardware Ids** to identify the Vendor ID (`VEN_xxxx`) and Device ID (`DEV_xxxx`).

### 5. Tools Required
- Device Manager (`devmgmt.msc`)
- PowerShell (`Get-PnpDevice`)
- Official vendor driver packages (HP / Dell / Lenovo support portals)

### 6. Commands & Output Interpretation
List all malfunctioning devices with error codes via PowerShell:
```powershell
Get-PnpDevice -Status "Error", "Degraded", "Unknown" | Select-Object FriendlyName, InstanceId, Class, Status, Problem
```
*Interpretation:* `Problem` column corresponds to standard Windows Device Manager error codes:
- `CM_PROB_FAILED_START` (Code 10): Device cannot start (often hardware or firmware mismatch).
- `CM_PROB_FAILED_INSTALL` (Code 28): Drivers for this device are not installed.
- `CM_PROB_DEVICE_FAILED` (Code 43): Device driver notified the OS that hardware reported failure.

Find hardware ID string for an unknown device:
```powershell
(Get-PnpDevice -FriendlyName "*Unknown*").InstanceId
```
*Interpretation:* A string like `PCI\VEN_8086&DEV_02F0` indicates Vendor `8086` (Intel Corporation) and Device `02F0` (Intel Wi-Fi 6 AX201).

### 7. Expected Observations
- Healthy: All devices in `devmgmt.msc` display normal icons with status *"This device is working properly."*
- Fault: Yellow triangle with exclamation mark, Code 10/28/43 displayed in device status.

### 8. Possible Root Causes
1. **Generic / Incompatible Driver Pushed by Windows Update:** Windows Update replaced a certified vendor OEM driver with an incompatible generic build.
2. **Missing Driver on Re-imaged Machine:** System was reinstalled without chipset or peripheral driver package (Code 28).
3. **Corrupted Driver Cache in DriverStore:** `C:\Windows\System32\DriverStore\FileRepository` contains damaged INF package.
4. **Hardware Failure / Loose Connection:** Physical ribbon cable loose or internal component failure.

### 9. Corrective Action
1. **Roll Back Driver (First Line Fix):**
   - In Device Manager > Device Properties > **Driver** tab > click **Roll Back Driver**.
   - If available, this immediately restores the previous working version.
2. **Uninstall and Scan for Hardware Changes:**
   - Right-click device > **Uninstall device** > check *"Attempt to remove the driver for this device"* if rollback failed.
   - Click **Action > Scan for hardware changes** to allow Windows to re-enumerate and install a fresh driver copy.
3. **Install OEM Manufacturer Driver:**
   - Download certified driver installer directly from HP/Dell/Lenovo official enterprise support portal using laptop serial number.
   - Run vendor installer executable as administrator.

### 10. Verification Procedure
- In Device Manager, verify yellow exclamation mark vanishes.
- Device status displays: *"This device is working properly."*
- Test physical device: launch Windows Camera app to verify video feed, or connect to office Wi-Fi network.

### 11. Escalation Conditions
- Escalate to **L2 Desktop Support** if OEM driver fails to initialize and hardware diagnostics in BIOS/UEFI indicate component failure requiring motherboard/module replacement.

### 12. Ticket Resolution Notes
> *"Addressed yellow exclamation mark on Intel Wi-Fi adapter (Code 10) following Windows Update. Device failed to start due to incompatible generic Microsoft driver build. Performed Roll Back Driver to restore certified OEM HP driver build. Re-scanned hardware; Wi-Fi adapter initialized successfully and connected to corporate SSID. Verified throughput."*

### 13. Interview Questions & Defensible Answers
- **Q: What does a yellow exclamation mark in Device Manager indicate, and how do you find the right driver if it says 'Unknown Device'?**  
  *A: "A yellow exclamation mark indicates a driver problem or hardware conflict—such as Code 28 (no driver installed) or Code 10 (device failed to start). If the device is listed as 'Unknown Device', I right-click it, go to Properties, switch to the Details tab, and select 'Hardware Ids' from the dropdown. I look for the VEN (Vendor) and DEV (Device) codes. For example, VEN_8086 is Intel and VEN_10EC is Realtek. I can search the hardware ID or use the vendor's serial number support portal to download the exact certified driver."*
