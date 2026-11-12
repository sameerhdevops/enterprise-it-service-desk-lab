# Network Support Runbooks: 8 Representative Incidents
**Document ID:** NET-RUN-001  
**Audience:** L1 Support Engineers / Service Desk Analysts  
**Scope:** Core L1 Network Triage & Troubleshooting Workflows

---

## Incident 1: No Internet Connectivity (INC-N001)
- **Reported Symptom:** User in Operations reports complete loss of internet; yellow triangle or globe icon on taskbar.
- **Troubleshooting Sequence:**
  1. Verify physical link (`Get-NetAdapter`).
  2. Run `ipconfig /all` to confirm IP address assignment.
  3. Ping loopback `127.0.0.1` -> ping default gateway `192.168.10.1` -> ping public DNS `8.8.8.8` -> ping `www.google.com`.
  4. Isolate break point: If ping to gateway fails, issue is local LAN/cable. If ping to 8.8.8.8 fails, WAN uplink is down. If only google.com fails, issue is DNS.
- **Resolution:** Reseat Ethernet patch cable, release/renew DHCP lease, or reset TCP/IP stack (`netsh int ip reset`).
- **Escalation Condition:** If all workstations on the floor report loss of gateway ping simultaneously, escalate immediately to **L2 Network Support** (core switch or router failure).

---

## Incident 2: DNS Resolution Failure (INC-N002)
- **Reported Symptom:** User can access internal file shares by IP address (`\\192.168.20.15`), but browser shows "Server IP address could not be found" (`DNS_PROBE_FINISHED_NXDOMAIN`).
- **Commands & Diagnostic Output:**
  ```cmd
  nslookup intranet.nexora.local
  ```
  *Output:* `DNS request timed out. Server: Unknown. Address: 192.168.20.10`
- **Root Causes:** DNS client cache corrupted; adapter configured with wrong DNS server; corporate DNS service on Domain Controller stopped.
- **Resolution:**
  ```cmd
  ipconfig /flushdns
  ipconfig /registerdns
  ```
  Verify active adapter IPv4 properties point to `192.168.20.10`.
- **Escalation:** Escalate to **L3 Infrastructure** if DNS Server service on `NEX-DC01` has crashed or stopped responding.

---

## Incident 3: DHCP Address Assignment Failure (APIPA 169.254.x.x) (INC-N003)
- **Reported Symptom:** Newly moved workstation in Finance has "Unidentified Network, No Internet".
- **Diagnosis:** `ipconfig` displays `Autoconfiguration IPv4 Address: 169.254.88.192` with Subnet Mask `255.255.0.0` and no Default Gateway.
- **Root Cause:** Wall jack connected to an unassigned switch port; switch port disabled; or DHCP relay (`ip helper-address`) missing on new VLAN.
- **Resolution:**
  - Execute `ipconfig /release` followed by `ipconfig /renew`.
  - If timeout recurs, trace wall port number back to patch panel and verify switch port status.
- **Escalation:** Escalate to **L2 Network** to patch port to VLAN 10 or investigate DHCP scope exhaustion.

---

## Incident 4: Incorrect Static IP Configuration / IP Conflict (INC-N004)
- **Reported Symptom:** Windows toast notification: *"There is an IP address conflict with another system on the network."* Network connectivity drops intermittently.
- **Investigation:**
  - Review Event Viewer System log for Event ID 4199 (`The system detected an address conflict for IP address 192.168.10.25 with the system having network hardware address...`).
  - Use `arp -a` to find the conflicting MAC address.
- **Root Cause:** A user or contractor manually assigned a static IP that overlaps with a DHCP dynamic pool address or an existing network printer.
- **Resolution:** Open `ncpa.cpl` > Properties > IPv4 Properties > switch from "Use the following IP address" to **"Obtain an IP address automatically"** (DHCP).
- **Verification:** IP conflict notification clears; device receives unique DHCP lease.

---

## Incident 5: Default Gateway Unreachable (INC-N005)
- **Reported Symptom:** `ping 192.168.10.1` returns `Destination host unreachable` or `Request timed out`.
- **Investigation Sequence:**
  - Confirm client subnet mask is `/24` (`255.255.255.0`). If mask was entered as `255.255.255.240`, the gateway may fall outside the local subnet range.
  - Check ARP table: `arp -a`. If gateway IP shows `incomplete` or missing MAC address, Layer 2 broadcast resolution is failing.
- **Resolution:** Correct subnet mask in adapter settings; reseat switch port cable; verify port VLAN configuration on switch.
- **Escalation:** Escalate to **L2 Network Support** if router interface `GigabitEthernet0/0/1.10` is shutdown or administratively down.

---

## Incident 6: VPN Connectivity Failure ("Gateway Timeout") (INC-N006)
- **Reported Symptom:** Remote employee using GlobalProtect client cannot connect; client hangs on "Connecting" for 45 seconds, then reports "Connection Failed: Gateway timed out".
- **Diagnostic Steps:**
  - Test user's public internet: verify home broadband speed and ping to `8.8.8.8`.
  - Test resolution of VPN portal: `nslookup vpn.nexora.com`.
  - Test port 443 reachability to gateway: `Test-NetConnection -ComputerName vpn.nexora.com -Port 443`.
- **Resolution:** If home ISP blocks IPsec UDP 4500, toggle client setting to SSL/TCP mode. If DNS failed, flush local DNS and update Wi-Fi router DNS to `8.8.8.8`.
- **Escalation:** Escalate to **L2 Network** if the external corporate firewall interface has exceeded maximum concurrent VPN tunnel capacity.

---

## Incident 7: Wi-Fi Connection Failure ("Can't connect to this network") (INC-N007)
- **Reported Symptom:** Laptop sees corporate Wi-Fi SSID `Nexora-Corp`, but clicking Connect results in an immediate *"Can't connect to this network"* error without prompting for password.
- **Root Cause:** Stale 802.1X security profile cached after user domain password change; or outdated wireless NIC driver.
- **Resolution:**
  - In Windows Settings > Network & internet > Wi-Fi > **Manage known networks** > select `Nexora-Corp` > click **Forget**.
  - Re-select `Nexora-Corp`, enter current domain credentials, and accept enterprise RADIUS certificate prompt.
- **Verification:** Wi-Fi icon displays connected status and obtains IP in `192.168.10.x` range.

---

## Incident 8: Network Printer Unavailable (INC-N008)
- **Reported Symptom:** All users on Floor 2 report network printer `PRN01` (192.168.10.25) is not responding; print queue says "Error - Printing".
- **Investigation:**
  - Ping printer IP: `ping 192.168.10.25`.
  - Open browser and navigate to `http://192.168.10.25` (Embedded Web Server).
  - Inspect physical printer: check power switch, network link light on printer's rear Ethernet port, and LCD control panel for paper jam or firmware crash.
- **Resolution:** If ping fails and link light is unlit, replace network patch cord at printer and wall jack. If ping succeeds but web UI is frozen, power-cycle the physical printer.
- **Verification:** Send Windows test page; verify job prints and clears from queue.
