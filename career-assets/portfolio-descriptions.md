# Professional Career Profile Assets & Portfolio Descriptions
**Project:** Enterprise IT Service Desk & End-User Support Operations Lab (Nexora Technologies)
**Target Roles:** IT Support Engineer L1 / Technical Support Engineer / Service Desk Analyst / Desktop Support Engineer
**Candidate:** Sameer H
**GitHub Repository:** [https://github.com/sameerhdevops/enterprise-it-service-desk-lab](https://github.com/sameerhdevops/enterprise-it-service-desk-lab)
**Disclaimer:** All achievements and technical descriptions below represent genuine, tested, and reproducible hands-on laboratory engineering work. Nexora Technologies is a simulated enterprise environment created for practical skills development.

---

## 1. Resume / CV Deliverables

### Project Entry (Ready to Copy into Resume):

**Enterprise IT Service Desk & End-User Support Operations Lab**
*Technologies: Windows 11 Enterprise, Samba 4 AD DC, Kerberos, LDAP, PowerShell, Python (Stdlib), tcpdump/TShark (Wireshark-compatible), ITIL v4, SQLite*
- **Deployed and configured** an isolated Samba 4 Active Directory Domain Controller (`nexora.test`) on Linux/WSL2; provisioned 12 domain users, 6 department OUs, and implemented AGDLP group access controls and Kerberos authentication.
- **Engineered an interactive IT Service Desk platform** supporting 10 customer request types, ITIL v4 incident lifecycle transitions (`New` $\rightarrow$ `Assigned` $\rightarrow$ `In Progress` $\rightarrow$ `Resolved` $\rightarrow$ `Closed`), dynamic Impact $\times$ Urgency priority matrix, and elapsed-clock-hour SLA timers.
- **Captured and analyzed live network traffic** (`.pcap`) using `tcpdump` and TShark (Wireshark-compatible); validated TCP 3-way handshakes (`SYN`, `SYN-ACK`, `ACK`), DNS SRV lookups, DNS error codes (`NXDOMAIN` / `rcode != 0`), and ICMP routing flows.
- **Authored 15 technical Windows troubleshooting runbooks** covering Fast Startup kernel persistence, printer spooler stall recovery, high CPU process wait chain analysis, and Microsoft 365 client diagnostics (Teams LocalCache, Click-to-Run builds, and network endpoints).
- **Automated Service Desk MIS reporting** using Python standard library; built a 13-test automated unit test suite verifying duration reconciliation, dataset schema integrity, MTTR (15.75h), and sample SLA compliance (85.0%). Built 17 automated functional HTTP tests for the Service Desk web application.

---

## 2. Naukri / Job Portal Profile Entry

**Project Title:** Enterprise IT Service Desk & End-User Support Operations Lab
**Client/Company:** Personal Technical Portfolio (Simulated Enterprise: Nexora Technologies)
**Role:** Project Creator / IT Support Lab Administrator
**Employment Type:** Self-Directed Practical Project
**Team Size:** 1 (Sole Author & Implementer)

**Project Summary:**
Designed, deployed, and tested a complete hands-on enterprise IT Service Desk and End-User Support operations lab simulating an IT department for a 25-employee consulting firm. Deployed an active Samba 4 Active Directory Domain Controller with DNS, Kerberos, and department shared folder permissions. Built a functioning web-based Service Desk portal with real-time ticket queues and SLA management. Executed live packet captures (`.pcap`) analyzing TCP, DNS, and ICMP protocols. Authored comprehensive operational runbooks and Python-based automated reporting tools to demonstrate day-to-day L1 IT support competence.

**Key Skills:**
IT Service Desk, Incident Management, ITIL v4, Active Directory Administration (OUs, AGDLP Group Nesting, Password Policies, Kerberos, LDAP), Samba 4, User Provisioning, Windows 11 Troubleshooting (Fast Startup, Event ID 4740, Spooler, Resource Monitor), PowerShell Scripting, Networking (TCP/IP, DNS, DHCP, APIPA, 802.1Q Subinterfaces), Wireshark / TShark Packet Analysis, Microsoft 365 Client Diagnostics, SLA Management, Mean Time to Resolve (MTTR).

---

## 3. LinkedIn Project & Post Descriptions

### Project Section Entry:
**Title:** Enterprise IT Service Desk & Operations Lab
**Associated with:** Self-Employed / Independent Learning
**Project URL:** `https://github.com/sameerhdevops/enterprise-it-service-desk-lab`
**Description:**
A practical, verifiable IT operations portfolio built to demonstrate day-to-day competencies required for entry-level IT Support Engineer L1 and Service Desk Analyst roles:
- Deployed a fully operational Samba 4 Active Directory Domain Controller on WSL2 Ubuntu with Kerberos ticket verification (`kinit`/`klist`), textbook AGDLP group nesting, and department SMB shared folder permissions.
- Implemented an interactive Service Desk web application with customer request portal, L1 agent console, 10 operational queues, PBKDF2 authentication, and elapsed-clock-hour SLA tracking.
- Captured genuine network traffic (`.pcap`) using tcpdump and Wireshark/TShark, forensically inspecting TCP 3-way handshakes and DNS query resolution.
- Developed PowerShell diagnostic tools and 15 Windows 11 troubleshooting runbooks covering Fast Startup architecture, high CPU wait chains, and M365 client caching.
- Created Python-based Service Desk MIS reporting tools with 100% passing automated unit tests.

---

## 4. GitHub Repository Readme Excerpt / Overview

```markdown
### Key Practical Highlights
- **Real Active Directory Domain Controller:** Provisioned via Samba 4 on WSL2 Ubuntu (`nexora.test`) with Kerberos KDC, LDAP, 12 fictional enterprise user accounts, and AGDLP security groups.
- **Operational Web Service Desk Engine:** Interactive web portal (`itsm/portal/app.py`) featuring 10 customer-facing request types, dynamic Impact x Urgency priority calculations, and agent queue management.
- **Packet Capture & Protocol Inspection:** Live `.pcap` capture file in `evidence/packet-captures/` (3,776 bytes, Wireshark-compatible) with verified TShark display filters for TCP handshakes, DNS SRV resolution, and ICMP diagnostics.
- **Windows 11 Troubleshooting Runbooks:** 15 standardized runbooks detailing command inputs, expected outputs, and root-cause explanations tested on the Windows 11 host.
- **Automated Validation:** 13 unit tests (`reporting/tests/test_validation.py`), 17 platform integration tests (`scripts/test_service_desk_platform.py`), and dataset validator (`scripts/validate-data.py`) running with zero external dependencies.
```

---

## 5. Technical Interview Explanations

### 60-Second Elevator Pitch:
> *"I built the Enterprise IT Service Desk Lab to bridge the gap between IT theory and practical, hands-on L1 support operations. Using Nexora Technologies—a simulated 25-employee consulting firm—as my model, I deployed a real Samba 4 Active Directory Domain Controller on Linux with Kerberos and user group permissions, built an interactive web-based Service Desk portal with ticket queues and SLA clocks, and captured real network traffic using tcpdump and analyzed TCP handshakes and DNS queries with TShark and Wireshark. I also authored 15 detailed Windows troubleshooting runbooks and built automated Python MIS reports with unit tests. It's fully reproducible on my laptop, and I can walk you through any part of the architecture or live commands."*

### 3-Minute Technical Walkthrough:
> *"When designing this lab, I focused on the five core areas an L1 IT Support Engineer touches daily: ticketing, identity, networking, desktop support, and metrics.*
>
> *First, for ticketing, I engineered a web-based Service Desk platform following ITIL v4 principles. It provides a customer portal with 10 service request types, an operator console with 10 filtered queues, PBKDF2 authentication, and automated Priority calculation based on an Impact times Urgency matrix. It tracks continuous elapsed clock hours for SLAs—4 hours for P1, 8 hours for P2, 72 hours for P3, and 120 hours for P4.*
>
> *Second, for directory services, rather than just reading about Active Directory, I deployed an actual Samba 4 Domain Controller for the domain `nexora.test` inside WSL2 Ubuntu. I structured department OUs, provisioned 12 domain user accounts, created security groups following the AGDLP framework, and configured domain password and lockout policies. I verified Kerberos ticket granting using `kinit` and `klist`, and tested SMB shared folder permissions, proving that unauthorized users receive access denied errors while authorized users can access department files.*
>
> *Third, for networking, I captured real network traffic using `tcpdump` into a native `.pcap` file. I verified critical TShark and Wireshark display filters, isolating ICMP echo requests, the TCP 3-way handshake on port 8085, and DNS SRV queries for LDAP discovery. I also simulated and analyzed negative DNS responses like NXDOMAIN to understand how to troubleshoot client name resolution failures.*
>
> *Fourth, on Windows support, I wrote 15 modular runbooks covering issues like Windows Fast Startup. I verified that Fast Startup hibernates the OS kernel session and loaded drivers to `hiberfil.sys`, which is why high uptime accumulates across normal shutdowns and why a cold reboot (`shutdown /r /t 0`) is necessary to clear persistent driver issues.*
>
> *Finally, I automated reporting using Python's standard library, generating daily summaries and SLA compliance reports, backed by a 13-test automated unit test suite and 17 automated Service Desk platform tests. Every command and script is stored in my GitHub repository, fully documented and tested."*
