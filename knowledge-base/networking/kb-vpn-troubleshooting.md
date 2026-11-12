# Standard Knowledge Base Article: Remote Worker VPN Troubleshooting
**KB ID:** KB0008  
**Category:** Networking / Remote Access  
**Author:** Sameer Kulkarni (L1 Support)  
**Last Reviewed:** 2024-11-12  

---

### Symptoms
- Remote employee working from home cannot connect to corporate VPN.
- GlobalProtect / AnyConnect client hangs on "Connecting" or reports "Gateway timed out" / "Authentication failed".
- VPN connects, but user cannot access internal file shares (`\\nexfs01`) or intranet.

### Applicable Systems
- Palo Alto GlobalProtect 6.x / Cisco AnyConnect SSL VPN client on Windows 10/11.

### Prerequisites
- Active internet connection on user's home broadband.
- Valid Active Directory credentials.

### Troubleshooting Steps
1. **Verify Home Internet Connectivity:**
   - Ask user to disconnect VPN and open public websites (`google.com`, `speedtest.net`).
   - If home internet is down or speed is below 5 Mbps, resolve home broadband first.
2. **Verify Portal URL:**
   - In GlobalProtect client settings, verify portal address is strictly: `vpn.nexora.com`.
3. **Check for Expired Active Directory Password:**
   - If user password expired, VPN authentication fails silently. Have user sign into webmail (`outlook.office.com`) to test credentials.
4. **Test Port 443 Reachability to Gateway:**
   - In PowerShell, run: `Test-NetConnection -ComputerName vpn.nexora.com -Port 443`.
   - If `TcpTestSucceeded` is `False`, user's local router or ISP is blocking outbound SSL VPN.
5. **Mitigate Packet Fragmentation (MTU Disconnection):**
   - If VPN connects but drops every 10–15 minutes during large file transfers:
   - In GlobalProtect settings > Connection, change protocol from `Auto` / `IPsec` to `TCP`.
   - Reduce adapter MTU to 1400.

### Resolution
- Clear cached VPN credentials and reinstall virtual adapter:
  ```powershell
  # Restart GlobalProtect service
  Restart-Service -Name "PanGPS" -Force
  ```
- Have user sign out of VPN client, re-enter corporate username and password, and approve MFA notification.

### Verification
- GlobalProtect displays status: "Connected".
- Open Command Prompt and run: `ping 192.168.20.10` (Corporate Domain Controller).
- Confirm 0% packet loss to internal server.

### Escalation Instructions
- Escalate to **L2 Network Support** if user's account is verified healthy but firewall gateway refuses connection with license/session limit errors.

### Related Incidents
- INC0004, PRB0001, CHG0002, NET-004
