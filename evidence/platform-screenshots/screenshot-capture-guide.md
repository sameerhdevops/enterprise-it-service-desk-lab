# Evidence Guide: Platform Screenshots & Live Artifact Checklists
**Document ID:** EVD-001  
**Status:** MANUAL ACTION REQUIRED (For SaaS platforms requiring candidate credentials)

---

## 1. Ethical Evidence Policy
In accordance with engineering ethics and portfolio defensibility rules:
- **NO FAKE SCREENSHOTS:** Never generate synthetic or AI-hallucinated images that imitate ServiceNow, Jira, or Windows system dialogs.
- **NO CREDENTIAL EXPOSURE:** When capturing screenshots from real accounts, blur or redact personal email addresses, private API tokens, or personal phone numbers.
- **HONEST STATUS:** Platform configuration is documented and templated locally; live cloud instances are documented as pending personal activation.

---

## 2. Checklist for Capturing Genuine ServiceNow Evidence (Once PDI Activated)

When the candidate logs into their free ServiceNow PDI ([https://developer.servicenow.com](https://developer.servicenow.com)):

| Evidence Item | Navigation Path in ServiceNow | Expected Screen Element | Target Filename |
|---|---|---|---|
| **Incident List** | `incident.list` in filter navigator | Grid showing INC0001–INC0020 with Priorities, Statuses, and Callers. | `evidence/platform-screenshots/sn-incident-list.png` |
| **P1 Incident View** | Open `INC0015` (Network degradation) | Incident form showing Priority 1, Impact 1, Urgency 1, and Work Notes. | `evidence/platform-screenshots/sn-p1-incident-form.png` |
| **SLA Countdown Timer** | Related Lists at bottom of Incident form | `Task SLAs` tab showing active resolution countdown timer and duration. | `evidence/platform-screenshots/sn-sla-timer.png` |
| **Knowledge Base** | `kb_knowledge.list` | List of published articles with view count and category. | `evidence/platform-screenshots/sn-knowledge-article.png` |
| **CMDB Dependency View** | `cmdb_ci.list` > select `SW-CORE-01` > View Dependency | Visual tree showing relationships from Switch to Servers and Business Services. | `evidence/platform-screenshots/sn-cmdb-bsm-map.png` |

---

## 3. Checklist for Capturing Jira Service Management Evidence (Once Free Cloud Active)

| Evidence Item | Navigation Path in JSM | Expected Screen Element | Target Filename |
|---|---|---|---|
| **Customer Portal** | `https://[site].atlassian.net/servicedesk/customer/portal/1` | Branded portal showing request categories (Computers, Logins, Applications). | `evidence/platform-screenshots/jsm-customer-portal.png` |
| **Agent Queue View** | Project > Queues > `Unassigned Incidents` | Triage queue sorted by priority with SLA time to first response badges. | `evidence/platform-screenshots/jsm-agent-queues.png` |
| **Ticket View** | Open ticket `NEX-1` | Ticket view showing customer comment vs internal note toggle. | `evidence/platform-screenshots/jsm-ticket-view.png` |

---

## 4. Host System Evidence (Captured Locally)
Genuine text-based command outputs and system architecture logs are archived in `evidence/command-output/`:
- `os-architecture.txt` — Host OS build, physical RAM, architecture
- `ipconfig-all.txt` — Full network configuration, DHCP and DNS servers
- `top-processes-cpu.txt` — Real-time CPU and memory process table
- `services-status.txt` — Print Spooler, Windows Update, DHCP client states
- `route-print.txt` — Windows IPv4 routing table and gateway metrics
- `test-netconnection-dns-port.txt` — Layer 4 TCP port probe
