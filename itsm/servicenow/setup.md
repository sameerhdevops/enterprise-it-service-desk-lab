# ServiceNow Personal Developer Instance (PDI) Setup Guide
**Document ID:** ITSM-SN-001  
**Target Audience:** L1 Support Engineer / Service Desk Analyst  
**Platform:** ServiceNow Developer Program (Utah/Vancouver/Washington DC releases)  
**Status:** MANUAL ACTION REQUIRED (Requires candidate account activation)

---

## 1. Overview
ServiceNow is the primary enterprise IT Service Management (ITSM) platform simulated in the Nexora Technologies lab. Because ServiceNow is a cloud-hosted enterprise SaaS product, live configuration is performed using a free **Personal Developer Instance (PDI)** provided via the ServiceNow Developer Program.

> **Status Notice:**  
> Cloud account registration and tenant provisioning require individual authentication. This guide provides the exact configuration sequence, data dictionaries, and validation steps so the lab owner can perform and defend the implementation.

---

## 2. Step-by-Step PDI Provisioning Procedure

1. **Sign Up for ServiceNow Developer Program:**
   - Navigate to [https://developer.servicenow.com/](https://developer.servicenow.com/).
   - Click **Sign Up** using your professional email address.
   - Complete email verification and log in to the developer portal.

2. **Request an Instance:**
   - In the Developer portal header, click **Request an Instance**.
   - Select the latest stable enterprise release (e.g., Washington DC or Vancouver).
   - Wait 5–10 minutes while the cloud instance spins up.
   - Record your instance URL (format: `https://devXXXXX.service-now.com/`) and temporary `admin` credentials securely in a private password manager (never commit to git).

3. **Initial Instance Hardening & Maintenance:**
   - PDIs hibernate after 2 hours of inactivity and reclaim after 10 days of non-use.
   - Log into the portal periodically to keep the instance active.
   - Reset the default admin password on first login.

---

## 3. Essential L1 Roles & Navigation
As an L1 Service Desk Analyst, daily operations do not use the `admin` superuser role. Instead, configure and use:

- **`itil` role:** Core role allowing analysts to create, update, investigate, and resolve Incidents, Problems, Changes, and Configuration Items.
- **`sn_request_write` / `approver_user`:** Allows viewing and fulfilling Service Catalog requests.
- **Application Navigator Shortcodes:**
  - `incident.list` — All incidents
  - `incident.filter` — Filtered incident view
  - `sys_user.list` — User database
  - `sys_user_group.list` — Assignment groups

---

## 4. Post-Provisioning Validation Checklist
- [ ] PDI URL accessible and admin authentication successful.
- [ ] Test ITIL user created (`sameer.kulkarni` with role `itil`).
- [ ] Assignment groups imported/created (`L1 Service Desk`, `L2 Desktop`, `L2 Network`).
- [ ] Fictional company caller records added for Nexora employees.
- [ ] Incident creation test ticket logged and verified in `incident.list`.
