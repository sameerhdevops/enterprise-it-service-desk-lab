# Enterprise Networking Fundamentals for L1 Support
**Document ID:** NET-001  
**Audience:** L1 Support Engineers / Service Desk Analysts  
**Scope:** OSI Model, TCP/IP Suite, IPv4 Addressing, Subnetting, Default Gateway

---

## 1. The OSI Model: Practical L1 Support Perspective

While textbooks teach 7 layers abstractly, an L1 Support Engineer uses the OSI model as a structured, bottom-up diagnostic methodology:

```
[Layer 7: Application] ──> Browser, Outlook, DNS, DHCP, HTTP/HTTPS
[Layer 6: Presentation] ──> SSL/TLS encryption, data formatting
[Layer 5: Session]      ──> RPC sessions, NetBIOS, session tokens
[Layer 4: Transport]    ──> TCP (reliable, ports 80, 443, 445), UDP (fast, ports 53, 67, 123)
[Layer 3: Network]      ──> IP addressing (IPv4/IPv6), Routers, ICMP (ping), Routing tables
[Layer 2: Data Link]    ──> MAC addressing, Switches, Ethernet frames, VLANs, Wi-Fi 802.11
[Layer 1: Physical]     ──> RJ-45 copper cables, Fiber optics, NIC link lights, Radio waves
```

### Bottom-Up Troubleshooting Sequence:
1. **Layer 1 Check:** Is the cable plugged in? Are green/amber link lights active on the RJ-45 jack? Is Wi-Fi toggled on?
2. **Layer 2 Check:** Is the switch port negotiating link speed? Is the MAC address learned on the port? Is the device in the correct VLAN?
3. **Layer 3 Check:** Does the device have a valid IP address (`ipconfig`)? Can it ping its Default Gateway? Can it ping external IPs (`8.8.8.8`)?
4. **Layer 4 Check:** Is the target port open and listening (`Test-NetConnection -Port 443`)? Are local or network firewalls blocking the TCP port?
5. **Layer 7 Check:** Is DNS resolving names (`nslookup`)? Is the web server returning HTTP 200 OK or HTTP 500 error?

---

## 2. IPv4 Addressing & Subnet Masks

In Nexora Technologies, private IPv4 addressing follows RFC 1918 standards:

| Address Class | RFC 1918 Private Range | Subnet Mask | Nexora Usage |
|---|---|---|---|
| **Class A** | `10.0.0.0` - `10.255.255.255` | `/8` (`255.0.0.0`) | Data center, cloud VPCs |
| **Class B** | `172.16.0.0` - `172.31.255.255` | `/12` (`255.240.0.0`) | Branch offices, VPN pools |
| **Class C** | `192.168.0.0` - `192.168.255.255` | `/24` (`255.255.255.0`) | Local Bengaluru Office LANs |

### Understanding the Subnet Mask
A subnet mask divides an IP address into two portions:
- **Network Portion:** Identifies which local network/VLAN the device belongs to.
- **Host Portion:** Identifies the unique device on that specific local network.

*Example:*  
IP Address: `192.168.10.45`  
Subnet Mask: `255.255.255.0` (`/24`)  
- Network ID: `192.168.10.0`
- Host ID: `45`
- Usable Host Range: `192.168.10.1` to `192.168.10.254`
- Broadcast Address: `192.168.10.255`

---

## 3. The Role of the Default Gateway

The **Default Gateway** is the IP address of the local router interface connected to the same subnet as the client (typically the first or last usable IP, e.g., `192.168.10.1`).

- **Rule:** If the destination IP address has the **same** Network ID as the sender, traffic stays on the local switch (Layer 2).
- **Rule:** If the destination IP address has a **different** Network ID (e.g., reaching a server on `192.168.20.10` or a website on the public internet), the computer encapsulates the packet and sends it directly to the **Default Gateway** for routing.

*L1 Diagnostic Golden Rule:* If a computer cannot ping its Default Gateway, it cannot reach ANY device outside its own immediate local subnet!
