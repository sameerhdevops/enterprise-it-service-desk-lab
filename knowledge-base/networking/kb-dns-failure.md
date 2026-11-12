# Standard Knowledge Base Article: Diagnosing & Resolving DNS Resolution Failures
**KB ID:** KB0003  
**Category:** Networking / DNS  
**Author:** Nexora IT Service Desk (L1 Support)  
**Last Reviewed:** 2024-11-12  

---

### Symptoms
- Workstation can ping external IP addresses (e.g., `8.8.8.8`), but cannot browse websites by name.
- Web browser reports: `DNS_PROBE_FINISHED_NXDOMAIN` or `Server IP address could not be found`.
- Internal hostnames like `nexfs01` or `intranet.nexora.local` fail to resolve.

### Applicable Systems
- All Windows 10/11 endpoints domain-joined to `nexora.local`.

### Prerequisites
- Command Prompt / PowerShell console.

### Troubleshooting Steps
1. **Differentiate IP vs. FQDN Resolution:**
   - Execute: `ping 8.8.8.8` (Confirms Layer 1–3 routing is working).
   - Execute: `ping www.google.com` (Fails with "could not find host").
2. **Inspect Current DNS Server Assignment:**
   - Run `ipconfig /all` and check `DNS Servers`.
   - Normal corporate DNS: `192.168.20.10` (NEX-DC01).
   - If set to a public address (e.g., `8.8.8.8` or `192.168.1.1` from a home Wi-Fi network), internal `.nexora.local` resources will fail.
3. **Query DNS via `nslookup`:**
   ```cmd
   nslookup intranet.nexora.local
   nslookup www.google.com 192.168.20.10
   ```
4. **Check Local Hosts File:**
   - Check `C:\Windows\System32\drivers\etc\hosts` to verify no incorrect hardcoded IP mappings exist.

### Resolution
- Flush the client DNS resolver cache:
  ```cmd
  ipconfig /flushdns
  ipconfig /registerdns
  ```
- Reset adapter DNS configuration to automatic DHCP:
  - Open `ncpa.cpl` > Properties > IPv4 Properties > select **"Obtain DNS server address automatically"**.

### Verification
- Run `nslookup intranet.nexora.local`; verify it returns valid IP `192.168.20.50`.
- Open browser and successfully load internal intranet and external websites.

### Escalation Instructions
- If `nslookup` against `192.168.20.10` returns "Server Failed" across multiple computers, escalate immediately to **L3 Infrastructure** (DNS Server service on Domain Controller down).

### Related Incidents
- INC-N002, PRB0003
