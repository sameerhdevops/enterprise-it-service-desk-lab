# Project Overview

## Background

I'm a recent BSc graduate (Computer Science and Chemistry) looking to break into IT support. During university I completed an internship at Davine Technologies working with AWS cloud services, which gave me a taste of real infrastructure work, but I don't have direct experience in an IT support desk role yet.

The job market for entry-level IT positions — IT Support Engineer (L1), Desktop Support Technician, Service Desk Analyst, Help Desk Technician — consistently asks for hands-on experience with tools and workflows that you can't really learn from just reading about them. Employers want to see that you've actually worked a ticket through ServiceNow, troubleshot a printer issue, or reset a user's AD password.

This project is my way of getting that experience before I have the job.

## What This Project Is

A self-directed lab that simulates working as an L1 IT support engineer at a small company (Nexora Technologies, ~25 employees). I set up real tools, create realistic scenarios, and work through them the way I would on the job — logging tickets, following procedures, documenting resolutions, writing KB articles.

The fictional company gives the work context. Instead of abstract exercises, I'm troubleshooting "Maria from Finance can't print" or "the new hire in Operations needs their accounts set up." That context matters because real support work is always about a specific person with a specific problem.

## Goals

1. **Build practical skills** with the tools and processes that L1 support roles actually use — ServiceNow, Jira Service Management, Active Directory, M365 admin, basic networking
2. **Create documented evidence** of those skills — not certificates, but actual work: tickets I've resolved, KB articles I've written, scripts I've built, network diagrams I've designed
3. **Learn ITIL foundations** by applying them in practice, not just memorizing definitions
4. **Develop troubleshooting methodology** — working through problems systematically rather than guessing
5. **Prepare for interviews** by having real scenarios and solutions I can talk about in detail

## Target Positions

This lab is specifically designed to build skills for:

- **IT Support Engineer (L1)** — The primary target. First line of support, handling user issues, following runbooks, escalating when needed.
- **Desktop Support Technician** — Hands-on hardware and software troubleshooting, workstation setup, peripheral management.
- **Service Desk Analyst** — Ticket management, SLA tracking, user communication, knowledge base maintenance.
- **Help Desk Technician** — Phone/email/portal support, password resets, basic troubleshooting, warm transfers.
- **Junior Systems Administrator** — A stretch goal. Some of the AD and networking work here applies, but this lab focuses on the support side.

## What Each Module Demonstrates

### ITSM Platforms (`itsm/`)
Demonstrates that I can work in industry-standard ticketing systems. Covers ServiceNow PDI configuration (incident forms, categories, assignment groups, SLA definitions, basic workflows) and Jira Service Management (project setup, request types, queues, automation rules). Shows I understand ticket lifecycle, not just how to click buttons.

### Incident Management (`incidents/`)
The core of L1 support. Each scenario is a simulated incident worked from initial report through resolution or escalation. Covers the range of issues L1 typically handles: password lockouts, connectivity problems, application crashes, hardware failures, permission issues. Each incident includes the troubleshooting steps I followed and why.

### Knowledge Base (`knowledge-base/`)
Writing KB articles is a real part of the job that gets overlooked in training. These are articles I've written for common issues — structured for a user audience (self-service) or a support audience (internal procedures). Organized by category: Windows, networking, Microsoft 365, user access.

### Active Directory (`active-directory/`)
User lifecycle management: provisioning new accounts, managing group memberships, handling password resets, disabling accounts for departing employees. Practiced through local simulation since a full AD domain controller needs a Windows Server VM (which is optional in this lab due to hardware constraints — see [environment-details.md](environment-details.md)).

### Networking (`networking/`)
Network fundamentals using Cisco Packet Tracer: building small office topologies, configuring VLANs, setting up DNS and DHCP, understanding subnetting. L1 doesn't usually configure switches, but understanding how the network works makes you much better at diagnosing connectivity issues.

### Windows Support (`windows-support/`)
This is probably the biggest single category of L1 tickets. Covers: OS troubleshooting (boot issues, blue screens, update failures), hardware (disk health, driver conflicts, peripheral issues), software (installation, compatibility, licensing), printers (the eternal nemesis), and remote support tools and procedures.

### Microsoft 365 (`microsoft-365/`)
M365 is everywhere in small to mid-size companies. Covers Outlook troubleshooting (sync issues, shared mailboxes, calendar problems), Teams (audio/video issues, permissions), OneDrive (sync conflicts, storage), and basic admin tasks (license assignment, user management).

### Asset Management (`asset-management/`)
Tracking hardware and software inventory. Uses CSV files (no database needed for a 25-person company) to record asset details, assignments, warranty dates, and lifecycle status. Simple but demonstrates understanding of why asset management matters.

### Operations (`operations/`)
Day-to-day operational procedures: shift handover templates (what's open, what's escalated, what's coming up), daily checklists, escalation procedures. The unglamorous but essential part of support work.

### Reporting (`reporting/`)
Python scripts that generate reports from incident and asset data. Uses only the standard library — csv module for data, string formatting for output. Demonstrates basic automation skills without overcomplicating things.

### Communication (`communication/`)
Professional communication templates: incident notifications, status updates, user instructions, escalation emails. Writing clearly for non-technical users is a skill, and it's one that interviewers ask about.

### ITIL Processes (`itil-processes/`)
ITIL v4 framework concepts applied in the context of Nexora Technologies. Not a study guide — more like "here's how incident management, problem management, change management, and SLA management actually work in a small IT team."

### Interview Preparation (`interview-preparation/`)
Study notes and practiced answers for common IT support interview questions, tied back to specific scenarios in this lab. "Tell me about a time you troubleshot a difficult issue" is a lot easier when you have documented examples to draw from.

## How I'm Using This

This isn't a one-shot project. I'm building it out module by module, treating each one like a work assignment. The git history shows the progression — what I learned, what I revised, how my documentation improved over time.

Each incident scenario gets worked through completely: log the ticket, diagnose the problem, resolve it (or escalate with documented reasoning), update the KB if it's a new issue. That's the cycle, and repeating it builds the habits.
