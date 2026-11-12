# ServiceNow Incident Lifecycle & L1 Workflow Guide
**Document ID:** ITSM-SN-003  
**Audience:** L1 Service Desk Analysts  
**Table:** `incident`

---

## 1. Incident State Transition Model

ServiceNow uses integer values for the `incident_state` field:

```
[1] New
 │  ├── Auto-routed to Assignment Group
 │  └── First response clock starts
 ▼
[2] In Progress
 │  ├── Assigned to individual technician (`assigned_to`)
 │  ├── Investigation & diagnosis documented in Work Notes (internal)
 │  └── Troubleshooting with caller documented in Additional Comments (customer-visible)
 ▼
[3] On Hold (Optional Pause)
 │  ├── Reason: Awaiting Caller / Awaiting Vendor / Awaiting Change
 │  └── SLA resolution timer pauses during valid hold states
 ▼
[6] Resolved
 │  ├── Resolution Code selected (Solved by Workaround, Solved Permanently, etc.)
 │  ├── Resolution Notes documented with detailed root cause & fix
 │  └── Resolution email automatically dispatched to Caller
 ▼
[7] Closed
    ├── User confirms resolution or 5 business days elapse with no response
    └── Record becomes read-only
```

---

## 2. Customer Comments vs. Internal Work Notes

A critical distinction tested in L1 technical interviews:

| Field | Visibility | Purpose | Example |
|---|---|---|---|
| **Additional Comments (Customer visible)** | Visible to the end-user via email notifications and Self-Service Portal. | Direct communication with the user: asking questions, giving instructions, confirming resolution. | *"Hello Akash, I have cleared your Outlook credentials. Please reboot your PC and let me know if you can sign in."* |
| **Work Notes (Internal)** | Visible ONLY to ITIL-licensed support personnel. Hidden from end-users. | Technical diagnostic logs, IP addresses, error codes, internal handoffs, vendor ticket IDs. | *"Ran netstat -ano; port 587 listening. Tested ping to mail.nexora.com: 14ms latency. Discovered corrupted profile in C:\Users\adesai\AppData\Local\Microsoft\Outlook."* |

---

## 3. L1 Escalation Workflow in ServiceNow

When an issue cannot be resolved within L1 scope (e.g. exceeds 30 minutes of troubleshooting without progress, requires network switch configuration, or hardware replacement):

1. **Document Technical Actions Taken:** Record all commands executed, tools used, and diagnostic findings in **Work Notes**.
2. **Set Assignment Group:** Change from `L1 Service Desk` to target group (e.g., `L2 Network Support`).
3. **Clear Assigned To:** Remove your own name so the ticket enters the L2 group queue unassigned, alerting the L2 dispatcher.
4. **Notify Caller:** Post an **Additional Comment** informing the caller that the ticket has been escalated to specialized engineering.
5. **Adjust Urgency/Impact:** Only adjust if investigation revealed the scope of impact is wider than initially reported.
