# IT Service Desk Shift Handover Report (Completed Example)
**Date:** 2024-11-12  
**Outgoing Shift:** Morning Shift (08:30 – 17:30 IST) | **Analyst:** Alex Chen (L1 Service Desk Analyst)  
**Incoming Shift:** Evening Shift (13:30 – 22:30 IST) | **Analyst:** Priya Sharma (L1 Service Desk Analyst)  
**Handover Time:** 17:15 IST  

---

### 1. Shift Metrics Summary
- Total Tickets Logged During Shift: 6
- Total Tickets Resolved First-Contact (FCR): 4
- Open Tickets in L1 Queue: 2
- Escalated Tickets (to L2/L3): 1
- Active SLA Breaches: 0

---

### 2. Critical & High Priority Incidents (P1 / P2)
| Ticket ID | Priority | Affected User / Dept | Description | Current Status & Immediate Action Required |
|---|---|---|---|---|
| **INC0015** | **P1** | Whole Office / Operations | Internet link degradation causing packet loss across Bengaluru office. | **Resolved at 12:15 IST.** Emergency change CHG0003 executed to replace failing core switch SFP+ transceiver. ISP link stabilized. Continue passive PRTG monitoring during evening shift. |
| **INC0004** | **P2** | Divya Ramesh / Engineering | VPN disconnects every 10 mins when working from home. | **Escalated to L2 Network (Arvind Rao).** Workaround applied (switched GlobalProtect client to TCP mode). Permanent fix scheduled under change CHG0002 for Saturday. User is operational. |

---

### 3. Escalations & Vendor Pending
- **INC0001 (HP Laptop Motherboard RMA):** HP onsite technician scheduled for tomorrow (Nov 13) between 10:00–13:00 IST. Service case #HP-99214. Temporary spare laptop (NXT-AST-015) successfully issued to user Kavitha Murthy.
- **INC0012 (Awaiting User):** SAP GUI connection timeout for Rajesh Bhat. Sent instructions to test on wired LAN. Awaiting user response.

---

### 4. Infrastructure & Facility Status
- Primary Tata Teleservices fiber WAN: Healthy (980 Mbps / 980 Mbps, latency 4ms).
- Domain Controllers (`NEX-DC01`, `NEX-DC02`): Replication healthy, zero DCDiag errors.
- Floor 2 HP MFD Printer (`192.168.10.25`): Restocked paper tray 2; toner at 64%.

---

### 5. Upcoming Scheduled Changes & Maintenance
- **CHG0001:** Monthly Windows Server OS patching scheduled for tonight at 23:00 IST. Handled by L3 Infrastructure (Suresh Hegde). Service Desk on standby for post-patching verification tomorrow morning at 08:30.
- **Onboarding:** 1 new hire starting tomorrow in HR (Naveen Kumar). Laptop `NXT-AST-012` imaged, AD account `nkumar` created, staged in IT secure locker.

---

### 6. General Operational Notes / Watchlist
- Teams Rooms A/V in Conference Room 'Cauvery' was restarted at 14:00 after audio stuttered during an executive call. Working fine now, but keep an eye if user reports recur.
