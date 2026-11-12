# End-to-End Network Connectivity Troubleshooting Runbook
**Document ID:** NET-005  
**Audience:** L1 Support Engineers / Service Desk Analysts  
**Scope:** Systematic Layer 1 through Layer 7 Diagnosis ("No Internet" Incident Workflow)

---

## 1. The Systematic L1 Troubleshooting Flowchart

When an employee reports: *"I have no internet access and cannot connect to anything"*, never guess or reboot randomly. Follow this deterministic sequence:

```
[Start: User reports "No Internet"]
  │
  ├── 1. Physical Layer (Layer 1)
  │      Is Ethernet cable plugged in with link lights? Or Wi-Fi connected to corporate SSID?
  │      NO  ──> Reseat cable, test different port, toggle Wi-Fi radio on.
  │      YES ──> Proceed to Layer 2/3.
  │
  ├── 2. IP Configuration Check (Layer 3)
  │      Run `ipconfig /all`. Is IP valid (192.168.10.x)? Or is it 169.254.x.x (APIPA)?
  │      APIPA / 0.0.0.0 ──> DHCP Failure. Run `ipconfig /renew`. Check switch VLAN.
  │      VALID IP ────────> Proceed to Gateway ping.
  │
  ├── 3. Default Gateway Reachability (Layer 3)
  │      Run `ping <DefaultGatewayIP>` (e.g., ping 192.168.10.1).
  │      FAILS ──> Local switch port down, ARP issue, or router interface offline.
  │      REPLIES ─> Local LAN is operational. Proceed to Public IP ping.
  │
  ├── 4. External Routing & WAN Reachability (Layer 3)
  │      Run `ping 8.8.8.8` or `ping 1.1.1.1`.
  │      FAILS ──> ISP link down, corporate firewall NAT failure, or proxy issue. Run `tracert`.
  │      REPLIES ─> Internet routing is operational. Proceed to DNS test.
  │
  ├── 5. Domain Name Resolution (Layer 7)
  │      Run `nslookup www.google.com` and `ping www.google.com`.
  │      FAILS ──> DNS server offline or adapter DNS settings wrong. Run `ipconfig /flushdns`.
  │      REPLIES ─> Full connectivity confirmed. Proceed to Browser/App check.
  │
  └── 6. Application / Browser Proxy (Layer 7)
         If ping succeeds but browser won't open web pages:
         Check Windows Proxy settings (`inetcpl.cpl` > Connections > LAN Settings).
         Ensure rogue manual proxy is unchecked and set to "Automatically detect settings".
```

---

## 2. Practical Diagnostic Commands & Outputs

### Step 1: Check Local Adapter
```cmd
ipconfig /all
```

### Step 2: Test Local TCP/IP Loopback (Rules out OS protocol stack corruption)
```cmd
ping 127.0.0.1
```
*Expected:* 4 replies in <1ms. If this fails, the local Windows network stack is corrupt (`netsh int ip reset` required).

### Step 3: Test Default Gateway
```cmd
ping 192.168.10.1
```
*Expected:* `Reply from 192.168.10.1: bytes=32 time<1ms TTL=64`.

### Step 4: Trace Hop-by-Hop Routing to Isolate Break Point
```cmd
tracert -d 8.8.8.8
```
*Interpretation:*
- Hop 1: `192.168.10.1` (Local Default Gateway router)
- Hop 2: `203.0.113.1` (ISP Gateway / WAN uplink)
- Hop 3+: ISP Transit hops
- *Diagnostic Note on Timeouts:* Intermediate hops displaying `* * * Request timed out` often indicate that an intermediate router is intentionally dropping or rate-limiting ICMP TTL-expired generation (control plane protection) rather than a failure point. A true network failure is confirmed only when timeouts persist continuously all the way to the destination, or when an intermediate hop returns an ICMP Destination/Network Unreachable message.
- *Break isolation:* If trace times out continuously starting at Hop 2 all the way to the end, the local LAN is functioning and the issue is an ISP fiber outage, firewall routing block, or WAN interface down.

### Step 5: Test Port Connectivity with PowerShell
```powershell
Test-NetConnection -ComputerName "intranet.nexora.local" -Port 443
```
*Interpretation:* Tests both DNS resolution and TCP handshake on HTTPS port 443 in a single command.
