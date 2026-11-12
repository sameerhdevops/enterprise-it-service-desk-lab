# Design Decisions

Technical choices made for this lab and why. Each decision is driven by some combination of: what's realistic for L1 support, what I can actually run on my hardware, and what's free.

## ITSM Platforms: ServiceNow PDI + Jira Free Tier

**Decision**: Use both ServiceNow (Personal Developer Instance) and Jira Service Management (free plan, up to 3 agents).

**Why two platforms?**

Job postings for L1 support roles mention both. Some companies are ServiceNow shops, others use Jira (or Zendesk, or Freshdesk, but ServiceNow and Jira are the most common for roles I'm targeting). Using both means I can talk about either one in an interview, and I can compare how they approach the same workflow differently.

**Why ServiceNow PDI specifically?**

- It's free — ServiceNow gives developer instances to anyone who registers on their developer portal.
- It's the real platform, not a demo or simulation. Same interface, same modules, same configuration that production instances use.
- The downside: PDIs reset if you don't log in for ~10 days, and they're on shared infrastructure so they can be slow. That's manageable for a learning lab. I save my configuration steps and screenshots so a reset isn't starting from zero.

**Why Jira SM free tier?**

- Free for up to 3 agents, which is exactly our fictional IT team size.
- Cloud-hosted, no setup beyond creating the project.
- Atlassian's ecosystem (Confluence, Jira Software) is common in tech companies, so familiarity with the Jira interface has broader value.

**What I'm not using:**

- Zendesk, Freshdesk, etc. — They'd work fine, but two platforms is enough. Adding more doesn't prove additional skills; it just spreads the work thinner.
- Self-hosted ticketing (osTicket, GLPI) — Would demonstrate different skills, but the industry momentum is toward cloud ITSM platforms. Spending time configuring a self-hosted PHP ticketing system isn't the best use of my time when the target roles use ServiceNow or Jira.

## Local Windows Tools Instead of VMs

**Decision**: Do most exercises directly on the Windows 11 host instead of spinning up Windows Server VMs.

**Why?**

- **Hardware constraints**: 16 GB RAM doesn't leave much room for comfortable VM usage alongside everything else (see [environment-details.md](environment-details.md)). Running ServiceNow in a browser + Packet Tracer + a Windows Server VM simultaneously would mean constant swapping.
- **Windows 11 Enterprise has most of what I need**: Group Policy Editor (gpedit.msc), Event Viewer, Disk Management, Device Manager, PowerShell with AD modules (limited, but functional for learning the commands), Computer Management — these are the same tools on the workstation side that an L1 engineer uses daily.
- **L1 support is mostly workstation-side anyway**: The majority of L1 tickets involve the user's Windows machine, not the server. Password resets, printer issues, Outlook problems, hardware troubleshooting — this all happens on Windows 10/11 workstations. Learning the server side matters, but it's more of an L2/sysadmin skill.

**The trade-off**:

I can't do full Active Directory domain exercises (domain join, GPO deployment to multiple machines, proper user provisioning with ADUC). That's a gap I'm aware of. The mitigation:
- Document the procedures as if I had a DC, referencing Microsoft's docs for accuracy
- Use PowerShell AD module commands where they work without a domain
- If I get access to a cloud lab (Azure AD, AWS WorkSpaces, etc.) or better hardware, I can add this module properly
- Note this gap honestly — interviewers would rather hear "I couldn't run a full DC on my laptop so I focused on X instead" than have me pretend I ran something I didn't

## CSV for Data (Not a Database)

**Decision**: Use CSV files for asset management, incident data, and reporting input rather than SQLite, PostgreSQL, or any database.

**Why?**

- **It's what small IT teams actually use**: A 25-person company's IT team is tracking assets in a spreadsheet, not a database. Being realistic here matters more than being technically sophisticated.
- **No dependencies**: CSV files work with Python's stdlib `csv` module, Excel, Google Sheets, and any text editor. No database drivers to install, no connection strings to manage, no server to run.
- **Git-friendly**: CSVs diff cleanly in Git. I can see exactly what changed between commits. A SQLite binary blob doesn't give me that.
- **Good enough**: For 25 employees' worth of assets and incidents, CSV performance isn't a concern. If this were a 2,500-person org, I'd want a database. At this scale, CSV is the right tool.
- **Easy to demonstrate**: If someone looks at the repo, they can read the CSV in a browser or text editor. No setup required.

**What I'd change at scale**:

If this were a real project or the fictional company grew, I'd move to SQLite first (single file, still no server, stdlib support in Python) and then to PostgreSQL if actual multi-user concurrent access were needed. The Python reporting scripts are written so this migration would mostly mean changing the data access layer, not the report logic.

## Python Standard Library Only for Reporting

**Decision**: No pip dependencies. Reporting scripts use only `csv`, `json`, `os`, `datetime`, `collections`, and string formatting.

**Why?**

- **Zero setup friction**: Clone the repo, run the script. No `pip install`, no virtual environment, no version conflicts. It just works if you have Python.
- **Demonstrates fundamentals**: Using pandas or openpyxl would be the "real" answer for production reporting, but this lab is about showing I can write working code, not that I can install libraries. The stdlib forces me to understand what I'm doing with the data instead of calling `df.groupby()`.
- **Relevant to the role**: L1 support scripting is usually quick-and-dirty PowerShell or Python to automate a repetitive task. It's not data engineering. Keeping the tools simple matches the role.
- **The `requirements.txt` says so explicitly**: The project's requirements.txt documents this choice — "Only standard library is required for core functionality. No external packages needed." That's the contract.

**Where I'd add dependencies**:

If I needed to generate formatted Excel files (`.xlsx`), I'd add `openpyxl`. If I needed data visualization (charts/graphs), I'd add `matplotlib`. But for now, HTML reports (generated from string templates) and CSV outputs cover what I need.

## Cisco Packet Tracer for Networking

**Decision**: Use Packet Tracer rather than GNS3, EVE-NG, or real hardware.

**Why?**

- **Free and lightweight**: Packet Tracer runs comfortably alongside everything else. GNS3 needs actual IOS images (licensing issues) and more RAM for the emulated devices.
- **Standard for learning**: It's what Cisco's own networking courses use. If I'm learning networking fundamentals (VLANs, DHCP, DNS, basic routing), Packet Tracer covers everything I need. I'm not trying to pass the CCNA right now — I'm trying to understand enough networking to diagnose "I can't reach the shared drive" from the L1 seat.
- **Visual topology builder**: Being able to drag-and-drop a network, cable it up, and test connectivity helps me understand topologies in a way that command-line-only simulators don't, at least at this stage.
- **Simulation mode**: Packet Tracer lets you watch packets travel hop-by-hop through the network, which is excellent for understanding how ARP, DNS queries, and TCP handshakes actually work.

**What Packet Tracer can't do**:

- It doesn't emulate real IOS fully — some advanced commands aren't available
- No Linux/Windows hosts inside the simulation (you get generic end devices)
- No real traffic generation or performance testing

For L1 networking skills, none of those limitations matter. I'm not configuring production switches. I'm building the mental model of how networks work so I can troubleshoot connectivity issues intelligently.

## Markdown for Documentation

**Decision**: All documentation in Markdown (`.md` files), no Word docs, no Confluence, no wiki platform.

**Why?**

- **Version control**: Markdown diffs cleanly in Git. I can see every edit, every improvement, every correction in the commit history.
- **Portable**: Renders on GitHub, in VS Code, in any text editor. No special software needed to read it.
- **Focus on content**: No time spent on formatting, fonts, or layouts. The content is what matters here.
- **Interview-ready**: If I share a GitHub link, the interviewer can read everything directly in their browser. No downloads, no file format issues.

**What I'd use in a real job**:

Whatever the company uses. Confluence, SharePoint, ServiceNow's knowledge base, Google Docs — the point of this lab is learning to write good documentation, not learning a specific documentation platform. The skills transfer regardless of the tool.

## Git for Everything

**Decision**: The entire lab is a single Git repository with all modules tracked.

**Why?**

- **History as evidence**: The commit history shows when I worked on what, how my approach evolved, and that this is genuine incremental work — not something generated in one sitting.
- **Branching for experiments**: If I want to try a different approach to something, I can branch, try it, and merge or discard. No risk of losing working configurations.
- **Practical skill**: Version control is expected even for non-developer IT roles now. Showing I use it naturally is a plus.
- **Single repo, not multiple**: One repository for the whole lab because the modules are interconnected. An incident scenario might touch `itsm/`, `windows-support/`, `knowledge-base/`, and `reporting/` — that cross-cutting workflow belongs in one repo.

## Directory Structure: By Function, Not by Tool

**Decision**: Top-level directories are organised by what they do (`incidents/`, `knowledge-base/`, `windows-support/`) rather than by which tool they use (`servicenow/`, `powershell/`, `python/`).

**Why?**

Real support work is organised around the work, not the tools. You don't think "I'm going to use PowerShell now" — you think "I need to fix this printer problem" and then use whatever tools are appropriate. The directory structure reflects that.

The `itsm/` directory is the one exception — it's organised by platform (`servicenow/`, `jira-service-management/`) because ITSM platform configuration is inherently platform-specific. You can't write a generic "ticketing setup" that applies to both.
