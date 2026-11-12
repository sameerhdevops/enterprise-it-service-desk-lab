# Troubleshooting Runbook: USB Device Not Recognised
**Incident ID:** INC-W011  
**Category:** Windows Support / Peripherals  
**Target Systems:** Windows 11 / Windows 10  

---

### 1. Reported Symptom
User reports: *"When I plug in my USB headset / mouse / flash drive, Windows makes the error chime and shows a toast notification: 'USB device not recognized. The last USB device you connected to this computer malfunctioned, and Windows does not recognize it'."*

### 2. User Impact
User cannot use external input devices or headset during customer calls. Single user affected. Priority: P3.

### 3. Initial Questions
1. Does this happen on all USB ports or just one specific port?
2. Does this USB device work when plugged into a different computer?
3. Are you plugging directly into the laptop or through a USB hub / docking station?

### 4. Investigation Sequence
1. Test device in a different physical USB port (e.g., USB 3.0 Type-A vs Type-C).
2. Check Device Manager > **Universal Serial Bus controllers** for "Unknown USB Device (Device Descriptor Request Failed)" or "Port Reset Failed".
3. Check USB Selective Suspend power settings (Windows aggressively puts idle USB root hubs to sleep on battery).
4. Inspect physical USB port on laptop for dust, lint, or bent connector pins.

### 5. Tools Required
- Device Manager (`devmgmt.msc`)
- Windows Power Options (`powercfg.cpl`)
- PowerShell (`Get-PnpDevice`)

### 6. Commands & Output Interpretation
Inspect USB controllers in error state:
```powershell
Get-PnpDevice -Class "USB" | Where-Object { $_.Status -ne "OK" } | Select-Object FriendlyName, InstanceId, Status, Problem
```
*Interpretation:* If `Problem` is `CM_PROB_FAILED_POST_START` (Code 43), the USB controller cannot communicate with device firmware or handshake failed.

Check USB Selective Suspend setting:
```cmd
powercfg /query SCHEME_CURRENT SUB_USB
```
*Interpretation:* Shows whether USB selective suspend is enabled on AC and battery power.

### 7. Expected Observations
- Healthy: When plugged in, device registers under USB controllers or Human Interface Devices (HID) as "USB Composite Device" with Status = OK.
- Fault: Device appears with yellow exclamation mark as "Unknown USB Device (Device Descriptor Request Failed)".

### 8. Possible Root Causes
1. **Insufficient USB Bus Power:** Device draws more current than the unpowered USB hub or laptop port provides.
2. **USB Selective Suspend Bug:** Windows power management suspended the USB root hub and failed to resume it.
3. **Dirty / Damaged Connector Pins:** Physical lint or debris inside USB port preventing clean electrical contact.
4. **Corrupted USB Root Hub Driver:** USB hub driver in Windows kernel entered a deadlocked state.
5. **Defective Peripheral Hardware:** Broken internal cable or failed controller chip inside the USB device.

### 9. Corrective Action
1. **Bypass Hub / Dock:** Plug device directly into a motherboard USB port without intermediaries.
2. **Disable USB Selective Suspend:**
   - Open `control.exe powercfg.cpl` > Change plan settings > Change advanced power settings > **USB settings** > **USB selective suspend setting** > Set to **Disabled**.
3. **Reinstall USB Controllers in Device Manager:**
   - In `devmgmt.msc`, expand *Universal Serial Bus controllers*.
   - Right-click **USB Root Hub (USB 3.0)** > click **Uninstall device**.
   - Restart the computer; Windows will automatically reinstall all USB root controllers upon reboot.
4. **Clear Static Charge (Cold Reset):**
   - Disconnect charger, power off laptop, hold power button down for 30 seconds to drain motherboard capacitors, then power back on.

### 10. Verification Procedure
- Plug USB peripheral back into the laptop port.
- Verify standard Windows connect chime sounds and no error notifications appear.
- Device Manager displays device cleanly under Human Interface Devices / Audio without warnings.
- Test peripheral functionality (audio playback, mouse movement).

### 11. Escalation Conditions
- Escalate to **L2 Desktop Support** if all USB ports on the laptop motherboard have ceased supplying 5V power (hardware motherboard failure).

### 12. Ticket Resolution Notes
> *"Troubleshot 'USB device not recognized' error on user laptop. Issue isolated to aggressive Windows USB selective suspend disabling USB 3.0 Root Hub during battery operation. Reinstalled USB Root Hub drivers in Device Manager and disabled USB selective suspend in active power profile. Tested headset across both USB ports; confirmed functional."*

### 13. Interview Questions & Defensible Answers
- **Q: What does 'USB device descriptor request failed' mean, and what are your troubleshooting steps?**  
  *A: "It means Windows sent an initial electrical signal to the USB device to ask for its identification descriptor (who manufactured it, what device type it is), but the device failed to respond or the data was corrupted. My steps are: 1) Test on a different port and bypass any docking station. 2) Test the device on another known-good PC to rule out physical device failure. 3) Uninstall the USB Root Hub in Device Manager and reboot so Windows rebuilds the USB bus stack. 4) Disable USB selective suspend in Power Options."*
