# Jira Service Management (JSM) Setup Guide
**Document ID:** ITSM-JSM-001  
**Platform:** Atlassian Jira Service Management (Cloud Free Tier)  
**Status:** MANUAL ACTION REQUIRED (Optional secondary platform demonstration)

---

## 1. Overview
Jira Service Management (JSM) is utilized as the secondary ITSM platform in the Nexora Technologies lab. Atlassian offers an official **Free Plan** supporting up to 3 agents, unlimited customers, customer portal, SLA tracking, and basic automation rules.

---

## 2. Step-by-Step JSM Setup Procedure

1. **Sign Up for Jira Service Management Cloud:**
   - Navigate to [https://www.atlassian.com/software/jira/service-management/free](https://www.atlassian.com/software/jira/service-management/free).
   - Claim a free Cloud site (e.g., `nexora-servicedesk.atlassian.net`).
   - Create your primary administrator/agent account.

2. **Project Creation:**
   - Select **Create Project** > **IT service management** template.
   - Choose **IT service desk** template (includes pre-built Request Types for Incidents, Service Requests, Changes, and Problems).
   - Project Name: `Nexora IT Support` (Project Key: `NEX`).

3. **Customer Portal Customization:**
   - Go to **Project Settings > Portal Settings**.
   - Set Portal title: `Nexora Technologies Help Center`.
   - Organize request groups: *Computers & Laptops*, *Logins & Accounts*, *Applications*, *Office Network*.

4. **Queue Management:**
   - Create customized queues for L1 triage:
     - `Unassigned Incidents` (`issuetype = Incident AND assignee is EMPTY ORDER BY priority DESC`)
     - `My Assigned Open Tickets` (`assignee = currentUser() AND statusCategory != Done`)
     - `Pending User Response` (`status = "Waiting for customer"`)
     - `High Priority (P1/P2)` (`priority in (Highest, High) AND statusCategory != Done`)
