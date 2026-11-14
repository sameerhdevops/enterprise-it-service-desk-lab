# Domain Name System (DNS) Troubleshooting Guide
**Document ID:** NET-002  
**Audience:** L1 Support Engineers / Service Desk Analysts  
**Protocol:** UDP Port 53 (Queries) / TCP Port 53 (Zone Transfers & Large Payloads)

---

## 1. How DNS Resolution Works (The Step-by-Step Flow)

When an employee types `portal.nexora.com` into their browser:

```
[1. Browser Cache] ──(Miss)──> [2. Windows OS DNS Cache] ──(Miss)──> [3. Local hosts File]
                                                                             │ (Miss)
                                                                             ▼
[6. Authoritative Server] <── [5. Root/TLD Servers] <── [4. Corporate Recursive DNS Server]
   (e.g., nexora.com DC)                                    (NEX-DC01 - 192.168.20.10)
```

1. **Client Cache Check:** Windows checks its local memory cache (`ipconfig /displaydns`) and `C:\Windows\System32\drivers\etc\hosts`.
2. **Recursive Query to Local DNS:** Workstation queries corporate DNS server (`192.168.20.10`).
3. **Internal vs External Lookup:**
   - If querying an internal domain resource (`nexfs01.nexora.test`), the internal Domain Controller returns the private IP (`192.168.20.15`).
   - If querying a public domain (`google.com`), the corporate DNS server queries external Root hints, TLD servers, and authoritative nameservers on the user's behalf (or forwards to ISP DNS / `8.8.8.8`).

---

## 2. Common DNS Symptoms & The "IP vs. Name" Test

The definitive test to determine if a network failure is caused by DNS:
- Step 1: Run `ping 8.8.8.8` (or public IP).
  - *Result:* **Replies succeed.** (Layer 1, 2, 3, and default gateway are 100% operational!)
- Step 2: Run `ping www.google.com`.
  - *Result:* **"Ping request could not find host www.google.com. Please check the name and try again."**
  - *Conclusion:* **DNS FAILURE.** The network is fine, but the machine cannot translate human names into IP addresses.

---

## 3. Investigating DNS with `nslookup`

`nslookup` is the standard cross-platform command-line utility for querying DNS servers:

### Standard Query:
```cmd
nslookup intranet.nexora.test
```
*Expected Output:*
```
Server:  nex-dc01.nexora.test
Address:  192.168.20.10

Name:    intranet.nexora.test
Address:  192.168.20.50
```

### Testing Against an Alternate DNS Server:
Bypasses local DNS to verify if the issue is with the local server:
```cmd
nslookup intranet.nexora.test 192.168.20.10
nslookup www.google.com 8.8.8.8
```

### Inspecting Specific DNS Record Types:
```cmd
nslookup -type=MX nexora.com
nslookup -type=TXT nexora.com
```

---

## 4. L1 Resolution Sequence for Client-Side DNS Issues
1. **Flush and Register DNS:**
   ```cmd
   ipconfig /flushdns
   ipconfig /registerdns
   ```
2. **Inspect the Local `hosts` File:**
   - Open `C:\Windows\System32\drivers\etc\hosts` in Notepad.
   - Verify no malicious or outdated static IP entries are overriding proper resolution.
3. **Verify Adapter DNS Settings:**
   - Open `ncpa.cpl` > Properties of active NIC > IPv4 Properties.
   - Ensure DNS is set to "Obtain DNS server address automatically" (or pointing to valid corporate DNS IPs, never `127.0.0.1` unless it is a Domain Controller).

---

## 5. Layer 4 Port Testing vs. Layer 7 DNS Resolution Diagnostics

A critical distinction in enterprise network troubleshooting:

| Diagnostic Tool | Layer | Protocol / Port | What It Actually Tests | Common Pitfall / Limitation |
|---|---|---|---|---|
| `Test-NetConnection -Port 53` (or `telnet`) | Layer 4 (Transport) | TCP Port 53 | Verifies TCP three-way handshake (`SYN`, `SYN-ACK`, `ACK`) can be established with the host. | Does **NOT** test standard client DNS queries (which operate over **UDP 53**). A stateful firewall may permit TCP 53 while blocking UDP 53. Does not test if the DNS service responds with valid DNS records. |
| `Resolve-DnsName` (PowerShell) | Layer 7 (Application) | UDP 53 / TCP 53 fallback | Formulates an actual DNS request packet, queries the target nameserver, and parses the returned Resource Records (A, CNAME, MX). | True end-to-end DNS test. Accurately reports whether the nameserver is authoritative, reachable, and capable of resolving records. |
| `nslookup` (CMD / Cross-platform) | Layer 7 (Application) | UDP 53 / TCP 53 fallback | Directly queries configured or specified nameservers for specific record types. | True Layer 7 query. Bypasses local hosts file and OS resolver cache to test server health directly. |

**Key L1 Rule:** Never assume DNS is healthy simply because `Test-NetConnection -ComputerName <DC> -Port 53` returns `TcpTestSucceeded : True`. Always follow up with a Layer 7 query: `Resolve-DnsName -Name portal.corp.nexoratech.com -Server <DC-IP>` or `nslookup`.

