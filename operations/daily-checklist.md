# L1 Service Desk Daily Operations Checklist
**Document ID:** OPS-CHK-001  
**Role:** L1 IT Support Engineer / Service Desk Analyst  
**Shift:** Morning Shift (08:30 – 17:30 IST) / Evening Shift (13:30 – 22:30 IST)

---

## 1. Morning Shift Start Routine (08:30 – 09:15)

- [ ] **Shift Handover Review:** Read previous evening's shift handover log. Identify any ongoing P1/P2 incidents, unresolved escalations, or pending morning VIP requests.
- [ ] **Ticket Queue Sweep (Triage):**
  - Check unassigned queue in ServiceNow / Jira Service Management.
  - Triage overnight emails and portal submissions.
  - Assign priority (P1–P4) based on Impact and Urgency matrix.
  - Route tickets to appropriate assignment groups (`L1 Service Desk`, `L2 Desktop`, `L2 Network`).
- [ ] **Infrastructure Health Check:**
  - Verify PRTG / SolarWinds / Ping monitoring dashboard for red/amber device status.
  - Ping key network assets:
    - Default Gateway (`192.168.10.1`)
    - Domain Controller / DNS (`192.168.20.10`)
    - File Server (`192.168.20.15`)
    - Core Switch (`SW-CORE-01`)
  - Verify internet WAN bandwidth link status.
- [ ] **Physical Walkthrough (Office Floors):**
  - Verify main departmental network printers have paper loaded and green "Ready" status.
  - Check conference room A/V equipment (Teams Rooms displays, microphones, HDMI docks).

---

## 2. Mid-Day Operational Cadence (09:15 – 16:30)

- [ ] **SLA Monitor:** Keep "Tickets Nearing Breach" dashboard open. Ensure all new tickets receive first response within SLA targets (P1: 15m, P2: 60m, P3: 4h).
- [ ] **Work Notes Updating:** Update customer-facing and internal work notes on all active tickets.
- [ ] **Pending User Follow-ups:** Review tickets in `On Hold / Waiting for customer` state. If user has not responded after 48 hours, send second reminder.
- [ ] **New Hire Prep:** Check Service Request queue for onboarding requests scheduled for the next 48 hours; stage laptops and verify account provisioning.

---

## 3. Shift Handover & Wrap-up Routine (16:30 – 17:30)

- [ ] **Escalation Review:** Follow up with L2/L3 engineers on escalated tickets; update callers on progress.
- [ ] **Queue Reconciliation:** Ensure no unassigned tickets remain in the general intake queue.
- [ ] **Draft Shift Handover Log:** Document all open high-priority incidents, equipment outages, and tasks awaiting vendor callbacks.
- [ ] **Handover Meeting:** Conduct 10-minute verbal walkthrough with the incoming shift analyst.
