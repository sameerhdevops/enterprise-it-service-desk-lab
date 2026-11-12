# Dynamic Host Configuration Protocol (DHCP) Troubleshooting Guide
**Document ID:** NET-003  
**Audience:** L1 Support Engineers / Service Desk Analysts  
**Protocol:** UDP Port 67 (Server) / UDP Port 68 (Client)

---

## 1. How DHCP Works: The DORA Process

When an employee connects their laptop to the office Ethernet or Wi-Fi, it negotiates an IP configuration through the 4-step **DORA** sequence:

```
Client (Unconfigured)                                           DHCP Server (NEX-DC01)
         │                                                                │
         ├─── [D] Discover (Broadcast: 255.255.255.255, UDP 67) ─────────>│  "Is there a DHCP server?"
         │                                                                │
         │<── [O] Offer (Unicast/Broadcast, IP: 192.168.10.45) ───────────┤  "Here is an available IP"
         │                                                                │
         ├─── [R] Request (Broadcast: "I accept 192.168.10.45") ─────────>│  "I would like to lease this IP"
         │                                                                │
         │<── [A] Acknowledge (Final lease parameters & options) ─────────┤  "Leased! Gateway: .1, DNS: .10"
         │                                                                │
```

### Essential DHCP Options Delivered to Client:
- **Option 3:** Router / Default Gateway IP (`192.168.10.1`).
- **Option 6:** Domain Name Servers (`192.168.20.10`).
- **Option 15:** Domain Name suffix (`nexora.local`).
- **Option 51:** IP Address Lease Time (e.g., 8 days for wired LAN, 8 hours for guest Wi-Fi).

---

## 2. The APIPA Signature: 169.254.x.x

When a Windows client sends a DHCP Discover broadcast but receives **NO response** within approximately 60 seconds:
- Windows automatically assigns an address from the **Automatic Private IP Addressing (APIPA)** range:  
  **`169.254.0.1` to `169.254.255.254`** with subnet mask `255.255.0.0` (RFC 3927).

### What Seeing 169.254.x.x Means to an L1 Engineer:
- **The physical cable and network card are working** (Windows detected a link state).
- **The client cannot reach or hear from a DHCP server.**
- **Possible reasons:**
  - DHCP server service is stopped or DHCP scope is 100% full (exhausted).
  - Client switch port is in an unrouted VLAN that lacks a `dhcp-relay` / `ip helper-address`.
  - Corporate 802.1X port authentication failed or guest network block is active.

---

## 3. L1 Troubleshooting Commands & Release/Renew Sequence

Run in Command Prompt or PowerShell:

### Inspect Current DHCP Lease:
```cmd
ipconfig /all
```
*Look for:* `DHCP Enabled: Yes`, `Lease Obtained`, `Lease Expires`, `DHCP Server IP`.

### Force Fresh DORA Handshake:
```cmd
:: 1. Release existing IP lease
ipconfig /release

:: 2. Wait 5 seconds, then request fresh configuration
ipconfig /renew
```

*Expected Success Output:*  
Connection-specific DNS Suffix: `nexora.local`  
IPv4 Address: `192.168.10.52`  
Subnet Mask: `255.255.255.0`  
Default Gateway: `192.168.10.1`

*Failure Output:*  
`An error occurred while renewing interface Ethernet : unable to contact your DHCP server. Request has timed out.`  
*(Confirms Layer 2 switch port VLAN misconfiguration or DHCP server failure).*
