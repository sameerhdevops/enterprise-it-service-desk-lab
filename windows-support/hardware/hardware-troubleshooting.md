# Hardware Troubleshooting Guide for L1 Support
**Document ID:** WIN-HW-001  
**Audience:** L1 Support Engineers / Desktop Support  
**Scope:** Laptops, Desktops, Monitors, Peripherals (Nexora Technologies Fleet)

---

## 1. Laptop Power & Battery Issues

### Symptoms & Diagnosis
- **Laptop does not power on (No POST):**
  - Check charging LED when AC adapter is plugged in.
  - If LED is OFF: Test with known-good power adapter and different wall outlet. Inspect AC adapter barrel/USB-C pin for physical bends.
  - If LED is ON but screen remains black and power button does not respond: Perform **Hard Reset / Residual Power Drain**.
    - *Procedure:* Disconnect AC adapter, press and hold the power button continuously for 30–60 seconds to discharge motherboard capacitors, reconnect AC adapter, and power on.
- **Battery Not Charging ("Plugged in, not charging"):**
  - Windows battery health report generation:
    ```cmd
    powercfg /batteryreport /output "C:\Temp\battery_report.html"
    ```
  - Open `battery_report.html` and compare **Design Capacity** vs. **Full Charge Capacity**. If Full Charge Capacity has degraded below 50% of Design Capacity, request battery replacement.
  - Reinstall Microsoft ACPI-Compliant Control Method Battery driver in Device Manager.

---

## 2. Thermal Management & Overheating

### Symptoms
- Laptop fan continuously running at maximum RPM; system shuts down unexpectedly during heavy workload without BSOD (thermal shutdown protection).
- CPU throttling down to 0.79 GHz.

### L1 Corrective Procedure
1. Inspect air intake grilles and exhaust vents using a flashlight for accumulated dust or pet hair.
2. Use compressed air (short bursts while holding fan blades steady with a plastic toothpick to prevent back-EMF bearing damage).
3. Ensure user is not operating laptop on soft surfaces (beds, blankets, couches) that suffocate intake vents.
4. Verify power plan is set to "Balanced" rather than "High Performance" on battery.

---

## 3. External Displays & Multi-Monitor Setup

### Common Symptoms
- External monitor shows "No Signal" via HDMI, DisplayPort, or USB-C Dock.
- Windows detects display but screen remains blank.

### L1 Diagnostic Checklist
1. **Windows Project Shortcut:** Press `Windows Key + P` to verify mode is set to **Extend** or **Duplicate** (not "PC screen only").
2. **Physical Connections:** Reseat cable at both ends; avoid cheap passive adapters (prefer active DP-to-HDMI).
3. **Power Cycle Monitor:** Disconnect monitor power cable for 15 seconds to reset internal display firmware.
4. **Docking Station Reset:** If connected through Dell/HP USB-C dock, unplug dock power, unplug host USB-C cable, wait 30 seconds, plug dock power in first, then reconnect to laptop.
5. **Driver / Graphics Refresh:** Press `Windows Key + Ctrl + Shift + B` to trigger an instant graphics subsystem driver restart (screen flashes and chimes).
