# Portfolio Evidence Register & Verification Index
**Document ID:** EVD-REG-001  
**Project:** Enterprise IT Service Desk & End-User Support Operations Lab  
**Organization:** Nexora Technologies (Simulated Lab)  
**Location:** `D:\Projects\enterprise-it-service-desk-lab\evidence`  
**Last Verified:** 2026-11-14 (Final Remediation & Verification)  

---

## 1. Evidence Classification & Provenance Policy

In accordance with strict engineering ethics and interview defensibility standards, all portfolio evidence is explicitly categorized by its genuine provenance:

1. **Genuine Host Output (`evidence/command-output/`):** Captured directly from the local Windows 11 host operating system without modification.
2. **Redacted Host Output (`evidence/command-output/`):** Captured directly from the Windows 11 host with sensitive personal identifiers (usernames, physical MACs, LAN IP subnets) replaced by transparent, explicit placeholders (`[REDACTED_HOST]`, `[REDACTED_IP]`, `[REDACTED_MAC]`, `[REDACTED_USERNAME]`).
3. **Simulated Technical Example (`evidence/network-diagrams/`):** Text-based technical configurations and topologies modeling lab networks (e.g., Cisco Packet Tracer router/switch specs).
4. **Generated Illustrative Diagram (`evidence/illustrative/`):** Standalone vector SVG diagrams clearly depicting workflows, architectures, and dashboards. Prominently watermarked `[ILLUSTRATIVE / SIMULATED LAB ARTIFACT - NOT A REAL VENDOR SCREENSHOT]`. Never misrepresented as actual application UI screenshots.
5. **Automated Test Output (`evidence/validation/`):** Execution logs of automated unit tests and CSV dataset validators run directly against project code.
6. **Manual Screenshot Guide (`evidence/platform-screenshots/`):** Procedural step-by-step navigation instructions and checklists for candidate capture when accessing external SaaS platforms. *Note: Procedural guides are instructional artifacts and are not classified as application screenshots.*

---

## 2. Complete Evidence Inventory

| Filename | Directory | Classification | Related Area | Description & Demonstrated Skill | Provenance | Verification Status |
|---|---|---|---|---|---|---|
| `os-architecture.txt` | `command-output/` | Genuine Host Output | Windows OS | Windows 11 Enterprise (Build 26300, 64-bit), 16GB physical RAM via `Win32_OperatingSystem`. | Direct Windows 11 Host Capture | **VERIFIED (Live)** |
| `services-status.txt` | `command-output/` | Genuine Host Output | Windows Services | Query of essential core services (`Spooler`, `Dhcp`, `Dnscache`, `EventLog`, `wuauserv`). | Direct Windows 11 Host Capture | **VERIFIED (Live)** |
| `nslookup-public-dns.txt` | `command-output/` | Genuine Host Output | Networking / DNS | Direct DNS resolution query testing nameserver `8.8.8.8` for `dns.google`. | Direct Windows 11 Host Capture | **VERIFIED (Live)** |
| `ipconfig-all.txt` | `command-output/` | Redacted Host Output | Networking | Adapter configuration, subnet mask, gateway, and DNS servers with privacy placeholders. | Redacted Host Output | **VERIFIED (Redacted)** |
| `route-print.txt` | `command-output/` | Redacted Host Output | Networking | Windows IPv4 active routing table, destinations, netmasks, and gateway metrics. | Redacted Host Output | **VERIFIED (Redacted)** |
| `net-user.txt` | `command-output/` | Redacted Host Output | Access / SAM | Local Windows user accounts query demonstrating Security Accounts Manager (SAM) triage. | Redacted Host Output | **VERIFIED (Redacted)** |
| `top-processes-cpu.txt` | `command-output/` | Redacted Host Output | Windows Performance | Process table sorted by CPU and Working Set memory consumption via PowerShell. | Redacted Host Output | **VERIFIED (Redacted)** |
| `test-netconnection-dns-port.txt` | `command-output/` | Redacted Host Output | Networking | Layer 4 TCP port 53 probe using PowerShell `Test-NetConnection`. | Redacted Host Output | **VERIFIED (Redacted)** |
| `nexora-topology.txt` | `network-diagrams/` | Simulated Technical Example | Networking | ASCII topology layout, VLAN 10/20 subnet plan, and port mapping for Cisco Packet Tracer. | Simulated Technical Spec | **VERIFIED (Lab Spec)** |
| `test-results-log.txt` | `validation/` | Automated Test Output | Reporting & QA | Execution log of 13 unit tests and 5 CSV dataset integrity validations (0 errors). | Automated Test Execution | **VERIFIED (100% Pass)** |
| `samba-ad-dc-verification.txt` | `active-directory/` | Genuine Domain Output | Active Directory / Identity | Live Samba 4 AD DC deployment: Forest functional level 2008 R2, password policy, 12 users with unique generated credentials, textbook AGDLP group nesting (`GG-*` -> `DL-*`), Kerberos ticket `kinit`/`klist`, clean DNS resolution (stale IPs purged; resolves strictly to DC IP), restrictive 2770 permissions, and verified `NT_STATUS_ACCESS_DENIED` blocks on unauthorized share access. | Direct Linux/WSL2 Samba AD Capture | **VERIFIED (Live)** |
| `nexora-lab-traffic.pcap` | `packet-captures/` | Genuine Packet Capture | Networking / Packet Analysis | Native 3,776-byte `.pcap` capture (20 frames) of isolated loopback ICMP, DNS SRV query, DNS NXDOMAIN, TCP 3-way handshake, and HTTP GET/200 traffic. | Direct tcpdump Capture | **VERIFIED (Live)** |
| `packet-analysis-report.md` | `packet-captures/` | Forensic Analysis Report | Networking / Wireshark | In-depth frame-by-frame analysis report with 8 display filters verified via `tshark 4.2.2`, packet flow diagrams, strict zero-fallback assertions, and dynamic frame queries. | Forensic TShark Inspection | **VERIFIED (Live)** |
| `live-service-desk-export.json` | `itsm/` | Operational Platform Export | ITSM / Service Desk | JSON export of 17 active tickets with calculated SLA metadata from the live operational web Service Desk engine (`itsm/portal/app.py`). | Live Platform Database Export | **VERIFIED (Live)** |
| `service-desk-test-evidence.txt` | `itsm/` | Automated Test Output | ITSM / Service Desk | Automated functional HTTP test log verifying 17 test modules: input validation, PBKDF2 auth, state machine transitions, XSS defense, customer token access, CSRF/origin checks (scheme, host, port), security headers & CSP, and existing DB credential migration. | Automated Test Execution | **VERIFIED (100% Pass)** |
| `m365-client-diagnostics-output.txt` | `microsoft-365/` | Genuine Host Output | Microsoft 365 & Cloud Identity | Live PowerShell diagnostic scan of Click-to-Run v16.0.19127, Teams LocalCache path, OneDrive process status, and measured TCP 443 connect latencies via direct TcpClient.Connect. | Direct Windows 11 Host Capture | **VERIFIED (Live)** |
| `it-service-desk-architecture.svg` | `illustrative/` | Generated Illustrative Diagram | Architecture | Multi-tiered support model: Intake channels -> ITSM -> L1 Support -> Escalation paths. | Generated Vector SVG | **VERIFIED (Illustrative)** |
| `incident-lifecycle-flow.svg` | `illustrative/` | Generated Illustrative Diagram | ITIL / ITSM | State transition machine: New -> In Progress -> On Hold -> Resolved -> Closed with pause rules. | Generated Vector SVG | **VERIFIED (Illustrative)** |
| `ticket-escalation-workflow.svg` | `illustrative/` | Generated Illustrative Diagram | ITIL / Operations | Functional escalation (L1 -> L2 Desktop / Network -> L3) and hierarchical management triggers. | Generated Vector SVG | **VERIFIED (Illustrative)** |
| `network-topology-diagram.svg` | `illustrative/` | Generated Illustrative Diagram | Networking | 2-VLAN network design: Cisco 2911 router-on-a-stick, Cisco 2960 switch, user and server subnets. | Generated Vector SVG | **VERIFIED (Illustrative)** |
| `windows-troubleshooting-flow.svg` | `illustrative/` | Generated Illustrative Diagram | Windows Support | Triage decision tree for slow Windows systems: uptime check, cold restart, CPU/RAM/Disk triage. | Generated Vector SVG | **VERIFIED (Illustrative)** |
| `asset-management-lifecycle.svg` | `illustrative/` | Generated Illustrative Diagram | Asset Management | 5-stage ITAM hardware lifecycle: Procurement -> Ingestion -> Deployment -> Maintenance -> Retirement. | Generated Vector SVG | **VERIFIED (Illustrative)** |
| `sla-reporting-dashboard.svg` | `illustrative/` | Generated Illustrative Diagram | Reporting / MIS | Visual MIS KPI dashboard: 28 interactions, 85% L1 Resolution, 15.75h MTTR, SLA compliance breakdown. | Generated Vector SVG | **VERIFIED (Illustrative)** |
| `screenshot-capture-guide.md` | `platform-screenshots/` | Manual Screenshot Guide | ITSM Platforms | Procedural step-by-step navigation paths and capture checklists for ServiceNow & JSM. | Procedural Guide Only | **DOCUMENTED (No Mockups)** |

---

## 3. Defensibility Summary
- **Zero Fabricated Screenshots:** No synthetic mockups or vendor interfaces are presented as genuine application screenshots.
- **Explicit Redaction:** Host privacy is protected using standard placeholders (`[REDACTED_HOST]`, `[REDACTED_IP]`) while maintaining exact real command structures.
- **Credential Hygiene & Local Secret Storage:** Historical Git commits contain invalidated test credentials that have been rotated. Live environments utilize securely generated, unique credentials stored in git-ignored local secret stores (`.ad_credentials.json`, `.local_credentials.json`) protected by operating system filesystem ACLs (`icacls` on Windows, `chmod 600` on POSIX).
- **Accurate Content Security Policy:** The Service Desk portal serves `default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self';`, properly securing network communication and media to same-origin while transparently permitting the local inline JavaScript necessary for self-contained single-page interfaces without claiming false strictness.
- **Clear Demarcation:** Illustrative diagrams reside strictly in `evidence/illustrative/` and carry prominent top-banner watermarks.
- **Reproducible Testing:** Automated unit tests (13 tests) and Service Desk functional tests (17 tests) execute directly via the Python standard library with zero external dependencies.
