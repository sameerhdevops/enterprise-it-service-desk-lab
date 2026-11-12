# Packet Analysis & Wireshark Diagnostics for L1 Support
**Document ID:** NET-006  
**Audience:** L1 Support Engineers / Service Desk Analysts  
**Tool:** Wireshark Packet Analyzer / tcpdump

---

## 1. When Does an L1 Support Engineer Use Packet Captures?

In high-volume L1 operations, basic connectivity issues are resolved with `ping`, `ipconfig`, and `nslookup`. Wireshark is utilized when:
- Intermittent disconnections occur with no clear error codes (e.g., VPN drops, VoIP audio stutter).
- Network administrators request evidence of client-side TCP resets (`RST`) or retransmissions.
- Verifying whether DHCP DORA or DNS queries are physically leaving the network interface card.

---

## 2. Essential Wireshark Display Filters for Triage

Display filters allow filtering thousands of captured frames down to the specific protocol of interest:

| Filter Syntax | What It Displays | Practical Diagnostic Purpose |
|---|---|---|
| `dns` | All DNS queries and responses. | Verify if workstation is receiving DNS answers or timing out (`Server failure`). |
| `bootp || dhcp` | DHCP Discover, Offer, Request, ACK packets. | Confirm whether client broadcast is eliciting an Offer from the DHCP server. |
| `icmp` | Ping Echo Requests and Echo Replies. | Observe packet loss, TTL expired in transit, or destination unreachable flags. |
| `tcp.port == 443` | All HTTPS traffic. | Inspect SSL/TLS client hello and handshake negotiation. |
| `tcp.analysis.flags` | TCP retransmissions, duplicate ACKs, window full, out-of-order packets. | Immediate indicator of high network latency, packet loss, or saturated bandwidth. |
| `tcp.flags.reset == 1` | TCP RST (Reset) packets. | Indicates a firewall or endpoint actively rejected and killed a connection attempt. |
| `ip.addr == 192.168.10.25` | All packets to or from a specific IP address (e.g., printer). | Isolate traffic between user PC and printer. |

---

## 3. Anatomy of a Healthy TCP 3-Way Handshake

When establishing a reliable connection (e.g., web server, file server, database):

```
Client (Port 51234)                                       Server (Port 443)
       │                                                         │
       ├─── [SYN] Seq=0 ────────────────────────────────────────>│  "Synchronize: let's connect"
       │                                                         │
       │<── [SYN, ACK] Seq=0, Ack=1 ─────────────────────────────┤  "Acknowledge and Synchronize"
       │                                                         │
       ├─── [ACK] Seq=1, Ack=1 ─────────────────────────────────>│  "Acknowledged: connection established!"
       │                                                         │
       │<══ [TLS Handshake / Application Data Exchange] ════════>│
```

### What a Broken Handshake Looks Like:
- **Client sends `[SYN]`, but receives `[RST, ACK]` immediately:** The server is reachable, but the port is CLOSED (no service listening) or a firewall rule rejected the packet.
- **Client sends `[SYN]`, followed by 3 retransmitted `[SYN]` packets with no response:** The packet is being silently dropped by an intermediate network firewall, routing black hole, or the server is completely powered off.
