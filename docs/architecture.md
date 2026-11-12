# Architecture

This document describes how the lab is structured — the support model it simulates, how the modules relate to each other, and which tools cover what.

## Support Model

Nexora Technologies uses a tiered support model. Employees contact IT through one of three channels, and requests flow through the service desk for triage and resolution.

```mermaid
flowchart TD
    E["Nexora Employees (~25)"]

    E --> P["Self-Service Portal\n(ServiceNow / Jira)"]
    E --> EM["Email\n(support@nexora.tech)"]
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

    INTERVIEW["interview-preparation/\nScenarios become\ninterview examples"]
    INC -.->|Feeds| INTERVIEW
```

The key insight: **incidents are the center of gravity**. Almost everything flows from or into a support incident. That's why the `incidents/` module connects to nearly everything else.

## Tool Landscape

Different modules use different tools. Here's what covers what:

```mermaid
flowchart TD
    subgraph Cloud["Cloud / Web Services"]
        SN["ServiceNow PDI"]
        JIRA["Jira Service\nManagement"]
    end

    subgraph Local["Local Tools"]
        PS["PowerShell 5.1"]
        PY["Python 3.14\n(stdlib only)"]
        GIT["Git 2.55.0"]
        PT["Cisco Packet\nTracer"]
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

    SN --> ITSM_M
    JIRA --> ITSM_M

    PS --> WIN_M
    PS --> AD_M
    PS --> SCRIPTS_M

    PY --> REP_M
    PY --> SCRIPTS_M

    PT --> NET_M

    GIT --> |"Version control\nfor everything"| Modules
```

### Tool Selection Summary

| Need | Tool | Rationale |
|------|------|-----------|
| Ticket management | ServiceNow PDI + Jira SM | Industry standard platforms, both free for learning |
| Network simulation | Cisco Packet Tracer | Free, widely used in CCNA training, good enough for L1 concepts |
| Windows admin | PowerShell 5.1 | Built into every Windows machine, essential IT support skill |
| Reporting & data | Python 3.14 (stdlib) | csv + json modules handle everything; no external dependencies |
| Version control | Git 2.55.0 | Track all changes, demonstrate progression |
| Documentation | Markdown files | Plain text, diffs well, renders on GitHub |

Full rationale for each choice is in [design-decisions.md](design-decisions.md).
