# 35 Defensible L1 Technical Interview Questions & Answers
**Document ID:** INT-002  
**Target Roles:** IT Support Engineer L1, Desktop Support Engineer, Service Desk Analyst

---

## Category 1: Windows Operating System & Desktop Support (8 Questions)

### Q1: What is the first thing you check when a user reports their Windows computer is running slow?
**A:** "I check system uptime in Task Manager or via PowerShell (`(Get-CimInstance Win32_OperatingSystem).LastBootUpTime`). In Windows 10 and 11, Fast Startup (hybrid boot) logs off user sessions but hibernates the Windows Kernel (Session 0) and device drivers to `hiberfil.sys`. When users click 'Shut Down', the kernel is not cold-booted; uptime continues to accumulate, and any corrupted driver states or kernel-mode memory leaks (in Non-Paged or Paged Pool) persist. In addition, users often leave laptops in sleep mode for weeks without closing applications, causing user-mode memory leaks. Clicking 'Restart' or running `shutdown /r /t 0` completely tears down both Session 0 and user sessions, re-initializing the kernel and clearing memory. If uptime is low, I then inspect Task Manager to see whether CPU, RAM, or Disk is pegged at 100%."

### Q2: Does Fast Startup preserve running user applications like Word or browser tabs across shutdowns?
**A:** "No. Fast Startup terminates the user session (Session 1), cleanly closing all user-mode applications and freeing user-mode RAM. It then writes only Session 0—the Windows kernel, executive subsystem, and loaded device drivers—to `hiberfil.sys`. The reason uptime accumulates is because the kernel state was restored rather than cold-booted. Any issues persisting across a Fast Startup shutdown are located in kernel drivers or system services, not in user applications."

### Q3: What is the difference between physical RAM and virtual memory?
**A:** "Physical RAM is the high-speed hardware memory installed on the motherboard where active programs execute. Virtual memory is an OS technique where Windows combines physical RAM with temporary space on the hard drive (the paging file, `pagefile.sys`). When physical RAM runs low, Windows offloads inactive memory pages to disk to free up physical RAM for active foreground tasks."

### Q4: Walk me through the exact steps to clear a stuck print job in Windows when you cannot cancel it in the GUI.
**A:** "In an elevated command prompt or PowerShell:
1. Inform the user that pending queued jobs will be purged and must be resent.
2. Stop the Print Spooler service: `net stop spooler` (or `Stop-Service Spooler -Force`). Never attempt to delete spool files while the service is active, as open file locks will cause access violations or spooler corruption.
3. Navigate to `C:\Windows\System32\spool\PRINTERS` and delete all temporary `.SPL` (Spool file containing raw print/EMF rendering data) and `.SHD` (Shadow file containing job header, owner, and printer properties) files inside.
4. Restart the Print Spooler service: `net start spooler` (or `Start-Service Spooler`).
5. Reopen the print queue to confirm it is empty, and send a fresh Windows test page to confirm proper operation."

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
**A:** "I follow a methodical bottom-up OSI approach:
1. Physical / Link: Check if Ethernet cable is plugged in with link lights or Wi-Fi is connected.
2. IP configuration: Run `ipconfig /all`. Check if IP is valid or APIPA (`169.254.x.x`).
3. Loopback test: `ping 127.0.0.1` to confirm local TCP/IP stack is working.
4. Default Gateway: `ping 192.168.10.1` to confirm local LAN reachability.
5. WAN / Internet: `ping 8.8.8.8` to test routing out to the internet.
6. DNS: `nslookup www.google.com` and `ping www.google.com` to test name resolution.
7. Proxy / Browser: Check LAN proxy settings if ping works but browsers fail."

### Q10: What does an IP address starting with 169.254.x.x mean?
**A:** "It is an Automatic Private IP Addressing (APIPA) address. It means the computer's network interface is enabled and detected a physical link, but it sent out a DHCP Discover broadcast and received no response from a DHCP server. It indicates a DHCP server failure, an exhausted DHCP scope, or the switch port is on the wrong VLAN."

### Q11: Explain the DORA process in DHCP.
**A:** "DORA is the 4-step handshake used by DHCP:
- Discover: Client broadcasts on UDP 67 asking if any DHCP server is available.
- Offer: DHCP server offers an available IP address to the client.
- Request: Client broadcasts that it accepts that offered IP.
- Acknowledge (ACK): DHCP server confirms the lease, providing default gateway, subnet mask, DNS servers, and lease duration."

### Q12: How do you determine whether a network problem is caused by DNS?
**A:** "By running the 'IP vs. Name' test. I ping a public IP address like `8.8.8.8`. If the ping succeeds, Layer 1 through Layer 3 routing is 100% operational. Then I ping `www.google.com`. If that fails with 'could not find host', the failure is definitively DNS. I then run `nslookup` or PowerShell's `Resolve-DnsName` to see which DNS server is failing to respond. Crucially, I test using Layer 7 DNS query tools rather than `Test-NetConnection -Port 53`, because Test-NetConnection only verifies Layer 4 TCP port reachability, whereas standard client DNS lookups occur over UDP port 53 and require an active, responsive DNS resolver service."

### Q13: What does the command `tracert` do, and how do you interpret its output?
**A:** "`tracert` traces the route packets take to a destination IP by sending ICMP packets with incrementing TTL (Time to Live) values. Each hop represents a router along the path. If packets start timing out (`* * * Request timed out`) after hop 1, it tells me the break point is at our local gateway router or ISP uplink, isolating whether the problem is internal or external."

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
**A:** "I investigate using two specific Windows Event IDs across the domain and client:
1. **On the Domain Controller (specifically the PDC Emulator):** I open Event Viewer > Security Log and filter for **Event ID 4740** ('A user account was locked out'). (Note: While 4740 is typically consolidated on the PDC Emulator, any DC that processes the bad authentication attempt can log it). In the event details, I check the **'Caller Computer Name'** field, which identifies the exact workstation, laptop, or mobile hostname where the failed authentications originated.
2. **On the Caller Workstation/Device:** I open the local Security Log on that source device and filter for **Event ID 4625** ('An account failed to log on'). I examine the **Logon Type** (e.g., Logon Type 2 for Interactive, Logon Type 3 for Network/Exchange ActiveSync/SMB share), the **Sub Status Code** (e.g., `0xC000006A` for bad password, `0xC0000234` for account locked), and the **Process Name** (e.g., `svchost.exe`, `lsass.exe`, or a mail app). This reveals whether a smartphone syncing corporate Wi-Fi with an expired password, a stale mapped drive credential in Windows Credential Manager, or a legacy background service is firing the bad attempts."

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
**A:** "Priority is calculated using a matrix of **Impact** and **Urgency** (`Priority = Impact x Urgency`). Impact measures how many users or critical business services are affected. Urgency measures how fast the business requires a resolution. A ticket is not prioritized simply because a user demands high priority."

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
