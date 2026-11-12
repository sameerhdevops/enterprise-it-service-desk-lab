# Standard Knowledge Base Article: Resolving No Internet Connectivity
**KB ID:** KB0002  
**Category:** Networking / LAN & Wi-Fi  
**Author:** Nexora IT Service Desk (L1 Support)  
**Last Reviewed:** 2024-11-12  

---

### Symptoms
- Workstation displays globe icon or yellow warning badge on taskbar network indicator.
- Web browser reports: "No internet" (`ERR_INTERNET_DISCONNECTED` or `ERR_NAME_NOT_RESOLVED`).
- User cannot connect to cloud email, Teams, or internet websites.

### Applicable Systems
- All Windows 10 & 11 endpoints connected via Ethernet or corporate Wi-Fi (`Nexora-Corp`).

### Prerequisites
- L1 administrative access on client machine for network stack reset.

### Troubleshooting Steps
1. **Physical & Adapter State Inspection:**
   - Verify Ethernet patch cable is firmly seated with active green/amber link LEDs.
   - Run `ncpa.cpl`; ensure Ethernet / Wi-Fi adapter is not set to `Disabled`.
2. **Examine IP Addressing via CLI:**
   - Open Command Prompt and run: `ipconfig /all`.
   - **Check IPv4 Address:** If address starts with `169.254.x.x` (APIPA), the workstation failed to communicate with the DHCP server.
   - **Check Default Gateway:** Verify IP is `192.168.10.1`.
3. **Layer 3 Reachability Tests:**
   - Test TCP/IP stack loopback: `ping 127.0.0.1`.
   - Test local default gateway: `ping 192.168.10.1`.
   - Test external public IP: `ping 8.8.8.8`.
   - Test DNS resolution: `ping www.google.com`.

### Resolution
- If APIPA address detected, force a fresh DHCP request:
  ```cmd
  ipconfig /release
  ipconfig /renew
  ```
- If network stack is unresponsive, execute complete stack reset:
  ```cmd
  netsh winsock reset
  netsh int ip reset
  ipconfig /flushdns
  ```
- Restart workstation: `shutdown /r /t 0`.

### Verification
- Confirm network icon in taskbar displays standard connected icon without warnings.
- Run `ping 8.8.8.8 -n 4` with 0% packet loss.
- Navigate to company intranet portal (`https://intranet.nexora.local`) in Edge.

### Escalation Instructions
- If ping to Default Gateway fails across multiple adjacent workstations on the floor, escalate immediately as a **P1/P2 Major Incident** to **L2 Network Support** (Floor switch or uplink down).

### Related Incidents
- INC0015, INC-N001, INC-N003, INC-N005
