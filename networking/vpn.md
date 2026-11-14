# Virtual Private Network (VPN) Troubleshooting Guide
**Document ID:** NET-004  
**Audience:** L1 Support Engineers / Service Desk Analysts  
**Client:** Palo Alto GlobalProtect / Cisco AnyConnect SSL/IPsec VPN

---

## 1. Remote Access VPN Fundamentals for L1

When employees work from home or travel, a Remote Access VPN creates an encrypted virtual tunnel over the untrusted public internet back into the corporate Nexora Technologies network:

```
[Remote Laptop at Home] ──(Encrypted Tunnel over Public Internet)──> [Corporate Firewall/VPN Gateway]
(Home IP: 192.168.1.15)                                            (Public IP: 203.0.113.10)
(Virtual VPN IP: 172.16.50.42)                                                 │
                                                                               ▼
                                                          [Internal LAN: Servers, SAP, File Shares]
                                                          (192.168.20.0/24 Subnet)
```

### Split Tunneling vs. Full Tunneling
- **Split Tunneling (Nexora Standard):** Only traffic destined for corporate IP ranges (`192.168.x.x`, `172.16.x.x`) routes through the encrypted VPN tunnel. General internet traffic (YouTube, Netflix, personal web browsing) egresses directly through the user's home broadband router.
- **Full Tunneling:** 100% of user network traffic is forced through the corporate firewall for inspection.

---

## 2. Common Scenarios & L1 Troubleshooting Workflows

### Scenario A: "Gateway Timed Out" / Connection Hangs at 50%
1. **Verify Home Internet Baseline First:**
   - Ask user to disconnect VPN, open browser, and navigate to public websites (`google.com`, `speedtest.net`).
   - If home internet is offline, VPN cannot connect!
2. **Check Corporate Portal URL:**
   - In GlobalProtect/AnyConnect client settings, ensure portal address is correctly formatted:  
     `vpn.nexora.com` (no trailing slashes, correct spelling).
3. **Inspect Local Wi-Fi / Hotspot Restrictions:**
   - Some public coffee shop or airport Wi-Fi networks block UDP port 4500/500 (IPsec).
   - *Workaround:* Switch VPN client transport protocol from IPsec to **SSL / TCP port 443** in client connection settings.

---

### Scenario B: VPN Connects, But Cannot Access Internal Servers / Shared Drives
1. **Check Virtual Adapter IP Assignment:**
   - Run `ipconfig /all`.
   - Locate virtual adapter (e.g., "Palo Alto Networks Virtual Adapter").
   - Ensure an IP from the VPN pool (e.g., `172.16.50.x`) and corporate DNS servers (`192.168.20.10`) are assigned.
2. **Check DNS Suffix Search List:**
   - If user can ping internal server by IP (`ping 192.168.20.15`), but fails by name (`ping nexfs01`), test with Full Qualified Domain Name (FQDN): `ping nexfs01.nexora.test`.
   - If FQDN works, append connection-specific DNS suffix in adapter properties.
3. **Inspect Routing Table:**
   - Run `route print` to verify routes for `192.168.0.0/16` point to the VPN virtual gateway.

---

### Scenario C: VPN Drops Intermittently Every 10–15 Minutes (INC0004 / PRB0001)
- **Root Cause:** MTU (Maximum Transmission Unit) mismatch or Path MTU Discovery black hole between home ISP broadband and enterprise firewall gateway causing packet fragmentation.
- **L1 Workaround:** In VPN Client > Settings > Advanced > reduce MTU from 1500 to **1400** or force TCP encapsulation mode.
