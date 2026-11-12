# IT Service Desk Escalation Procedure
**Document ID:** OPS-ESC-001  
**Audience:** L1 Service Desk Analysts  
**Scope:** Functional (L1 -> L2/L3) & Hierarchical (Management) Escalation

---

## 1. When to Escalate (Functional Escalation Criteria)

An L1 Service Desk Analyst must NOT hold onto a ticket indefinitely. Functional escalation is triggered when:
1. **Time Threshold Exceeded:** Initial investigation and standard runbooks have been executed for **30 minutes** without progress or positive diagnosis.
2. **Permission / Privilege Boundaries:** Resolution requires administrative rights outside L1 scope (e.g., firewall policy modification, switch port configuration, database schema change, hypervisor console access).
3. **Physical Hardware Disassembly:** Equipment requires motherboard replacement, internal soldering, or manufacturer warranty depot RMA.
4. **Major Incident (P1 / Critical):** System outage impacting an entire business department or core revenue service requires immediate L2/L3 mobilization.

---

## 2. Mandatory Information Required in an Escalation Handover

Never pass a "naked" ticket to L2. Every escalated ticket MUST contain a structured **Work Note** adhering to the **S-B-A-R** format (Situation, Background, Assessment, Recommendation):

```
=== L1 ESCALATION SUMMARY ===
1. Issue Summary: Brief, clear description of the specific technical failure.
2. Troubleshooting Performed: Exact commands run, tools used, and results observed.
3. Steps Ruled Out: What has been eliminated as the root cause.
4. Reason for Escalation: Why L2/L3 expertise is required.
5. User Availability / Impact: Urgency, callback number, and best time to contact.
=============================
```

### Example of a High-Quality Escalation Work Note:
> *"=== L1 ESCALATION TO L2 NETWORK ===*  
> *Issue: User unable to connect to GlobalProtect VPN from home broadband. Displays 'Gateway timed out'.*  
> *Troubleshooting Done: Verified user home internet speed (85 Mbps down, ping 8.8.8.8 < 15ms). Reinstalled GlobalProtect client 6.1. Flushed DNS. Tested TCP/SSL mode—client connects but immediately drops after 60 seconds.*  
> *Ruled Out: Home ISP connectivity failure, incorrect portal URL, expired user credentials.*  
> *Reason for Escalation: Suspected MTU fragmentation or gateway-side tunnel disconnect. Requires firewall session log inspection.*  
> *Caller Contact: Divya Ramesh, +91-98765-43210 (Available till 18:00 IST)."*

---

## 3. Hierarchical Escalation (Management Escalation)

Hierarchical escalation is not about technical assistance—it is about notifying management of business risk, SLA breaches, or customer dissatisfaction:
- **P1 Incident Trigger:** Immediate notification to IT Service Desk Lead (within 15 minutes of logging).
- **SLA Breach Threat:** When a P2 ticket reaches 75% of its resolution SLA timer without a clear fix, notify Service Desk Lead to assign additional resources.
- **Customer Escalation / Irreconcilable Conflict:** When a user requests management intervention or becomes unprofessionally abusive, escalate immediately to Team Lead without engaging in an argument.
