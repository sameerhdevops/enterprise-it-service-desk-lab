# Portfolio Evidence Register & Verification Index
**Document ID:** EVD-REG-001  
**Project:** Enterprise IT Service Desk & End-User Support Operations Lab  
**Organization:** Nexora Technologies (Simulated Lab)  
**Location:** `D:\Projects\enterprise-it-service-desk-lab\evidence`  
**Last Verified:** 2026-11-12  

---

## 1. Evidence Classification Policy
In accordance with professional engineering ethics and interview defensibility standards:
- **Category A — Genuine Command Outputs (`evidence/command-output/`):** Real text-based outputs captured directly from the Windows 11 host machine, formatted and sanitized with standard Nexora corporate enterprise hostnames and private subnets (`NEX-WS01`, `192.168.10.x`) to preserve host privacy while maintaining 100% technical accuracy.
- **Category B — Generated Illustrative Visuals (`evidence/illustrative/`):** Vector-rendered diagrams illustrating workflows, architectures, and topologies. Prominently watermarked and labeled as `ILLUSTRATIVE / SIMULATED`. Never fabricated as vendor UI screenshots.
- **Category C — Genuine Application Screenshots (`evidence/platform-screenshots/`):** Real screenshots captured from live application sessions. Setup guides and capture checklists provided for SaaS platforms requiring candidate cloud credentials.
- **Category D — Automated Validation Artifacts (`evidence/validation/`):** Execution logs of automated unit tests and CSV dataset validators.

---

## 2. Complete Evidence Inventory

| Filename | Directory | Category | Related Module | What It Demonstrates | Genuine or Illustrative | Verification Status |
|---|---|---|---|---|---|---|
| `os-architecture.txt` | `command-output/` | A | Win Support | Host OS build (Win 11 Ent 26300), 64-bit architecture, and 16GB physical memory verification. | **Genuine Host Output** | **VERIFIED (Live Captured)** |
| `ipconfig-all.txt` | `command-output/` | A | Networking | Full network adapter configuration, IPv4 lease, default gateway, and DNS servers. | **Genuine Host Output** | **VERIFIED (Live Captured)** |
| `route-print.txt` | `command-output/` | A | Networking | Windows IPv4 active routing table, network destinations, netmasks, and interface metrics. | **Genuine Host Output** | **VERIFIED (Live Captured)** |
| `top-processes-cpu.txt` | `command-output/` | A | Win Support | Live process table sorted by CPU and Working Set memory consumption via PowerShell. | **Genuine Host Output** | **VERIFIED (Live Captured)** |
| `services-status.txt` | `command-output/` | A | Win Support | Live service state query (Print Spooler, Windows Update, DHCP Client, DNS Cache, EventLog). | **Genuine Host Output** | **VERIFIED (Live Captured)** |
| `net-user.txt` | `command-output/` | A | Active Directory | Local user accounts list query demonstrating Windows Security Accounts Manager (SAM) triage. | **Genuine Host Output** | **VERIFIED (Live Captured)** |
| `test-netconnection-dns-port.txt` | `command-output/` | A | Networking | Layer 4 TCP port probe (port 53 DNS reachability) using PowerShell `Test-NetConnection`. | **Genuine Host Output** | **VERIFIED (Live Captured)** |
| `nslookup-public-dns.txt` | `command-output/` | A | Networking | DNS resolution query to public DNS (`8.8.8.8`) testing external name resolution. | **Genuine Host Output** | **VERIFIED (Live Captured)** |
| `nexora-topology.txt` | `network-diagrams/` | A | Networking | Full ASCII topology layout, VLAN 10/20 subnet plan, and port mapping for Cisco Packet Tracer. | **Genuine Technical Spec** | **VERIFIED (Lab Model)** |
| `test-results-log.txt` | `validation/` | D | Reporting & QA | Execution log of 7 unit tests and 5 CSV dataset integrity validations (0 errors). | **Genuine Automated Log** | **VERIFIED (100% Pass)** |
| `it-service-desk-architecture.svg` | `illustrative/` | B | Architecture | Multi-tiered support model: Employee intake channels -> ITSM -> L1 Support -> Resolution/Escalation. | **Illustrative Diagram** | **VERIFIED (Generated SVG)** |
| `incident-lifecycle-flow.svg` | `illustrative/` | B | ITIL / ITSM | State transition machine: New -> In Progress -> On Hold -> Resolved -> Closed with SLA pause rules. | **Illustrative Diagram** | **VERIFIED (Generated SVG)** |
| `ticket-escalation-workflow.svg` | `illustrative/` | B | ITIL / Operations | Functional escalation (L1 -> L2 Desktop / Network -> L3) and hierarchical management escalation triggers. | **Illustrative Diagram** | **VERIFIED (Generated SVG)** |
| `network-topology-diagram.svg` | `illustrative/` | B | Networking | Visual 2-VLAN network design: Cisco 2911 router-on-a-stick, Cisco 2960 switch, user and server subnets. | **Illustrative Diagram** | **VERIFIED (Generated SVG)** |
| `windows-troubleshooting-flow.svg` | `illustrative/` | B | Win Support | Decision tree for troubleshooting slow Windows systems: uptime check, Fast Startup triage, CPU/RAM/Disk. | **Illustrative Diagram** | **VERIFIED (Generated SVG)** |
| `asset-management-lifecycle.svg` | `illustrative/` | B | Asset Management | 5-stage ITAM hardware lifecycle: Procurement -> Ingestion -> Deployment -> Maintenance -> Retirement. | **Illustrative Diagram** | **VERIFIED (Generated SVG)** |
| `sla-reporting-dashboard.svg` | `illustrative/` | B | Reporting / MIS | Visual MIS KPI dashboard: 28 interactions, 85% L1 Resolution Rate, 11.51h MTTR, and SLA compliance matrix. | **Illustrative Diagram** | **VERIFIED (Generated SVG)** |
| `screenshot-capture-guide.md` | `platform-screenshots/` | C | ITSM Platforms | Detailed step-by-step navigation paths and checklists for capturing genuine ServiceNow & JSM screenshots. | **Procedural Guide** | **DOCUMENTED (Manual Step)** |

---

## 3. Defensibility Summary
- **Zero Hallucinated Screenshots:** No synthetic mockups are masqueraded as genuine software interfaces.
- **Clear Demarcation:** Illustrative diagrams reside strictly in `evidence/illustrative/` and carry explicit top-banner watermarks.
- **Reproducible Evidence:** All genuine command logs and test execution logs can be re-executed and reproduced on the host machine at any time using provided scripts.
