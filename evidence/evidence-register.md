# Portfolio Evidence Register & Verification Index
**Document ID:** EVD-REG-001
**Project:** IT Support & Service Desk Operations Lab
**Organization:** Nexora Technologies (Simulated Lab)

---

## 1. Evidence Classification & Provenance Policy

In accordance with engineering ethics and interview defensibility standards, all portfolio evidence is explicitly categorized by its genuine provenance:

1. **Genuine Host Output (`evidence/command-output/`):** Output from diagnostic tools executing on the local Windows host environment.
2. **Sanitized Host Output (`evidence/command-output/`):** Output from diagnostic tools with personal host identifiers (usernames, physical MACs, LAN IP subnets) replaced by transparent, explicit placeholders (`[REDACTED_HOST]`, `[REDACTED_IP]`, `[REDACTED_MAC]`, `[REDACTED_USERNAME]`).
3. **Simulated Technical Example (`evidence/network-diagrams/`):** Text-based network design specifications and ASCII topologies modeling small office networks.
4. **Automated Test Output (`evidence/validation/`, `evidence/itsm/`):** Execution logs of automated unit tests, dataset validators, and functional HTTP test suites run directly against project code.
5. **Direct Platform / Domain Capture (`evidence/active-directory/`, `evidence/packet-captures/`):** Outputs captured directly from local lab services (Samba 4 Active Directory Domain Controller in WSL2, tcpdump/TShark packet traces).

---

## 2. Evidence Inventory

| Filename | Directory | Classification | Related Area | Description & Demonstrated Skill | Provenance |
|---|---|---|---|---|---|
| `os-architecture.txt` | `command-output/` | Host Output | Windows OS | Windows 11 Enterprise (64-bit), physical RAM query via `Win32_OperatingSystem`. | Windows Host Command |
| `services-status.txt` | `command-output/` | Host Output | Windows Services | Query of core Windows services (`Spooler`, `Dhcp`, `Dnscache`, `EventLog`, `wuauserv`). | Windows Host Command |
| `nslookup-public-dns.txt` | `command-output/` | Host Output | Networking / DNS | Direct DNS resolution query testing nameserver `8.8.8.8` for `dns.google`. | Windows Host Command |
| `ipconfig-all.txt` | `command-output/` | Sanitized Host Output | Networking | Adapter configuration, subnet mask, gateway, and DNS servers with privacy placeholders. | Sanitized Output |
| `route-print.txt` | `command-output/` | Sanitized Host Output | Networking | Windows IPv4 active routing table, destinations, netmasks, and gateway metrics. | Sanitized Output |
| `net-user.txt` | `command-output/` | Sanitized Host Output | Access / SAM | Local Windows user accounts query demonstrating Security Accounts Manager (SAM) triage. | Sanitized Output |
| `top-processes-cpu.txt` | `command-output/` | Sanitized Host Output | Windows Performance | Process table sorted by CPU and Working Set memory consumption via PowerShell. | Sanitized Output |
| `test-netconnection-dns-port.txt` | `command-output/` | Sanitized Host Output | Networking | Layer 4 TCP port 53 probe using PowerShell `Test-NetConnection`. | Sanitized Output |
| `nexora-topology.txt` | `network-diagrams/` | Technical Specification | Networking | ASCII topology layout, 3-VLAN (VLAN 10/20/99) subnet plan, and port mapping for Cisco reference design. | Technical Spec |
| `test-results-log.txt` | `validation/` | Automated Test Output | Reporting & QA | Execution log of 13 unit tests and 5 CSV dataset integrity validations (0 errors). | Automated Test Log |
| `samba-ad-dc-verification.txt` | `active-directory/` | Domain Capture | Active Directory | Live Samba 4 AD DC deployment: Forest functional level, password policy, AGDLP group nesting, Kerberos ticket `kinit`/`klist`, clean DNS resolution, restrictive 2770 permissions, and verified `NT_STATUS_ACCESS_DENIED` blocks on unauthorized share access. | Linux/WSL2 Samba AD Capture |
| `nexora-lab-traffic.pcap` | `packet-captures/` | Packet Capture | Networking / TShark | Native 3,776-byte `.pcap` capture (20 frames) of isolated loopback ICMP, DNS SRV query, DNS NXDOMAIN, TCP 3-way handshake, and HTTP GET/200 traffic. | Direct tcpdump Capture |
| `packet-analysis-report.md` | `packet-captures/` | Analysis Report | Networking / TShark | Frame-by-frame analysis report with 8 display filters verified via `tshark 4.2.2`, packet flow diagrams, and dynamic frame queries. | Forensic TShark Inspection |
| `live-service-desk-export.json` | `itsm/` | Platform Export | ITSM / Service Desk | Sanitized JSON export of active tickets with calculated SLA metadata from the live operational web Service Desk engine (`itsm/portal/app.py`). | Sanitized Platform Export |
| `service-desk-test-evidence.txt` | `itsm/` | Automated Test Output | ITSM / Service Desk | Automated functional HTTP test log verifying 17 test modules: input validation, PBKDF2 auth, state machine transitions, XSS defense, customer token access, Origin/Referer same-origin checks (scheme, host, port), security headers & CSP, and database credential migration. | Automated Test Log |
| `m365-client-diagnostics-output.txt` | `microsoft-365/` | Host Output | Microsoft 365 Client | PowerShell diagnostic scan of Click-to-Run Office, Teams local cache path, OneDrive process status, and measured TCP 443 socket connect latencies. | Windows Host Diagnostic |

---

## 3. Defensibility & Privacy Standards
- **Zero Fabricated Screenshots:** No synthetic mockups or vendor interfaces are presented as genuine application screenshots.
- **Explicit Redaction:** Host privacy is protected using standard placeholders (`[REDACTED_HOST]`, `[REDACTED_IP]`) while maintaining exact command syntax and output structures.
- **Credential Hygiene:** Live environments utilize securely generated, unique credentials stored in git-ignored local secret stores (`.ad_credentials.json`, `.local_credentials.json`) protected by operating system filesystem permissions.
- **Reproducible Testing:** Automated unit tests (13 tests), Service Desk functional tests (17 tests), and dataset validators execute cleanly with zero external runtime dependencies.
