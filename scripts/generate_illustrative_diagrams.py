#!/usr/bin/env python3
"""
Enterprise IT Service Desk & End-User Support Operations Lab
Illustrative Visual Evidence Generator
Author: Sameer Kulkarni (L1 Support Engineer)
Platform: Python 3 Standard Library Only (No external dependencies)

Generates 7 clean, high-resolution vector SVG diagrams in evidence/illustrative/.
Every diagram is prominently watermarked and labeled as ILLUSTRATIVE / SIMULATED.
"""

import os

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "evidence", "illustrative")

def save_svg(filename, content):
    filepath = os.path.join(OUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[Generated SVG] {filepath}")

# 1. IT Service Desk Architecture
def make_architecture_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 650" width="100%" height="100%" style="background:#0f172a; font-family:system-ui, -apple-system, sans-serif;">
  <defs>
    <linearGradient id="primaryGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3b82f6"/>
      <stop offset="100%" stop-color="#1d4ed8"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
  </defs>

  <!-- Banner -->
  <rect x="0" y="0" width="1000" height="40" fill="#dc2626"/>
  <text x="500" y="25" fill="#ffffff" font-size="14" font-weight="bold" text-anchor="middle" letter-spacing="1">
    [ILLUSTRATIVE / SIMULATED LAB ARTIFACT - NOT A REAL VENDOR SCREENSHOT]
  </text>

  <!-- Title -->
  <text x="500" y="75" fill="#f8fafc" font-size="22" font-weight="bold" text-anchor="middle">
    Nexora Technologies — Enterprise IT Service Desk Architecture
  </text>
  <text x="500" y="98" fill="#94a3b8" font-size="13" text-anchor="middle">
    Multi-Tiered Support Model for ~25 Employees Across HR, Finance, Operations &amp; Engineering
  </text>

  <!-- Employees Section -->
  <rect x="100" y="125" width="800" height="70" rx="8" fill="url(#cardGrad)" stroke="#334155" stroke-width="2"/>
  <text x="120" y="155" fill="#38bdf8" font-size="15" font-weight="bold">EMPLOYEES (Callers &amp; Requesters)</text>
  <text x="120" y="175" fill="#94a3b8" font-size="12">~25 Corporate Users in Bengaluru Office (Human Resources, Finance, Operations, Engineering)</text>
  
  <!-- Channels -->
  <g transform="translate(100, 220)">
    <!-- Portal -->
    <rect x="30" y="0" width="220" height="55" rx="6" fill="#1e293b" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="140" y="25" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle">Self-Service Portal</text>
    <text x="140" y="42" fill="#94a3b8" font-size="11" text-anchor="middle">Service Catalog &amp; Web Intake</text>
    
    <!-- Email -->
    <rect x="290" y="0" width="220" height="55" rx="6" fill="#1e293b" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="400" y="25" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle">Email Ingestion</text>
    <text x="400" y="42" fill="#94a3b8" font-size="11" text-anchor="middle">servicedesk@nexora.local</text>
    
    <!-- Phone -->
    <rect x="550" y="0" width="220" height="55" rx="6" fill="#1e293b" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="660" y="25" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle">Phone / Direct Hotline</text>
    <text x="660" y="42" fill="#94a3b8" font-size="11" text-anchor="middle">Internal Extension 4100</text>
  </g>

  <!-- ITSM Core -->
  <rect x="200" y="305" width="600" height="65" rx="8" fill="url(#primaryGrad)"/>
  <text x="500" y="333" fill="#ffffff" font-size="16" font-weight="bold" text-anchor="middle">IT SERVICE MANAGEMENT (ITSM) PLATFORM</text>
  <text x="500" y="353" fill="#dbeafe" font-size="12" text-anchor="middle">Incident Triage • Priority Matrix (Impact x Urgency) • SLA Clock • CMDB Binding</text>

  <!-- L1 Service Desk Engine -->
  <rect x="80" y="395" width="840" height="135" rx="8" fill="url(#cardGrad)" stroke="#38bdf8" stroke-width="2"/>
  <text x="500" y="422" fill="#38bdf8" font-size="15" font-weight="bold" text-anchor="middle">
    TIER 1 (L1) SERVICE DESK ANALYSTS (First-Contact Resolution)
  </text>
  
  <g transform="translate(100, 435)">
    <!-- Box 1 -->
    <rect x="0" y="0" width="175" height="80" rx="6" fill="#0f172a" stroke="#475569"/>
    <text x="87" y="22" fill="#e2e8f0" font-size="12" font-weight="bold" text-anchor="middle">Windows Support</text>
    <text x="87" y="40" fill="#94a3b8" font-size="10" text-anchor="middle">• Taskmgr / Resmon</text>
    <text x="87" y="55" fill="#94a3b8" font-size="10" text-anchor="middle">• Event Viewer / SFC</text>
    <text x="87" y="70" fill="#94a3b8" font-size="10" text-anchor="middle">• Print Spooler / Drivers</text>

    <!-- Box 2 -->
    <rect x="195" y="0" width="175" height="80" rx="6" fill="#0f172a" stroke="#475569"/>
    <text x="282" y="22" fill="#e2e8f0" font-size="12" font-weight="bold" text-anchor="middle">Network Triage</text>
    <text x="282" y="40" fill="#94a3b8" font-size="10" text-anchor="middle">• IP / DHCP (APIPA)</text>
    <text x="282" y="55" fill="#94a3b8" font-size="10" text-anchor="middle">• Ping / Gateway / Tracert</text>
    <text x="282" y="70" fill="#94a3b8" font-size="10" text-anchor="middle">• DNS (nslookup) / VPN</text>

    <!-- Box 3 -->
    <rect x="390" y="0" width="175" height="80" rx="6" fill="#0f172a" stroke="#475569"/>
    <text x="477" y="22" fill="#e2e8f0" font-size="12" font-weight="bold" text-anchor="middle">Identity &amp; Access</text>
    <text x="477" y="40" fill="#94a3b8" font-size="10" text-anchor="middle">• AD Account Unlock</text>
    <text x="477" y="55" fill="#94a3b8" font-size="10" text-anchor="middle">• Identity Verify Password</text>
    <text x="477" y="70" fill="#94a3b8" font-size="10" text-anchor="middle">• AGDLP Group Perms</text>

    <!-- Box 4 -->
    <rect x="585" y="0" width="215" height="80" rx="6" fill="#0f172a" stroke="#475569"/>
    <text x="692" y="22" fill="#e2e8f0" font-size="12" font-weight="bold" text-anchor="middle">Microsoft 365 Client</text>
    <text x="692" y="40" fill="#94a3b8" font-size="10" text-anchor="middle">• Outlook Profile / OST</text>
    <text x="692" y="55" fill="#94a3b8" font-size="10" text-anchor="middle">• Teams Cache Purge</text>
    <text x="692" y="70" fill="#94a3b8" font-size="10" text-anchor="middle">• OneDrive Files On-Demand</text>
  </g>

  <!-- Output outcomes -->
  <g transform="translate(100, 555)">
    <rect x="40" y="0" width="340" height="65" rx="6" fill="#065f46" stroke="#10b981" stroke-width="1.5"/>
    <text x="210" y="25" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle">RESOLVED (First Contact / L1)</text>
    <text x="210" y="43" fill="#a7f3d0" font-size="11" text-anchor="middle">Verified with User • Resolution Code • KB Linked</text>

    <rect x="420" y="0" width="340" height="65" rx="6" fill="#78350f" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="590" y="25" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle">ESCALATED (&gt;30 min / Privilege Bound)</text>
    <text x="590" y="43" fill="#fde68a" font-size="11" text-anchor="middle">L2 Desktop • L2 Network • L3 Infra • Hardware RMA</text>
  </g>
</svg>"""

# 2. Incident Lifecycle Flow
def make_incident_lifecycle_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 520" width="100%" height="100%" style="background:#0f172a; font-family:system-ui, -apple-system, sans-serif;">
  <!-- Watermark Banner -->
  <rect x="0" y="0" width="1000" height="35" fill="#dc2626"/>
  <text x="500" y="23" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle" letter-spacing="1">
    [ILLUSTRATIVE / SIMULATED LAB ARTIFACT - ITIL 4 INCIDENT LIFECYCLE MODEL]
  </text>

  <text x="500" y="70" fill="#f8fafc" font-size="20" font-weight="bold" text-anchor="middle">
    ServiceNow &amp; JSM Incident State Transition Engine
  </text>

  <!-- States -->
  <!-- New -->
  <g transform="translate(50, 120)">
    <rect x="0" y="0" width="140" height="80" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
    <circle cx="70" cy="25" r="12" fill="#0284c7"/>
    <text x="70" y="29" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">1</text>
    <text x="70" y="55" fill="#f8fafc" font-size="14" font-weight="bold" text-anchor="middle">NEW</text>
    <text x="70" y="70" fill="#94a3b8" font-size="10" text-anchor="middle">Triage &amp; Priority</text>
  </g>

  <!-- In Progress -->
  <g transform="translate(260, 120)">
    <rect x="0" y="0" width="160" height="80" rx="8" fill="#1e293b" stroke="#3b82f6" stroke-width="2"/>
    <circle cx="80" cy="25" r="12" fill="#2563eb"/>
    <text x="80" y="29" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">2</text>
    <text x="80" y="55" fill="#f8fafc" font-size="14" font-weight="bold" text-anchor="middle">IN PROGRESS</text>
    <text x="80" y="70" fill="#94a3b8" font-size="10" text-anchor="middle">Investigation / Work</text>
  </g>

  <!-- On Hold -->
  <g transform="translate(500, 120)">
    <rect x="0" y="0" width="160" height="80" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
    <circle cx="80" cy="25" r="12" fill="#d97706"/>
    <text x="80" y="29" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">3</text>
    <text x="80" y="55" fill="#f8fafc" font-size="14" font-weight="bold" text-anchor="middle">ON HOLD</text>
    <text x="80" y="70" fill="#fbbf24" font-size="10" text-anchor="middle">SLA Timer Paused</text>
  </g>

  <!-- Resolved -->
  <g transform="translate(740, 120)">
    <rect x="0" y="0" width="160" height="80" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
    <circle cx="80" cy="25" r="12" fill="#059669"/>
    <text x="80" y="29" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">6</text>
    <text x="80" y="55" fill="#f8fafc" font-size="14" font-weight="bold" text-anchor="middle">RESOLVED</text>
    <text x="80" y="70" fill="#a7f3d0" font-size="10" text-anchor="middle">Resolution Notes</text>
  </g>

  <!-- Closed -->
  <g transform="translate(740, 270)">
    <rect x="0" y="0" width="160" height="80" rx="8" fill="#1e293b" stroke="#64748b" stroke-width="2"/>
    <circle cx="80" cy="25" r="12" fill="#475569"/>
    <text x="80" y="29" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">7</text>
    <text x="80" y="55" fill="#f8fafc" font-size="14" font-weight="bold" text-anchor="middle">CLOSED</text>
    <text x="80" y="70" fill="#cbd5e1" font-size="10" text-anchor="middle">Read-Only Audit State</text>
  </g>

  <!-- Connecting Arrows -->
  <line x1="190" y1="160" x2="260" y2="160" stroke="#38bdf8" stroke-width="2"/>
  <line x1="420" y1="160" x2="500" y2="160" stroke="#f59e0b" stroke-width="2"/>
  <line x1="660" y1="160" x2="740" y2="160" stroke="#10b981" stroke-width="2"/>
  <line x1="820" y1="200" x2="820" y2="270" stroke="#64748b" stroke-width="2"/>

  <!-- Description Box -->
  <rect x="50" y="380" width="850" height="110" rx="8" fill="#1e293b" stroke="#334155"/>
  <text x="70" y="408" fill="#38bdf8" font-size="13" font-weight="bold">KEY OPERATIONAL RULES AT L1:</text>
  <text x="70" y="430" fill="#e2e8f0" font-size="11">• Customer Comments: Visible to caller via email/portal (updates, appointment times, instructions).</text>
  <text x="70" y="450" fill="#e2e8f0" font-size="11">• Work Notes: Strictly internal to IT support staff (diagnostics, command output, IP addresses, escalation context).</text>
  <text x="70" y="470" fill="#e2e8f0" font-size="11">• On Hold Reasons: Awaiting Caller Info (pauses SLA) | Awaiting Vendor RMA (pauses SLA) | Awaiting Change Window.</text>
</svg>"""

# 3. Escalation Workflow
def make_escalation_workflow_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 550" width="100%" height="100%" style="background:#0f172a; font-family:system-ui, -apple-system, sans-serif;">
  <rect x="0" y="0" width="1000" height="35" fill="#dc2626"/>
  <text x="500" y="23" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle" letter-spacing="1">
    [ILLUSTRATIVE / SIMULATED LAB ARTIFACT - ESCALATION MATRIX]
  </text>
  <text x="500" y="70" fill="#f8fafc" font-size="20" font-weight="bold" text-anchor="middle">
    Service Desk Functional &amp; Hierarchical Escalation Matrix
  </text>

  <!-- L1 Box -->
  <rect x="80" y="110" width="240" height="200" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
  <text x="200" y="140" fill="#38bdf8" font-size="16" font-weight="bold" text-anchor="middle">L1 Service Desk</text>
  <text x="200" y="165" fill="#94a3b8" font-size="11" text-anchor="middle">First Contact Intake &amp; Triage</text>
  <text x="100" y="195" fill="#cbd5e1" font-size="11">• 30-Minute Investigation Limit</text>
  <text x="100" y="215" fill="#cbd5e1" font-size="11">• Desktop Client Diagnostics</text>
  <text x="100" y="235" fill="#cbd5e1" font-size="11">• Password Resets &amp; Unlocks</text>
  <text x="100" y="255" fill="#cbd5e1" font-size="11">• Standard Peripheral Triage</text>
  <text x="100" y="275" fill="#cbd5e1" font-size="11">• SBAR Handover Documentation</text>

  <!-- Escalation Criteria Arrow -->
  <line x1="320" y1="210" x2="420" y2="210" stroke="#f59e0b" stroke-width="3"/>
  <text x="370" y="195" fill="#f59e0b" font-size="11" font-weight="bold" text-anchor="middle">Time &gt;30m or</text>
  <text x="370" y="235" fill="#f59e0b" font-size="11" font-weight="bold" text-anchor="middle">Privilege Block</text>

  <!-- L2 Tier Box -->
  <rect x="420" y="110" width="260" height="200" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
  <text x="550" y="140" fill="#f59e0b" font-size="16" font-weight="bold" text-anchor="middle">L2 Technical Support</text>
  <text x="440" y="175" fill="#e2e8f0" font-size="12" font-weight="bold">L2 Desktop Support:</text>
  <text x="440" y="195" fill="#94a3b8" font-size="11">• Physical hardware teardown &amp; RMA</text>
  <text x="440" y="215" fill="#94a3b8" font-size="11">• OS Re-imaging &amp; BitLocker recovery</text>
  <text x="440" y="245" fill="#e2e8f0" font-size="12" font-weight="bold">L2 Network Support:</text>
  <text x="440" y="265" fill="#94a3b8" font-size="11">• Switch port VLAN assignments</text>
  <text x="440" y="285" fill="#94a3b8" font-size="11">• Firewall MTU policies &amp; VPN config</text>

  <!-- L3 Tier Box -->
  <rect x="730" y="110" width="200" height="200" rx="8" fill="#1e293b" stroke="#ef4444" stroke-width="2"/>
  <text x="830" y="140" fill="#ef4444" font-size="16" font-weight="bold" text-anchor="middle">L3 / Infrastructure</text>
  <text x="745" y="175" fill="#cbd5e1" font-size="11">• Domain Controllers (FSMO)</text>
  <text x="745" y="195" fill="#cbd5e1" font-size="11">• Hypervisors &amp; SAN Storage</text>
  <text x="745" y="215" fill="#cbd5e1" font-size="11">• Exchange Online Tenant</text>
  <text x="745" y="235" fill="#cbd5e1" font-size="11">• Third-Party Vendors (SAP, HP)</text>
  <text x="745" y="255" fill="#cbd5e1" font-size="11">• Emergency Changes (ECAB)</text>

  <!-- Hierarchical Row -->
  <rect x="80" y="340" width="850" height="150" rx="8" fill="#1e293b" stroke="#8b5cf6" stroke-width="1.5"/>
  <text x="110" y="375" fill="#a78bfa" font-size="15" font-weight="bold">HIERARCHICAL (MANAGEMENT) ESCALATION PATH</text>
  <text x="110" y="405" fill="#e2e8f0" font-size="12">• P1 Major Incident Trigger: Immediate notification to IT Service Desk Lead within 15 minutes of occurrence.</text>
  <text x="110" y="430" fill="#e2e8f0" font-size="12">• SLA At-Risk Warning: Escalation when an active P2 incident reaches 75% of resolution SLA target without clear root cause.</text>
  <text x="110" y="455" fill="#e2e8f0" font-size="12">• Customer Dissatisfaction / Executive Escalation: Immediate routing to Service Desk Lead for mediation.</text>
</svg>"""

# 4. Network Topology
def make_network_topology_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 620" width="100%" height="100%" style="background:#0f172a; font-family:system-ui, -apple-system, sans-serif;">
  <rect x="0" y="0" width="1000" height="35" fill="#dc2626"/>
  <text x="500" y="23" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle" letter-spacing="1">
    [ILLUSTRATIVE / SIMULATED LAB ARTIFACT - NETWORK TOPOLOGY DESIGN]
  </text>
  <text x="500" y="70" fill="#f8fafc" font-size="20" font-weight="bold" text-anchor="middle">
    Nexora Technologies — 2-VLAN Office Network Infrastructure
  </text>

  <!-- Internet & Router -->
  <circle cx="500" cy="120" r="30" fill="#0284c7"/>
  <text x="500" y="125" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">INTERNET</text>

  <!-- Router -->
  <rect x="420" y="180" width="160" height="60" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
  <text x="500" y="205" fill="#38bdf8" font-size="13" font-weight="bold" text-anchor="middle">NEX-RTR01 (Cisco 2911)</text>
  <text x="500" y="225" fill="#94a3b8" font-size="10" text-anchor="middle">Default Gateway • 802.1Q ROAS</text>

  <!-- Trunk Link -->
  <line x1="500" y1="240" x2="500" y2="290" stroke="#f59e0b" stroke-width="3"/>
  <text x="535" y="270" fill="#f59e0b" font-size="10" font-weight="bold">802.1Q Trunk</text>

  <!-- Switch -->
  <rect x="420" y="290" width="160" height="60" rx="6" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
  <text x="500" y="315" fill="#f59e0b" font-size="13" font-weight="bold" text-anchor="middle">SW-CORE-01 (Cisco 2960)</text>
  <text x="500" y="335" fill="#94a3b8" font-size="10" text-anchor="middle">24-Port Managed Core Switch</text>

  <!-- Left: VLAN 10 (Corporate Users) -->
  <rect x="80" y="390" width="380" height="190" rx="8" fill="#1e293b" stroke="#3b82f6" stroke-width="2"/>
  <text x="270" y="420" fill="#38bdf8" font-size="15" font-weight="bold" text-anchor="middle">VLAN 10: Corporate Users</text>
  <text x="270" y="440" fill="#94a3b8" font-size="11" text-anchor="middle">Subnet: 192.168.10.0/24 | Gateway: 192.168.10.1</text>
  <text x="100" y="475" fill="#cbd5e1" font-size="11">• PC-HR01 (192.168.10.11) — HR Workstation</text>
  <text x="100" y="495" fill="#cbd5e1" font-size="11">• PC-FIN01 (192.168.10.12) — Finance Workstation</text>
  <text x="100" y="515" fill="#cbd5e1" font-size="11">• PRN01 (192.168.10.25) — HP LaserJet MFD</text>
  <text x="100" y="535" fill="#cbd5e1" font-size="11">• DHCP Dynamic Pool Range: .100 to .200</text>
  <text x="100" y="555" fill="#cbd5e1" font-size="11">• Relay Agent: ip helper-address 192.168.20.10</text>

  <!-- Right: VLAN 20 (Server Farm) -->
  <rect x="540" y="390" width="380" height="190" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
  <text x="730" y="420" fill="#10b981" font-size="15" font-weight="bold" text-anchor="middle">VLAN 20: Server Farm</text>
  <text x="730" y="440" fill="#94a3b8" font-size="11" text-anchor="middle">Subnet: 192.168.20.0/24 | Gateway: 192.168.20.1</text>
  <text x="560" y="475" fill="#cbd5e1" font-size="11">• NEX-DC01 (192.168.20.10) — Primary Domain Controller</text>
  <text x="560" y="495" fill="#cbd5e1" font-size="11">• Services on DC: Active Directory, DNS, DHCP Server</text>
  <text x="560" y="515" fill="#cbd5e1" font-size="11">• NEX-FS01 (192.168.20.15) — Departmental SMB File Server</text>
  <text x="560" y="535" fill="#cbd5e1" font-size="11">• NEX-APP01 (192.168.20.50) — SAP ERP / Intranet Portal</text>
  <text x="560" y="555" fill="#cbd5e1" font-size="11">• Addressing: 100% Statically Configured</text>
</svg>"""

# 5. Windows Troubleshooting Flow
def make_windows_troubleshooting_flow_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 580" width="100%" height="100%" style="background:#0f172a; font-family:system-ui, -apple-system, sans-serif;">
  <rect x="0" y="0" width="1000" height="35" fill="#dc2626"/>
  <text x="500" y="23" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle" letter-spacing="1">
    [ILLUSTRATIVE / SIMULATED LAB ARTIFACT - WINDOWS L1 TRIAGE WORKFLOW]
  </text>
  <text x="500" y="70" fill="#f8fafc" font-size="20" font-weight="bold" text-anchor="middle">
    Windows 11 Slow Performance &amp; Resource Exhaustion Triage
  </text>

  <!-- Step 1 -->
  <rect x="350" y="100" width="300" height="60" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
  <text x="500" y="125" fill="#38bdf8" font-size="14" font-weight="bold" text-anchor="middle">STEP 1: Check System Uptime</text>
  <text x="500" y="145" fill="#94a3b8" font-size="11" text-anchor="middle">Task Manager &gt; Performance &gt; CPU (Up time)</text>

  <line x1="500" y1="160" x2="500" y2="200" stroke="#94a3b8" stroke-width="2"/>

  <!-- Decision 1 -->
  <polygon points="500,200 620,250 500,300 380,250" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
  <text x="500" y="245" fill="#f59e0b" font-size="12" font-weight="bold" text-anchor="middle">Is Uptime &gt; 14 Days?</text>
  <text x="500" y="260" fill="#94a3b8" font-size="10" text-anchor="middle">(Fast Startup / Sleep)</text>

  <!-- Branch Yes -->
  <line x1="620" y1="250" x2="740" y2="250" stroke="#10b981" stroke-width="2"/>
  <text x="670" y="240" fill="#10b981" font-size="11" font-weight="bold">YES</text>
  <rect x="740" y="220" width="220" height="60" rx="6" fill="#065f46" stroke="#10b981"/>
  <text x="850" y="245" fill="#ffffff" font-size="12" font-weight="bold" text-anchor="middle">Execute Clean Reboot</text>
  <text x="850" y="263" fill="#a7f3d0" font-size="10" text-anchor="middle">shutdown /r /t 0 (Reset Session 0)</text>

  <!-- Branch No -->
  <line x1="500" y1="300" x2="500" y2="340" stroke="#ef4444" stroke-width="2"/>
  <text x="515" y="325" fill="#ef4444" font-size="11" font-weight="bold">NO</text>

  <!-- Step 2 -->
  <rect x="350" y="340" width="300" height="60" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
  <text x="500" y="365" fill="#38bdf8" font-size="14" font-weight="bold" text-anchor="middle">STEP 2: Inspect Resource Graphs</text>
  <text x="500" y="385" fill="#94a3b8" font-size="11" text-anchor="middle">Identify bottleneck: CPU, Memory, or Disk at 100%</text>

  <!-- Three Columns of Outcomes -->
  <g transform="translate(60, 430)">
    <!-- High CPU -->
    <rect x="0" y="0" width="270" height="120" rx="6" fill="#1e293b" stroke="#334155"/>
    <text x="135" y="25" fill="#ef4444" font-size="13" font-weight="bold" text-anchor="middle">High CPU (&gt;85%)</text>
    <text x="15" y="50" fill="#94a3b8" font-size="11">• If User App: End task</text>
    <text x="15" y="70" fill="#94a3b8" font-size="11">• If TiWorker: Allow update finish</text>
    <text x="15" y="90" fill="#94a3b8" font-size="11">• If System (PID 4): Hardware DPC</text>
    <text x="15" y="110" fill="#94a3b8" font-size="11">• If Throttling: Inspect vents &amp; fan</text>

    <!-- High Memory -->
    <rect x="310" y="0" width="270" height="120" rx="6" fill="#1e293b" stroke="#334155"/>
    <text x="445" y="25" fill="#f59e0b" font-size="13" font-weight="bold" text-anchor="middle">High Memory (&gt;90%)</text>
    <text x="325" y="50" fill="#94a3b8" font-size="11">• Purge Teams/browser cache</text>
    <text x="325" y="70" fill="#94a3b8" font-size="11">• Enable auto virtual memory</text>
    <text x="325" y="90" fill="#94a3b8" font-size="11">• Inspect Non-Paged Pool leak</text>
    <text x="325" y="110" fill="#94a3b8" font-size="11">• Update Wi-Fi/chipset driver</text>

    <!-- High Disk -->
    <rect x="620" y="0" width="270" height="120" rx="6" fill="#1e293b" stroke="#334155"/>
    <text x="755" y="25" fill="#3b82f6" font-size="13" font-weight="bold" text-anchor="middle">High Disk I/O (100%)</text>
    <text x="635" y="50" fill="#94a3b8" font-size="11">• Run cleanmgr /d c: (Free space)</text>
    <text x="635" y="70" fill="#94a3b8" font-size="11">• Pause Windows Search Indexer</text>
    <text x="635" y="90" fill="#94a3b8" font-size="11">• Run sfc /scannow repair</text>
    <text x="635" y="110" fill="#94a3b8" font-size="11">• SMART error check (Escalate L2)</text>
  </g>
</svg>"""

# 6. Asset Management Lifecycle
def make_asset_lifecycle_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 480" width="100%" height="100%" style="background:#0f172a; font-family:system-ui, -apple-system, sans-serif;">
  <rect x="0" y="0" width="1000" height="35" fill="#dc2626"/>
  <text x="500" y="23" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle" letter-spacing="1">
    [ILLUSTRATIVE / SIMULATED LAB ARTIFACT - IT ASSET MANAGEMENT (ITAM) MODEL]
  </text>
  <text x="500" y="70" fill="#f8fafc" font-size="20" font-weight="bold" text-anchor="middle">
    Nexora Technologies — 5-Stage Hardware Asset Lifecycle
  </text>

  <!-- 5 Circular Stages -->
  <g transform="translate(60, 120)">
    <!-- Stage 1 -->
    <rect x="0" y="0" width="160" height="140" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
    <text x="80" y="30" fill="#38bdf8" font-size="13" font-weight="bold" text-anchor="middle">1. PROCUREMENT</text>
    <text x="15" y="60" fill="#94a3b8" font-size="11">• Purchase Requisition</text>
    <text x="15" y="80" fill="#94a3b8" font-size="11">• Vendor PO (Dell/HP)</text>
    <text x="15" y="100" fill="#94a3b8" font-size="11">• 3-Year ProSupport</text>
    <text x="15" y="120" fill="#94a3b8" font-size="11">• Warranty Registration</text>

    <!-- Stage 2 -->
    <rect x="180" y="0" width="160" height="140" rx="8" fill="#1e293b" stroke="#3b82f6" stroke-width="2"/>
    <text x="260" y="30" fill="#3b82f6" font-size="13" font-weight="bold" text-anchor="middle">2. INGESTION</text>
    <text x="195" y="60" fill="#94a3b8" font-size="11">• Barcode Asset Tagging</text>
    <text x="195" y="80" fill="#94a3b8" font-size="11">• Format: NXT-AST-0XX</text>
    <text x="195" y="100" fill="#94a3b8" font-size="11">• Enter Serial in CMDB</text>
    <text x="195" y="120" fill="#94a3b8" font-size="11">• Status: In Stock</text>

    <!-- Stage 3 -->
    <rect x="360" y="0" width="160" height="140" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
    <text x="440" y="30" fill="#10b981" font-size="13" font-weight="bold" text-anchor="middle">3. DEPLOYED</text>
    <text x="375" y="60" fill="#94a3b8" font-size="11">• Windows 11 Image</text>
    <text x="375" y="80" fill="#94a3b8" font-size="11">• BitLocker Escrow</text>
    <text x="375" y="100" fill="#94a3b8" font-size="11">• Assigned to Employee</text>
    <text x="375" y="120" fill="#94a3b8" font-size="11">• Status: Active</text>

    <!-- Stage 4 -->
    <rect x="540" y="0" width="160" height="140" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
    <text x="620" y="30" fill="#f59e0b" font-size="13" font-weight="bold" text-anchor="middle">4. MAINTENANCE</text>
    <text x="555" y="60" fill="#94a3b8" font-size="11">• Hardware RMA Repair</text>
    <text x="555" y="80" fill="#94a3b8" font-size="11">• Loaner Spare Issued</text>
    <text x="555" y="100" fill="#94a3b8" font-size="11">• Battery Replacement</text>
    <text x="555" y="120" fill="#94a3b8" font-size="11">• Status: In Repair</text>

    <!-- Stage 5 -->
    <rect x="720" y="0" width="160" height="140" rx="8" fill="#1e293b" stroke="#64748b" stroke-width="2"/>
    <text x="800" y="30" fill="#cbd5e1" font-size="13" font-weight="bold" text-anchor="middle">5. RETIREMENT</text>
    <text x="735" y="60" fill="#94a3b8" font-size="11">• DoD 5220 Disk Wipe</text>
    <text x="735" y="80" fill="#94a3b8" font-size="11">• AD &amp; Intune Deregister</text>
    <text x="735" y="100" fill="#94a3b8" font-size="11">• E-Waste Recycling</text>
    <text x="735" y="120" fill="#94a3b8" font-size="11">• Status: Decommissioned</text>
  </g>

  <!-- Bottom Info Box -->
  <rect x="60" y="300" width="880" height="130" rx="8" fill="#1e293b" stroke="#334155"/>
  <text x="80" y="330" fill="#38bdf8" font-size="13" font-weight="bold">ITAM vs. CMDB DISTINCTION (KEY INTERVIEW CONCEPT):</text>
  <text x="80" y="355" fill="#e2e8f0" font-size="11">• IT Asset Management (ITAM): Tracks financial &amp; contractual properties (Purchase price, depreciation, serial number, warranty expiry date).</text>
  <text x="80" y="380" fill="#e2e8f0" font-size="11">• Configuration Management (CMDB): Tracks operational dependencies and relationships (Which switch port does this server connect to? Which ERP application relies on this database?).</text>
  <text x="80" y="405" fill="#e2e8f0" font-size="11">• In this lab: 25 hardware assets tracked in asset-inventory.csv across laptops, desktops, network MFD printers, and switches.</text>
</svg>"""

# 7. SLA Reporting Dashboard Mockup
def make_sla_dashboard_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 600" width="100%" height="100%" style="background:#0f172a; font-family:system-ui, -apple-system, sans-serif;">
  <rect x="0" y="0" width="1000" height="35" fill="#dc2626"/>
  <text x="500" y="23" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle" letter-spacing="1">
    [ILLUSTRATIVE / SIMULATED LAB ARTIFACT - SERVICE DESK MIS DASHBOARD]
  </text>
  <text x="500" y="70" fill="#f8fafc" font-size="20" font-weight="bold" text-anchor="middle">
    Service Desk Operational Performance &amp; SLA Dashboard
  </text>
  <text x="500" y="92" fill="#94a3b8" font-size="12" text-anchor="middle">
    Simulated Metrics Generated from incidents/incident-register.csv (November 2024 Consolidated)
  </text>

  <!-- 4 KPI Cards -->
  <g transform="translate(60, 115)">
    <!-- Total Logged -->
    <rect x="0" y="0" width="200" height="90" rx="8" fill="#1e293b" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="20" y="30" fill="#94a3b8" font-size="12">Total Interactions</text>
    <text x="20" y="65" fill="#ffffff" font-size="28" font-weight="bold">28</text>
    <text x="20" y="80" fill="#38bdf8" font-size="10">20 Incidents + 8 Requests</text>

    <!-- Resolved Rate -->
    <rect x="225" y="0" width="200" height="90" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="1.5"/>
    <text x="245" y="30" fill="#94a3b8" font-size="12">First Contact Resolution</text>
    <text x="245" y="65" fill="#10b981" font-size="28" font-weight="bold">85.0%</text>
    <text x="245" y="80" fill="#a7f3d0" font-size="10">17 of 20 resolved at L1</text>

    <!-- MTTR -->
    <rect x="450" y="0" width="200" height="90" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="470" y="30" fill="#94a3b8" font-size="12">Mean Time to Resolve</text>
    <text x="470" y="65" fill="#f59e0b" font-size="28" font-weight="bold">11.51h</text>
    <text x="470" y="80" fill="#fde68a" font-size="10">Across 17 resolved incidents</text>

    <!-- SLA Compliance -->
    <rect x="675" y="0" width="205" height="90" rx="8" fill="#1e293b" stroke="#8b5cf6" stroke-width="1.5"/>
    <text x="695" y="30" fill="#94a3b8" font-size="12">Resolved SLA Rate</text>
    <text x="695" y="65" fill="#8b5cf6" font-size="28" font-weight="bold">100.0%</text>
    <text x="695" y="80" fill="#ddd6fe" font-size="10">17 of 17 within target</text>
  </g>

  <!-- SLA Breakdown Table Mockup -->
  <rect x="60" y="235" width="880" height="310" rx="8" fill="#1e293b" stroke="#334155"/>
  <text x="85" y="270" fill="#f8fafc" font-size="15" font-weight="bold">SLA PERFORMANCE BREAKDOWN BY PRIORITY TIER</text>

  <!-- Table Header -->
  <rect x="85" y="290" width="830" height="30" fill="#0f172a"/>
  <text x="100" y="310" fill="#94a3b8" font-size="11" font-weight="bold">PRIORITY</text>
  <text x="220" y="310" fill="#94a3b8" font-size="11" font-weight="bold">SLA TARGET</text>
  <text x="360" y="310" fill="#94a3b8" font-size="11" font-weight="bold">TOTAL</text>
  <text x="480" y="310" fill="#94a3b8" font-size="11" font-weight="bold">RESOLVED MET</text>
  <text x="630" y="310" fill="#94a3b8" font-size="11" font-weight="bold">ACTIVE BREACH</text>
  <text x="790" y="310" fill="#94a3b8" font-size="11" font-weight="bold">COMPLIANCE</text>

  <!-- Row P1 -->
  <text x="100" y="345" fill="#ef4444" font-size="12" font-weight="bold">P1 - Critical</text>
  <text x="220" y="345" fill="#cbd5e1" font-size="12">4 Hours</text>
  <text x="360" y="345" fill="#cbd5e1" font-size="12">3</text>
  <text x="480" y="345" fill="#10b981" font-size="12">2 (66.7%)</text>
  <text x="630" y="345" fill="#ef4444" font-size="12">1 (INC0010)</text>
  <text x="790" y="345" fill="#ef4444" font-size="12" font-weight="bold">66.7%</text>

  <!-- Row P2 -->
  <text x="100" y="385" fill="#f59e0b" font-size="12" font-weight="bold">P2 - High</text>
  <text x="220" y="385" fill="#cbd5e1" font-size="12">8 Business Hours</text>
  <text x="360" y="385" fill="#cbd5e1" font-size="12">5</text>
  <text x="480" y="385" fill="#10b981" font-size="12">3 (60.0%)</text>
  <text x="630" y="385" fill="#f59e0b" font-size="12">2 (INC0004, 19)</text>
  <text x="790" y="385" fill="#f59e0b" font-size="12" font-weight="bold">60.0%</text>

  <!-- Row P3 -->
  <text x="100" y="425" fill="#3b82f6" font-size="12" font-weight="bold">P3 - Medium</text>
  <text x="220" y="425" fill="#cbd5e1" font-size="12">3 Business Days</text>
  <text x="360" y="425" fill="#cbd5e1" font-size="12">7</text>
  <text x="480" y="425" fill="#10b981" font-size="12">7 (100.0%)</text>
  <text x="630" y="425" fill="#cbd5e1" font-size="12">0</text>
  <text x="790" y="425" fill="#10b981" font-size="12" font-weight="bold">100.0%</text>

  <!-- Row P4 -->
  <text x="100" y="465" fill="#64748b" font-size="12" font-weight="bold">P4 - Low</text>
  <text x="220" y="465" fill="#cbd5e1" font-size="12">5 Business Days</text>
  <text x="360" y="465" fill="#cbd5e1" font-size="12">5</text>
  <text x="480" y="465" fill="#10b981" font-size="12">5 (100.0%)</text>
  <text x="630" y="465" fill="#cbd5e1" font-size="12">0</text>
  <text x="790" y="465" fill="#10b981" font-size="12" font-weight="bold">100.0%</text>

  <!-- Overall -->
  <line x1="85" y1="485" x2="915" y2="485" stroke="#475569" stroke-width="1"/>
  <text x="100" y="515" fill="#ffffff" font-size="13" font-weight="bold">OVERALL TOTAL</text>
  <text x="220" y="515" fill="#ffffff" font-size="13">Portfolio</text>
  <text x="360" y="515" fill="#ffffff" font-size="13" font-weight="bold">20</text>
  <text x="480" y="515" fill="#10b981" font-size="13" font-weight="bold">17 Met</text>
  <text x="630" y="515" fill="#ef4444" font-size="13" font-weight="bold">3 Breached</text>
  <text x="790" y="515" fill="#38bdf8" font-size="14" font-weight="bold">85.0%</text>
</svg>"""

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    save_svg("it-service-desk-architecture.svg", make_architecture_svg())
    save_svg("incident-lifecycle-flow.svg", make_incident_lifecycle_svg())
    save_svg("ticket-escalation-workflow.svg", make_escalation_workflow_svg())
    save_svg("network-topology-diagram.svg", make_network_topology_svg())
    save_svg("windows-troubleshooting-flow.svg", make_windows_troubleshooting_flow_svg())
    save_svg("asset-management-lifecycle.svg", make_asset_lifecycle_svg())
    save_svg("sla-reporting-dashboard.svg", make_sla_dashboard_svg())
    print("\nAll 7 illustrative SVG diagrams generated successfully.")

if __name__ == "__main__":
    main()
