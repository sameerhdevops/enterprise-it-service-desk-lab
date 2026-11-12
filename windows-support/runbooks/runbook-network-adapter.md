# Troubleshooting Runbook: Network Adapter Issue
**Incident ID:** INC-W015  
**Category:** Windows Support / Network & Hardware  
**Target Systems:** Windows 11 / Windows 10 (Ethernet & Wi-Fi NICs)  

---

### 1. Reported Symptom
User reports: *"My laptop completely lost network access. The Wi-Fi icon turned into a globe with a cancel sign, and clicking on it shows 'No internet, secured' or 'No Wi-Fi networks found'. Plugging in an Ethernet cable also does nothing."*

### 2. User Impact
Total loss of connectivity. User cannot access corporate network, email, cloud apps, or internet. Priority: P2/P3.

### 3. Initial Questions
1. Did the network disconnect suddenly while working, or when waking the laptop from sleep?
2. Are you in the office or working remotely from home?
3. Is Airplane Mode enabled on your laptop keyboard or action center?
4. Are other nearby colleagues able to connect to the Wi-Fi?

### 4. Investigation Sequence
1. Check physical hardware state: Airplane mode toggle (function keys `Fn + F12` or hardware wireless switch), Ethernet link lights on RJ-45 port (amber/green).
2. Inspect Network Connections control panel (`ncpa.cpl`) to see if the adapter is **Disabled**.
3. Check Device Manager (`devmgmt.msc`) under **Network adapters** for yellow warning signs or driver error codes.
4. Review IP configuration via `ipconfig /all`: Check for APIPA address (`169.254.x.x`), missing default gateway, or blank DNS servers.
5. Check if third-party VPN virtual adapters (e.g., TAP/TUN adapter or Cisco/GlobalProtect virtual NIC) are conflicting with physical adapters.

### 5. Tools Required
- Network Connections (`ncpa.cpl`)
- Device Manager (`devmgmt.msc`)
- Command Prompt / PowerShell (`ipconfig`, `netsh`, `Get-NetAdapter`)

### 6. Commands & Output Interpretation
Inspect network adapter status and link speed via PowerShell:
```powershell
Get-NetAdapter | Select-Object Name, InterfaceDescription, Status, LinkSpeed, MediaConnectionState
```
*Interpretation:* If `Status` is `Disabled`, the adapter was software-disabled. If `Status` is `Not Present`, the hardware NIC has disconnected internally or power-management shut it down.

Reset the TCP/IP stack and Winsock catalog via Command Prompt (Admin):
```cmd
netsh winsock reset
netsh int ip reset
```
*Interpretation:* Clears corrupt network protocol sockets, Layered Service Providers (LSPs), and resets TCP/IP registry settings back to clean defaults.

Flush DNS and release/renew DHCP lease:
```cmd
ipconfig /release
ipconfig /flushdns
ipconfig /renew
```
*Interpretation:* Forces the network interface to drop current IP bindings and request a fresh configuration from the DHCP server.

### 7. Expected Observations
- Healthy: Adapter shows Status = `Up`, LinkSpeed = `1 Gbps` or `866 Mbps`, valid IPv4 address in subnet (e.g., `192.168.10.x`), ping to default gateway < 1 ms.
- Fault: Status = `Disabled`, or IP is `169.254.x.x` (APIPA), or globe icon displayed in system tray.

### 8. Possible Root Causes
1. **Network Adapter Disabled:** User or accidental keypress disabled the adapter in Windows settings or `ncpa.cpl`.
2. **Corrupted TCP/IP Stack / Winsock Catalog:** Third-party VPN, antivirus firewall, or malware damaged network stack bindings.
3. **Power Management Suspend Bug:** Windows put the PCIe/USB network card into low-power sleep and failed to wake it.
4. **Corrupted / Outdated NIC Driver:** Recent update broke driver compatibility.
5. **Hardware Failure:** Damaged Ethernet port pins or defective onboard M.2 Wi-Fi card.

### 9. Corrective Action
1. **Enable Adapter via PowerShell / GUI:**
   ```powershell
   Enable-NetAdapter -Name "Wi-Fi" -Confirm:$false
   ```
2. **Disable Power Management Sleep on NIC:**
   - In Device Manager > Network Adapters > Properties > **Power Management** tab > Uncheck **"Allow the computer to turn off this device to save power"**.
3. **Execute Full Network Stack Reset:**
   - Run elevated commands:
     ```cmd
     netsh winsock reset
     netsh int ip reset
     ipconfig /flushdns
     ```
   - Restart the workstation.
4. **Reinstall Network Adapter Driver:**
   - Right-click adapter in Device Manager > **Uninstall device** (do not delete driver software).
   - Click **Action > Scan for hardware changes** to force clean hardware re-enumeration.

### 10. Verification Procedure
- In system tray, verify Wi-Fi / Ethernet icon displays connected status (no globe or warning badge).
- Run `ping 8.8.8.8` and `ping www.google.com` to confirm both Layer 3 routing and DNS resolution.
- Open browser and navigate to company intranet portal.

### 11. Escalation Conditions
- Escalate to **L2 Desktop Support** if physical M.2 Wi-Fi card or motherboard Ethernet controller is physically damaged or fails hardware diagnostics.

### 12. Ticket Resolution Notes
> *"Troubleshot 'No Internet' condition on user laptop caused by disabled network adapter. Discovered Intel Wi-Fi 6 AX201 adapter was disabled in software and Windows power management was shutting down the PCIe interface upon battery sleep. Re-enabled adapter via PowerShell, unchecked 'Allow the computer to turn off this device to save power' in Device Manager properties, and reset TCP/IP stack. Verified solid connection to corporate Wi-Fi with full internet access."*

### 13. Interview Questions & Defensible Answers
- **Q: What is the very first thing you check when a user says their Wi-Fi adapter has completely disappeared from Windows?**  
  *A: "First, I check if Airplane mode or a physical Wi-Fi toggle key was pressed. Next, I open Device Manager to see if the network adapter is listed under 'Network adapters' with a yellow exclamation mark, or if it has moved under 'Other devices' as an Unknown device. If it is completely missing, I check if it's hidden (`View > Show hidden devices`) or if the laptop BIOS has disabled the wireless controller. Finally, I check `ncpa.cpl` to verify the adapter wasn't simply disabled in software."*
