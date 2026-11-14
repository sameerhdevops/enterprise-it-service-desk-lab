# Service Level Agreement — IT Support Services

> ⚠️ **FICTIONAL DOCUMENT** — This is a simulated SLA policy for **Nexora Technologies**, a fictional company used in a learning lab. It does not represent any real organization's policies or commitments.

---

**Document ID:** NXT-SLA-001
**Version:** 1.0
**Effective Date:** November 1, 2024
**Review Date:** May 1, 2025
**Owner:** IT Service Management, Nexora Technologies
**Approved By:** Ramesh Iyer, IT Manager

---

## 1. Purpose

This Service Level Agreement defines the expected response and resolution times for IT support services provided by the Nexora Technologies IT Service Desk to all internal users. It establishes clear, measurable targets to ensure consistent service quality and accountability.

## 2. Scope

This SLA covers all IT support services delivered by the L1 Service Desk team, including:

- Incident management (break/fix)
- Service request fulfilment
- Access and account management
- Hardware and software support
- Network connectivity support
- Printing support
- Email and communication tools support

**Out of scope:** Application development, business process changes, third-party vendor management (covered by separate OLAs).

## 3. Service Hours & SLA Measurement Policy

> **Lab Policy Note (Elapsed Clock Hours):**
> For the Nexora Technologies learning lab and reporting dataset, all SLA targets are tracked using **elapsed clock hours** (continuous 24x7 elapsed time from ticket creation to resolution). This provides an unambiguous, mathematically reproducible evaluation across all incidents and reports:
> - **P1 — Critical:** 4 elapsed hours (24x7 continuous clock)
> - **P2 — High:** 8 elapsed clock hours
> - **P3 — Medium:** 72 elapsed clock hours (3 calendar days) — *Note: explicitly measured as 72 elapsed hours, not 3 business days*
> - **P4 — Low:** 120 elapsed clock hours (5 calendar days) — *Note: explicitly measured as 120 elapsed hours, not 5 business days*
>
> These targets represent fictional Nexora organizational policy choices designed for straightforward laboratory calculation, not universal ITIL requirements.

| Service Level | Description | Applied SLA Clock |
|---|---|---|
| Standard Support | Operational Service Desk (Monday – Friday, 09:00 – 18:00 IST) | Elapsed Clock Hours (All priorities) |
| On-Call Escalation | Emergency Tier 2/3 Escalations (24/7) | Elapsed Clock Hours (P1 / Critical) |

## 4. Priority Definitions

Priority is determined by the combination of **Impact** and **Urgency**, using the standard priority matrix.

### Impact Levels

| Level | Definition | Criteria |
|-------|-----------|----------|
| **1 — High** | Business-critical service is down or severely degraded | ≥50% of users affected, OR a revenue-generating/regulatory system is unavailable |
| **2 — Medium** | A service is degraded or a group of users is affected | 5-49% of users affected, OR a non-critical system is unavailable with no workaround |
| **3 — Low** | A single user is affected with minimal business impact | Single user, workaround available, cosmetic issue |

### Urgency Levels

| Level | Definition | Criteria |
|-------|-----------|----------|
| **1 — High** | Work is completely blocked, no workaround | User or team cannot perform primary job function |
| **2 — Medium** | Work is impaired but can continue at reduced capacity | Partial functionality, workaround available but inconvenient |
| **3 — Low** | Minor inconvenience, workaround is easy | Issue can wait, doesn't affect deliverables |

### Priority Matrix

| | **Urgency 1** | **Urgency 2** | **Urgency 3** |
|---|---|---|---|
| **Impact 1** | **P1 — Critical** | **P2 — High** | **P3 — Medium** |
| **Impact 2** | **P2 — High** | **P3 — Medium** | **P4 — Low** |
| **Impact 3** | **P3 — Medium** | **P4 — Low** | **P4 — Low** |

## 5. Service Level Targets — Incidents

| Priority | Response Target | Resolution Target (Elapsed Clock Hours) | Measurement Scope |
|---|---|---|---|
| **P1 — Critical** | 15 minutes | 4 elapsed hours | 24x7 Continuous Clock |
| **P2 — High** | 1 hour | 8 elapsed clock hours | Continuous Clock |
| **P3 — Medium** | 4 hours | 72 elapsed clock hours (3 calendar days) | Continuous Clock |
| **P4 — Low** | 24 hours | 120 elapsed clock hours (5 calendar days) | Continuous Clock |

### 5.1 Response Time — Definition

**Response time** is measured from the moment the incident is logged in the ITSM system to the moment an analyst:

1. Acknowledges the ticket (status moves from New to Assigned), **AND**
2. Makes initial contact with the affected user (phone, email, portal update, or in-person)

Simply assigning the ticket without contacting the user does not satisfy the response SLA. The user must know someone is working on their issue.

### 5.2 Resolution Time — Definition

**Resolution time** is measured from the moment the incident is logged to the moment the service is restored to normal operation and the user confirms resolution (or the confirmation period expires).

**Clarifications:**
- A **workaround** that fully restores the user's ability to work counts as resolution. The underlying problem can be tracked separately in a problem record.
- **Continuous Elapsed Clock:** In this laboratory and the local Service Desk application, resolution time is tracked continuously 24x7 from the moment of ticket creation (`created_at`) until technical resolution (`resolved_at`).
- **No Pausing for Pending States:** The application does not implement calendar schedules or pause the clock for `Pending Customer` or `Pending Vendor` states. Elapsed hours accumulate continuously (`elapsed_hours = (resolved_at or now) - created_at`).

### 5.3 SLA Clock Behavior

| Priority | Clock Starts | Clock Runs | Clock Pauses | Resolution Target |
|----------|-------------|------------|--------------|-------------------|
| P1 | On ticket creation | 24/7 continuous elapsed time | Does not pause | 4 elapsed hours |
| P2 | On ticket creation | 24/7 continuous elapsed time | Does not pause | 8 elapsed hours |
| P3 | On ticket creation | 24/7 continuous elapsed time | Does not pause | 72 elapsed hours |
| P4 | On ticket creation | 24/7 continuous elapsed time | Does not pause | 120 elapsed hours |

**Continuous Clock Evaluation:**
- Elapsed time begins immediately upon ticket submission.
- All targets are evaluated as continuous elapsed clock hours, providing an unambiguous and mathematically reproducible calculation across all reports and test suites.

## 6. Service Level Targets — Service Requests

| Request Type | Target Fulfilment Time |
|-------------|----------------------|
| Password Reset / Account Unlock | 30 minutes |
| Standard Software Install | 4 hours |
| New User Account | 4 hours (from approved request) |
| Hardware Provisioning | 3-5 business days |
| Access Permission Change | 4 hours (from approved request) |
| Licensed Software Install | 2 business days (pending license availability) |

Service request SLAs run during standard support hours only. Time waiting for approval is excluded from the fulfilment time measurement.

## 7. Escalation Triggers

Automatic escalation occurs at the following SLA thresholds:

| Priority | Warning at | Breach at | Escalated To |
|----------|-----------|-----------|-------------|
| P1 | 50% of resolution time (2 hours) | 100% (4 hours) | IT Manager + Senior Engineer |
| P2 | 75% of resolution time (6 hours) | 100% (8 hours) | Service Desk Lead + L2 Team Lead |
| P3 | 75% of resolution time | 100% (3 business days) | Service Desk Lead |
| P4 | No warning | 100% (5 business days) | Service Desk Lead |

See [escalation-matrix.md](../itil-processes/escalation-matrix.md) for the full escalation path.

## 8. SLA Compliance Targets

| Metric | Target | Measurement Period |
|--------|--------|--------------------|
| P1 response SLA compliance | ≥95% | Monthly |
| P1 resolution SLA compliance | ≥90% | Monthly |
| P2 response SLA compliance | ≥95% | Monthly |
| P2 resolution SLA compliance | ≥90% | Monthly |
| P3 response SLA compliance | ≥95% | Monthly |
| P3 resolution SLA compliance | ≥92% | Monthly |
| P4 response SLA compliance | ≥95% | Monthly |
| P4 resolution SLA compliance | ≥95% | Monthly |
| Overall SLA compliance | ≥93% | Monthly |

## 9. Exclusions

The SLA does not apply in the following situations:

- **Force majeure** — Natural disasters, power outages beyond Nexora's control, internet service provider failures
- **Scheduled maintenance** — Planned maintenance during approved windows (users notified ≥48 hours in advance)
- **User-caused issues** — Damage from unauthorized software installation, physical damage from misuse
- **Third-party service outages** — When the root cause is entirely at a third-party provider (e.g., Microsoft 365 global outage), though communication SLAs still apply
- **Insufficient information** — When the user has not yet provided necessary information to diagnose the issue

## 10. Reporting

| Report | Frequency | Audience |
|--------|-----------|----------|
| SLA Compliance Dashboard | Real-time | Service Desk Team |
| Weekly SLA Summary | Weekly (Monday) | IT Manager, Service Desk Lead |
| Monthly SLA Report | Monthly (1st business day) | IT Manager, Department Heads |
| SLA Breach Report | Per breach (within 1 business day) | IT Manager |

### Monthly Report Contents

- Total incidents by priority
- SLA compliance percentage by priority
- Breached tickets with root cause of breach
- Trend analysis (month-over-month)
- Top 5 incident categories
- First contact resolution rate
- Mean time to resolve by priority
- Service request fulfilment compliance

## 11. Ticket Reopening & Continuous Clock SLA Recalculation Policy

When a resolved or closed incident is reopened by a user or technician (transitioning back to **In Progress**):

1. **Resolution Timestamp Cleared:** The existing resolution timestamp (`resolved_at`) is set to `NULL`.
2. **Continuous Clock Resume:** The SLA timer resumes measuring elapsed time against the original ticket creation timestamp (`created_at`).
   - The SLA clock is **NOT reset to 0.0 hours**. Historical elapsed time is strictly preserved.
   - Reopening an incident does not grant a new or refreshed SLA resolution window.
3. **Breach Evaluation on Reopening:**
   - If cumulative elapsed continuous clock time since ticket creation (`now - created_at`) exceeds the defined SLA target hours (e.g. >4.0h for P1), the reopened ticket immediately registers as **Breached** (`sla_breached = 1`, `sla_status = 'Breached'`).
   - If cumulative elapsed time remains within the SLA target window, the remaining time is calculated as `target_hours - elapsed_hours`, and the ticket remains **Within SLA** (or **At Risk** if elapsed time is ≥75% of target).
4. **Subsequent Re-resolution:** Upon subsequent technical resolution, a new `resolved_at` timestamp is recorded, capturing the total elapsed time from ticket creation to final resolution.

## 12. Review and Amendment

This SLA is reviewed every 6 months or when:

- A significant change in IT services occurs
- SLA targets are consistently not being met (3 consecutive months below target)
- Organizational changes affect support requirements

Changes require approval from the IT Manager and notification to all department heads.

---

> ⚠️ **Reminder:** This is a fictional SLA for learning purposes. Real-world SLAs would include legal terms, penalty clauses, service credits, and formal signature blocks.
