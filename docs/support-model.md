# Nexora Technologies — IT Support Model

## Company Overview

Nexora Technologies is a small tech consulting firm with approximately 25 employees. They provide technology consulting services to mid-market clients, which means the IT team supports a mix of technical and non-technical staff who rely heavily on their tools working.

## Organisational Structure

### Departments and Headcount

| Department | Approx. Headcount | Key Systems Used |
|-----------|-------------------|-----------------|
| **HR** | 4 | Microsoft 365 (Outlook, Teams, SharePoint), HRIS |
| **Finance** | 5 | Microsoft 365, accounting software, Excel (heavy use) |
| **Operations** | 12 | Microsoft 365, project management tools, client-facing systems |
| **IT** | 3 | Everything — plus admin consoles, monitoring, ServiceNow/Jira |
| **Leadership** | 1 (Managing Director) | Microsoft 365, reporting dashboards |

**Total: ~25 employees**

### IT Team Structure

The IT team is small, which is realistic for a company this size:

| Role | Name (Fictional) | Responsibilities |
|------|-------------------|-----------------|
| **IT Manager** | Raj Patel | Strategy, vendor management, budget, L2/L3 escalations, infrastructure decisions |
| **L1 Support Engineer** | *(This is the role I'm simulating)* | Daily support, ticket handling, user provisioning, troubleshooting, KB maintenance |
| **Junior IT Admin** | Sam Torres | Assists with support queue, handles routine tasks, backup for L1 |

In a team this small, boundaries between roles blur. The L1 engineer handles things that might be split across multiple people in a larger organisation.

## Support Channels

Nexora employees can reach IT support through three channels:

### 1. Self-Service Portal
- **Platform**: ServiceNow (primary) or Jira Service Management
- **How it works**: Employees log in, select a category (hardware, software, access, etc.), fill in the details, and submit. Ticket is created automatically with a reference number.
- **Best for**: Non-urgent requests, access requests, software installation requests, issues where the user can keep working while waiting.
- **Target response**: Acknowledgement within 1 business hour.

### 2. Email
- **Address**: support@nexora.test (fictional)
- **How it works**: Email hits a shared inbox monitored by IT. L1 creates a ticket from the email and responds with the ticket number.
- **Best for**: Detailed issue descriptions, attaching screenshots, follow-ups on existing tickets.
- **Target response**: Acknowledgement within 1 business hour.

### 3. Phone
- **Number**: Internal extension 500
- **How it works**: L1 takes the call, logs the issue into the ticketing system while talking to the user, and begins troubleshooting immediately if possible.
- **Best for**: Urgent issues (can't log in at all, system completely down), situations where back-and-forth diagnosis is needed right away.
- **Target response**: Immediate.

### Channel Priority

| Urgency | Recommended Channel | Reason |
|---------|-------------------|--------|
| Can't work at all | Phone | Immediate attention |
| Blocked but have workaround | Portal or Email | Documented, tracked |
| General request | Portal | Self-service, forms guide the request |
| Follow-up on existing ticket | Email (reply to thread) | Keeps context together |

## Support Tiers

### L1 — First-Line Support (This Lab's Focus)

L1 is the first point of contact. The goal is to resolve as many issues as possible at first contact, and escalate cleanly when something is beyond scope.

**What L1 handles:**

| Category | Typical Issues |
|----------|---------------|
| **Account & Access** | Password resets, account lockouts, new user provisioning, permission changes, MFA issues |
| **Email & Calendar** | Outlook sync problems, shared mailbox access, calendar delegation, out-of-office setup |
| **Hardware** | Laptop won't boot, monitor not detected, keyboard/mouse failures, docking station issues, peripheral setup |
| **Software** | Application crashes, installation requests, update failures, license activation, browser issues |
| **Printing** | Printer offline, paper jams, driver issues, adding network printers, scan-to-email setup |
| **Connectivity** | Wi-Fi not connecting, VPN issues, slow network, can't reach internal resources |
| **Microsoft 365** | Teams audio/video problems, OneDrive sync conflicts, SharePoint access, license questions |
| **General** | "How do I...?" questions, new starter setup, equipment returns, basic training |

**What L1 is expected to do:**

1. **Log every contact** as a ticket — no informal fixes that aren't tracked
2. **Categorise and prioritise** based on impact and urgency (see SLA section below)
3. **Check the knowledge base** before troubleshooting from scratch
4. **Attempt resolution** using documented procedures and standard troubleshooting
5. **Document everything** — steps taken, what worked, what didn't
6. **Escalate with context** when the issue is beyond L1 scope — never a bare "I can't fix it"
7. **Update the user** at every stage — acknowledgement, progress, resolution
8. **Update or create KB articles** when a new solution is found

**What L1 does NOT handle:**

- Server infrastructure changes
- Network equipment configuration (switches, routers, firewalls)
- Database administration
- Code deployments
- Security incident response (beyond initial reporting and containment)
- Vendor contract negotiation

### L2 — Specialist Support / Escalation

In this lab, L2 is the escalation endpoint. It represents:

- The IT Manager handling infrastructure or complex issues
- External vendors for hardware warranty or specialised software
- Cloud service providers for platform-level issues (Microsoft 365 admin centre, etc.)

When I escalate in a scenario, I document:
- What I tried and why it didn't work
- What I think the problem is (or that I don't know)
- What information L2 will need
- How urgent it is and what the user impact is

That escalation documentation is the deliverable, because clean handoffs are a skill in themselves.

## SLA Framework

Nexora uses a simple priority matrix based on ITIL's impact × urgency model:

### Priority Matrix

| | **High Urgency** (Work blocked now) | **Medium Urgency** (Work impaired) | **Low Urgency** (Inconvenience) |
|---|---|---|---|
| **High Impact** (Multiple users / critical system) | **P1 — Critical** | **P2 — High** | **P3 — Medium** |
| **Medium Impact** (Single user, core function) | **P2 — High** | **P3 — Medium** | **P4 — Low** |
| **Low Impact** (Single user, non-core function) | **P3 — Medium** | **P4 — Low** | **P4 — Low** |

### SLA Targets

| Priority | Response Time | Resolution Target | Example |
|----------|--------------|-------------------|---------|
| **P1 — Critical** | 15 minutes | 4 hours | Email system down for everyone, network outage |
| **P2 — High** | 30 minutes | 8 hours | User can't log in, critical application crash |
| **P3 — Medium** | 4 hours | 24 hours | Printer issue (workaround available), non-critical software bug |
| **P4 — Low** | 8 hours | 72 hours | Feature request, cosmetic issue, "how do I" question |

These are aggressive for a 3-person IT team, but they're based on common real-world targets. In practice, a small team often beats these for simple issues and misses them for complex ones — which is itself a useful thing to track and report on.

## Escalation Procedure

When L1 determines an issue needs escalation:

1. **Exhaust L1 options** — Don't escalate just because it's hard. Try the documented procedures, check the KB, search for known issues.
2. **Document thoroughly** — What the user reported, what you tried, what the results were, any error messages or logs collected.
3. **Set the right priority** — Re-assess if initial priority was wrong based on what you've learned during troubleshooting.
4. **Reassign the ticket** — Move to the appropriate L2 queue (IT Manager, vendor, specialist) with all documentation attached.
5. **Notify the user** — Tell them it's been escalated, give a realistic expectation, and let them know their ticket number still tracks it.
6. **Add to handover** — If it's end of shift, include it in the shift handover notes.

## Communication Standards

Every user interaction follows a basic structure:

- **Acknowledgement**: "I've received your request (ticket #INC001234). I'm looking into it now."
- **Progress update** (if resolution isn't immediate): "I've identified the issue as [X]. I'm working on [Y] and expect to have it resolved by [time]."
- **Resolution**: "This has been resolved by [action]. Please test and let me know if the issue recurs."
- **Escalation notification**: "I've escalated this to [team/person] because [reason]. Your ticket number is still INC001234 — I'll follow up to make sure it's being handled."

Templates for these are in `communication/`.
