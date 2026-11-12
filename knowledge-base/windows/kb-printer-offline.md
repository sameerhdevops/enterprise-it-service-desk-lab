# Standard Knowledge Base Article: Fixing Printer Offline Problems
**KB ID:** KB0004  
**Category:** Windows / Printers & Peripherals  
**Author:** Nexora IT Service Desk (L1 Support)  
**Last Reviewed:** 2024-11-12  

---

### Symptoms
- Printer status in Windows Settings or application print dialog displays as "Offline".
- Print jobs accumulate in the queue without printing.
- No physical error lights are visible on the physical printer.

### Applicable Systems
- Windows 10/11 workstations printing to network MFD printers (HP LaserJet, Canon imageRUNNER).

### Prerequisites
- L1 Administrative elevation for print spooler restart and port changes.

### Troubleshooting Steps
1. **Physical Status Verification:**
   - Verify physical printer is powered ON, LCD screen is ready, and paper tray is not empty.
2. **Ping Test to Printer IP:**
   - Run `ping 192.168.10.25` (HR/Finance HP MFD).
   - If ping fails, check printer network cable and link LED on wall jack.
3. **Check Print Queue Settings:**
   - Press `Windows Key + R` > type `control printers` > double-click affected printer.
   - Click **Printer** in top menu.
   - Verify **"Use Printer Offline"** is UNCHECKED.
   - Verify **"Pause Printing"** is UNCHECKED.
4. **Inspect Port Configuration:**
   - In Printer Properties > **Ports** tab:
   - If port is `WSD-xxx`, Windows Web Services for Devices has lost communication with the device.

### Resolution
- **Switch to Standard TCP/IP Port:**
  - In Ports tab, click **Add Port** > **Standard TCP/IP Port** > New Port.
  - Enter printer IP: `192.168.10.25`.
  - Uncheck "SNMP Status Enabled" if SNMP is blocked between subnets.
- **Restart Local Print Spooler:**
  ```powershell
  Restart-Service -Name Spooler -Force
  ```

### Verification
- Confirm printer status changes from "Offline" to "Ready".
- Click **Print Test Page** in General tab; confirm test page prints and queue clears.

### Escalation Instructions
- Escalate to **L2 Desktop Support** if printer hardware shows mechanical failure (roller paper jam, fuser error 50.x).

### Related Incidents
- INC-W006, INC-W007, INC-N008
