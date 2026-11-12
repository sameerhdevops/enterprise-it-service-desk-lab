# Jira Service Management Incident Workflow
**Document ID:** ITSM-JSM-003  
**Platform:** Jira Service Management Cloud

---

## 1. JSM Incident Workflow States

```
[Open] ────────────────────────┐
  │                            │ (Cancel request)
  │ (Assign / Start work)      ▼
  ▼                       [Canceled]
[Work in progress] ────────────┐
  │         ▲                  │
  │         │ (Customer responds)
  │ (Need info)                │
  ▼         │                  ▼
[Waiting for customer]    [Resolved]
                               │
                               │ (After 3 days auto-close)
                               ▼
                            [Closed]
```

## 2. Customer Comments vs. Internal Notes in Jira
- **Reply to customer:** Sends an email notification to the reporter and posts on the Customer Portal. Used for updates and gathering diagnostic logs.
- **Internal note:** Yellow highlighted background. Only visible to team members with agent licenses. Used for internal troubleshooting steps, IP addresses, escalation context.
