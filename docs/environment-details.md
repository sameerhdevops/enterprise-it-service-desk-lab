# Lab Environment Details

## Hardware

| Component | Specification |
|-----------|--------------|
| **Processor** | Intel Core i5-1035G1 (10th Gen Ice Lake) — 4 cores / 8 threads, 1.0 GHz base / 3.6 GHz turbo |
| **Memory** | 16 GB DDR4 |
| **Storage** | 512 GB SSD (D: drive has ~191 GB free) |
| **Form Factor** | Laptop |

This is a consumer-grade laptop, not a lab server. It works fine for what I'm doing — running local tools, Packet Tracer simulations, and lightweight scripting. It would struggle with multiple VMs running simultaneously, which is why I've made certain design choices around that (see below).

## Operating System

| Detail | Value |
|--------|-------|
| **OS** | Windows 11 Enterprise |
| **Build** | 26300 |

Windows 11 Enterprise gives access to features like BitLocker, Group Policy Editor, and Hyper-V that the Home edition doesn't include. That matters for this lab because those are tools you'd encounter in a real corporate environment.

## Installed Software & Tools

### Core Tools

| Tool | Version | Purpose in This Lab |
|------|---------|-------------------|
| **Python** | 3.14.7 | Reporting scripts, data processing. Using stdlib only (csv, json, os, datetime) — no pip dependencies. |
| **Git** | 2.55.0 | Version control for the entire lab. Every change is tracked. |
| **PowerShell** | 5.1 (built-in) | Windows administration, system info gathering, automation scripts |
| **Windows Terminal** | (bundled with Windows 11) | Primary terminal for PowerShell and WSL access |

### ITSM Platforms (Cloud/Web)

| Platform | Access Method |
|----------|--------------|
| **ServiceNow** | Personal Developer Instance (PDI) — free, browser-based, resets periodically |
| **Jira Service Management** | Free tier — up to 3 agents, browser-based |

These aren't installed locally — they're cloud services accessed through the browser. Configuration and evidence (screenshots, export data) are saved in `itsm/`.

### Simulation & Networking

| Tool | Purpose |
|------|---------|
| **Cisco Packet Tracer** | Network topology design and simulation (VLANs, DNS, DHCP, routing basics) |

### Virtualisation (Available but Limited)

| Component | Status | Notes |
|-----------|--------|-------|
| **WSL2** | Installed, Ubuntu distribution | Currently stopped. Available for Linux-side testing if needed. |
| **Docker Desktop** | Installed | Currently stopped. Not actively used in the lab — most work is native Windows. |
| **Hyper-V** | Available via Windows 11 Enterprise | Not currently running VMs (see resource constraints below). |

## Resource Constraints

### Why No Windows Server VM

A proper Active Directory lab ideally runs on a Windows Server VM acting as a domain controller. I haven't set that up for practical reasons:

- **RAM**: With 16 GB total, Windows 11 uses about 4–6 GB at idle. A Windows Server VM needs a minimum of 2 GB (realistically 4 GB to be usable). Running both alongside Packet Tracer, a browser with ServiceNow open, and Python scripts gets tight.
- **Storage**: A Windows Server installation takes 15–20 GB minimum. With 191 GB free that's doable, but adding snapshots and test data eats space fast.
- **CPU**: 4 cores / 8 threads is enough for a VM, but it slows everything else down noticeably when the VM is active.
- **Windows Server licensing**: The evaluation ISO is free for 180 days, but it's another thing to manage and rebuild when it expires.

The trade-off I've made: Active Directory exercises are documented procedurally using local tools (PowerShell AD modules where available, documented procedures for the rest). If I get access to better hardware or a cloud lab environment, I can set up a proper DC. For now, the priority is learning the concepts and workflows, not running a domain.

### What Runs Concurrently

A typical lab session looks like:

- Windows 11 (host OS) — ~5 GB RAM
- Browser with 3–5 tabs (ServiceNow PDI, Jira, reference docs) — ~1.5–2 GB
- VS Code or text editor — ~500 MB
- Packet Tracer (when doing networking modules) — ~500 MB
- Python script execution — negligible
- PowerShell sessions — negligible

That leaves enough headroom to work comfortably without swapping.

## Directory & Storage Layout

The lab lives on the **D: drive** at `D:\Projects\enterprise-it-service-desk-lab`. The D: partition has roughly 191 GB free, which is plenty for documentation, CSVs, Packet Tracer files, and screenshots.

No data is stored in cloud storage or network drives — everything is local and version-controlled through Git.

## Network Access

The lab machine connects to a standard home network. Internet access is needed for:

- ServiceNow PDI (browser)
- Jira Service Management (browser)
- Cisco Packet Tracer (download / occasional updates)
- Git (pushing to remote, if configured)

All network simulation happens inside Packet Tracer — no real network reconfiguration is involved.
