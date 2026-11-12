# Defensible Interview Walkthrough: Project Explanation
**Document ID:** INT-001  
**Candidate Background:** Fresher / B.Sc Computer Science & Chemistry / AWS Cloud Internship  
**Target Roles:** IT Support Engineer L1, Desktop Support Engineer, Service Desk Analyst, Technical Support Engineer

---

## Part 1: The 60-Second Elevator Pitch
*(Practice delivering this naturally, calmly, and without sounding rehearsed).*

> "To prepare practically for an entry-level IT Support and Service Desk role, I designed and built an end-to-end **Enterprise IT Service Desk & Support Operations Lab**. 
>
> I simulated the IT operations of a 25-employee company called **Nexora Technologies**, handling real-world L1 support responsibilities. The lab covers the full ITIL incident lifecycle in **ServiceNow** and **Jira Service Management**, 15 detailed Windows 11 troubleshooting runbooks, local Active Directory and group management, Microsoft 365 client diagnosis, enterprise networking with Cisco Packet Tracer, and an automated Python reporting tool that calculates daily SLA compliance and MTTR.
>
> It gave me hands-on practice diagnosing real issues—from Print Spooler crashes and DNS failures to Kerberos token refreshes—and taught me how to communicate with users professionally while documenting tickets accurately."

---

## Part 2: The 3-to-5 Minute Comprehensive Walkthrough
*(Use this when the interviewer says: "Walk me through this project in detail. What did you build and why?")*

### 1. Motivation & Context
"Coming from a B.Sc in Computer Science and Chemistry, followed by a cloud internship, I wanted to ensure my practical fundamentals in enterprise desktop support and infrastructure were rock-solid. Many freshers only read theory about Active Directory or DHCP; I wanted a hands-on lab where I could practice the exact troubleshooting sequences and ticketing workflows used on day one in a corporate IT department."

### 2. Organizational Setup & Support Model
"I modeled the lab around a simulated company called **Nexora Technologies**, employing 25 staff across HR, Finance, Operations, and IT. I established a multi-tiered support model:
- Users reach out via self-service portal, email, or phone.
- As the L1 Service Desk Analyst, I handle first-contact intake, ticket triage, priority scoring using an Impact-by-Urgency matrix, and first-line resolution.
- For issues exceeding 30 minutes or requiring infrastructure changes (like switch port reconfigurations or server hardware RMAs), I designed formal functional escalation procedures to L2 Desktop and L2 Network teams."

### 3. Core Technical Modules
"The project is structured into six practical operational areas:
- **ITSM & Ticketing:** I configured workflows in both ServiceNow and Jira Service Management. I created 20 realistic incidents, 8 service requests, 3 problem records, and 3 change records. A key skill I practiced was strictly separating customer-visible comments from internal technical work notes so sensitive logs or IP addresses are never exposed to end users.
- **Windows Desktop Support:** I authored 15 comprehensive runbooks covering slow systems, memory leaks, Print Spooler corruptions, low disk space, and application crashes. I practiced using native Windows tools: Resource Monitor's 'Analyze Wait Chain', Event Viewer error codes (like Event ID 1000 for app crashes and Event ID 7000 for service failures), and PowerShell commands.
- **Active Directory & Identity:** I documented user account lifecycles, AGDLP role-based group permissions, password resets with caller identity verification, and onboarding/offboarding checklists. I also built a hands-on local administrative lab to demonstrate NTFS permissions and Kerberos token refreshes using `klist`.
- **Microsoft 365:** Focused on client-side troubleshooting for Outlook, Teams, and OneDrive—including Cached Exchange Mode vs. Online Mode, regenerating `.ost` files, and clearing Teams cache.
- **Enterprise Networking:** Designed a 2-VLAN network topology in Cisco Packet Tracer with inter-VLAN routing and DHCP relay, and documented step-by-step diagnostic workflows using `ipconfig`, `ping`, `tracert`, and `nslookup`.
- **Service Desk Reporting:** Finally, I wrote a zero-dependency Python tool that analyzes our incident records to calculate real operational metrics: total ticket volume, open backlog, category breakdowns, and SLA compliance percentages."

### 4. Key Lessons Learned
"The biggest lesson I learned is that troubleshooting in an enterprise is systematic, not guesswork. You don't just randomly reboot a computer. You start at Layer 1 and work upwards, test reachability methodically, ask the user clarifying questions, and document the root cause so the next engineer can follow your work. It also taught me that customer communication is just as important as technical knowledge—staying calm and empathetic when an employee is stressed during month-end closing makes all the difference."
