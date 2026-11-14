# Architecture

This document describes how the lab is structured — the support model it simulates, how the modules relate to each other, and which tools cover what.

## Support Model

Nexora Technologies uses a tiered support model. Employees contact IT through one of three channels, and requests flow through the service desk for triage and resolution.

```mermaid
flowchart TD
    E["Nexora Employees (~25)"]

    E --> P["Self-Service Portal\n(ServiceNow / Jira)"]
    E --> EM["Email\n(support@nexora.test)"]
    E --> PH["Phone\n(Internal Extension)"]

    P --> SD["Service Desk\nTicket Created & Triaged"]
    EM --> SD
    PH --> SD

    SD --> L1["L1 Support\n(First-line resolution)"]

    L1 -->|Resolved| RES["Resolution\nTicket Closed + KB Updated"]
    L1 -->|Cannot resolve| ESC["Escalation to L2\nWith documentation"]

    ESC --> L2["L2 Support / Vendor\n(Infrastructure, Networking,\nSpecialist issues)"]
    L2 --> RES
```

In this lab, I'm playing the L1 role. L2 exists in the model but is represented as an escalation endpoint — when a scenario is beyond L1 scope, I document the escalation handoff rather than pretending to resolve something I wouldn't handle in a real job.

See [support-model.md](support-model.md) for the full details on how the support tiers work at Nexora.

## Module Relationships

The modules aren't isolated — they connect the way real support workflows do. An incident scenario might involve logging a ticket in ServiceNow, running Windows troubleshooting, updating the asset register, and writing a KB article.

```mermaid
flowchart LR
    INC["incidents/\nScenario triggered"]

    INC --> ITSM["itsm/\nTicket logged in\nServiceNow or Jira"]
    INC --> WIN["windows-support/\nOS, hardware, software,\nprinter troubleshooting"]
    INC --> NET["networking/\nConnectivity diagnosis,\nPacket Tracer labs"]
    INC --> M365["microsoft-365/\nOutlook, Teams,\nOneDrive issues"]
    INC --> AD["active-directory/\nAccount & access\nmanagement"]

    WIN --> KB["knowledge-base/\nNew or updated\nKB article"]
    NET --> KB
    M365 --> KB
    AD --> KB

    ITSM --> OPS["operations/\nShift handover,\nescalation logs"]

    INC --> ASSET["asset-management/\nAsset record updated\nif hardware involved"]

    INC --> REP["reporting/\nIncident data feeds\ninto reports"]
    ASSET --> REP

    ITIL["itil-processes/\nFramework applied\nacross all modules"]
    ITIL -.->|Guides| INC
    ITIL -.->|Guides| ITSM
    ITIL -.->|Guides| OPS

    COMM["communication/\nUser notifications,\nstatus updates"]
    INC --> COMM

    SCRIPTS["scripts/\nAutomation utilities"]
    SCRIPTS -.->|Supports| WIN
    SCRIPTS -.->|Supports| AD
    SCRIPTS -.->|Supports| REP

    DOCS["docs/\nWalkthrough & Scope\nVerification"]
    INC -.->|Feeds| DOCS
```

The key insight: **incidents are the center of gravity**. Almost everything flows from or into a support incident. That's why the `incidents/` module connects to nearly everything else.

## Tool Landscape

Different modules use different tools. Here's what covers what:

```mermaid
flowchart TD
    subgraph Deployed["Local Running Services"]
        PORTAL["Python Service Desk\n(itsm/portal/app.py)"]
        SAMBA["Samba 4 AD DC\n(WSL2 Ubuntu)"]
    end

    subgraph Reference["Reference Blueprints & Designs"]
        SN["ServiceNow Blueprint\n(itsm/servicenow/)"]
        JIRA["Jira SM Blueprint\n(itsm/jira-service-management/)"]
        PT["Cisco Network Design\n(networking/packet-tracer/)"]
    end

    subgraph Local["Local Tools"]
        PS["PowerShell 5.1"]
        PY["Python 3.14\n(stdlib only)"]
        GIT["Git"]
        TSHARK["Wireshark / TShark"]
    end

    subgraph Modules["Lab Modules"]
        ITSM_M["itsm/"]
        INC_M["incidents/"]
        KB_M["knowledge-base/"]
        AD_M["active-directory/"]
        NET_M["networking/"]
        WIN_M["windows-support/"]
        M365_M["microsoft-365/"]
        ASSET_M["asset-management/"]
        REP_M["reporting/"]
        SCRIPTS_M["scripts/"]
    end

    PORTAL --> ITSM_M
    SN -.-> ITSM_M
    JIRA -.-> ITSM_M
    SAMBA --> AD_M

    PS --> WIN_M
    PS --> AD_M
    PS --> SCRIPTS_M

    PY --> REP_M
    PY --> SCRIPTS_M
    PY --> PORTAL

    PT -.-> NET_M
    TSHARK --> NET_M

    GIT --> |"Version control\nfor everything"| Modules
```

### Tool Selection Summary

| Need | Tool | Implementation & Rationale |
|------|------|----------------------------|
| Interactive Service Desk | Python stdlib (`http.server` + `sqlite3`) | Real local interactive web portal at `localhost:8080` with queues, agent console, and customer tracking. Zero external dependencies. |
| Enterprise ITSM Design | ServiceNow & Jira SM Runbooks | Documented reference blueprints, field dictionaries, SLA definitions, and configuration runbooks in `itsm/`. |
| Directory Services | Samba 4 AD DC (WSL2 Ubuntu) | Real local Active Directory domain controller (`nexora.test`) providing LDAP, Kerberos, AGDLP group nesting, and SMB share testing without heavy VM resource usage. |
| Network Analysis | Wireshark / TShark | Packet analysis using a 20-frame loopback `.pcap` capture and TShark display filters. |
| Network Design | Cisco IOS Running Configs | Syntax-accurate Cisco 2911 router and 2960 switch configuration drafts and topology documentation in `networking/packet-tracer/`. |
| Windows Admin | PowerShell 5.1 | Built into Windows; runbooks for desktop troubleshooting, client diagnostics, and automated audits. |
| Reporting & Validation | Python 3.14 (stdlib) | Native CSV and JSON processing for MTTR, SLA calculations, and schema verification; 13/13 passing unit tests. |
| Version Control | Git | Tracking all iterations, code, and documentation cleanly. |
| Documentation | Markdown files | Plain text, clean diffs, and readable directly on GitHub. |

Full rationale for each choice is in [design-decisions.md](design-decisions.md).
