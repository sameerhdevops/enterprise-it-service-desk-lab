# Dynamic Host Configuration Protocol (DHCP) Troubleshooting Guide
**Document ID:** NET-003  
**Audience:** L1 Support Engineers / Service Desk Analysts  
**Protocol:** UDP Port 67 (Server) / UDP Port 68 (Client)

---

## 1. How DHCP Works: The DORA Process

When an employee connects their laptop to the office Ethernet or Wi-Fi, it negotiates an IP configuration through the 4-step **DORA** sequence. DHCPv4 operates over UDP: **Server listens on UDP port 67**, and **Client listens on UDP port 68**.

```
Client (Port 68)                                                DHCP Server (Port 67)
       │                                                                │
       ├─── [D] Discover (Src: 0.0.0.0:68, Dst: 255.255.255.255:67) ───>│  "Is there a DHCP server?"
       │                                                                │
       │<── [O] Offer (Src: ServerIP:67, Dst: 255.255.255.255:68) ──────┤  "Here is an available IP"
       │                                                                │
       ├─── [R] Request (Src: 0.0.0.0:68, Dst: 255.255.255.255:67) ────>│  "I would like to lease this IP"
       │                                                                │
       │<── [A] Acknowledge (Src: ServerIP:67, Dst: Port 68) ───────────┤  "Leased! Gateway: .1, DNS: .10"
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
- **Physical Link Detected:** The physical network adapter is enabled and detected an electrical/optical link state.
- **DHCP Negotiation Failed:** The client did not receive a `DHCPOFFER` response.
- **Comprehensive Troubleshooting Checklist (Do Not Assume Server is Down):**
  - **Local Client:** Damaged patch cable, faulty NIC hardware, corrupted network adapter driver, or the Windows `DHCP Client` service stopped/disabled.
  - **Local Switching / VLAN:** The switch port is untagged or assigned to an unrouted/isolated VLAN, 802.1X port security authentication failed, or MAC filtering is active on the switch.
  - **Infrastructure / Relay:** The DHCP scope on the server is exhausted (100% leased), the DHCP Server service is stopped, or the router's DHCP Relay Agent (`ip helper-address`) is misconfigured or failing to forward broadcasts across subnets.
  - **Host Security:** Local endpoint firewall or antivirus software blocking inbound/outbound UDP broadcast traffic on ports 67/68.

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
