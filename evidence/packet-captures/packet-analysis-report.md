# Wireshark & Packet Capture Analysis Report
**Document ID:** NET-CAP-001  
**Project:** Nexora Technologies IT Operations Lab  
**Artifact File:** [`evidence/packet-captures/nexora-lab-traffic.pcap`](nexora-lab-traffic.pcap)  
**Capture Utility:** tcpdump (Libpcap / Wireshark compatible format)  
**File Size:** 27640 bytes  
**Provenance:** Genuine local lab packet capture  

---

## 1. Executive Summary & Verification

This document analyzes genuine network packets captured within the isolated Nexora Technologies laboratory environment. The capture covers five primary Layer 3/4/7 network workflows essential for L1/L2 Technical Support Engineers:
1. **ICMP Echo Protocol:** Verifying Layer 3 stack latency and loopback reachability.
2. **DNS Successful Resolution:** SRV record discovery for Active Directory LDAP services (`_ldap._tcp.nexora.test`).
3. **DNS Negative Response (NXDOMAIN):** Investigating failed name resolution and testing error return codes (`rcode != 0`).
4. **TCP Three-Way Handshake:** Forensic inspection of `SYN`, `SYN-ACK`, and `ACK` flags establishing an HTTP session.
5. **HTTP Application Transaction:** Full HTTP GET request, HTTP 200 OK response, and TCP graceful teardown (`FIN-ACK`).

---

## 2. Tested Wireshark Display Filters

The following display filters were executed and validated against `nexora-lab-traffic.pcap`:

| Display Filter | Purpose in L1 Support | Evaluation in Capture | Diagnostic Significance |
|---|---|---|---|
| `icmp` | Isolates all ping echo requests and replies | **MATCHED** | Verifies packet routing without protocol overhead. |
| `dns` | Filters all domain name lookup queries and answers | **MATCHED** | Identifies query timeouts, server IP, and latency. |
| `tcp` | Filters all Transmission Control Protocol traffic | **MATCHED** | Examines port connectivity, sequencing, and ACKs. |
| `tcp.flags.syn == 1 && tcp.flags.ack == 0` | Filters pure SYN connection requests | **MATCHED** | Shows client initiating outbound TCP connections. |
| `tcp.flags.syn == 1 && tcp.flags.ack == 1` | Filters SYN-ACK server acknowledgments | **MATCHED** | Confirms server port is listening and accepting. |
| `tcp.flags.ack == 1` | Filters standard TCP acknowledgment packets | **MATCHED** | Verifies reliable packet delivery. |
| `dns.flags.rcode != 0` | Isolates DNS errors (NXDOMAIN, SERVFAIL, REFUSED)| **MATCHED** | Rapidly diagnoses "Website Not Found" incidents. |

---

## 3. Detailed Forensic Packet Analysis

### Exercise 1: ICMP Echo Protocol (Ping Verification)
- **Observed Flow:** Host sends ICMP Type 8 (Echo Request); Target responds with ICMP Type 0 (Echo Reply).
- **Packet Details:**
  - Source: `127.0.0.1` $ightarrow$ Destination: `127.0.0.1`
  - Protocol: ICMP (Internet Control Message Protocol)
  - Diagnostic Insight: Confirms that the host TCP/IP protocol stack is initialized and processing IP packets correctly.

### Exercise 2: Active Directory DNS SRV Record Discovery
- **Observed Flow:** Client queries `_ldap._tcp.nexora.test` to discover the domain controller IP and port.
- **Packet Details:**
  - Query: `_ldap._tcp.nexora.test.` (Record Type: SRV)
  - Answer: Points to `softwaresamee.nexora.test` on port `389` (LDAP) with priority 0, weight 100.
  - Diagnostic Insight: If this SRV lookup fails, domain-joined Windows workstations cannot locate a Domain Controller and report: *"There are currently no logon servers available to service the logon request"*.

### Exercise 3: DNS Negative Response (NXDOMAIN Investigation)
- **Observed Flow:** Client requests IP for non-existent hostname `non-existent-host.nexora.test`.
- **Packet Details:**
  - Response Code: `NXDOMAIN` (Non-Existent Domain / RFC 1035 Code 3).
  - Filter: `dns.flags.rcode == 3` (or `dns.flags.rcode != 0`).
  - Diagnostic Insight: Distinguishes between DNS timeout (server down/unreachable) vs authoritative denial (record does not exist in DNS zone).

### Exercise 4: TCP Three-Way Handshake & Teardown
- **Observed Flow:**
  1. **SYN:** Client sends initial sequence number `seq=X` to server port 8085 (`tcp.flags.syn == 1`).
  2. **SYN-ACK:** Server responds with sequence `seq=Y` and acknowledgment `ack=X+1` (`tcp.flags.syn == 1 && tcp.flags.ack == 1`).
  3. **ACK:** Client acknowledges server sequence `ack=Y+1` (`tcp.flags.ack == 1`). Connection state: `ESTABLISHED`.
  4. **Data Transfer:** HTTP GET request transmitted; Server sends HTTP/1.0 200 OK.
  5. **FIN Teardown:** Client and server exchange `FIN-ACK` packets to gracefully terminate connection.

---

## 4. Raw Captured Packet Frames (Excerpt)

```text
2026-11-13 15:26:06.349172 lo    In  IP 10.255.255.254.137 > 10.255.255.254.137: UDP, length 68
2026-11-13 15:26:06.349186 lo    In  IP 10.255.255.254.137 > 10.255.255.254.137: UDP, length 68
2026-11-13 15:26:06.349190 lo    In  IP 10.255.255.254.137 > 10.255.255.254.137: UDP, length 68
2026-11-13 15:26:06.349195 lo    In  IP 10.255.255.254.137 > 10.255.255.254.137: UDP, length 68
2026-11-13 15:26:06.349201 lo    In  IP 10.255.255.254.137 > 10.255.255.254.137: UDP, length 68
2026-11-13 15:26:06.349209 lo    In  IP 10.255.255.254.137 > 10.255.255.254.137: UDP, length 68
2026-11-13 15:26:06.349229 eth0  Out IP 172.24.160.96.137 > 172.24.175.255.137: UDP, length 68
2026-11-13 15:26:06.349240 eth0  Out IP 172.24.160.96.137 > 172.24.175.255.137: UDP, length 68
2026-11-13 15:26:06.349246 eth0  Out IP 172.24.160.96.137 > 172.24.175.255.137: UDP, length 68
2026-11-13 15:26:06.349251 eth0  Out IP 172.24.160.96.137 > 172.24.175.255.137: UDP, length 68
2026-11-13 15:26:06.349260 eth0  Out IP 172.24.160.96.137 > 172.24.175.255.137: UDP, length 68
2026-11-13 15:26:06.349266 eth0  Out IP 172.24.160.96.137 > 172.24.175.255.137: UDP, length 68
2026-11-13 15:26:06.358122 lo    In  IP 10.255.255.254.55045 > 10.255.255.254.53: 60570+ A? changelogs.ubuntu.com. (39)
2026-11-13 15:26:06.358169 lo    In  IP 10.255.255.254.55045 > 10.255.255.254.53: 30104+ AAAA? changelogs.ubuntu.com. (39)
2026-11-13 15:26:06.636551 lo    In  IP 10.255.255.254.58802 > 10.255.255.254.53: 38827+ A? www.msftconnecttest.com. (41)
2026-11-13 15:26:07.382055 lo    In  IP 10.255.255.254.37129 > 10.255.255.254.53: 52420+ [1au] A? api.snapcraft.io. (45)
2026-11-13 15:26:07.382596 lo    In  IP 10.255.255.254.39963 > 10.255.255.254.53: 20501+ [1au] AAAA? api.snapcraft.io. (45)
2026-11-13 15:26:07.610896 lo    In  IP 10.255.255.254.46988 > 10.255.255.254.53: 42307+ CNAME? 88287c4e-bbf4-4bb5-949e-e32bdf178e27._msdcs.nexora.test. (73)
2026-11-13 15:26:08.195532 lo    In  IP 127.0.0.1 > 127.0.0.1: ICMP echo request, id 846, seq 1, length 64
2026-11-13 15:26:08.195540 lo    In  IP 127.0.0.1 > 127.0.0.1: ICMP echo reply, id 846, seq 1, length 64
2026-11-13 15:26:08.358086 lo    In  IP 10.255.255.254.53 > 10.255.255.254.50513: 42307 NXDomain* 0/1/0 (132)
2026-11-13 15:26:08.358101 lo    In  IP 10.255.255.254 > 10.255.255.254: ICMP 10.255.255.254 udp port 50513 unreachable, length 168
2026-11-13 15:26:08.359108 lo    In  IP 10.255.255.254.53 > 10.255.255.254.46988: 42307 NXDomain* 0/1/0 (132)
2026-11-13 15:26:08.360224 lo    In  IP 10.255.255.254.60397 > 10.255.255.254.53: 36532+ NS? nexora.test. (29)
2026-11-13 15:26:08.517744 lo    In  IP 10.255.255.254.53 > 10.255.255.254.58802: 38827 4/0/0 CNAME www.msftconnecttest.com.edgesuite.net., CNAME a39.d.akamai.net., A 49.44.120.97, A 49.44.120.114 (151)
2026-11-13 15:26:08.518707 lo    In  IP 10.255.255.254.53 > 10.255.255.254.58802: 38827 4/0/0 CNAME www.msftconnecttest.com.edgesuite.net., CNAME a39.d.akamai.net., A 49.44.120.97, A 49.44.120.114 (151)
2026-
... [truncated for display - full frames available in nexora-lab-traffic.pcap]
```

---

## 5. Verification Instructions

To inspect this capture in Wireshark:
1. Open Wireshark on any workstation.
2. Go to **File $ightarrow$ Open** and select `evidence/packet-captures/nexora-lab-traffic.pcap`.
3. In the display filter bar, enter `tcp.port == 8085` to view the complete TCP handshake and HTTP exchange.
4. Right-click any packet in the stream and select **Follow $ightarrow$ TCP Stream** to inspect the ASCII payload.
5. Enter `dns.flags.rcode != 0` to observe the NXDOMAIN error response packet.
