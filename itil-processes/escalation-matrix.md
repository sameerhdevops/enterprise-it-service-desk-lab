# Escalation Matrix

> **Nexora Technologies — IT Service Desk**
> Functional and hierarchical escalation paths for incident management.

> ⚠️ **FICTIONAL** — All names, titles, and contact details are fictional. This document is part of a learning lab.

## Escalation Types

### Functional Escalation

Moving a ticket to a team with deeper technical expertise. This is normal — it means the issue requires skills or access beyond the current level.

### Hierarchical Escalation

Notifying management when an incident is at risk of breaching SLA, when impact is larger than initially assessed, or when business pressure requires executive visibility.

## Support Tiers

| Tier | Team | Scope | Typical Resolution |
|------|------|-------|-------------------|
| **L1 — Service Desk** | L1-Desktop, L1-Network, L1-Access | First contact, known fixes, standard procedures, password resets, basic troubleshooting | 70% of all incidents |
| **L2 — Technical Support** | Systems, Network Engineering, Application Support | Advanced diagnostics, configuration changes, non-standard issues, server-side fixes | 25% of all incidents |
| **L3 — Engineering / Vendor** | Internal developers, infrastructure architects, vendor support | Code fixes, firmware patches, architectural changes, vendor RMA | 5% of all incidents |

## L1 Assignment Groups

| Group | Handles | Team Members (Fictional) |
|-------|---------|--------------------------|
| **L1-Desktop** | Hardware, software, OS, printing, peripherals | Kavya Krishnan, Rohit Menon |
| **L1-Network** | Connectivity, Wi-Fi, VPN, DNS, network performance | Meera Pillai |
| **L1-Access** | AD accounts, password resets, permissions, mailboxes, group memberships | Kavya Krishnan, Rohit Menon |

## Functional Escalation Path

### When to Escalate from L1

Escalate when **any** of these conditions are met:

| Condition | Example |
|-----------|---------|
| You've exhausted knowledge base articles and standard procedures | Tried all documented fixes for Outlook crash, none worked |
| The fix requires access you don't have | Need to restart a service on the server, need domain admin |
| The issue involves server-side configuration | Exchange mailbox corruption, GPO issue |
| Hardware needs vendor-level repair | Laptop motherboard failure, under warranty |
| You've spent >30 min on a P1 or >60 min on a P2 without progress | Time-boxed diagnosis exceeded |
| Multiple users are affected by the same issue | Potential major incident — escalate and flag |
| The issue requires code changes or deep application knowledge | Custom app throwing errors in production |

### Escalation Path by Category

| Category | L1 → L2 | L2 → L3 |
|----------|---------|---------|
| **Hardware — Laptop/Desktop** | L1-Desktop → Systems Team | Systems → Vendor (HP/Dell/Lenovo warranty) |
| **Hardware — Network Equipment** | L1-Network → Network Engineering | Network Eng → Vendor (Cisco/Aruba) |
| **Hardware — Printer** | L1-Desktop → Systems Team | Systems → Vendor (HP/Canon service) |
| **Software — OS** | L1-Desktop → Systems Team | Systems → Microsoft Support |
| **Software — Office/Outlook** | L1-Desktop → Application Support | App Support → Microsoft Support |
| **Software — Business App** | L1-Desktop → Application Support | App Support → App Development / Vendor |
| **Network — Connectivity** | L1-Network → Network Engineering | Network Eng → ISP / Vendor |
| **Network — VPN** | L1-Network → Network Engineering | Network Eng → Security Team |
| **Access — AD/Permissions** | L1-Access → Systems Team | Systems → Security Team |
| **Email — Exchange/M365** | L1-Access → Systems Team | Systems → Microsoft Support |
| **Security — Suspected breach** | L1 → Security Team (immediately) | Security → CISO / External IR |

## L2 Teams and Contacts

| Team | Lead (Fictional) | Contact | Handles |
|------|------------------|---------|---------|
| **Systems Team** | Deepak Nair | deepak.nair@nexora.tech / ext. 2201 | Server, AD, GPO, SCCM/Intune, backup/recovery |
| **Network Engineering** | Arjun Mehta | arjun.mehta@nexora.tech / ext. 2202 | Switches, routers, firewalls, VPN concentrator, Wi-Fi |
| **Application Support** | Sneha Desai | sneha.desai@nexora.tech / ext. 2203 | Business applications, database connectivity, integrations |
| **Security Team** | Vikram Joshi | vikram.joshi@nexora.tech / ext. 2204 | Security incidents, access review, vulnerability management |

## Hierarchical Escalation Path

### Management Escalation Triggers

| Trigger | Action |
|---------|--------|
| P1 incident declared | Notify IT Manager immediately |
| P1 not resolved within 2 hours (50% of SLA) | Notify IT Manager + CTO |
| P2 not resolved within 6 hours (75% of SLA) | Notify Service Desk Lead |
| Any SLA breach | Notify IT Manager within 30 minutes of breach |
| User requests management escalation | Notify Service Desk Lead |
| Impact assessment increased (e.g., P3 → P1) | Re-notify per new priority |
| Multiple P1s simultaneously | Notify CTO |
| Security incident confirmed | Notify IT Manager + CISO immediately |

### Management Contacts

| Level | Name (Fictional) | Title | Contact | Escalate For |
|-------|------------------|-------|---------|-------------|
| 1 | Ananya Rao | Service Desk Lead | ananya.rao@nexora.tech / ext. 2100 | SLA warnings, workload issues, user complaints, P2+ awareness |
| 2 | Ramesh Iyer | IT Manager | ramesh.iyer@nexora.tech / ext. 2001 | SLA breaches, P1 incidents, resource conflicts, cross-team coordination |
| 3 | Suresh Venkat | CTO | suresh.venkat@nexora.tech / ext. 1001 | Extended P1 outages, security incidents, business-impacting decisions |
| 4 | Nadia Fernandez | CEO | nadia.fernandez@nexora.tech / ext. 1000 | Only for company-wide impact or regulatory/legal implications |

## Escalation Procedure

### How to Escalate (Step by Step)

1. **Update the ticket** before escalating:
   - Document everything you've tried and the results
   - Attach diagnostic data (screenshots, logs, command output)
   - Update the category/subcategory if your investigation changed the picture
   - Note the current impact and any workaround in place

2. **Reassign the ticket** in the ITSM tool to the appropriate L2 team

3. **Notify the receiving team:**
   - For P1/P2: Phone call or Teams message to the team lead — don't just reassign and wait
   - For P3/P4: Reassignment notification via ITSM is sufficient

4. **Notify the user** that their ticket has been escalated:
   - "I've escalated your ticket [INC number] to our [Systems/Network/Application] team for further investigation. They have all the details and diagnostic information I've collected."

5. **Don't disappear** — You're still the user's point of contact. If they call back, you check the ticket status and relay updates.

### Information to Include When Escalating

| Required | Detail |
|----------|--------|
| ✅ Incident ID | INC0015 |
| ✅ User and department | Priya Sharma, Finance |
| ✅ Description and symptoms | Outlook crashes on attachment open since Nov 12 |
| ✅ Impact | 3 users in Finance affected |
| ✅ What you've tried | Cleared cache, repaired Office, disabled add-ins — issue persists |
| ✅ Diagnostic data | Outlook crash log attached, Event Viewer screenshot attached |
| ✅ Workaround status | User can view attachments in OWA (webmail) as interim |
| ✅ Urgency notes | Month-end close starting next week, Finance needs full Outlook functionality |

### What NOT to Do

- Don't escalate a blank ticket — "Please look at this" with no notes wastes everyone's time
- Don't call it P1 to get faster service if it's really P3
- Don't escalate because you're busy — that's a workload issue for your lead, not an L2 problem
- Don't skip L2 to go directly to L3 or vendor unless L2 explicitly tells you to

## Major Incident Escalation

For major incidents (P1 affecting multiple users or critical service):

```
0 min   L1 detects → Logs as P1 → Notifies Service Desk Lead
5 min   Service Desk Lead declares Major Incident → Notifies IT Manager
10 min  IT Manager activates bridge call → Pulls in L2/L3 as needed
15 min  Communicator posts first status update to affected users
30 min  Status update every 30 minutes until resolved
2 hr    If unresolved: CTO notified
4 hr    SLA breach: post-incident review mandatory
```

## Vendor Escalation

For issues requiring vendor support:

| Vendor (Fictional) | Support Portal | SLA | Contract |
|---------------------|---------------|-----|----------|
| HP (hardware) | support.hp.com | NBD on-site for warranty devices | Contract #NXT-HP-2024 |
| Microsoft (M365/Azure) | admin.microsoft.com | 1hr response for Sev A | E3 license support |
| Cisco (network) | mycase.cloudapps.cisco.com | 4hr for P1, NBD for P2 | SmartNet #NXT-CISCO-2024 |
| ISP — Bharti Airtel | Enterprise portal | 4hr for link down | Lease line SLA |

When escalating to a vendor, always get a case number and document it in the ticket.

## Quick Reference Card

For L1 analysts to keep handy:

```
P1 (Critical) → Respond 15min → Resolve 4hr → Call L2 lead NOW + IT Manager
P2 (High)     → Respond 1hr  → Resolve 8hr → Reassign + Teams msg to L2 lead
P3 (Medium)   → Respond 4hr  → Resolve 3BD → Reassign via ITSM
P4 (Low)      → Respond 1BD  → Resolve 5BD → Reassign via ITSM

Stuck >30min on P1? Escalate.
Stuck >60min on P2? Escalate.
Not sure who to escalate to? Ask your Service Desk Lead.
```
