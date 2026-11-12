# 35 Defensible L1 Technical Interview Questions & Answers
**Document ID:** INT-002  
**Target Roles:** IT Support Engineer L1, Desktop Support Engineer, Service Desk Analyst

---

## Category 1: Windows Operating System & Desktop Support (8 Questions)

### Q1: What is the first thing you check when a user reports their Windows computer is running slow?
**A:** "I check system uptime in Task Manager or via PowerShell (`(Get-CimInstance Win32_OperatingSystem).LastBootUpTime`). In Windows 10 and 11, Fast Startup logs off user sessions and hibernates the Windows kernel session and device-driver state to `hiberfil.sys`. When users click 'Shut Down', the operating system does not perform a cold reboot; uptime accumulates across power cycles. However, high uptime does not automatically prove a memory leak. I inspect Task Manager's CPU, Memory, and Disk meters to check for actual resource pressure. If a full clean reboot is needed, clicking 'Restart' or running `shutdown /r /t 0` performs a complete cold boot cycle, re-initializing the kernel and loaded drivers rather than restoring a hibernated state."

### Q2: Does Fast Startup preserve running user applications like Word or browser tabs across shutdowns?
**A:** "No. Fast Startup terminates user sessions, closing user-mode applications and freeing user-mode RAM. It then hibernates the Windows kernel session and loaded device-driver state into `hiberfil.sys`. Uptime accumulates because the kernel session was restored rather than re-initialized from a cold start. Note that the kernel session should not be equated with Session 0 (which hosts system services and non-interactive user mode components). Any driver state or kernel-mode pool issues persist across a Fast Startup shutdown, but user applications must be reopened upon next logon."

### Q3: What is the difference between physical RAM and virtual memory?
**A:** "Physical RAM is the high-speed hardware memory installed on the motherboard where active programs execute. Virtual memory is an OS technique where Windows combines physical RAM with temporary space on the hard drive (the paging file, `pagefile.sys`). When physical RAM runs low, Windows offloads inactive memory pages to disk to free up physical RAM for active foreground tasks."

### Q4: Walk me through the exact steps to clear a stuck print job in Windows when you cannot cancel it in the GUI.
**A:** "In an elevated command prompt or PowerShell:
1. Confirm whether the print queue is local to the workstation or hosted on a shared corporate print server (`\\NEX-PRN01`). If hosted on a print server, modifying or purging shared print queues requires appropriate administrative authorization and user coordination.
2. Inform the user that pending queued jobs will be purged and must be resent.
3. Stop the Print Spooler service: `net stop spooler` (or `Stop-Service Spooler -Force`). Never attempt to delete spool files while the service is active, as open file locks will cause access violations or spooler corruption.
4. Navigate to `C:\Windows\System32\spool\PRINTERS` and delete all temporary `.SPL` (Spool file containing raw print/EMF rendering data) and `.SHD` (Shadow file containing job header, owner, and printer properties) files inside.
5. Restart the Print Spooler service: `net start spooler` (or `Start-Service Spooler`).
6. Reopen the print queue to confirm it is empty, and send a fresh Windows test page to confirm proper operation."

### Q5: What does Windows Installer Error 1603 mean, and how do you find the root cause?
**A:** "Error 1603 is a generic fatal error code returned by Windows Installer (`msiexec`). To identify the exact failure point, I re-run the installation from an elevated command prompt with verbose logging enabled: `msiexec /i installer.msi /l*v C:\temp\install.log`. In the log, I search for the string 'Return value 3', which marks the exact custom action, missing prerequisite, or locked file that failed right before the installer rolled back."

### Q6: If an application crashes silently without showing an error dialog, how do you investigate?
**A:** "I open the Windows Event Viewer (`eventvwr.msc`) and go to Windows Logs > Application. I look for Event ID 1000 with source 'Application Error'. In the event details, I check the 'Faulting application name' and the 'Faulting module name'. The faulting module tells me whether a corrupted C++ runtime (`VCRUNTIME140.dll`), an OS library (`KERNELBASE.dll`), or a third-party add-in caused the crash."

### Q7: What are the SFC and DISM commands, and in what order should you run them?
**A:** "DISM (`DISM.exe /Online /Cleanup-image /Restorehealth`) repairs the Windows Component Store (`WinSxS`) using Windows Update as the clean source. SFC (`sfc /scannow`) scans and repairs protected operating system files using the component store as its reference cache. You should always run DISM first so that if SFC finds corrupt system files, it has a healthy, verified component store from which to copy clean replacements."

### Q8: What does a yellow exclamation mark in Device Manager indicate?
**A:** "It indicates a hardware device driver problem—such as Code 28 (no driver installed) or Code 10 (device failed to start). To resolve it, I right-click the device, go to Properties > Details, and look at the 'Hardware Ids' property to identify the Vendor (VEN) and Device (DEV) IDs. I can then download the certified OEM driver from the manufacturer's enterprise support portal."

---

## Category 2: Networking & Connectivity (8 Questions)

### Q9: A user cannot browse the internet. Walk me through your step-by-step troubleshooting sequence.
**A:** "I follow a methodical bottom-up OSI troubleshooting approach while keeping in mind the exact scope of each test:
1. **Physical & Data Link:** Verify the physical connection—check Ethernet cable seating and link/activity lights on the NIC and switch, or verify Wi-Fi association and signal strength.
2. **IP Configuration:** Run `ipconfig /all`. Check if the adapter received a valid enterprise IP or an APIPA address (`169.254.x.x`).
3. **Loopback Test:** `ping 127.0.0.1`. Note: This only verifies that the local TCP/IP protocol stack is initialized in software; it does not test the physical network adapter hardware or cabling.
4. **Local Subnet / Default Gateway:** `ping <Default_Gateway_IP>` (e.g., `192.168.10.1`). This tests basic Layer 3 reachability to the local router interface across the local LAN switch or AP.
5. **WAN / Internet Routing:** `ping 8.8.8.8` (or another public IP). This verifies Layer 3 ICMP routing out through the firewall and ISP, confirming WAN path viability. Note: Passing this test only proves ICMP echo traffic is routed; it does not test DNS, proxy servers, or web application protocols (HTTP/HTTPS).
6. **DNS Name Resolution:** `nslookup www.google.com` and `ping www.google.com`. This verifies whether hostnames resolve to IP addresses via the configured DNS servers.
7. **Application / Proxy Layer:** If pinging public IPs and DNS resolution both work, check browser proxy settings, captive portals, TLS certificate errors, or corporate web filtering."

### Q10: What does an IP address starting with 169.254.x.x mean?
**A:** "An address in the `169.254.0.0/16` range is an Automatic Private IP Addressing (APIPA) / IPv4 Link-Local address (RFC 3927). It indicates that the network interface is physically connected (link detected), but the host failed to obtain a DHCP lease after broadcasting DHCP Discover packets. APIPA addresses allow local peer-to-peer communication on the same physical segment but cannot route through gateways to other subnets or the internet.

Crucially, an APIPA address does not automatically mean the DHCP server is down. As an L1 engineer, I investigate the full chain of possible causes:
- **Local Client Issues:** Faulty physical patch cable, damaged NIC hardware, corrupted network adapter drivers, or the local 'DHCP Client' Windows service being stopped/disabled.
- **Local Network / Port Issues:** The switch port is configured with an incorrect or unrouted VLAN, 802.1X port security authentication failure, or port-level MAC address filtering.
- **Infrastructure / Scope Issues:** The DHCP scope on the server is exhausted (100% address pool utilization), the DHCP server service is stopped, or the DHCP Relay Agent (IP helper) on the router is misconfigured or failing to forward broadcasts between subnets.
- **Firewall Filtering:** Client host firewall or endpoint security software blocking UDP broadcast ports 67/68."

### Q11: Explain the DORA process in DHCP.
**A:** "DORA is the 4-step negotiation process by which a client acquires an IPv4 configuration. DHCPv4 uses two specific UDP port numbers: **Server listens on UDP port 67**, and **Client listens on UDP port 68**.
- **Discover (Client -> Broadcast):** The client sends a `DHCPDISCOVER` packet from source `0.0.0.0:68` to destination `255.255.255.255:67` requesting an IP configuration from any listening DHCP server.
- **Offer (Server -> Client):** A listening DHCP server reserves an available IP from its pool and sends a `DHCPOFFER` from source `<Server_IP>:67` to destination `255.255.255.255:68` (or unicast) containing the proposed IP address, subnet mask, default gateway, DNS servers, and lease duration.
- **Request (Client -> Broadcast):** The client selects the offer and broadcasts a `DHCPREQUEST` from `0.0.0.0:68` to `255.255.255.255:67`. Broadcasting this confirms acceptance to the chosen server while formally informing other DHCP servers that their offers were declined so they can return those IPs to their pools.
- **Acknowledge (Server -> Client):** The chosen server sends a `DHCPACK` from `<Server_IP>:67` to destination port `68`, committing the binding to its lease database and officially granting the client permission to use the IP parameters."

### Q12: How do you determine whether a network problem is caused by DNS?
**A:** "By running the 'IP vs. Name' test. I ping a public IP address like `8.8.8.8`. If the ping succeeds, Layer 1 through Layer 3 routing is 100% operational. Then I ping `www.google.com`. If that fails with 'could not find host', the failure is definitively DNS. I then run `nslookup` or PowerShell's `Resolve-DnsName` to see which DNS server is failing to respond. Crucially, I test using Layer 7 DNS query tools rather than `Test-NetConnection -Port 53`, because Test-NetConnection only verifies Layer 4 TCP port reachability, whereas standard client DNS lookups occur over UDP port 53 and require an active, responsive DNS resolver service."

### Q13: What does the command `tracert` do, and how do you interpret its output?
**A:** "`tracert` (Trace Route) maps the network path packets travel from the local host to a destination IP by transmitting ICMP Echo Request packets (on Windows) with incrementally increasing Time to Live (TTL) fields in the IP header. Each intermediate router decrements the TTL; when TTL reaches 0, the router drops the packet and responds with an ICMP Time Exceeded (Type 11, Code 0) message, revealing its IP address and round-trip latency.

When interpreting `tracert` output, a crucial technical reality is that intermediate timeouts (`* * * Request timed out`) do **not** automatically indicate a network failure or broken route. Many enterprise and ISP core routers intentionally drop or rate-limit ICMP TTL Exceeded message generation to protect their CPU/control planes, while continuing to forward transit data packets at wire speed. A genuine route failure is only confirmed when timeouts persist consistently from an intermediate hop all the way through to the final destination, or when an intermediate router explicitly returns an ICMP Destination Unreachable message."

### Q14: What is the difference between TCP and UDP?
**A:** "TCP (Transmission Control Protocol) is connection-oriented and reliable—it uses a 3-way handshake (`SYN`, `SYN-ACK`, `ACK`), guarantees packet sequencing, and retransmits lost packets (used for HTTP/HTTPS, Outlook, file transfers). UDP (User Datagram Protocol) is connectionless and lightweight—it sends packets without handshakes or delivery guarantees, prioritizing speed over reliability (used for DNS queries, VoIP audio, video streaming)."

### Q15: What is the purpose of a Default Gateway?
**A:** "The Default Gateway is the router interface on the local subnet that routes traffic destined for any IP address outside the local network. When a computer checks the destination IP and sees the network ID is different from its own, it sends the packet directly to the default gateway's MAC address."

### Q16: What is the difference between Split Tunneling and Full Tunneling in a VPN?
**A:** "In Split Tunneling, only traffic destined for internal corporate subnets (like file shares and ERP) travels through the encrypted VPN tunnel, while general public internet traffic (like streaming or YouTube) exits directly through the user's home broadband. In Full Tunneling, 100% of the user's internet traffic is routed through the corporate firewall."

---

## Category 3: Active Directory & Access Management (5 Questions)

### Q17: What is the difference between an Active Directory account and a local Windows account?
**A:** "A local account is stored in the local computer's SAM database (`C:\Windows\System32\config\SAM`) and can only authenticate on that single physical machine. An Active Directory account is stored centrally in the `ntds.dit` database on a Domain Controller, allowing the user to sign into any authorized domain-joined computer across the enterprise with single sign-on."

### Q18: What is the difference between a Security Group and a Distribution Group in Active Directory?
**A:** "A Security Group can be assigned permissions to resources (like NTFS shared folders, printers, and SharePoint) and appears in Access Control Lists (ACLs). A Distribution Group is used exclusively for sending emails to multiple users via Microsoft Exchange and cannot be used to assign file or folder access rights."

### Q19: Explain the AGDLP principle for assigning permissions in Active Directory.
**A:** "AGDLP stands for: **A**ccounts go into **G**lobal groups (job roles), which go into **D**omain **L**ocal groups (resource permissions), which receive **P**ermissions. It means we never assign individual users directly to folder permissions. If a new accountant joins, we simply add their user account to the Global Finance group, and they automatically inherit all required folder access."

### Q20: A user is added to a new security group to access a shared drive, but still gets 'Access Denied'. Why?
**A:** "Because group memberships are written into the user's Kerberos Ticket Granting Ticket (TGT) only at logon time. If the user is currently logged in, their existing security token does not contain the new group SID. They must sign out and sign back in (or run `klist purge`) so Windows requests a fresh Kerberos token containing the updated group SID."

### Q21: What is the very first thing you must do before resetting a user's password over the phone?
**A:** "Verify the caller's identity to prevent social engineering attacks. I confirm their Employee ID number, manager name, and department against the HR directory, or call them back on their registered corporate mobile phone number on file before resetting credentials."

### Q21b: An employee's account keeps locking out every 15 minutes after being unlocked. How do you find the source device using Event Viewer?
**A:** "I investigate using Windows Security Event logs across the Domain Controllers and the authenticating endpoints by correlating two primary Event IDs:
1. **On Active Directory Domain Controllers:** I filter the Security Log for **Event ID 4740** ('A user account was locked out'). While lockout events are frequently consolidated or forwarded to the PDC Emulator FSMO role holder, Event 4740 can be recorded on *any* Domain Controller that evaluated the authentication attempt that exceeded the lockout threshold. In the event XML details, I inspect the **'Caller Computer Name'** field to identify the NetBIOS name or IP of the originating host or upstream authentication proxy (such as a RADIUS/NPS server or VPN gateway).
2. **On the Originating Host / Endpoint:** I inspect the Security Log for **Event ID 4625** ('An account failed to log on') matching the exact lockout timestamp. I analyze three critical fields:
   - **Logon Type:** **Logon Type 3** indicates a **Network Logon** (connecting across the network via SMB file shares, IIS/OWA, RPC, or network services—it is a general network authentication, not exclusively mobile or ActiveSync). Other common types include Logon Type 2 (Interactive console logon), Logon Type 10 (RemoteInteractive/RDP), and Logon Type 4 (Batch/Scheduled Task).
   - **Failure Reason & Sub Status:** E.g., `0xC000006A` (bad password entered) versus `0xC0000234` (account was already locked out).
   - **Caller Process Name:** Identifies the initiating process (e.g., `lsass.exe`, `svchost.exe`, or a custom background application).
   
This forensic correlation reveals the root cause: whether a stale saved credential in Windows Credential Manager, an unmapped persistent network drive, a Windows Service running under a user account with an expired password, or a mobile device attempting Wi-Fi/ActiveSync connection."

---

## Category 4: Microsoft 365 & Application Support (4 Questions)

### Q22: What is the difference between Cached Exchange Mode and Online Mode in Outlook?
**A:** "Cached Exchange Mode downloads a local copy of the user's mailbox into an offline `.ost` file on the computer (`C:\Users\<user>\AppData\Local\Microsoft\Outlook`), allowing fast searching and offline access. Online Mode connects directly to the Exchange server without local caching, which is slower over poor connections but essential on shared virtual desktop environments where disk space is limited."

### Q23: How do you troubleshoot Microsoft Outlook freezing on launch?
**A:** "First, I launch Outlook in Safe Mode by running `outlook.exe /safe`. If it opens cleanly, a third-party COM Add-in is the culprit, so I disable non-essential add-ins in File > Options > Add-ins. If safe mode fails, I direct the user to Outlook on the Web (`outlook.office.com`) to confirm mailbox health, and then recreate the Outlook profile via Control Panel > Mail."

### Q24: What is the most effective first troubleshooting step when Microsoft Teams is freezing or showing status glitches?
**A:** "Clearing the Microsoft Teams local cache. For New Teams (MSIX), I terminate `ms-teams.exe` and purge `LocalCache` under `%LOCALAPPDATA%\Packages\MSTeams_8wekyb3d8bbwe\LocalCache` (or run `Reset-AppxPackage`). This forces Teams to fetch fresh tokens and session states from the cloud without deleting chat history."

### Q25: What do the blue cloud and green checkmark icons mean next to files in OneDrive?
**A:** "A blue cloud icon means the file is 'Online-only'—it exists in cloud storage and consumes 0 bytes of local disk space until opened. A green checkmark means the file has been downloaded and is available locally on the hard drive for offline editing."

---

## Category 5: ITIL & Service Desk Operations (5 Questions)

### Q26: What is the difference between an Incident and a Service Request?
**A:** "An Incident is an unplanned interruption or reduction in quality of an IT service ('Something is broken', like a crashed laptop or offline printer). A Service Request is a formal request from a user for something new to be provided ('I need something', like a new employee account, a software license, or a dual monitor)."

### Q27: How is ticket Priority determined in ITIL?
**A:** "In ITIL, Priority is calculated using a two-dimensional matrix evaluating **Impact** and **Urgency** (`Priority = Impact x Urgency`):
- **Impact:** Evaluates the degree of business disruption—how many users, branch offices, or mission-critical services are affected.
- **Urgency:** Evaluates how rapidly the business requires a resolution based on deadlines, revenue impact, or operational dependencies.

Crucially, while ITIL defines the general Impact/Urgency framework, the specific matrix lookup rules (e.g., High Impact + High Urgency = P1 Critical, Low Impact + Low Urgency = P4 Low) and automated calculation triggers are **company-specific configurations implemented in the ITSM platform (such as ServiceNow or Jira Service Management)**, rather than universal platform defaults. Furthermore, ticket priority is strictly determined by business impact criteria, not simply because an individual user requests high urgency."

### Q28: What is the difference between Work Notes and Customer Comments in a ticketing system?
**A:** "Customer Comments (or Additional Comments) are visible to the end user via email notifications and the self-service portal, used for communicating updates and gathering info. Work Notes are strictly internal to IT support staff, used for logging technical diagnostics, IP addresses, error codes, and handover notes that users do not need to see."

### Q29: What is the difference between an Incident and a Problem in ITIL?
**A:** "An Incident is an individual disruption to service, and the goal is rapid restoration of normal operations (even via a temporary workaround). A Problem is the underlying unknown root cause of one or multiple recurring incidents, and the goal is permanent root-cause elimination so the incidents do not recur."

### Q30: What is an SLA, and what is the difference between Response SLA and Resolution SLA?
**A:** "An SLA (Service Level Agreement) is a documented commitment between IT and the business defining target service times. A Response SLA measures the time from ticket creation until an IT analyst acknowledges the ticket and begins work. A Resolution SLA measures the total time from ticket creation until the issue is fully fixed and verified."

---

## Category 6: Customer Service & Communication (5 Questions)

### Q31: How do you handle an angry or frustrated user whose computer is not working?
**A:** "I remain calm, empathetic, and professional, and I never take their frustration personally. I acknowledge their situation immediately—for example: 'I understand you are facing month-end deadlines, Deepak, and having your computer freeze is very stressful. I am taking personal ownership of this right now.' I then ask targeted diagnostic questions and walk them through actionable steps rather than making empty promises."

### Q32: What do you do if you cannot solve a user's problem within the expected time limit?
**A:** "If I have investigated for 30 minutes without progress, I initiate functional escalation. I explain the situation honestly to the user: 'I have ruled out local software issues, but this requires network firewall adjustments from our senior network team.' I document all my diagnostic findings in internal Work Notes and ensure the user knows who will contact them and by when."

### Q33: Why is ticket documentation important after resolving an issue?
**A:** "Because ticket documentation creates an audit trail, informs reporting metrics like MTTR and SLA compliance, and builds the internal knowledge base. If another analyst encounters the same error code next week, they can read my resolution notes to fix it in 5 minutes instead of starting from scratch."

### Q34: How do you explain a technical issue to a non-technical employee?
**A:** "I avoid technical acronyms and use simple, relatable analogies. For example, instead of explaining 'Your local DNS resolver cache failed to query recursive root nameservers', I say: 'Your computer temporarily lost its address book that translates website names into numbers. We refreshed that address book, and now it knows how to reach the site again.'"

### Q35: Why do you want to work as an entry-level IT Support Engineer?
**A:** "I enjoy practical troubleshooting and helping people solve problems that block their daily work. While I have cloud and programming fundamentals from my degree and internship, I find the operational rhythm of the service desk—diagnosing systems, working with Active Directory and networking, and restoring services—deeply rewarding. I want to build a strong foundational career in IT infrastructure."
