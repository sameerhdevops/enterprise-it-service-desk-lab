#!/usr/bin/env python3
"""
Nexora Technologies - Operational IT Service Desk Platform
Provides an interactive Customer Portal and L1 Agent Console with
real ticket lifecycle workflows, Impact x Urgency priority matrix,
elapsed-clock-hour SLA timers, and integrated Knowledge Base search.
Zero external dependencies (Python standard library only).
"""

import http.server
import socketserver
import sqlite3
import json
import urllib.parse
import os
import sys
from datetime import datetime, timezone, timedelta

PORT = 8080
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nexora_servicedesk.db")

SLA_POLICY = {
    "P1": {"name": "Critical", "hours": 4, "desc": "4 Elapsed Clock Hours (24x7)"},
    "P2": {"name": "High", "hours": 8, "desc": "8 Elapsed Clock Hours"},
    "P3": {"name": "Medium", "hours": 72, "desc": "72 Elapsed Clock Hours (3 Days)"},
    "P4": {"name": "Low", "hours": 120, "desc": "120 Elapsed Clock Hours (5 Days)"}
}

PRIORITY_MATRIX = {
    ("High", "High"): "P1",
    ("High", "Medium"): "P2",
    ("High", "Low"): "P3",
    ("Medium", "High"): "P2",
    ("Medium", "Medium"): "P3",
    ("Medium", "Low"): "P4",
    ("Low", "High"): "P3",
    ("Low", "Medium"): "P4",
    ("Low", "Low"): "P4"
}

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT UNIQUE,
        title TEXT NOT NULL,
        request_type TEXT NOT NULL,
        caller_name TEXT NOT NULL,
        caller_email TEXT NOT NULL,
        department TEXT NOT NULL,
        impact TEXT NOT NULL,
        urgency TEXT NOT NULL,
        priority TEXT NOT NULL,
        status TEXT NOT NULL,
        assigned_to TEXT,
        assignment_group TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        resolved_at TEXT,
        sla_target_hours REAL NOT NULL,
        sla_breached INTEGER DEFAULT 0,
        description TEXT,
        resolution_notes TEXT
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS ticket_activity (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_key TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        author TEXT NOT NULL,
        activity_type TEXT NOT NULL, -- 'STATUS_CHANGE', 'WORK_NOTE', 'CUSTOMER_COMMENT'
        message TEXT NOT NULL
    )
    """)
    conn.commit()
    
    # Check if seed data exists
    c.execute("SELECT COUNT(*) FROM tickets")
    count = c.fetchone()[0]
    if count == 0:
        seed_tickets(conn)
    conn.close()

def seed_tickets(conn):
    c = conn.cursor()
    base_time = datetime(2024, 11, 10, 9, 0, 0)
    
    sample_tickets = [
        ("NEX-101", "Locked out of Windows account after password change", "Password Reset / Account Unlock", "Kavitha Murthy", "kavitha.murthy@nexora.com", "HR", "Medium", "High", "P2", "Resolved", "Alex Chen", "L1 Service Desk", 0.5, "Account unlocked and bad password cache flushed on smartphone."),
        ("NEX-102", "Outlook fails to connect - stuck on 'Loading Profile'", "Microsoft 365 Client Issue", "Deepak Rao", "deepak.rao@nexora.com", "Finance", "Medium", "Medium", "P3", "Resolved", "Priya Sharma", "L1 Service Desk", 2.0, "Recreated corrupt Outlook profile and rebuilt OST cache."),
        ("NEX-103", "Finance shared network drive F: inaccessible", "Network Connectivity", "Deepak Rao", "deepak.rao@nexora.com", "Finance", "High", "High", "P1", "Resolved", "Alex Chen", "L1 Service Desk", 1.25, "Verified Kerberos ticket expiry; executed klist purge and refreshed group membership."),
        ("NEX-104", "GlobalProtect VPN gateway timeout when working remotely", "VPN Issue", "Divya Ramesh", "divya.ramesh@nexora.com", "Engineering", "Medium", "High", "P2", "In Progress", "Suresh Hegde", "L2 Network", 0, "Switched client protocol to TCP/SSL as workaround. Investigating MTU black hole."),
        ("NEX-105", "Dell 24-inch monitor display flickering intermittently", "Hardware Problem", "Shreya Patil", "shreya.patil@nexora.com", "Sales", "Low", "Low", "P4", "Resolved", "Alex Chen", "L1 Service Desk", 4.5, "Replaced damaged DisplayPort cable with certified OEM cable."),
        ("NEX-106", "Need Adobe Acrobat Pro installed for contract review", "Software Installation", "Karthik Subramaniam", "karthik.s@nexora.com", "Engineering", "Low", "Medium", "P4", "Waiting for Customer", "Priya Sharma", "L1 Service Desk", 0, "Requested manager approval confirmation from department head."),
        ("NEX-107", "HR Floor 2 network printer showing 'Offline'", "Printer Issue", "Kavitha Murthy", "kavitha.murthy@nexora.com", "HR", "Medium", "Medium", "P3", "Resolved", "Alex Chen", "L1 Service Desk", 0.75, "Restarted Print Spooler service on print server and cleared hung queue."),
        ("NEX-108", "Laptop freezing and fan spinning loudly at 100% CPU", "Laptop Performance Issue", "Arun Nair", "arun.nair@nexora.com", "Operations", "Medium", "Medium", "P3", "Resolved", "Priya Sharma", "L1 Service Desk", 1.5, "Terminated runaway Chrome renderer thread and scheduled cold reboot to bypass Fast Startup."),
        ("NEX-109", "Suspicious phishing email reporting urgent wire transfer", "Security Incident", "Prasad Joshi", "prasad.joshi@nexora.com", "Operations", "High", "High", "P1", "Resolved", "Rajesh Bhat", "IT Security", 0.5, "Purged phishing email tenant-wide via Defender Explorer and blocked sender domain."),
        ("NEX-110", "New Employee Account Provisioning - Frontend Engineer", "New User Access", "Rajesh Bhat", "rajesh.bhat@nexora.com", "IT", "Low", "High", "P3", "New", "Unassigned", "L1 Service Desk", 0, "New hire onboarding ticket created. Awaiting HR verification.")
    ]
    
    for t in sample_tickets:
        key, title, req_type, caller, email, dept, impact, urgency, priority, status, assignee, group, res_hours, notes = t
        created_dt = base_time + timedelta(hours=int(key.split("-")[1]) % 20)
        created_str = created_dt.strftime("%Y-%m-%d %H:%M:%S")
        target_hours = SLA_POLICY[priority]["hours"]
        resolved_str = (created_dt + timedelta(hours=res_hours)).strftime("%Y-%m-%d %H:%M:%S") if status == "Resolved" else None
        
        c.execute("""
        INSERT INTO tickets (
            key, title, request_type, caller_name, caller_email, department,
            impact, urgency, priority, status, assigned_to, assignment_group,
            created_at, updated_at, resolved_at, sla_target_hours, sla_breached,
            description, resolution_notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            key, title, req_type, caller, email, dept,
            impact, urgency, priority, status, assignee, group,
            created_str, created_str, resolved_str, target_hours, 0,
            f"User reported: {title}", notes
        ))
        
        # Add initial activity
        c.execute("""
        INSERT INTO ticket_activity (ticket_key, timestamp, author, activity_type, message)
        VALUES (?, ?, ?, ?, ?)
        """, (key, created_str, caller, "CUSTOMER_COMMENT", f"Created ticket: {title}"))
        
        if status == "Resolved":
            c.execute("""
            INSERT INTO ticket_activity (ticket_key, timestamp, author, activity_type, message)
            VALUES (?, ?, ?, ?, ?)
            """, (key, resolved_str, assignee, "STATUS_CHANGE", f"Ticket Resolved. {notes}"))
            
    conn.commit()

class ServiceDeskHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)
        
        if path == "/" or path == "/portal":
            self.serve_portal()
        elif path == "/agent":
            self.serve_agent_console()
        elif path == "/api/tickets":
            self.api_get_tickets(query)
        elif path == "/api/ticket":
            self.api_get_ticket(query)
        elif path == "/api/stats":
            self.api_get_stats()
        elif path == "/api/export":
            self.api_export_tickets()
        else:
            self.send_error(404, "Page not found")
            
    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get('content-length', 0))
        body = self.rfile.read(length).decode('utf-8')
        try:
            data = json.loads(body)
        except Exception:
            data = urllib.parse.parse_qs(body)
            data = {k: v[0] for k, v in data.items()}
            
        if path == "/api/tickets":
            self.api_create_ticket(data)
        elif path == "/api/ticket/update":
            self.api_update_ticket(data)
        elif path == "/api/ticket/comment":
            self.api_add_comment(data)
        else:
            self.send_error(404, "Endpoint not found")

    def api_get_tickets(self, query):
        queue = query.get("queue", ["all"])[0]
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        sql = "SELECT * FROM tickets"
        params = []
        if queue == "unassigned":
            sql += " WHERE assigned_to = 'Unassigned' OR assigned_to IS NULL"
        elif queue == "p1":
            sql += " WHERE priority = 'P1' AND status != 'Closed'"
        elif queue == "p2":
            sql += " WHERE priority = 'P2' AND status != 'Closed'"
        elif queue == "l1":
            sql += " WHERE assignment_group = 'L1 Service Desk' AND status NOT IN ('Resolved', 'Closed')"
        elif queue == "wait_customer":
            sql += " WHERE status = 'Waiting for Customer'"
        elif queue == "resolved":
            sql += " WHERE status IN ('Resolved', 'Closed')"
            
        sql += " ORDER BY id DESC"
        c.execute(sql, params)
        rows = [dict(r) for r in c.fetchall()]
        conn.close()
        
        self.send_json({"status": "success", "count": len(rows), "tickets": rows})

    def api_get_ticket(self, query):
        key = query.get("key", [""])[0]
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM tickets WHERE key = ?", (key,))
        ticket = c.fetchone()
        if not ticket:
            conn.close()
            self.send_json({"status": "error", "message": "Ticket not found"}, 404)
            return
            
        ticket_data = dict(ticket)
        c.execute("SELECT * FROM ticket_activity WHERE ticket_key = ? ORDER BY id ASC", (key,))
        activities = [dict(r) for r in c.fetchall()]
        conn.close()
        
        ticket_data["activities"] = activities
        self.send_json({"status": "success", "ticket": ticket_data})

    def api_create_ticket(self, data):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT MAX(id) FROM tickets")
        max_id = c.fetchone()[0] or 100
        new_key = f"NEX-{max_id + 1}"
        
        impact = data.get("impact", "Medium")
        urgency = data.get("urgency", "Medium")
        priority = PRIORITY_MATRIX.get((impact, urgency), "P3")
        target_hours = SLA_POLICY[priority]["hours"]
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        c.execute("""
        INSERT INTO tickets (
            key, title, request_type, caller_name, caller_email, department,
            impact, urgency, priority, status, assigned_to, assignment_group,
            created_at, updated_at, sla_target_hours, description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            new_key, data.get("title", "Untitled Request"),
            data.get("request_type", "General IT Request"),
            data.get("caller_name", "Anonymous"),
            data.get("caller_email", "user@nexora.com"),
            data.get("department", "Operations"),
            impact, urgency, priority, "New", "Unassigned", "L1 Service Desk",
            now_str, now_str, target_hours, data.get("description", "")
        ))
        
        c.execute("""
        INSERT INTO ticket_activity (ticket_key, timestamp, author, activity_type, message)
        VALUES (?, ?, ?, ?, ?)
        """, (new_key, now_str, data.get("caller_name", "User"), "CUSTOMER_COMMENT", "Ticket submitted via Nexora Customer Portal"))
        
        conn.commit()
        conn.close()
        self.send_json({"status": "success", "key": new_key, "priority": priority, "target_hours": target_hours})

    def api_update_ticket(self, data):
        key = data.get("key")
        status = data.get("status")
        assigned_to = data.get("assigned_to")
        resolution = data.get("resolution_notes")
        author = data.get("author", "L1 Agent")
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        
        updates = ["updated_at = ?"]
        params = [now_str]
        
        if status:
            updates.append("status = ?")
            params.append(status)
            if status in ("Resolved", "Closed"):
                updates.append("resolved_at = ?")
                params.append(now_str)
        if assigned_to:
            updates.append("assigned_to = ?")
            params.append(assigned_to)
        if resolution:
            updates.append("resolution_notes = ?")
            params.append(resolution)
            
        params.append(key)
        c.execute(f"UPDATE tickets SET {', '.join(updates)} WHERE key = ?", params)
        
        msg = f"Ticket updated to status '{status}'" if status else "Ticket details updated"
        if resolution:
            msg += f" with resolution: {resolution}"
        c.execute("""
        INSERT INTO ticket_activity (ticket_key, timestamp, author, activity_type, message)
        VALUES (?, ?, ?, ?, ?)
        """, (key, now_str, author, "STATUS_CHANGE", msg))
        
        conn.commit()
        conn.close()
        self.send_json({"status": "success", "message": msg})

    def api_add_comment(self, data):
        key = data.get("key")
        author = data.get("author", "Support Agent")
        comment_type = data.get("type", "WORK_NOTE")
        message = data.get("message", "")
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("""
        INSERT INTO ticket_activity (ticket_key, timestamp, author, activity_type, message)
        VALUES (?, ?, ?, ?, ?)
        """, (key, now_str, author, comment_type, message))
        c.execute("UPDATE tickets SET updated_at = ? WHERE key = ?", (now_str, key))
        conn.commit()
        conn.close()
        self.send_json({"status": "success", "message": "Activity recorded"})

    def api_get_stats(self):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM tickets")
        total = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM tickets WHERE status IN ('Resolved', 'Closed')")
        resolved = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM tickets WHERE status NOT IN ('Resolved', 'Closed')")
        open_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM tickets WHERE priority = 'P1' AND status NOT IN ('Resolved', 'Closed')")
        p1_open = c.fetchone()[0]
        conn.close()
        self.send_json({
            "total_tickets": total,
            "resolved_tickets": resolved,
            "open_backlog": open_count,
            "p1_critical_open": p1_open,
            "l1_resolution_rate": f"{(resolved/total*100):.1f}%" if total > 0 else "0%"
        })

    def api_export_tickets(self):
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM tickets ORDER BY id ASC")
        rows = [dict(r) for r in c.fetchall()]
        conn.close()
        self.send_json({"export_timestamp": datetime.now().isoformat(), "tickets": rows})

    def send_json(self, data, code=200):
        body = json.dumps(data, indent=2).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def serve_portal(self):
        html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Nexora Technologies | IT Help Center</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  :root { --primary: #0052cc; --primary-dark: #0747a6; --bg: #f4f5f7; --card: #ffffff; --text: #172b4d; --border: #dfe1e6; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 0; }
  header { background: var(--primary); color: white; padding: 20px 40px; display: flex; justify-content: space-between; align-items: center; }
  header h1 { margin: 0; font-size: 20px; font-weight: 600; }
  header a { color: white; text-decoration: none; font-size: 14px; background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 4px; }
  header a:hover { background: rgba(255,255,255,0.3); }
  .container { max-width: 1000px; margin: 40px auto; padding: 0 20px; }
  .hero { text-align: center; margin-bottom: 40px; }
  .hero h2 { font-size: 28px; margin-bottom: 8px; }
  .hero p { color: #5e6c84; font-size: 16px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
  .card { background: var(--card); border: 1px solid var(--border); border-radius: 6px; padding: 24px; cursor: pointer; transition: all 0.2s; }
  .card:hover { transform: translateY(-3px); box-shadow: 0 4px 12px rgba(0,0,0,0.08); border-color: var(--primary); }
  .card h3 { margin-top: 0; font-size: 18px; color: var(--primary); }
  .card p { color: #5e6c84; font-size: 14px; line-height: 1.4; margin-bottom: 0; }
  /* Modal */
  .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); align-items: center; justify-content: center; z-index: 1000; }
  .modal.active { display: flex; }
  .modal-content { background: white; width: 500px; border-radius: 8px; padding: 30px; box-shadow: 0 8px 24px rgba(0,0,0,0.15); max-height: 90vh; overflow-y: auto; }
  .form-group { margin-bottom: 16px; }
  .form-group label { display: block; font-size: 13px; font-weight: 600; margin-bottom: 6px; color: #344563; }
  .form-group input, .form-group select, .form-group textarea { width: 100%; padding: 8px 12px; border: 1px solid var(--border); border-radius: 4px; box-sizing: border-box; font-size: 14px; }
  .form-row { display: flex; gap: 12px; }
  .form-row .form-group { flex: 1; }
  .btn { background: var(--primary); color: white; border: none; padding: 10px 20px; border-radius: 4px; font-size: 14px; font-weight: 600; cursor: pointer; }
  .btn:hover { background: var(--primary-dark); }
  .btn-cancel { background: #ebecf0; color: #42526e; margin-left: 8px; }
  .alert-success { background: #e3fcef; border: 1px solid #abf5d1; color: #006644; padding: 12px; border-radius: 4px; margin-bottom: 16px; display: none; }
</style>
</head>
<body>
<header>
  <div><h1>Nexora Technologies</h1><small>IT Operations & Support Services</small></div>
  <a href="/agent">Switch to L1 Agent Console &rarr;</a>
</header>
<div class="container">
  <div class="hero">
    <h2>Welcome to the IT Service Portal</h2>
    <p>Select a service request category below to submit an incident or service request.</p>
  </div>
  <div id="success-banner" class="alert-success"></div>
  <div class="grid">
    <div class="card" onclick="openRequest('Password Reset / Account Unlock')">
      <h3>🔑 Password Reset / Unlock</h3>
      <p>Self-service and assisted Windows domain or M365 account recovery.</p>
    </div>
    <div class="card" onclick="openRequest('New User Access')">
      <h3>👤 New User Access</h3>
      <p>Onboarding request for Active Directory, shared drives, and M365 licenses.</p>
    </div>
    <div class="card" onclick="openRequest('Hardware Problem')">
      <h3>💻 Hardware Problem</h3>
      <p>Report laptop issues, broken screens, monitors, or docking stations.</p>
    </div>
    <div class="card" onclick="openRequest('Software Installation')">
      <h3>📦 Software Installation</h3>
      <p>Request enterprise approved software deployments (Acrobat, VS Code, etc.).</p>
    </div>
    <div class="card" onclick="openRequest('Network Connectivity')">
      <h3>🌐 Network Connectivity</h3>
      <p>Troubleshoot office Ethernet, Wi-Fi drops, or local default gateway issues.</p>
    </div>
    <div class="card" onclick="openRequest('VPN Issue')">
      <h3>🛡️ VPN Issue</h3>
      <p>Assistance with Palo Alto GlobalProtect disconnections or remote gateways.</p>
    </div>
    <div class="card" onclick="openRequest('Printer Issue')">
      <h3>🖨️ Printer Issue</h3>
      <p>Resolve paper jams, offline print queues, or network printer mapping.</p>
    </div>
    <div class="card" onclick="openRequest('Microsoft 365 Client Issue')">
      <h3>📧 Microsoft 365 Client Issue</h3>
      <p>Outlook profile freezing, Microsoft Teams cache glitches, or OneDrive sync.</p>
    </div>
    <div class="card" onclick="openRequest('Laptop Performance Issue')">
      <h3>⚡ Laptop Performance Issue</h3>
      <p>High CPU usage, loud fans, thermal throttling, or slow startup.</p>
    </div>
    <div class="card" onclick="openRequest('Security Incident')">
      <h3>🚨 Security Incident</h3>
      <p>Report phishing emails, suspicious popups, malware alerts, or lost assets.</p>
    </div>
  </div>
</div>

<div id="requestModal" class="modal">
  <div class="modal-content">
    <h3 id="modalTitle" style="margin-top:0; color:var(--primary);">Submit IT Request</h3>
    <form id="ticketForm" onsubmit="submitTicket(event)">
      <input type="hidden" id="reqType">
      <div class="form-group">
        <label>Your Name *</label>
        <input type="text" id="callerName" required placeholder="e.g. Deepak Rao">
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Email *</label>
          <input type="email" id="callerEmail" required placeholder="user@nexora.com">
        </div>
        <div class="form-group">
          <label>Department *</label>
          <select id="callerDept">
            <option>HR</option><option>Finance</option><option>Operations</option><option>Sales</option><option>Engineering</option><option>IT</option>
          </select>
        </div>
      </div>
      <div class="form-group">
        <label>Summary / Title *</label>
        <input type="text" id="ticketTitle" required placeholder="Brief description of the issue">
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Impact *</label>
          <select id="ticketImpact">
            <option value="Low">Low (Affects only me)</option>
            <option value="Medium" selected>Medium (Affects my team / department)</option>
            <option value="High">High (Affects whole company)</option>
          </select>
        </div>
        <div class="form-group">
          <label>Urgency *</label>
          <select id="ticketUrgency">
            <option value="Low">Low (Can wait standard SLA)</option>
            <option value="Medium" selected>Medium (Impacting today's work)</option>
            <option value="High">High (Critical work blocked)</option>
          </select>
        </div>
      </div>
      <div class="form-group">
        <label>Detailed Description *</label>
        <textarea id="ticketDesc" rows="4" required placeholder="Provide exact error messages, computer Asset Tag, and steps taken..."></textarea>
      </div>
      <div style="text-align:right; margin-top:20px;">
        <button type="submit" class="btn">Submit Ticket</button>
        <button type="button" class="btn btn-cancel" onclick="closeModal()">Cancel</button>
      </div>
    </form>
  </div>
</div>

<script>
function openRequest(type) {
  document.getElementById('reqType').value = type;
  document.getElementById('modalTitle').innerText = 'Submit Request: ' + type;
  document.getElementById('requestModal').classList.add('active');
}
function closeModal() {
  document.getElementById('requestModal').classList.remove('active');
}
async function submitTicket(e) {
  e.preventDefault();
  const payload = {
    request_type: document.getElementById('reqType').value,
    caller_name: document.getElementById('callerName').value,
    caller_email: document.getElementById('callerEmail').value,
    department: document.getElementById('callerDept').value,
    title: document.getElementById('ticketTitle').value,
    impact: document.getElementById('ticketImpact').value,
    urgency: document.getElementById('ticketUrgency').value,
    description: document.getElementById('ticketDesc').value
  };
  const res = await fetch('/api/tickets', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  closeModal();
  document.getElementById('ticketForm').reset();
  const banner = document.getElementById('success-banner');
  banner.innerHTML = `<strong>Ticket Logged Successfully!</strong> Ticket ID: <strong>${data.key}</strong> | Priority: <strong>${data.priority}</strong> (Target SLA: ${data.target_hours} elapsed clock hours). An L1 Service Desk agent has been notified.`;
  banner.style.display = 'block';
  window.scrollTo({top: 0, behavior: 'smooth'});
}
</script>
</body>
</html>
"""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def serve_agent_console(self):
        html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Nexora Technologies | L1 Service Desk Console</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  :root { --sidebar: #0747a6; --bg: #f4f5f7; --card: #ffffff; --text: #172b4d; --border: #dfe1e6; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: var(--text); margin: 0; display: flex; height: 100vh; overflow: hidden; }
  aside { width: 260px; background: #0747a6; color: white; display: flex; flex-direction: column; }
  aside .logo { padding: 20px; font-size: 18px; font-weight: 700; border-bottom: 1px solid rgba(255,255,255,0.1); }
  aside .nav-group { padding: 15px 0; }
  aside .nav-title { padding: 0 20px 8px; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.7; }
  aside a { display: block; padding: 10px 20px; color: white; text-decoration: none; font-size: 14px; opacity: 0.85; }
  aside a:hover, aside a.active { background: rgba(255,255,255,0.15); opacity: 1; font-weight: 600; }
  main { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
  header { background: white; padding: 16px 24px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }
  header h2 { margin: 0; font-size: 20px; }
  .stats-bar { display: flex; gap: 20px; }
  .stat-badge { background: #ebecf0; padding: 4px 10px; border-radius: 4px; font-size: 13px; font-weight: 500; }
  .stat-badge strong { color: #0052cc; }
  .content { flex: 1; display: flex; overflow: hidden; }
  .ticket-list { width: 450px; border-right: 1px solid var(--border); overflow-y: auto; background: white; }
  .ticket-item { padding: 14px 18px; border-bottom: 1px solid var(--border); cursor: pointer; }
  .ticket-item:hover, .ticket-item.active { background: #f0f7ff; }
  .ticket-key { font-weight: 700; color: #0052cc; font-size: 13px; }
  .ticket-title { font-size: 14px; font-weight: 600; margin: 4px 0; }
  .ticket-meta { font-size: 12px; color: #5e6c84; display: flex; gap: 10px; }
  .priority-badge { font-size: 11px; padding: 2px 6px; border-radius: 3px; font-weight: 700; }
  .p-P1 { background: #ffebe6; color: #de350b; }
  .p-P2 { background: #fffae6; color: #ff8b00; }
  .p-P3 { background: #e3fcef; color: #006644; }
  .p-P4 { background: #ebecf0; color: #42526e; }
  .ticket-detail { flex: 1; padding: 24px; overflow-y: auto; background: var(--bg); }
  .detail-card { background: white; border: 1px solid var(--border); border-radius: 6px; padding: 20px; margin-bottom: 20px; }
  .action-bar { display: flex; gap: 10px; margin-top: 15px; }
  .btn { padding: 6px 12px; border-radius: 4px; font-size: 13px; font-weight: 600; cursor: pointer; border: 1px solid var(--border); background: white; }
  .btn-primary { background: #0052cc; color: white; border: none; }
  .btn-success { background: #00875a; color: white; border: none; }
  .activity-log { margin-top: 20px; }
  .activity-item { padding: 10px; border-left: 3px solid #0052cc; background: white; margin-bottom: 10px; font-size: 13px; border-radius: 0 4px 4px 0; }
</style>
</head>
<body>
<aside>
  <div class="logo">Nexora IT Service Desk<br><small style="font-weight:400; opacity:0.8;">L1 Operator Console</small></div>
  <div class="nav-group">
    <div class="nav-title">Queues</div>
    <a href="#" class="active" onclick="loadQueue('all', this)">All Incidents</a>
    <a href="#" onclick="loadQueue('unassigned', this)">Unassigned Incidents</a>
    <a href="#" onclick="loadQueue('p1', this)">P1 Critical Queue</a>
    <a href="#" onclick="loadQueue('p2', this)">P2 High Queue</a>
    <a href="#" onclick="loadQueue('l1', this)">Assigned to L1 Support</a>
    <a href="#" onclick="loadQueue('wait_customer', this)">Waiting for Customer</a>
    <a href="#" onclick="loadQueue('resolved', this)">Recently Resolved</a>
  </div>
  <div class="nav-group" style="margin-top:auto; padding:20px;">
    <a href="/portal" style="padding:8px 12px; background:rgba(255,255,255,0.2); border-radius:4px; text-align:center;">&larr; Customer Portal</a>
  </div>
</aside>
<main>
  <header>
    <h2 id="queueTitle">All Incidents</h2>
    <div class="stats-bar" id="statsBar">
      <div class="stat-badge">Total: <strong id="stTotal">0</strong></div>
      <div class="stat-badge">Open: <strong id="stOpen">0</strong></div>
      <div class="stat-badge">P1 Critical: <strong id="stP1" style="color:#de350b;">0</strong></div>
      <div class="stat-badge">L1 Resolution Rate: <strong id="stFCR" style="color:#00875a;">0%</strong></div>
    </div>
  </header>
  <div class="content">
    <div class="ticket-list" id="ticketList"></div>
    <div class="ticket-detail" id="ticketDetail">
      <div style="text-align:center; padding:60px; color:#5e6c84;">
        <h3>Select a ticket from the queue</h3>
        <p>Review incident diagnostics, SLA elapsed timers, and execute state transitions.</p>
      </div>
    </div>
  </div>
</main>

<script>
let currentQueue = 'all';
let selectedKey = null;

async function loadStats() {
  const res = await fetch('/api/stats');
  const d = await res.json();
  document.getElementById('stTotal').innerText = d.total_tickets;
  document.getElementById('stOpen').innerText = d.open_backlog;
  document.getElementById('stP1').innerText = d.p1_critical_open;
  document.getElementById('stFCR').innerText = d.l1_resolution_rate;
}

async function loadQueue(queue, el) {
  currentQueue = queue;
  if (el) {
    document.querySelectorAll('aside a').forEach(a => a.classList.remove('active'));
    el.classList.add('active');
    document.getElementById('queueTitle').innerText = el.innerText;
  }
  const res = await fetch('/api/tickets?queue=' + queue);
  const data = await res.json();
  const list = document.getElementById('ticketList');
  list.innerHTML = '';
  data.tickets.forEach(t => {
    const item = document.createElement('div');
    item.className = 'ticket-item' + (selectedKey === t.key ? ' active' : '');
    item.onclick = () => selectTicket(t.key);
    item.innerHTML = `
      <div style="display:flex; justify-content:space-between;">
        <span class="ticket-key">${t.key}</span>
        <span class="priority-badge p-${t.priority}">${t.priority} ${t.status}</span>
      </div>
      <div class="ticket-title">${t.title}</div>
      <div class="ticket-meta">
        <span>${t.caller_name} (${t.department})</span>
        <span>•</span>
        <span>${t.assigned_to || 'Unassigned'}</span>
      </div>
    `;
    list.appendChild(item);
  });
  if (data.tickets.length > 0 && !selectedKey) {
    selectTicket(data.tickets[0].key);
  }
}

async function selectTicket(key) {
  selectedKey = key;
  document.querySelectorAll('.ticket-item').forEach(el => el.classList.remove('active'));
  const res = await fetch('/api/ticket?key=' + key);
  const data = await res.json();
  const t = data.ticket;
  const detail = document.getElementById('ticketDetail');
  
  let actsHtml = '';
  t.activities.forEach(a => {
    actsHtml += `
      <div class="activity-item">
        <div style="font-size:11px; color:#5e6c84; margin-bottom:4px;"><strong>${a.author}</strong> • ${a.timestamp} • [${a.activity_type}]</div>
        <div>${a.message}</div>
      </div>
    `;
  });

  detail.innerHTML = `
    <div class="detail-card">
      <div style="display:flex; justify-content:space-between; align-items:flex-start;">
        <div>
          <span class="ticket-key" style="font-size:16px;">${t.key}</span>
          <h2 style="margin:6px 0 12px;">${t.title}</h2>
          <div style="font-size:13px; color:#5e6c84;">
            Caller: <strong>${t.caller_name}</strong> (${t.caller_email}) • Dept: <strong>${t.department}</strong> • Type: <strong>${t.request_type}</strong>
          </div>
        </div>
        <div style="text-align:right;">
          <span class="priority-badge p-${t.priority}" style="font-size:14px; padding:4px 8px;">${t.priority}</span>
          <div style="font-size:12px; margin-top:6px; color:#5e6c84;">SLA Target: ${t.sla_target_hours}h elapsed</div>
        </div>
      </div>
      <hr style="border:0; border-top:1px solid #dfe1e6; margin:16px 0;">
      <div>
        <h4>Description</h4>
        <p style="font-size:14px; line-height:1.5;">${t.description}</p>
      </div>
      ${t.resolution_notes ? `
      <div style="background:#e3fcef; border:1px solid #abf5d1; padding:12px; border-radius:4px; margin-top:12px;">
        <h4 style="margin:0 0 6px; color:#006644;">Resolution Notes</h4>
        <p style="margin:0; font-size:13px; color:#006644;">${t.resolution_notes}</p>
      </div>` : ''}
      <div class="action-bar">
        <button class="btn btn-primary" onclick="updateTicket('${t.key}', 'In Progress', 'Alex Chen')">Start Work (Assign to Me)</button>
        <button class="btn" onclick="updateTicket('${t.key}', 'Waiting for Customer')">Wait for Customer</button>
        <button class="btn" onclick="updateTicket('${t.key}', 'Waiting for Vendor')">Wait for Vendor</button>
        <button class="btn btn-success" onclick="resolveTicketPrompt('${t.key}')">Resolve Incident</button>
        <button class="btn" onclick="updateTicket('${t.key}', 'Closed')">Close Ticket</button>
      </div>
    </div>

    <div class="detail-card">
      <h4 style="margin-top:0;">Add Internal Work Note / Customer Comment</h4>
      <textarea id="commentBox" style="width:100%; box-sizing:border-box; padding:8px; border:1px solid #dfe1e6; border-radius:4px;" rows="3" placeholder="Log technical findings, IP addresses, or customer communication..."></textarea>
      <div style="margin-top:10px; display:flex; gap:10px;">
        <button class="btn" onclick="postComment('${t.key}', 'WORK_NOTE')">Add Internal Work Note</button>
        <button class="btn" onclick="postComment('${t.key}', 'CUSTOMER_COMMENT')">Send Customer Comment</button>
      </div>
    </div>

    <div class="detail-card">
      <h4 style="margin-top:0;">Audit Trail & Ticket History</h4>
      <div class="activity-log">${actsHtml}</div>
    </div>
  `;
}

async function updateTicket(key, status, assignee) {
  const payload = { key: key, status: status, author: 'Alex Chen (L1 Lead)' };
  if (assignee) payload.assigned_to = assignee;
  await fetch('/api/ticket/update', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
  });
  loadStats();
  loadQueue(currentQueue);
  selectTicket(key);
}

async function resolveTicketPrompt(key) {
  const notes = prompt("Enter Resolution Notes (Root cause and corrective action):");
  if (!notes) return;
  const payload = {
    key: key,
    status: 'Resolved',
    resolution_notes: notes,
    author: 'Alex Chen (L1 Lead)'
  };
  await fetch('/api/ticket/update', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
  });
  loadStats();
  loadQueue(currentQueue);
  selectTicket(key);
}

async function postComment(key, type) {
  const msg = document.getElementById('commentBox').value;
  if (!msg) return;
  await fetch('/api/ticket/comment', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ key: key, author: 'Alex Chen (L1)', type: type, message: msg })
  });
  selectTicket(key);
}

// Initial boot
loadStats();
loadQueue('all');
</script>
</body>
</html>
"""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

def run_server():
    init_db()
    server_address = ('', PORT)
    httpd = socketserver.TCPServer(server_address, ServiceDeskHandler)
    print(f"==================================================================")
    print(f"  NEXORA IT SERVICE DESK PLATFORM ONLINE")
    print(f"  Customer Portal:    http://localhost:{PORT}/portal")
    print(f"  L1 Agent Console:   http://localhost:{PORT}/agent")
    print(f"  API Endpoint:       http://localhost:{PORT}/api/tickets")
    print(f"==================================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down service desk portal.")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
