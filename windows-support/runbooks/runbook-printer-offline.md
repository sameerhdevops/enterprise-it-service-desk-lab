# Troubleshooting Runbook: Printer Offline
**Incident ID:** INC-W006  
**Category:** Windows Support / Printers  
**Target Systems:** Windows 11 / Windows 10 (Networked & Direct USB Printers)  

---

### 1. Reported Symptom
User reports: *"When I try to print invoices from Excel, the printer status says 'Offline' and nothing prints. The documents are just stuck in the print queue."*

### 2. User Impact
User cannot print time-sensitive invoices or shipping manifests. Moderate urgency; if shared department printer, multiple users in Finance/Operations affected. Priority: P2/P3.

### 3. Initial Questions
1. Is this a shared network printer or a USB desktop printer directly plugged into your computer?
2. Are other colleagues in your department able to print to this same printer right now?
3. Is the physical printer powered on, and is the LCD display illuminated with a green ready status?
4. Have there been any recent paper jams or error lights blinking on the printer?

### 4. Investigation Sequence
1. Check physical printer state: Power, ready status, LCD screen for error messages (e.g., Paper Out, Toner Empty, Paper Jam).
2. Check network connectivity: If network printer, ping printer's IP address from client machine.
3. Check Windows printer status in Settings > Bluetooth & devices > Printers & scanners.
4. Verify whether "Use Printer Offline" is accidentally toggled in the legacy print queue window.
5. Check printer port configuration (Standard TCP/IP Port vs WSD / Web Services for Devices).
6. Inspect the local Print Spooler service (`spoolsv.exe`).

### 5. Tools Required
- Windows Settings / Control Panel (`control printers`)
- Print Management console (`printmanagement.msc`)
- Command Prompt / PowerShell (`ping`, `Test-NetConnection`, `Get-Printer`)
- Web browser (for printer Embedded Web Server / EWS)

### 6. Commands & Output Interpretation
Check printer configuration and status via PowerShell:
```powershell
Get-Printer | Select-Object Name, DriverName, PortName, PrinterStatus, JobCount
```
*Interpretation:* If `PrinterStatus` shows `Offline` or `Error`, inspect the `PortName`. If it starts with `WSD-`, Windows may have lost dynamic device pairing.

Test network connectivity to printer IP:
```powershell
Test-NetConnection -ComputerName 192.168.10.25 -Port 9100
```
*Interpretation:* Port 9100 is standard RAW printing. If `TcpTestSucceeded` is `True`, the network pathway is operational and the issue is software/driver configuration. If `False`, printer is physically disconnected or on a different subnet.

### 7. Expected Observations
- Healthy: Printer status = `Normal` or `Idle`, Port = Standard TCP/IP Port with fixed IP, RAW port 9100 responds.
- Fault: Status = `Offline`, or printer pingable but print queue shows 15 documents paused.

### 8. Possible Root Causes
1. **Network Connectivity Loss:** Network cable unplugged, bad Wi-Fi connection, or printer IP address changed via DHCP.
2. **"Use Printer Offline" Toggled:** User or Windows automatically set the queue to offline after a temporary disconnection.
3. **WSD Port Failure:** Windows Web Services for Devices (WSD) port going to sleep and failing to wake up across subnets.
4. **Physical Error:** Paper jam, empty paper tray, or open door not reported back clearly to the OS.
5. **Print Spooler Jam:** A corrupt print job holding the spooler queue.

### 9. Corrective Action
1. **Untoggle Offline Mode:** Open Print Queue > Click **Printer** in menu bar > Uncheck **"Use Printer Offline"** and uncheck **"Pause Printing"**.
2. **Switch from WSD to Standard TCP/IP Port:**
   - In Printer Properties > **Ports** tab > click **Add Port** > select **Standard TCP/IP Port**.
   - Enter static printer IP (e.g., `192.168.10.25`). Uncheck "SNMP Status Enabled" if SNMP is blocked across VLANs.
3. **Restart Print Spooler Service:**
   ```powershell
   Restart-Service -Name Spooler -Force
   ```
4. **Clear Stuck Spooler Queue:** (See INC-W007).
5. **Reboot Physical Printer:** Power cycle the printer to reinitialize network interface and clear memory.

### 10. Verification Procedure
- In Printers & scanners, verify status changes from *Offline* to *Ready*.
- Print a Windows Test Page: Printer Properties > General > **Print Test Page**.
- Confirm test page physically prints and job clears from the queue.

### 11. Escalation Conditions
- Escalate to **L2 Desktop / Network Support** if printer hardware has internal roller failure, requires maintenance kit, or if network switch port is down.

### 12. Ticket Resolution Notes
> *"Troubleshot 'Printer Offline' status on HR departmental HP LaserJet (192.168.10.25). Verified network ping and port 9100 listening. Discovered Windows had configured the printer using an unreliable WSD port which dropped connection after sleep. Reconfigured printer port to a static Standard TCP/IP Port. Restarted Print Spooler service and sent Windows test page. Test page printed successfully. Verified with user."*

### 13. Interview Questions & Defensible Answers
- **Q: Why do network printers often show 'Offline' in Windows even though you can ping them?**  
  *A: "This frequently happens when the printer is configured using a WSD (Web Services for Devices) port instead of a Standard TCP/IP Port. WSD relies on multicast discovery packets, which are often filtered between subnets or fail to wake up the printer. In addition, if SNMP is enabled on the TCP/IP port settings but the community name is wrong or firewalls block UDP 161, Windows assumes the printer is offline even if port 9100 is open. The fix is to switch the port to a Standard TCP/IP port and verify SNMP settings."*
