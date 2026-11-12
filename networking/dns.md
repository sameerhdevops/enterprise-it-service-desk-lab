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
   - If querying an internal domain resource (`nexfs01.nexora.local`), the internal Domain Controller returns the private IP (`192.168.20.15`).
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
nslookup intranet.nexora.local
```
*Expected Output:*
```
Server:  nex-dc01.nexora.local
Address:  192.168.20.10

Name:    intranet.nexora.local
Address:  192.168.20.50
```

### Testing Against an Alternate DNS Server:
Bypasses local DNS to verify if the issue is with the local server:
```cmd
nslookup intranet.nexora.local 192.168.20.10
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
