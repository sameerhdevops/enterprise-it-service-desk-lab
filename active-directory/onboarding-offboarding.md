# Employee IT Onboarding & Offboarding Standard Operating Procedure
**Document ID:** AD-005  
**Audience:** L1 Service Desk Analysts  
**Scope:** Identity Lifecycle, Asset Provisioning, Deprovisioning, Audit Compliance

---

## 1. Employee IT Onboarding Workflow

When a new employee joins Nexora Technologies, HR submits a Service Request (`SR-ONBOARD`) at least 3 business days prior to the start date.

```
[HR Submits Request] ──> [Manager Approval] ──> [L1 Service Desk Fulfillment Task]
                                                        │
                      ┌─────────────────────────────────┴─────────────────────────────────┐
                      ▼                                                                   ▼
           [1. Identity & Access]                                              [2. Hardware & Setup]
  - Create AD Account in Department OU                                - Provision Laptop from Asset Inventory
  - Assign Email License (Exchange/M365)                              - Image with Windows 11 Enterprise
  - Add to Baseline Security Groups                                  - Install Standard App Suite
  - Enable MFA Requirement                                            - Record Serial in CMDB as "Assigned"
                      │                                                                   │
                      └─────────────────────────────────┬─────────────────────────────────┘
                                                        ▼
                                       [3. Day 1 Handover & Welcome Email]
                                       - Issue hardware & asset handover form
                                       - Provide temporary password & MFA guide
                                       - Verify successful logon with user
```

### L1 Onboarding Checklist:
- [ ] User account created in correct departmental OU (`OU=Finance,OU=Nexora-Users,DC=nexora,DC=local`).
- [ ] Group memberships assigned per role template (e.g., `DEPT-Finance`, `SHARE-Finance-ReadWrite`).
- [ ] Microsoft 365 E3 license assigned via Microsoft 365 Admin Center or dynamic group licensing.
- [ ] Laptop provisioned, updated to latest security patches, BitLocker recovery key escrowed in AD/Intune.
- [ ] Asset inventory updated (`NXT-AST-0xx` set to `Active`, AssignedTo set to employee name).
- [ ] Welcome email sent to user's manager with first-day IT login instructions.

---

## 2. Employee IT Offboarding Workflow

Offboarding is a critical security procedure designed to prevent data theft and unauthorized access after employee departure. Triggered by HR request (`SR-OFFBOARD`).

### L1 Offboarding Checklist:
1. **Immediate Account Revocation (Day of Departure at 18:00 IST):**
   - Reset the user's AD password to a random 32-character string.
   - Disable the Active Directory account (`Disable-ADAccount`).
   - Move the user object to the `OU=Disabled-Users,DC=nexora,DC=local` OU.
   - Revoke all active Azure AD / M365 refresh tokens to force immediate logout across all mobile devices and web sessions.
2. **Email & Data Archival:**
   - Convert user mailbox to a **Shared Mailbox** (frees up the paid M365 license while preserving email history).
   - Grant mailbox Read & Manage permissions to the departing employee's manager (requires signed HR approval).
   - Set internal auto-reply out-of-office message routing business inquiries to the team lead.
3. **Hardware Collection & Asset Reconciliation:**
   - Collect laptop, charger, security access badge, and external monitors.
   - Inspect hardware for physical damage.
   - Move asset status in CMDB to **In Stock (Pending Wipe)**.
   - Securely wipe and re-image workstation with standard corporate OS image prior to reissuing to inventory.
