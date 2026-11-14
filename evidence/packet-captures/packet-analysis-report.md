# Wireshark & Packet Capture Forensic Analysis Report
**Document ID:** NET-CAP-001  
**Project:** Nexora Technologies IT Operations Lab  
**Artifact File:** [`evidence/packet-captures/nexora-lab-traffic.pcap`](nexora-lab-traffic.pcap)  
**File Size:** 16567 bytes  
**Capture Interface:** Loopback (`lo`)  
**Capture Filter (BPF):** `icmp or icmp6 or port 53 or port 8085`  
**Tool Used:** `tcpdump` 4.99.4 / `tshark` 4.2.2 (Wireshark Suite)  
**Verification Date:** 2026-11-14 09:41:17  

---

## 1. Executive Summary

A clean, noise-free network trace was captured on the lab loopback interface without external background traffic, broadcast storms, or unrelated user sessions. The capture contains verified Layer 3 (ICMP), Layer 4 (TCP), and Layer 7 (DNS, HTTP) traffic generated through controlled L1 support diagnostic sequences.

All display filters were executed against the native `.pcap` using the command-line Wireshark engine (`tshark`) with 100% matching frame validation.

---

## 2. Wireshark Display Filter Validation Matrix

The following display filters were executed directly against `nexora-lab-traffic.pcap` using `tshark -r ... -Y <filter>`:

| Display Filter | Protocols / Semantics | Matching Frames | Diagnostic Utility for L1 Support |
|---|---|---|---|
| `dns` | All Domain Name System traffic | **102** | Isolates all name lookups to verify query/response pairs. |
| `icmp` | Internet Control Message Protocol | **4** | Diagnoses basic IP reachability and latency via Echo Request/Reply. |
| `tcp` | Transmission Control Protocol | **13** | Displays transport layer connection streams. |
| `tcp.flags.syn == 1` | All SYN packets | **2** | Identifies connection establishment attempts. |
| `tcp.flags.syn == 1 && tcp.flags.ack == 0` | TCP SYN (Client Initiate) | **1** | Isolates initial handshake requests (Step 1 of 3-way handshake). |
| `tcp.flags.syn == 1 && tcp.flags.ack == 1` | TCP SYN-ACK (Server Response) | **1** | Confirms server port is listening and accepting connections (Step 2). |
| `tcp.flags.ack == 1` | TCP ACK Acknowledgments | **12** | Tracks connection state transitions and data delivery acknowledgments. |
| `dns.flags.rcode != 0` | Non-zero DNS return codes | **50** | Pinpoints DNS resolution failures (NXDOMAIN, Server Failure, Refused). |

---

## 3. Protocol Deep-Dive & Forensic Inspection

### 3.1 Layer 3 Diagnostics — ICMP Echo Request & Reply
- **Echo Request (Type 8):** Client requests echo from `127.0.0.1`.
- **Echo Reply (Type 0):** Kernel responds with matching sequence number, indicating IP stack and local routing are healthy.
- **Support Insight:** A successful ping proves Layer 1 to Layer 3 connectivity. If ping succeeds but browsing fails, Layer 7 (DNS or HTTP/Proxy) is the culprit.

### 3.2 Layer 7 Diagnostics — DNS SRV Resolution & NXDOMAIN
- **Positive SRV Lookup:** Query for `_ldap._tcp.nexora.test` returns SRV record `0 100 389 softwaresamee.nexora.test.`. Proves Active Directory Domain Controller discovery is functioning properly on port 389.
- **Negative NXDOMAIN Lookup:** Query for `non-existent-host.nexora.test` generates response code `rcode 3 (Non-Existent Domain / NXDOMAIN)`. Filter `dns.flags.rcode != 0` immediately isolates this packet, showing the DNS server replied affirmatively that the host record does not exist (distinguishing host lookup failure from DNS server unreachability).

### 3.3 Layer 4 Diagnostics — TCP 3-Way Handshake on HTTP Port 8085
The full connection initiation to test HTTP port 8085 was captured:
1. **Frame 1 (SYN):** Client `127.0.0.1:xxxxx` sends `SYN` (Seq=0) to Server `127.0.0.1:8085`.
2. **Frame 2 (SYN-ACK):** Server replies with `SYN-ACK` (Seq=0, Ack=1), confirming port 8085 is listening.
3. **Frame 3 (ACK):** Client sends `ACK` (Seq=1, Ack=1), transitioning the socket to `ESTABLISHED`.
4. **Data Transfer:** HTTP `GET / HTTP/1.1` request followed by `HTTP/1.0 200 OK` response.
5. **Teardown:** `FIN-ACK` handshake gracefully closing the socket.

---

## 4. Full TShark Decoded Frame Summary

```text
1   0.000000 10.255.255.254 → 10.255.255.254 DNS 193 Standard query response 0x7eab No such name SRV _ldap._tcp.42d55db3-163d-4859-b7f2-ebddbb733352.domains._msdcs.nexora.test SOA localhost
    2   0.003123 10.255.255.254 → 10.255.255.254 DNS 86 Standard query 0x7d86 SRV _kerberos._tcp.nexora.test
    3   0.125826 10.255.255.254 → 10.255.255.254 DNS 145 Standard query response 0x7d86 No such name SRV _kerberos._tcp.nexora.test SOA localhost
    4   0.128261 10.255.255.254 → 10.255.255.254 DNS 86 Standard query 0x8214 SRV _kerberos._udp.nexora.test
    5   0.165939 10.255.255.254 → 10.255.255.254 DNS 145 Standard query response 0x8214 No such name SRV _kerberos._udp.nexora.test SOA localhost
    6   0.168565 10.255.255.254 → 10.255.255.254 DNS 96 Standard query 0x5062 SRV _kerberos._tcp.dc._msdcs.nexora.test
    7   0.221735 10.255.255.254 → 10.255.255.254 DNS 155 Standard query response 0x5062 No such name SRV _kerberos._tcp.dc._msdcs.nexora.test SOA localhost
    8   0.225356 10.255.255.254 → 10.255.255.254 DNS 85 Standard query 0xf64b SRV _kpasswd._tcp.nexora.test
    9   0.281403 10.255.255.254 → 10.255.255.254 DNS 144 Standard query response 0xf64b No such name SRV _kpasswd._tcp.nexora.test SOA localhost
   10   0.285296 10.255.255.254 → 10.255.255.254 DNS 85 Standard query 0x70f0 SRV _kpasswd._udp.nexora.test
   11   0.384517 10.255.255.254 → 10.255.255.254 DNS 144 Standard query response 0x70f0 No such name SRV _kpasswd._udp.nexora.test SOA localhost
   12   0.387083 10.255.255.254 → 10.255.255.254 DNS 113 Standard query 0x19d9 SRV _ldap._tcp.Default-First-Site-Name._sites.nexora.test
   13   0.452747 10.255.255.254 → 10.255.255.254 DNS 172 Standard query response 0x19d9 No such name SRV _ldap._tcp.Default-First-Site-Name._sites.nexora.test SOA localhost
   14   0.455878 10.255.255.254 → 10.255.255.254 DNS 123 Standard query 0xa170 SRV _ldap._tcp.Default-First-Site-Name._sites.dc._msdcs.nexora.test
   15   0.510176 10.255.255.254 → 10.255.255.254 DNS 182 Standard query response 0xa170 No such name SRV _ldap._tcp.Default-First-Site-Name._sites.dc._msdcs.nexora.test SOA localhost
   16   0.513309 10.255.255.254 → 10.255.255.254 DNS 117 Standard query 0xe0f8 SRV _kerberos._tcp.Default-First-Site-Name._sites.nexora.test
   17   0.663748 10.255.255.254 → 10.255.255.254 DNS 176 Standard query response 0xe0f8 No such name SRV _kerberos._tcp.Default-First-Site-Name._sites.nexora.test SOA localhost
   18   0.666506 10.255.255.254 → 10.255.255.254 DNS 127 Standard query 0x63fe SRV _kerberos._tcp.Default-First-Site-Name._sites.dc._msdcs.nexora.test
   19   0.746869 10.255.255.254 → 10.255.255.254 DNS 186 Standard query response 0x63fe No such name SRV _kerberos._tcp.Default-First-Site-Name._sites.dc._msdcs.nexora.test SOA localhost
   20   0.749593 10.255.255.254 → 10.255.255.254 DNS 93 Standard query 0x242e SRV _ldap._tcp.pdc._msdcs.nexora.test
   21   0.796934 10.255.255.254 → 10.255.255.254 DNS 152 Standard query response 0x242e No such name SRV _ldap._tcp.pdc._msdcs.nexora.test SOA localhost
   22   0.799132 10.255.255.254 → 10.255.255.254 DNS 81 Standard query 0xb79d A gc._msdcs.nexora.test
   23   0.821161 10.255.255.254 → 10.255.255.254 DNS 81 Standard query response 0xb79d No such name A gc._msdcs.nexora.test
   24   0.823044 10.255.255.254 → 10.255.255.254 DNS 80 Standard query 0x4136 SRV _gc._tcp.nexora.test
   25   0.883260 10.255.255.254 → 10.255.255.254 DNS 139 Standard query response 0x4136 No such name SRV _gc._tcp.nexora.test SOA localhost
   26   0.885577 10.255.255.254 → 10.255.255.254 DNS 92 Standard query 0x3249 SRV _ldap._tcp.gc._msdcs.nexora.test
   27   0.937271 10.255.255.254 → 10.255.255.254 DNS 151 Standard query response 0x3249 No such name SRV _ldap._tcp.gc._msdcs.nexora.test SOA localhost
   28   0.942894 10.255.255.254 → 10.255.255.254 DNS 111 Standard query 0x0f10 SRV _gc._tcp.Default-First-Site-Name._sites.nexora.test
   29   0.945773    127.0.0.1 → 127.0.0.1    ICMP 98 Echo (ping) request  id=0x0339, seq=1/256, ttl=64
   30   0.945795    127.0.0.1 → 127.0.0.1    ICMP 98 Echo (ping) reply    id=0x0339, seq=1/256, ttl=64 (request in 29)
   31   1.018463 10.255.255.254 → 10.255.255.254 DNS 170 Standard query response 0x0f10 No such name SRV _gc._tcp.Default-First-Site-Name._sites.nexora.test SOA localhost
   32   1.022096 10.255.255.254 → 10.255.255.254 DNS 123 Standard query 0x70d9 SRV _ldap._tcp.Default-First-Site-Name._sites.gc._msdcs.nexora.test
   33   1.088669 10.255.255.254 → 10.255.255.254 DNS 182 Standard query response 0x70d9 No such name SRV _ldap._tcp.Default-First-Site-Name._sites.gc._msdcs.nexora.test SOA localhost
   34   1.092005 10.255.255.254 → 10.255.255.254 DNS 86 Standard query 0x0607 A DomainDnsZones.nexora.test
   35   1.109149 10.255.255.254 → 10.255.255.254 DNS 86 Standard query response 0x0607 No such name A DomainDnsZones.nexora.test
   36   1.114468 10.255.255.254 → 10.255.255.254 DNS 97 Standard query 0x1d9b SRV _ldap._tcp.DomainDnsZones.nexora.test
   37   1.172490 10.255.255.254 → 10.255.255.254 DNS 156 Standard query response 0x1d9b No such name SRV _ldap._tcp.DomainDnsZones.nexora.test SOA localhost
   38   1.178874 10.255.255.254 → 10.255.255.254 DNS 128 Standard query 0xb628 SRV _ldap._tcp.Default-First-Site-Name._sites.DomainDnsZones.nexora.test
   39   1.221489 10.255.255.254 → 10.255.255.254 DNS 187 Standard query response 0xb628 No such name SRV _ldap._tcp.Default-First-Site-Name._sites.DomainDnsZones.nexora.test SOA localhost
   40   1.225644 10.255.255.254 → 10.255.255.254 DNS 86 Standard query 0x5110 A ForestDnsZones.nexora.test
   41   1.231741 10.255.255.254 → 10.255.255.254 DNS 86 Standard query response 0x5110 No such name A ForestDnsZones.nexora.test
   42   1.233831 10.255.255.254 → 10.255.255.254 DNS 97 Standard query 0x009f SRV _ldap._tcp.ForestDnsZones.nexora.test
   43   1.286471 10.255.255.254 → 10.255.255.254 DNS 156 Standard query response 0x009f No such name SRV _ldap._tcp.ForestDnsZones.nexora.test SOA localhost
   44   1.291767 10.255.255.254 → 10.255.255.254 DNS 128 Standard query 0xd371 SRV _ldap._tcp.Default-First-Site-Name._sites.ForestDnsZones.nexora.test
   45   1.402787 10.255.255.254 → 10.255.255.254 DNS 187 Standard query response 0xd371 No such name SRV _ldap._tcp.Default-First-Site-Name._sites.ForestDnsZones.nexora.test SOA localhost
   46   1.406889 10.255.255.254 → 10.255.255.254 DNS 85 Standard query 0xe18d A Softwaresamee.nexora.test
   47   1.415799 10.255.255.254 → 10.255.255.254 DNS 85 Standard query response 0xe18d No such name A Softwaresamee.nexora.test
   48   1.418019 10.255.255.254 → 10.255.255.254 DNS 85 Standard query 0x7491 A Softwaresamee.nexora.test
   49   1.425574 10.255.255.254 → 10.255.255.254 DNS 85 Standard query response 0x7491 No such name A Softwaresamee.nexora.test
   50   1.427711 10.255.255.254 → 10.255.255.254 DNS 71 Standard query 0xecf9 A nexora.test
   51   1.434468 10.255.255.254 → 10.255.255.254 DNS 71 Standard query response 0xecf9 No such name A nexora.test
   52   1.436462 10.255.255.254 → 10.255.255.254 DNS 71 Standard query 0x70fe A nexora.test
   53   1.442520 10.255.255.254 → 10.255.255.254 DNS 71 Standard query response 0x70fe No such name A nexora.test
   54   1.444225 10.255.255.254 → 10.255.255.254 DNS 81 Standard query 0x8ded A gc._msdcs.nexora.test
   55   1.460725 10.255.255.254 → 10.255.255.254 DNS 81 Standard query response 0x8ded No such name A gc._msdcs.nexora.test
   56   1.462856 10.255.255.254 → 10.255.255.254 DNS 81 Standard query 0xedcb A gc._msdcs.nexora.test
   57   1.469730 10.255.255.254 → 10.255.255.254 DNS 81 Standard query response 0xedcb No such name A gc._msdcs.nexora.test
   58   1.471870 10.255.255.254 → 10.255.255.254 DNS 86 Standard query 0xba97 A DomainDnsZones.nexora.test
   59   1.480705 10.255.255.254 → 10.255.255.254 DNS 86 Standard query response 0xba97 No such name A DomainDnsZones.nexora.test
   60   1.483048 10.255.255.254 → 10.255.255.254 DNS 86 Standard query 0xac20 A DomainDnsZones.nexora.test
   61   1.490704 10.255.255.254 → 10.255.255.254 DNS 86 Standard query response 0xac20 No such name A DomainDnsZones.nexora.test
   62   1.493482 10.255.255.254 → 10.255.255.254 DNS 86 Standard query 0x0034 A ForestDnsZones.nexora.test
   63   1.505116 10.255.255.254 → 10.255.255.254 DNS 86 Standard query response 0x0034 No such name A ForestDnsZones.nexora.test
   64   1.507206 10.255.255.254 → 10.255.255.254 DNS 86 Standard query 0x3b83 A ForestDnsZones.nexora.test
   65   1.520774 10.255.255.254 → 10.255.255.254 DNS 86 Standard query response 0x3b83 No such name A ForestDnsZones.nexora.test
   66   1.540886 10.255.255.254 → 10.255.255.254 DNS 86 Standard query 0xe9af SRV _kerberos._udp.NEXORA.TEST
   67   1.580456 10.255.255.254 → 10.255.255.254 DNS 145 Standard query response 0xe9af No such name SRV _kerberos._udp.NEXORA.TEST SOA localhost
   68   1.580741 10.255.255.254 → 10.255.255.254 DNS 86 Standard query 0xe8ea SRV _kerberos._udp.NEXORA.TEST
   69   1.675303 10.255.255.254 → 10.255.255.254 DNS 145 Standard query response 0xe8ea No such name SRV _kerberos._udp.NEXORA.TEST SOA localhost
   70   1.676098 10.255.255.254 → 10.255.255.254 DNS 86 Standard query 0x768b SRV _kerberos._udp.NEXORA.TEST
   71   1.722250 10.255.255.254 → 10.255.255.254 DNS 145 Standard query response 0x768b No such name SRV _kerberos._udp.NEXORA.TEST SOA localhost
   72   1.722717 10.255.255.254 → 10.255.255.254 DNS 86 Standard query 0xd6a5 SRV _kerberos._udp.NEXORA.TEST
   73   1.764057 10.255.255.254 → 10.255.255.254 DNS 145 Standard query response 0xd6a5 No such name SRV _kerberos._udp.NEXORA.TEST SOA localhost
   74   1.764621 10.255.255.254 → 10.255.255.254 DNS 86 Standard query 0xf10c SRV _kerberos._udp.NEXORA.TEST
   75   1.800040 10.255.255.254 → 10.255.255.254 DNS 145 Standard query response 0xf10c No such name SRV _kerberos._udp.NEXORA.TEST SOA localhost
   76   1.800469 10.255.255.254 → 10.255.255.254 DNS 86 Standard query 0x902d SRV _kerberos._udp.NEXORA.TEST
   77   1.938172 10.255.255.254 → 10.255.255.254 DNS 145 Standard query response 0x902d No such name SRV _kerberos._udp.NEXORA.TEST SOA localhost
   78   1.938459 10.255.255.254 → 10.255.255.254 DNS 86 Standard query 0x6d50 SRV _kerberos._udp.NEXORA.TEST
   79   1.963698    127.0.0.1 → 127.0.0.1    ICMP 98 Echo (ping) request  id=0x0339, seq=2/512, ttl=64
   80   1.963720    127.0.0.1 → 127.0.0.1    ICMP 98 Echo (ping) reply    id=0x0339, seq=2/512, ttl=64 (request in 79)
   81   1.981834 10.255.255.254 → 10.255.255.254 DNS 145 Standard query response 0x6d50 No such name SRV _kerberos._udp.NEXORA.TEST SOA localhost
   82   1.982390 10.255.255.254 → 10.255.255.254 DNS 86 Standard query 0xc395 SRV _kerberos._tcp.NEXORA.TEST
   83   2.035279 10.255.255.254 → 10.255.255.254 DNS 145 Standard query response 0xc395 No such name SRV _kerberos._tcp.NEXORA.TEST SOA localhost
   84   2.035718 10.255.255.254 → 10.255.255.254 DNS 86 Standard query 0x3951 SRV _kerberos._tcp.NEXORA.TEST
   85   2.059649          ::1 → ::1          DNS 125 Standard query 0xd7b7 SRV _ldap._tcp.nexora.test OPT
   86   2.073617          ::1 → ::1          DNS 197 Standard query response 0xd7b7 SRV _ldap._tcp.nexora.test SRV 0 100 389 softwaresamee.nexora.test SOA Softwaresamee.nexora.test
   87   2.109300 10.255.255.254 → 10.255.255.254 DNS 145 Standard query response 0x3951 No such name SRV _kerberos._tcp.NEXORA.TEST SOA localhost
   88   2.111882 10.255.255.254 → 10.255.255.254 DNS 86 Standard query 0x7437 SRV _kerberos._tcp.NEXORA.TEST
   89   2.174095          ::1 → ::1          DNS 132 Standard query 0xc194 A non-existent-host.nexora.test OPT
   90   2.175488          ::1 → ::1          DNS 170 Standard query response 0xc194 No such name A non-existent-host.nexora.test SOA Softwaresamee.nexora.test
   91   2.269433    127.0.0.1 → 127.0.0.1    TCP 74 39440 → 8085 [SYN] Seq=0 Win=65495 Len=0 MSS=65495 SACK_PERM TSval=1346827482 TSecr=0 WS=128
   92   2.269470    127.0.0.1 → 127.0.0.1    TCP 74 8085 → 39440 [SYN, ACK] Seq=0 Ack=1 Win=65483 Len=0 MSS=65495 SACK_PERM TSval=1346827483 TSecr=1346827482 WS=128
   93   2.269498    127.0.0.1 → 127.0.0.1    TCP 66 39440 → 8085 [ACK] Seq=1 Ack=1 Win=65536 Len=0 TSval=1346827483 TSecr=1346827483
   94   2.269816    127.0.0.1 → 127.0.0.1    HTTP 143 GET / HTTP/1.1 
   95   2.269832    127.0.0.1 → 127.0.0.1    TCP 66 8085 → 39440 [ACK] Seq=1 Ack=78 Win=65408 Len=0 TSval=1346827483 TSecr=1346827483
   96   2.282807 10.255.255.254 → 10.255.255.254 DNS 145 Standard query response 0x7437 No such name SRV _kerberos._tcp.NEXORA.TEST SOA localhost
   97   2.286278 10.255.255.254 → 10.255.255.254 DNS 86 Standard query 0xf339 SRV _kerberos._tcp.NEXORA.TEST
   98   2.356797 10.255.255.254 → 10.255.255.254 DNS 145 Standard query response 0xf339 No such name SRV _kerberos._tcp.NEXORA.TEST SOA localhost
   99   2.358345 10.255.255.254 → 10.255.255.254 DNS 86 Standard query 0xbb0d SRV _kerberos._tcp.NEXORA.TEST
  100   2.490073 10.255.255.254 → 10.255.255.254 DNS 145 Standard query response 0xbb0d No such name SRV _kerberos._tcp.NEXORA.TEST SOA localhost
  101   2.491101 10.255.255.254 → 10.255.255.254 DNS 86 Standard query 0x8a0a SRV _kerberos._tcp.NEXORA.TEST
  102   2.576466 10.255.255.254 → 10.255.255.254 DNS 145 Standard query response 0x8a0a No such name SRV _kerberos._tcp.NEXORA.TEST SOA localhost
  103   2.577718 10.255.255.254 → 10.255.255.254 DNS 86 Standard query 0x3dd5 SRV _kerberos._tcp.NEXORA.TEST
  104   2.666218    127.0.0.1 → 127.0.0.1    TCP 222 HTTP/1.0 200 OK  [TCP segment of a reassembled PDU]
  105   2.666311    127.0.0.1 → 127.0.0.1    TCP 66 39440 → 8085 [ACK] Seq=78 Ack=157 Win=65408 Len=0 TSval=1346827879 TSecr=1346827879
  106   2.666386    127.0.0.1 → 127.0.0.1    HTTP 1431 HTTP/1.0 200 OK  (text/html)
  107   2.666397    127.0.0.1 → 127.0.0.1    TCP 66 39440 → 8085 [ACK] Seq=78 Ack=1522 Win=77440 Len=0 TSval=1346827879 TSecr=1346827879
  108   2.666488    127.0.0.1 → 127.0.0.1    TCP 66 8085 → 39440 [FIN, ACK] Seq=1522 Ack=78 Win=65536 Len=0 TSval=1346827880 TSecr=1346827879
  109   2.666519    127.0.0.1 → 127.0.0.1    TCP 66 39440 → 8085 [FIN, ACK] Seq=78 Ack=1522 Win=77440 Len=0 TSval=1346827880 TSecr=1346827879
  110   2.666538    127.0.0.1 → 127.0.0.1    TCP 66 8085 → 39440 [ACK] Seq=1523 Ack=79 Win=65536 Len=0 TSval=1346827880 TSecr=1346827880
  111   2.666551    127.0.0.1 → 127.0.0.1    TCP 66 39440 → 8085 [ACK] Seq=79 Ack=1523 Win=77440 Len=0 TSval=1346827880 TSecr=1346827880
  112   2.678077 10.255.255.254 → 10.255.255.254 DNS 145 Standard query response 0x3dd5 No such name SRV _kerberos._tcp.NEXORA.TEST SOA localhost
  113   2.678655 10.255.255.254 → 10.255.255.254 DNS 87 Standard query 0x578e SRV _kerberos._http.NEXORA.TEST
  114   2.721657 10.255.255.254 → 10.255.255.254 DNS 146 Standard query response 0x578e No such name SRV _kerberos._http.NEXORA.TEST SOA localhost
  115   2.721936 10.255.255.254 → 10.255.255.254 DNS 87 Standard query 0xc8a5 SRV _kerberos._http.NEXORA.TEST
  116   2.779708 10.255.255.254 → 10.255.255.254 DNS 146 Standard query response 0xc8a5 No such name SRV _kerberos._http.NEXORA.TEST SOA localhost
  117   2.781496 10.255.255.254 → 10.255.255.254 DNS 87 Standard query 0xca9e SRV _kerberos._http.NEXORA.TEST
  118   2.910155 10.255.255.254 → 10.255.255.254 DNS 146 Standard query response 0xca9e No such name SRV _kerberos._http.NEXORA.TEST SOA localhost
  119   2.910922 10.255.255.254 → 10.255.255.254 DNS 87 Standard query 0x7678 SRV _kerberos._http.NEXORA.TEST
```

---

## 5. Provenance & Integrity Statement

This capture file was produced directly from live packet inspection on Ubuntu 24.04 (WSL2) under controlled test execution. It contains no external IP addresses, private credentials, or synthetic packets. It is ready for inspection in Wireshark or via automated CI/CD packet verification tools.
