#!/usr/bin/env python3
"""
Nexora Technologies - Operational IT Service Desk Platform
Provides an interactive Customer Portal and L1 Agent Console with
real ticket lifecycle workflows, Impact x Urgency priority matrix,
elapsed-clock-hour SLA timers, and integrated Knowledge Base search.

Zero external dependencies (Python standard library only).
Security hardened: Localhost binding (127.0.0.1), PBKDF2 authentication,
dynamic credential bootstrap, role-based authorization, state-machine validation,
XSS escaping, CSRF verification, dynamic SLA evaluation, customer token protection,
and 10 operational queues.
"""

import http.server
import socketserver
import sqlite3
import json
import urllib.parse
import os
import sys
import html
import hashlib
import secrets
import re
from datetime import datetime, timezone, timedelta

DEFAULT_PORT = 8080
DEFAULT_HOST = "127.0.0.1"
DEFAULT_DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nexora_servicedesk.db")
LOCAL_CREDENTIALS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".local_credentials.json")

# Maximum allowed HTTP payload size (64 KB)
MAX_PAYLOAD_SIZE = 65536

# In-memory active sessions: {session_token: {"username": str, "full_name": str, "role": str, "expires": datetime}}
ACTIVE_SESSIONS = {}

SLA_POLICY = {
    "P1": {"name": "Critical", "hours": 4.0, "desc": "4 Elapsed Clock Hours (24x7)"},
    "P2": {"name": "High", "hours": 8.0, "desc": "8 Elapsed Clock Hours"},
    "P3": {"name": "Medium", "hours": 72.0, "desc": "72 Elapsed Clock Hours (3 Days)"},
    "P4": {"name": "Low", "hours": 120.0, "desc": "120 Elapsed Clock Hours (5 Days)"}
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

ALLOWED_TRANSITIONS = {
    "New": ["Assigned", "In Progress"],
    "Assigned": ["In Progress", "Waiting for Customer", "Waiting for Vendor"],
    "In Progress": ["Waiting for Customer", "Waiting for Vendor", "Resolved"],
    "Waiting for Customer": ["In Progress", "Resolved"],
    "Waiting for Vendor": ["In Progress", "Resolved"],
    "Resolved": ["Closed", "In Progress"],
    "Closed": ["In Progress"]  # Reopening closed ticket resets resolution timestamp
}

VALID_DEPARTMENTS = ("HR", "Finance", "Operations", "IT", "Engineering", "Sales", "Admin")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

def hash_password(password: str, salt: str = None) -> tuple:
    """Hashes a password using PBKDF2-HMAC-SHA256 with a secure salt."""
    if not salt:
        salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return key.hex(), salt

def verify_password(password: str, salt: str, expected_hash: str) -> bool:
    """Verifies a password against a stored salt and hash using constant-time comparison."""
    key, _ = hash_password(password, salt)
    return secrets.compare_digest(key, expected_hash)

def protect_local_file(filepath: str) -> bool:
    """
    Applies restrictive operating system filesystem permissions to a local credentials file:
    - On Windows NTFS: Uses icacls to remove inheritance and grant Full Control strictly
      to the current user (%USERNAME%) and BUILTIN\\Administrators (*S-1-5-32-544).
      Captures return code, treats failures as real errors, and verifies the resulting ACL.
    - On POSIX / Linux: Uses chmod 0600 (owner read/write only) and verifies file mode.
    Returns True on success, or raises RuntimeError/PermissionError on failure.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Target file does not exist: {filepath}")
    
    if os.name == "nt":
        import subprocess
        username = os.environ.get("USERNAME")
        if not username:
            raise RuntimeError("Cannot resolve USERNAME environment variable for ACL configuration")
        
        # 1. Apply restrictive ACLs
        res = subprocess.run(
            ["icacls.exe", filepath, "/inheritance:r", "/grant:r", f"{username}:(F)", "/grant:r", "*S-1-5-32-544:(F)"],
            capture_output=True,
            text=True
        )
        if res.returncode != 0 or "Failed processing 0 files" not in res.stdout:
            raise PermissionError(f"Failed to apply Windows ACLs on {filepath} (code {res.returncode}): {res.stderr or res.stdout}")
        
        # 2. Verify resulting ACL
        verify_res = subprocess.run(["icacls.exe", filepath], capture_output=True, text=True)
        if verify_res.returncode != 0:
            raise PermissionError(f"Failed to query ACLs on {filepath} (code {verify_res.returncode}): {verify_res.stderr}")
        
        out = verify_res.stdout.upper()
        if "(F)" not in out or username.upper() not in out:
            raise PermissionError(f"ACL verification failed for {filepath}. Resulting ACL:\n{verify_res.stdout}")
        return True

    elif hasattr(os, "chmod"):
        import stat
        os.chmod(filepath, 0o600)
        mode = stat.S_IMODE(os.stat(filepath).st_mode)
        if mode != 0o600:
            raise PermissionError(f"POSIX permission verification failed for {filepath}: mode is {oct(mode)}, expected 0o600")
        return True
    
    return False

def get_or_create_bootstrap_password(creds_file: str = LOCAL_CREDENTIALS_FILE) -> str:
    """
    Obtains the initial bootstrap password for alex.chen from:
    1. NEXORA_PORTAL_ADMIN_PASS environment variable, or
    2. Local ignored secrets file (.local_credentials.json), or
    3. Securely generated random token saved to .local_credentials.json
    Protected by local operating system filesystem ACLs.
    """
    env_pass = os.environ.get("NEXORA_PORTAL_ADMIN_PASS")
    if env_pass:
        return env_pass.strip()

    if os.path.exists(creds_file):
        try:
            with open(creds_file, "r", encoding="utf-8") as f:
                creds = json.load(f)
                if "bootstrap_password" in creds:
                    return creds["bootstrap_password"]
        except Exception:
            pass

    generated_pass = secrets.token_urlsafe(16)
    dir_name = os.path.dirname(os.path.abspath(creds_file))
    tmp_file = os.path.join(dir_name, f".tmp_creds_{secrets.token_hex(6)}.json")
    try:
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump({
                "username": "alex.chen",
                "bootstrap_password": generated_pass,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "note": "Local credential store for IT Service Desk. Ignored by Git."
            }, f, indent=2)
        protect_local_file(tmp_file)
        if os.path.exists(creds_file):
            os.replace(tmp_file, creds_file)
        else:
            os.rename(tmp_file, creds_file)
        protect_local_file(creds_file)
    except Exception as e:
        if os.path.exists(tmp_file):
            try: os.unlink(tmp_file)
            except Exception: pass
        print(f"[WARN] Could not write local credentials file: {e}", file=sys.stderr)

    return generated_pass

def migrate_or_rotate_user_credentials(db_path: str, username: str = "alex.chen", new_password: str = None, creds_file: str = LOCAL_CREDENTIALS_FILE) -> str:
    """
    Rotates credentials for a user in an existing database without deleting, modifying,
    or recreating any tickets or ticket activity logs.
    Ensures safe persistence and verified ACL protection before updating the database.
    """
    if not new_password:
        new_password = secrets.token_urlsafe(16)
    
    pwd_hash, salt = hash_password(new_password)
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    # Step 1: Safely persist and protect new credentials FIRST
    dir_name = os.path.dirname(os.path.abspath(creds_file))
    tmp_file = os.path.join(dir_name, f".tmp_creds_{secrets.token_hex(6)}.json")
    try:
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump({
                "username": username,
                "bootstrap_password": new_password,
                "rotated_at": now_str,
                "note": "Local credential store for IT Service Desk. Ignored by Git."
            }, f, indent=2)
        protect_local_file(tmp_file)
        if os.path.exists(creds_file):
            os.replace(tmp_file, creds_file)
        else:
            os.rename(tmp_file, creds_file)
        protect_local_file(creds_file)
    except Exception as e:
        if os.path.exists(tmp_file):
            try: os.unlink(tmp_file)
            except Exception: pass
        raise RuntimeError(f"Cannot safely persist credentials to {creds_file}; aborting rotation: {e}")

    # Step 2: Update users table in existing database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, username FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    if row:
        c.execute("""
        UPDATE users
        SET password_hash = ?, salt = ?
        WHERE username = ?
        """, (pwd_hash, salt, username))
    else:
        c.execute("""
        INSERT INTO users (username, full_name, role, password_hash, salt, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (username, "Alex Chen (L1 Lead)", "agent", pwd_hash, salt, now_str))
    conn.commit()
    conn.close()

    return new_password

def init_db(db_path=DEFAULT_DB_FILE, creds_file=LOCAL_CREDENTIALS_FILE):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL, -- 'agent', 'admin'
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT UNIQUE NOT NULL,
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
        due_at TEXT NOT NULL,
        sla_target_hours REAL NOT NULL,
        sla_breached INTEGER DEFAULT 0,
        description TEXT,
        resolution_notes TEXT,
        customer_access_token TEXT
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

    # Schema migration check: ensure customer_access_token exists
    c.execute("PRAGMA table_info(tickets)")
    columns = [col[1] for col in c.fetchall()]
    if "customer_access_token" not in columns:
        c.execute("ALTER TABLE tickets ADD COLUMN customer_access_token TEXT")
        conn.commit()

    # Seed default L1 agent account if users table is empty
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        admin_pass = get_or_create_bootstrap_password(creds_file)
        pwd_hash, salt = hash_password(admin_pass)
        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        c.execute("""
        INSERT INTO users (username, full_name, role, password_hash, salt, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """, ("alex.chen", "Alex Chen (L1 Lead)", "agent", pwd_hash, salt, now_str))
        conn.commit()
    else:
        # Check for legacy password hash on existing alex.chen user and rotate safely
        c.execute("SELECT id, username, password_hash, salt FROM users WHERE username = 'alex.chen'")
        alex_row = c.fetchone()
        if alex_row:
            user_id, username, stored_hash, stored_salt = alex_row
            # Check if legacy default password is in use
            if verify_password("NexoraSupport#2026", stored_salt, stored_hash):
                new_pass = secrets.token_urlsafe(16)
                new_hash, new_salt = hash_password(new_pass)
                now_iso = datetime.now(timezone.utc).isoformat()
                
                # Step 1: Safely persist and protect the new credentials FIRST
                dir_name = os.path.dirname(os.path.abspath(creds_file))
                tmp_file = os.path.join(dir_name, f".tmp_mig_{secrets.token_hex(6)}.json")
                try:
                    with open(tmp_file, "w", encoding="utf-8") as f:
                        json.dump({
                            "username": "alex.chen",
                            "bootstrap_password": new_pass,
                            "migrated_at": now_iso,
                            "note": "Migrated from legacy credentials. Local secret store protected by OS ACLs."
                        }, f, indent=2)
                    protect_local_file(tmp_file)
                    if os.path.exists(creds_file):
                        os.replace(tmp_file, creds_file)
                    else:
                        os.rename(tmp_file, creds_file)
                    protect_local_file(creds_file)
                except Exception as e:
                    if os.path.exists(tmp_file):
                        try: os.unlink(tmp_file)
                        except Exception: pass
                    conn.close()
                    raise RuntimeError(f"Cannot safely persist migrated credentials to {creds_file}; aborting credential rotation: {e}")

                # Step 2: Update users table only after verified persistence
                c.execute("UPDATE users SET password_hash = ?, salt = ? WHERE id = ?", (new_hash, new_salt, user_id))
                conn.commit()

    # Check if seed tickets exist
    c.execute("SELECT COUNT(*) FROM tickets")
    count = c.fetchone()[0]
    if count == 0:
        seed_tickets(conn)
    else:
        # Ensure any tickets missing customer_access_token get one generated
        c.execute("SELECT id FROM tickets WHERE customer_access_token IS NULL OR customer_access_token = ''")
        missing_tokens = c.fetchall()
        for row in missing_tokens:
            token = secrets.token_urlsafe(24)
            c.execute("UPDATE tickets SET customer_access_token = ? WHERE id = ?", (token, row[0]))
        if missing_tokens:
            conn.commit()

    conn.close()

def parse_iso_datetime(dt_str: str) -> datetime:
    """Parses various datetime string formats into UTC-aware datetime objects."""
    if not dt_str:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            dt = datetime.strptime(dt_str.strip(), fmt)
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None

def compute_ticket_sla(ticket: dict, now: datetime = None) -> dict:
    """Computes dynamic elapsed hours, remaining hours, and breach status."""
    if not now:
        now = datetime.now(timezone.utc)
    
    created_dt = parse_iso_datetime(ticket.get("created_at"))
    target_hours = float(ticket.get("sla_target_hours", 72.0))
    status = ticket.get("status", "New")
    resolved_dt = parse_iso_datetime(ticket.get("resolved_at"))
    
    if status in ("Resolved", "Closed") and resolved_dt and created_dt:
        elapsed = max(0.0, (resolved_dt - created_dt).total_seconds() / 3600.0)
        remaining = 0.0
        breached = elapsed > target_hours
    elif created_dt:
        elapsed = max(0.0, (now - created_dt).total_seconds() / 3600.0)
        remaining = max(0.0, target_hours - elapsed)
        breached = elapsed > target_hours
    else:
        elapsed = 0.0
        remaining = target_hours
        breached = False

    is_at_risk = (not breached) and (status not in ("Resolved", "Closed")) and (elapsed >= 0.75 * target_hours)

    ticket_copy = dict(ticket)
    ticket_copy["elapsed_hours"] = round(elapsed, 2)
    ticket_copy["remaining_hours"] = round(remaining, 2)
    ticket_copy["sla_breached"] = 1 if breached else 0
    ticket_copy["sla_at_risk"] = 1 if is_at_risk else 0
    ticket_copy["sla_status"] = "Breached" if breached else ("At Risk" if is_at_risk else "Within SLA")
    return ticket_copy

def seed_tickets(conn):
    c = conn.cursor()
    base_time = datetime(2024, 11, 10, 9, 0, 0, tzinfo=timezone.utc)
    
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
        due_str = (created_dt + timedelta(hours=target_hours)).strftime("%Y-%m-%d %H:%M:%S")
        resolved_str = (created_dt + timedelta(hours=res_hours)).strftime("%Y-%m-%d %H:%M:%S") if status == "Resolved" else None
        breached_val = 1 if (res_hours > target_hours) else 0
        customer_tok = secrets.token_urlsafe(24)
        
        c.execute("""
        INSERT INTO tickets (
            key, title, request_type, caller_name, caller_email, department,
            impact, urgency, priority, status, assigned_to, assignment_group,
            created_at, updated_at, resolved_at, due_at, sla_target_hours, sla_breached,
            description, resolution_notes, customer_access_token
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            key, title, req_type, caller, email, dept,
            impact, urgency, priority, status, assignee, group,
            created_str, created_str, resolved_str, due_str, target_hours, breached_val,
            f"User reported: {title}", notes, customer_tok
        ))
        
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
    db_path = DEFAULT_DB_FILE

    def get_session(self):
        """Extracts and validates session token from Cookie or X-Session-Token header."""
        auth_header = self.headers.get("X-Session-Token")
        if auth_header and auth_header in ACTIVE_SESSIONS:
            sess = ACTIVE_SESSIONS[auth_header]
            if sess["expires"] > datetime.now(timezone.utc):
                return sess
            else:
                del ACTIVE_SESSIONS[auth_header]

        cookie_header = self.headers.get("Cookie")
        if cookie_header:
            cookies = urllib.parse.parse_qs(cookie_header.replace("; ", "&"))
            token = cookies.get("nexora_session", [None])[0]
            if token and token in ACTIVE_SESSIONS:
                sess = ACTIVE_SESSIONS[token]
                if sess["expires"] > datetime.now(timezone.utc):
                    return sess
                else:
                    del ACTIVE_SESSIONS[token]
        return None

    def require_agent_auth(self):
        """Verifies caller is an authenticated agent or admin, sending 401 JSON if not."""
        sess = self.get_session()
        if not sess or sess.get("role") not in ("agent", "admin"):
            self.send_json({"status": "error", "message": "Authentication required. Please sign in with an agent account."}, 401)
            return None
        return sess

    def is_valid_origin_url(self, url_str: str) -> bool:
        """Validates that a URL matches the allowed scheme, hostname, and server port."""
        if not url_str:
            return False
        try:
            parsed = urllib.parse.urlparse(url_str)
            
            # Require origin scheme to match the actual server scheme (reject HTTPS when serving HTTP)
            expected_scheme = "https" if getattr(self.server, "is_ssl", False) else "http"
            if parsed.scheme != expected_scheme:
                return False

            # Validate hostname: must be localhost, 127.0.0.1, or bound server host
            allowed_hosts = {"127.0.0.1", "localhost"}
            server_host = self.server.server_address[0]
            if server_host and server_host != "0.0.0.0":
                allowed_hosts.add(server_host)
                
            if not parsed.hostname or parsed.hostname not in allowed_hosts:
                return False

            # Validate port: must match server listening port exactly
            server_port = self.server.server_address[1]
            try:
                origin_port = parsed.port if parsed.port is not None else (80 if parsed.scheme == "http" else 443)
            except (ValueError, TypeError):
                # Malformed port (e.g. non-integer or > 65535)
                return False

            if origin_port != server_port:
                return False

            return True
        except Exception:
            return False

    def verify_csrf_and_origin(self) -> bool:
        """
        Enforces same-origin request verification on mutating POST endpoints.
        Validates the complete allowed origin including scheme, hostname, and port.
        Rejects cross-origin POSTs, port mismatches (e.g. port 9000 vs 8080),
        unexpected schemes (e.g. HTTPS when serving HTTP, or ftp://),
        invalid ports, untrusted hostnames, or missing Origin and Referer headers.
        Returns a controlled HTTP 403 Forbidden without throwing uncaught exceptions.
        """
        try:
            origin = self.headers.get("Origin")
            referer = self.headers.get("Referer")

            # Mutating requests require either an Origin or Referer header
            if not origin and not referer:
                self.send_json({"status": "error", "message": "Forbidden: Origin or Referer header required for mutating request."}, 403)
                return False

            if origin:
                if not self.is_valid_origin_url(origin):
                    self.send_json({"status": "error", "message": "Forbidden: Untrusted, cross-origin or malformed Origin header."}, 403)
                    return False

            if referer:
                if not self.is_valid_origin_url(referer):
                    self.send_json({"status": "error", "message": "Forbidden: Untrusted, cross-origin or malformed Referer header."}, 403)
                    return False

            return True
        except Exception as e:
            self.send_json({"status": "error", "message": f"Forbidden: Malformed request origin ({type(e).__name__})."}, 403)
            return False

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)
        
        if path == "/" or path == "/portal":
            self.serve_portal()
        elif path == "/agent":
            self.serve_agent_console()
        elif path == "/api/auth/status":
            self.api_auth_status()
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
        if not self.verify_csrf_and_origin():
            return

        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        try:
            length = int(self.headers.get('content-length', 0))
        except (ValueError, TypeError):
            length = 0

        if length > MAX_PAYLOAD_SIZE:
            self.send_json({"status": "error", "message": f"Payload too large (Max {MAX_PAYLOAD_SIZE} bytes)"}, 413)
            return

        body = self.rfile.read(length).decode('utf-8', errors='replace')
        try:
            data = json.loads(body)
        except Exception:
            data = urllib.parse.parse_qs(body)
            data = {k: v[0] for k, v in data.items()}
            
        if path == "/api/auth/login":
            self.api_login(data)
        elif path == "/api/auth/logout":
            self.api_logout()
        elif path == "/api/tickets":
            self.api_create_ticket(data)
        elif path == "/api/ticket/update":
            self.api_update_ticket(data)
        elif path == "/api/ticket/comment":
            self.api_add_comment(data)
        else:
            self.send_error(404, "Endpoint not found")

    def api_login(self, data):
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        
        if not username or not password:
            self.send_json({"status": "error", "message": "Username and password are required"}, 400)
            return

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT id, username, full_name, role, password_hash, salt FROM users WHERE username = ?", (username,))
        row = c.fetchone()
        conn.close()
        
        if row and verify_password(password, row[5], row[4]):
            token = secrets.token_hex(24)
            expires = datetime.now(timezone.utc) + timedelta(hours=8)
            ACTIVE_SESSIONS[token] = {
                "username": row[1],
                "full_name": row[2],
                "role": row[3],
                "expires": expires
            }
            cookie = f"nexora_session={token}; Path=/; HttpOnly; SameSite=Strict"
            self.send_json({"status": "success", "token": token, "user": {"username": row[1], "full_name": row[2], "role": row[3]}}, headers=[("Set-Cookie", cookie)])
        else:
            self.send_json({"status": "error", "message": "Invalid username or password"}, 401)

    def api_logout(self):
        token = None
        cookie_header = self.headers.get("Cookie")
        if cookie_header:
            cookies = urllib.parse.parse_qs(cookie_header.replace("; ", "&"))
            token = cookies.get("nexora_session", [None])[0]
        if not token:
            token = self.headers.get("X-Session-Token")
            
        if token and token in ACTIVE_SESSIONS:
            del ACTIVE_SESSIONS[token]
            
        cookie = "nexora_session=deleted; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT"
        self.send_json({"status": "success", "message": "Logged out successfully"}, headers=[("Set-Cookie", cookie)])

    def api_auth_status(self):
        sess = self.get_session()
        if sess:
            self.send_json({"authenticated": True, "user": {"username": sess["username"], "full_name": sess["full_name"], "role": sess["role"]}})
        else:
            self.send_json({"authenticated": False})

    def api_get_tickets(self, query):
        sess = self.require_agent_auth()
        if not sess:
            return

        queue = query.get("queue", ["all"])[0]
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        c.execute("SELECT * FROM tickets ORDER BY id DESC")
        all_rows = [dict(r) for r in c.fetchall()]
        conn.close()
        
        now = datetime.now(timezone.utc)
        computed_tickets = [compute_ticket_sla(t, now) for t in all_rows]
        
        current_user = sess["full_name"]

        if queue == "unassigned":
            filtered = [t for t in computed_tickets if not t.get("assigned_to") or t.get("assigned_to") == "Unassigned"]
        elif queue == "assigned_me":
            filtered = [t for t in computed_tickets if t.get("assigned_to") and ("Alex Chen" in t.get("assigned_to") or current_user in t.get("assigned_to"))]
        elif queue == "p1":
            filtered = [t for t in computed_tickets if t.get("priority") == "P1" and t.get("status") != "Closed"]
        elif queue == "p2":
            filtered = [t for t in computed_tickets if t.get("priority") == "P2" and t.get("status") != "Closed"]
        elif queue == "wait_customer":
            filtered = [t for t in computed_tickets if t.get("status") == "Waiting for Customer"]
        elif queue == "wait_vendor":
            filtered = [t for t in computed_tickets if t.get("status") == "Waiting for Vendor"]
        elif queue == "sla_risk":
            filtered = [t for t in computed_tickets if t.get("sla_at_risk") == 1]
        elif queue == "sla_breached":
            filtered = [t for t in computed_tickets if t.get("sla_breached") == 1]
        elif queue == "resolved":
            filtered = [t for t in computed_tickets if t.get("status") in ("Resolved", "Closed")]
        else: # 'all'
            filtered = computed_tickets
            
        self.send_json({"status": "success", "queue": queue, "count": len(filtered), "tickets": filtered})

    def api_get_ticket(self, query):
        key = query.get("key", [""])[0].strip()
        customer_token = query.get("token", [""])[0].strip()

        if not key:
            self.send_json({"status": "error", "message": "Missing ticket key"}, 400)
            return

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM tickets WHERE key = ?", (key,))
        ticket = c.fetchone()
        if not ticket:
            conn.close()
            self.send_json({"status": "error", "message": "Ticket not found"}, 404)
            return
            
        ticket_dict = dict(ticket)
        sess = self.get_session()
        is_agent = sess and sess.get("role") in ("agent", "admin")

        # Security check: if not agent, customer must provide matching customer_access_token
        if not is_agent:
            stored_token = ticket_dict.get("customer_access_token")
            if not customer_token or not stored_token or not secrets.compare_digest(customer_token, stored_token):
                conn.close()
                self.send_json({"status": "error", "message": "Access denied. Valid agent session or ticket-specific customer token required."}, 401)
                return

        ticket_data = compute_ticket_sla(ticket_dict)
        c.execute("SELECT * FROM ticket_activity WHERE ticket_key = ? ORDER BY id ASC", (key,))
        activities = [dict(r) for r in c.fetchall()]
        conn.close()
        
        # Strip internal work notes and security tokens from customer view
        if not is_agent:
            activities = [a for a in activities if a["activity_type"] != "WORK_NOTE"]
            ticket_data.pop("customer_access_token", None)
            
        ticket_data["activities"] = activities
        self.send_json({"status": "success", "ticket": ticket_data})

    def api_create_ticket(self, data):
        # Input Validation
        title = data.get("title", "").strip()
        caller_name = data.get("caller_name", "").strip()
        caller_email = data.get("caller_email", "").strip()
        department = data.get("department", "Operations").strip()
        request_type = data.get("request_type", "General IT Request").strip()
        impact = data.get("impact", "Medium").strip()
        urgency = data.get("urgency", "Medium").strip()
        description = data.get("description", "").strip()
        
        if not title or not caller_name or not caller_email:
            self.send_json({"status": "error", "message": "Missing required fields: title, caller_name, and caller_email are mandatory."}, 400)
            return

        if len(title) < 3 or len(title) > 200:
            self.send_json({"status": "error", "message": "Title must be between 3 and 200 characters."}, 400)
            return

        if len(caller_name) < 2 or len(caller_name) > 100:
            self.send_json({"status": "error", "message": "Caller name must be between 2 and 100 characters."}, 400)
            return

        if len(caller_email) > 120 or not EMAIL_REGEX.match(caller_email):
            self.send_json({"status": "error", "message": "Invalid email address format."}, 400)
            return

        if len(description) > 4000:
            self.send_json({"status": "error", "message": "Description exceeds maximum length of 4000 characters."}, 400)
            return

        if department not in VALID_DEPARTMENTS:
            department = "Operations"
            
        if impact not in ("High", "Medium", "Low"):
            impact = "Medium"
        if urgency not in ("High", "Medium", "Low"):
            urgency = "Medium"
            
        priority = PRIORITY_MATRIX.get((impact, urgency), "P3")
        target_hours = SLA_POLICY[priority]["hours"]
        now_dt = datetime.now(timezone.utc)
        now_str = now_dt.strftime("%Y-%m-%d %H:%M:%S")
        due_str = (now_dt + timedelta(hours=target_hours)).strftime("%Y-%m-%d %H:%M:%S")
        customer_token = secrets.token_urlsafe(24)
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT MAX(id) FROM tickets")
        max_id = c.fetchone()[0] or 100
        new_key = f"NEX-{max_id + 1}"
        
        c.execute("""
        INSERT INTO tickets (
            key, title, request_type, caller_name, caller_email, department,
            impact, urgency, priority, status, assigned_to, assignment_group,
            created_at, updated_at, due_at, sla_target_hours, sla_breached, description, customer_access_token
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            new_key, title, request_type, caller_name, caller_email, department,
            impact, urgency, priority, "New", "Unassigned", "L1 Service Desk",
            now_str, now_str, due_str, target_hours, 0, description, customer_token
        ))
        
        c.execute("""
        INSERT INTO ticket_activity (ticket_key, timestamp, author, activity_type, message)
        VALUES (?, ?, ?, ?, ?)
        """, (new_key, now_str, caller_name, "CUSTOMER_COMMENT", "Ticket submitted via Nexora Customer Portal"))
        
        conn.commit()
        conn.close()
        self.send_json({
            "status": "success",
            "key": new_key,
            "customer_access_token": customer_token,
            "priority": priority,
            "target_hours": target_hours,
            "due_at": due_str
        })

    def api_update_ticket(self, data):
        sess = self.require_agent_auth()
        if not sess:
            return
            
        key = data.get("key", "").strip()
        new_status = data.get("status", "").strip()
        assigned_to = data.get("assigned_to")
        resolution = data.get("resolution_notes")
        author = sess["full_name"]
        now_dt = datetime.now(timezone.utc)
        now_str = now_dt.strftime("%Y-%m-%d %H:%M:%S")
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM tickets WHERE key = ?", (key,))
        ticket = c.fetchone()
        if not ticket:
            conn.close()
            self.send_json({"status": "error", "message": "Ticket not found"}, 404)
            return
            
        current_status = ticket["status"]
        
        # State machine transition enforcement
        if new_status and new_status != current_status:
            allowed = ALLOWED_TRANSITIONS.get(current_status, [])
            if new_status not in allowed:
                conn.close()
                self.send_json({
                    "status": "error",
                    "message": f"Illegal state transition from '{current_status}' to '{new_status}'. Allowed transitions: {', '.join(allowed)}."
                }, 400)
                return
                
            if new_status == "Resolved" and (not resolution or not resolution.strip()):
                conn.close()
                self.send_json({
                    "status": "error",
                    "message": "Resolution notes are mandatory when marking ticket as Resolved."
                }, 400)
                return

        updates = ["updated_at = ?"]
        params = [now_str]
        
        if new_status:
            updates.append("status = ?")
            params.append(new_status)
            
            # Reopening: Transitioning from Resolved or Closed back to In Progress
            if new_status == "In Progress" and current_status in ("Resolved", "Closed"):
                updates.append("resolved_at = NULL")
                # Continuous clock elapsed SLA evaluation:
                # Reopening resumes measuring continuous elapsed clock hours from created_at
                created_dt = parse_iso_datetime(ticket["created_at"])
                if created_dt:
                    elapsed = (now_dt - created_dt).total_seconds() / 3600.0
                    breached = 1 if (elapsed > float(ticket["sla_target_hours"])) else 0
                    updates.append("sla_breached = ?")
                    params.append(breached)
            
            # Resolution: Transitioning to Resolved or Closed
            elif new_status == "Resolved":
                updates.append("resolved_at = ?")
                params.append(now_str)
                # Compute elapsed hours against continuous clock
                created_dt = parse_iso_datetime(ticket["created_at"])
                if created_dt:
                    elapsed = (now_dt - created_dt).total_seconds() / 3600.0
                    breached = 1 if (elapsed > float(ticket["sla_target_hours"])) else 0
                    updates.append("sla_breached = ?")
                    params.append(breached)

        if assigned_to is not None:
            updates.append("assigned_to = ?")
            params.append(assigned_to)
        if resolution is not None:
            updates.append("resolution_notes = ?")
            params.append(resolution.strip())
            
        params.append(key)
        c.execute(f"UPDATE tickets SET {', '.join(updates)} WHERE key = ?", params)
        
        if new_status == "In Progress" and current_status in ("Resolved", "Closed"):
            msg = f"Ticket Reopened by technician {author}. Previous resolution reset; ticket returned to In Progress."
        elif new_status and resolution:
            msg = f"Transitioned to {new_status}: {resolution}"
        elif new_status:
            msg = f"Transitioned to {new_status}"
        else:
            msg = "Ticket details updated"

        c.execute("""
        INSERT INTO ticket_activity (ticket_key, timestamp, author, activity_type, message)
        VALUES (?, ?, ?, ?, ?)
        """, (key, now_str, author, "STATUS_CHANGE", msg))
        
        conn.commit()
        conn.close()
        self.send_json({"status": "success", "message": msg, "current_status": new_status or current_status})

    def api_add_comment(self, data):
        key = data.get("key", "").strip()
        comment_type = data.get("type", "CUSTOMER_COMMENT").strip()
        message = data.get("message", "").strip()
        token = data.get("customer_access_token", "").strip()
        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        
        if not key or not message:
            self.send_json({"status": "error", "message": "Ticket key and comment message cannot be empty"}, 400)
            return

        if len(message) > 2000:
            self.send_json({"status": "error", "message": "Comment message exceeds 2000 character limit"}, 400)
            return

        if comment_type not in ("WORK_NOTE", "CUSTOMER_COMMENT"):
            self.send_json({"status": "error", "message": "Invalid comment type"}, 400)
            return

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM tickets WHERE key = ?", (key,))
        ticket = c.fetchone()
        if not ticket:
            conn.close()
            self.send_json({"status": "error", "message": "Ticket not found"}, 404)
            return

        sess = self.get_session()
        is_agent = sess and sess.get("role") in ("agent", "admin")

        if comment_type == "WORK_NOTE":
            if not is_agent:
                conn.close()
                self.send_json({"status": "error", "message": "Agent authentication required to post internal work notes"}, 401)
                return
            author = sess["full_name"]
        else:
            # Customer comment
            if is_agent:
                author = sess["full_name"]
            else:
                stored_token = ticket["customer_access_token"]
                if not token or not stored_token or not secrets.compare_digest(token, stored_token):
                    conn.close()
                    self.send_json({"status": "error", "message": "Access denied. Valid customer token required to add comment."}, 401)
                    return
                author = ticket["caller_name"]  # Disallow caller impersonation

        c.execute("""
        INSERT INTO ticket_activity (ticket_key, timestamp, author, activity_type, message)
        VALUES (?, ?, ?, ?, ?)
        """, (key, now_str, author, comment_type, message))
        c.execute("UPDATE tickets SET updated_at = ? WHERE key = ?", (now_str, key))
        conn.commit()
        conn.close()
        self.send_json({"status": "success", "message": f"{comment_type} recorded successfully"})

    def api_get_stats(self):
        sess = self.require_agent_auth()
        if not sess:
            return

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM tickets")
        tickets = [dict(r) for r in c.fetchall()]
        conn.close()
        
        now = datetime.now(timezone.utc)
        computed = [compute_ticket_sla(t, now) for t in tickets]
        
        total = len(computed)
        resolved = len([t for t in computed if t["status"] in ("Resolved", "Closed")])
        open_count = total - resolved
        p1_open = len([t for t in computed if t["priority"] == "P1" and t["status"] not in ("Resolved", "Closed")])
        sla_breached_count = len([t for t in computed if t["sla_breached"] == 1])
        sla_at_risk_count = len([t for t in computed if t["sla_at_risk"] == 1])
        
        within_sla = len([t for t in computed if t["sla_breached"] == 0])
        sla_compliance = f"{(within_sla / total * 100):.1f}%" if total > 0 else "100.0%"
        
        self.send_json({
            "total_tickets": total,
            "resolved_tickets": resolved,
            "open_backlog": open_count,
            "p1_critical_open": p1_open,
            "sla_breached_count": sla_breached_count,
            "sla_at_risk_count": sla_at_risk_count,
            "sla_compliance_rate": sla_compliance,
            "resolved_ticket_share": f"{(resolved/total*100):.1f}%" if total > 0 else "0.0%"
        })

    def api_export_tickets(self):
        sess = self.require_agent_auth()
        if not sess:
            return

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM tickets ORDER BY id ASC")
        rows = [dict(r) for r in c.fetchall()]
        conn.close()
        now = datetime.now(timezone.utc)
        computed = [compute_ticket_sla(r, now) for r in rows]
        self.send_json({"export_timestamp": now.isoformat(), "count": len(computed), "tickets": computed})

    def send_security_headers(self, content_type: str = "text/html; charset=utf-8"):
        """Emits standard security response headers across HTML and API responses."""
        self.send_header('Content-Type', content_type)
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'SAMEORIGIN')
        self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self';")

    def send_json(self, data, code=200, headers=None):
        body = json.dumps(data, indent=2).encode('utf-8')
        self.send_response(code)
        self.send_security_headers('application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        if headers:
            for k, v in headers:
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def serve_portal(self):
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Nexora Technologies | IT Help Center</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  :root { --primary: #0052cc; --primary-dark: #0747a6; --bg: #f4f5f7; --card: #ffffff; --text: #172b4d; --border: #dfe1e6; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 0; }
  header { background: var(--primary); color: white; padding: 18px 36px; display: flex; justify-content: space-between; align-items: center; }
  header h1 { margin: 0; font-size: 20px; font-weight: 600; }
  header a { color: white; text-decoration: none; font-size: 13px; background: rgba(255,255,255,0.2); padding: 8px 14px; border-radius: 4px; font-weight: 500; }
  header a:hover { background: rgba(255,255,255,0.3); }
  .container { max-width: 1000px; margin: 30px auto; padding: 0 20px; }
  .hero { text-align: center; margin-bottom: 30px; }
  .hero h2 { font-size: 26px; margin-bottom: 6px; }
  .hero p { color: #5e6c84; font-size: 15px; margin-top: 0; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 18px; }
  .card { background: var(--card); border: 1px solid var(--border); border-radius: 6px; padding: 20px; cursor: pointer; transition: all 0.2s; }
  .card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.08); border-color: var(--primary); }
  .card h3 { margin-top: 0; font-size: 17px; color: var(--primary); }
  .card p { color: #5e6c84; font-size: 13px; line-height: 1.4; margin-bottom: 0; }
  .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); align-items: center; justify-content: center; z-index: 1000; }
  .modal.active { display: flex; }
  .modal-content { background: white; width: 500px; border-radius: 8px; padding: 26px; box-shadow: 0 8px 24px rgba(0,0,0,0.15); max-height: 90vh; overflow-y: auto; }
  .form-group { margin-bottom: 14px; }
  .form-group label { display: block; font-size: 12px; font-weight: 600; margin-bottom: 4px; color: #344563; }
  .form-group input, .form-group select, .form-group textarea { width: 100%; padding: 8px 10px; border: 1px solid var(--border); border-radius: 4px; box-sizing: border-box; font-size: 13px; }
  .form-row { display: flex; gap: 12px; }
  .form-row .form-group { flex: 1; }
  .btn { background: var(--primary); color: white; border: none; padding: 9px 18px; border-radius: 4px; font-size: 13px; font-weight: 600; cursor: pointer; }
  .btn:hover { background: var(--primary-dark); }
  .btn-cancel { background: #ebecf0; color: #42526e; margin-left: 8px; }
  .alert-success { background: #e3fcef; border: 1px solid #abf5d1; color: #006644; padding: 12px; border-radius: 4px; margin-bottom: 16px; display: none; }
  .track-box { background: white; border: 1px solid var(--border); border-radius: 6px; padding: 18px; margin-bottom: 24px; display: flex; gap: 12px; align-items: flex-end; }
</style>
</head>
<body>
<header>
  <div><h1>Nexora Technologies</h1><small>IT Operations & Support Services (Port 8080 - Localhost)</small></div>
  <a href="/agent">L1 Agent Console &rarr;</a>
</header>
<div class="container">
  <div class="hero">
    <h2>Welcome to the IT Service Portal</h2>
    <p>Select a service request category below to submit an incident or track existing requests.</p>
  </div>
  <div id="success-banner" class="alert-success"></div>

  <div class="track-box">
    <div style="flex:1;">
      <label style="font-size:12px; font-weight:600; color:#344563; display:block; margin-bottom:4px;">Track Existing Ticket</label>
      <input type="text" id="trackKey" placeholder="Ticket Key (e.g. NEX-101)" style="width:100%; padding:8px; border:1px solid var(--border); border-radius:4px; box-sizing:border-box;">
    </div>
    <div style="flex:2;">
      <label style="font-size:12px; font-weight:600; color:#344563; display:block; margin-bottom:4px;">Customer Security Token</label>
      <input type="text" id="trackToken" placeholder="Paste Customer Access Token" style="width:100%; padding:8px; border:1px solid var(--border); border-radius:4px; box-sizing:border-box;">
    </div>
    <div>
      <button class="btn" type="button" onclick="trackTicket()">Track Ticket</button>
    </div>
  </div>

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
function escapeHtml(str) {
  if (!str) return '';
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
}
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
    headers: {'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest'},
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  closeModal();
  document.getElementById('ticketForm').reset();
  const banner = document.getElementById('success-banner');
  banner.innerHTML = `<strong>Ticket Logged Successfully!</strong> Ticket ID: <strong>${escapeHtml(data.key)}</strong> | Customer Token: <code style="background:#fff; padding:2px 6px; border-radius:3px;">${escapeHtml(data.customer_access_token)}</code><br><small>Save your customer token to check ticket progress or submit follow-up comments.</small>`;
  banner.style.display = 'block';
  window.scrollTo({top: 0, behavior: 'smooth'});
}
async function trackTicket() {
  const k = document.getElementById('trackKey').value.trim();
  const tok = document.getElementById('trackToken').value.trim();
  if (!k || !tok) { alert('Please enter both Ticket Key and Customer Token'); return; }
  const res = await fetch(`/api/ticket?key=${encodeURIComponent(k)}&token=${encodeURIComponent(tok)}`);
  const data = await res.json();
  if (!res.ok) {
    alert(data.message || 'Access denied');
    return;
  }
  const banner = document.getElementById('success-banner');
  banner.innerHTML = `<strong>Ticket ${escapeHtml(data.ticket.key)}: ${escapeHtml(data.ticket.title)}</strong><br>Status: <strong>${escapeHtml(data.ticket.status)}</strong> | Priority: <strong>${escapeHtml(data.ticket.priority)}</strong> | SLA Elapsed: <strong>${escapeHtml(data.ticket.elapsed_hours)} hrs</strong>`;
  banner.style.display = 'block';
}
</script>
</body>
</html>
"""
        self.send_response(200)
        self.send_security_headers('text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(html_content.encode('utf-8'))))
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

    def serve_agent_console(self):
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Nexora Technologies | L1 Service Desk Console</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  :root { --sidebar: #0747a6; --bg: #f4f5f7; --card: #ffffff; --text: #172b4d; --border: #dfe1e6; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: var(--text); margin: 0; display: flex; height: 100vh; overflow: hidden; }
  aside { width: 250px; background: #0747a6; color: white; display: flex; flex-direction: column; }
  aside .logo { padding: 18px; font-size: 16px; font-weight: 700; border-bottom: 1px solid rgba(255,255,255,0.1); }
  aside .nav-group { padding: 10px 0; overflow-y: auto; flex: 1; }
  aside .nav-title { padding: 0 18px 6px; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.7; }
  aside a { display: flex; justify-content: space-between; align-items: center; padding: 8px 18px; color: white; text-decoration: none; font-size: 13px; opacity: 0.85; }
  aside a:hover, aside a.active { background: rgba(255,255,255,0.15); opacity: 1; font-weight: 600; }
  aside a span.badge { background: rgba(255,255,255,0.25); padding: 1px 6px; border-radius: 10px; font-size: 11px; }
  main { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
  header { background: white; padding: 14px 24px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }
  header h2 { margin: 0; font-size: 18px; }
  .stats-bar { display: flex; gap: 14px; align-items: center; }
  .stat-badge { background: #ebecf0; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 500; }
  .stat-badge strong { color: #0052cc; }
  .user-badge { display: flex; align-items: center; gap: 8px; font-size: 12px; }
  .user-badge button { background: #de350b; color: white; border: none; padding: 4px 8px; border-radius: 3px; cursor: pointer; }
  .content { flex: 1; display: flex; overflow: hidden; }
  .ticket-list { width: 420px; border-right: 1px solid var(--border); overflow-y: auto; background: white; }
  .ticket-item { padding: 12px 16px; border-bottom: 1px solid var(--border); cursor: pointer; }
  .ticket-item:hover, .ticket-item.active { background: #f0f7ff; }
  .ticket-key { font-weight: 700; color: #0052cc; font-size: 13px; }
  .ticket-title { font-size: 13px; font-weight: 600; margin: 3px 0; }
  .ticket-meta { font-size: 11px; color: #5e6c84; display: flex; gap: 8px; }
  .priority-badge { font-size: 11px; padding: 2px 6px; border-radius: 3px; font-weight: 700; }
  .p-P1 { background: #ffebe6; color: #de350b; }
  .p-P2 { background: #fffae6; color: #ff8b00; }
  .p-P3 { background: #e3fcef; color: #006644; }
  .p-P4 { background: #ebecf0; color: #42526e; }
  .sla-badge { font-size: 10px; padding: 1px 5px; border-radius: 3px; font-weight: 600; }
  .sla-breached { background: #ffebe6; color: #de350b; }
  .sla-risk { background: #fffae6; color: #ff8b00; }
  .sla-ok { background: #e3fcef; color: #006644; }
  .ticket-detail { flex: 1; padding: 20px; overflow-y: auto; background: var(--bg); }
  .detail-card { background: white; border: 1px solid var(--border); border-radius: 6px; padding: 18px; margin-bottom: 16px; }
  .action-bar { display: flex; gap: 8px; margin-top: 14px; flex-wrap: wrap; }
  .btn { padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: 600; cursor: pointer; border: 1px solid var(--border); background: white; }
  .btn-primary { background: #0052cc; color: white; border: none; }
  .btn-success { background: #00875a; color: white; border: none; }
  .activity-log { margin-top: 14px; }
  .activity-item { padding: 10px; border-left: 3px solid #0052cc; background: white; margin-bottom: 8px; font-size: 12px; border-radius: 0 4px 4px 0; }
  .act-work-note { border-left-color: #ff8b00; background: #fffbf0; }
  .modal-login { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); align-items: center; justify-content: center; z-index: 2000; }
  .modal-login.active { display: flex; }
  .login-card { background: white; width: 360px; padding: 24px; border-radius: 8px; box-shadow: 0 8px 24px rgba(0,0,0,0.2); }
</style>
</head>
<body>
<aside>
  <div class="logo">Nexora IT Service Desk<br><small style="font-weight:400; opacity:0.8;">L1 Operator Console</small></div>
  <div class="nav-group">
    <div class="nav-title">10 Core Queues</div>
    <a href="#" class="active" onclick="loadQueue('all', this)"><span>All Incidents</span> <span id="q-all" class="badge">0</span></a>
    <a href="#" onclick="loadQueue('unassigned', this)"><span>Unassigned</span> <span id="q-unassigned" class="badge">0</span></a>
    <a href="#" onclick="loadQueue('assigned_me', this)"><span>Assigned to Me</span> <span id="q-assigned_me" class="badge">0</span></a>
    <a href="#" onclick="loadQueue('p1', this)"><span>P1 Critical</span> <span id="q-p1" class="badge">0</span></a>
    <a href="#" onclick="loadQueue('p2', this)"><span>P2 High</span> <span id="q-p2" class="badge">0</span></a>
    <a href="#" onclick="loadQueue('wait_customer', this)"><span>Wait for Customer</span> <span id="q-wait_customer" class="badge">0</span></a>
    <a href="#" onclick="loadQueue('wait_vendor', this)"><span>Wait for Vendor</span> <span id="q-wait_vendor" class="badge">0</span></a>
    <a href="#" onclick="loadQueue('sla_risk', this)"><span>SLA at Risk</span> <span id="q-sla_risk" class="badge">0</span></a>
    <a href="#" onclick="loadQueue('sla_breached', this)"><span>SLA Breached</span> <span id="q-sla_breached" class="badge">0</span></a>
    <a href="#" onclick="loadQueue('resolved', this)"><span>Resolved / Closed</span> <span id="q-resolved" class="badge">0</span></a>
  </div>
  <div style="padding:16px;">
    <a href="/portal" style="padding:8px 12px; background:rgba(255,255,255,0.2); border-radius:4px; text-align:center; display:block;">&larr; Customer Portal</a>
  </div>
</aside>
<main>
  <header>
    <h2 id="queueTitle">All Incidents</h2>
    <div class="stats-bar">
      <div class="stat-badge">Total: <strong id="stTotal">0</strong></div>
      <div class="stat-badge">Open: <strong id="stOpen">0</strong></div>
      <div class="stat-badge">P1: <strong id="stP1" style="color:#de350b;">0</strong></div>
      <div class="stat-badge">SLA: <strong id="stSLA" style="color:#00875a;">100%</strong></div>
      <div id="authProfile" class="user-badge">
        <span id="userNameDisplay">Not Signed In</span>
        <button id="authBtn" onclick="openLoginModal()">Sign In</button>
      </div>
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

<div id="loginModal" class="modal-login">
  <div class="login-card">
    <h3 style="margin-top:0; color:#0052cc;">L1 Technician Login</h3>
    <p style="font-size:12px; color:#5e6c84;">Sign in to access incident queues, apply state transitions, and record internal work notes.</p>
    <div id="loginError" style="color:#de350b; font-size:12px; margin-bottom:10px; display:none;"></div>
    <form onsubmit="handleLogin(event)">
      <div style="margin-bottom:12px;">
        <label style="display:block; font-size:12px; font-weight:600; margin-bottom:4px;">Username</label>
        <input type="text" id="loginUser" placeholder="e.g. alex.chen" required style="width:100%; box-sizing:border-box; padding:8px; border:1px solid #dfe1e6; border-radius:4px;">
      </div>
      <div style="margin-bottom:16px;">
        <label style="display:block; font-size:12px; font-weight:600; margin-bottom:4px;">Password</label>
        <input type="password" id="loginPass" placeholder="Enter agent password" required style="width:100%; box-sizing:border-box; padding:8px; border:1px solid #dfe1e6; border-radius:4px;">
      </div>
      <div style="text-align:right;">
        <button type="button" class="btn" onclick="closeLoginModal()">Cancel</button>
        <button type="submit" class="btn btn-primary">Sign In</button>
      </div>
    </form>
  </div>
</div>

<script>
let currentQueue = 'all';
let selectedKey = null;
let currentUser = null;

function escapeHtml(str) {
  if (!str) return '';
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
}

async function checkAuth() {
  try {
    const res = await fetch('/api/auth/status');
    const d = await res.json();
    if (d.authenticated) {
      currentUser = d.user;
      document.getElementById('userNameDisplay').innerText = currentUser.full_name;
      document.getElementById('authBtn').innerText = 'Sign Out';
      document.getElementById('authBtn').onclick = handleLogout;
    } else {
      currentUser = null;
      document.getElementById('userNameDisplay').innerText = 'Not Signed In';
      document.getElementById('authBtn').innerText = 'Sign In';
      document.getElementById('authBtn').onclick = openLoginModal;
    }
  } catch (e) {
    console.error('Auth check error:', e);
  }
}

function openLoginModal() { document.getElementById('loginModal').classList.add('active'); }
function closeLoginModal() { document.getElementById('loginModal').classList.remove('active'); }

async function handleLogin(e) {
  e.preventDefault();
  const u = document.getElementById('loginUser').value.trim();
  const p = document.getElementById('loginPass').value.trim();
  const errDiv = document.getElementById('loginError');
  errDiv.style.display = 'none';

  const res = await fetch('/api/auth/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest'},
    body: JSON.stringify({username: u, password: p})
  });
  const data = await res.json();
  if (res.ok && data.status === 'success') {
    closeLoginModal();
    await checkAuth();
    await loadStats();
    await loadQueue(currentQueue);
  } else {
    errDiv.innerText = data.message || 'Invalid username or password';
    errDiv.style.display = 'block';
  }
}

async function handleLogout() {
  await fetch('/api/auth/logout', {
    method: 'POST',
    headers: {'X-Requested-With': 'XMLHttpRequest'}
  });
  await checkAuth();
  document.getElementById('ticketList').innerHTML = '<div style="padding:20px; color:#5e6c84;">Please sign in to view queues.</div>';
  document.getElementById('ticketDetail').innerHTML = '<div style="text-align:center; padding:60px; color:#5e6c84;"><h3>Authentication Required</h3><p>Sign in with an agent account to manage tickets.</p></div>';
}

async function loadStats() {
  if (!currentUser) return;
  try {
    const res = await fetch('/api/stats');
    if (!res.ok) return;
    const s = await res.json();
    document.getElementById('stTotal').innerText = s.total_tickets;
    document.getElementById('stOpen').innerText = s.open_backlog;
    document.getElementById('stP1').innerText = s.p1_critical_open;
    document.getElementById('stSLA').innerText = s.sla_compliance_rate;
  } catch (e) {
    console.error('Failed to load stats:', e);
  }
}

async function loadQueue(queue, elem) {
  if (!currentUser) {
    document.getElementById('ticketList').innerHTML = '<div style="padding:20px; color:#5e6c84;">Please sign in to view incident queues.</div>';
    return;
  }
  currentQueue = queue;
  if (elem) {
    document.querySelectorAll('aside a').forEach(a => a.classList.remove('active'));
    elem.classList.add('active');
  }
  const titles = {
    'all': 'All Incidents',
    'unassigned': 'Unassigned Incidents',
    'assigned_me': 'Assigned to Me',
    'p1': 'P1 - Critical Priority',
    'p2': 'P2 - High Priority',
    'wait_customer': 'Waiting for Customer',
    'wait_vendor': 'Waiting for Vendor',
    'sla_risk': 'SLA at Risk (>75% Elapsed)',
    'sla_breached': 'SLA Breached Incidents',
    'resolved': 'Resolved & Closed Archive'
  };
  document.getElementById('queueTitle').innerText = titles[queue] || 'Incident Queue';

  try {
    const res = await fetch('/api/tickets?queue=' + queue);
    if (!res.ok) {
      if (res.status === 401) { openLoginModal(); }
      return;
    }
    const data = await res.json();
    document.getElementById('q-' + queue).innerText = data.count;

    const listDiv = document.getElementById('ticketList');
    if (data.tickets.length === 0) {
      listDiv.innerHTML = '<div style="padding:20px; text-align:center; color:#5e6c84;">No tickets in this queue.</div>';
      return;
    }

    listDiv.innerHTML = data.tickets.map(t => `
      <div class="ticket-item ${selectedKey === t.key ? 'active' : ''}" onclick="selectTicket('${escapeHtml(t.key)}')">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span class="ticket-key">${escapeHtml(t.key)}</span>
          <span class="priority-badge p-${escapeHtml(t.priority)}">${escapeHtml(t.priority)}</span>
        </div>
        <div class="ticket-title">${escapeHtml(t.title)}</div>
        <div class="ticket-meta">
          <span>${escapeHtml(t.caller_name)} (${escapeHtml(t.department)})</span>
          <span>&bull;</span>
          <span class="sla-badge ${t.sla_breached ? 'sla-breached' : (t.sla_at_risk ? 'sla-risk' : 'sla-ok')}">${escapeHtml(t.sla_status)} (${escapeHtml(t.elapsed_hours)}h / ${escapeHtml(t.sla_target_hours)}h)</span>
        </div>
      </div>
    `).join('');
  } catch (e) {
    console.error('Queue load failure:', e);
  }
}

async function selectTicket(key) {
  selectedKey = key;
  document.querySelectorAll('.ticket-item').forEach(el => el.classList.remove('active'));

  const res = await fetch('/api/ticket?key=' + encodeURIComponent(key));
  if (!res.ok) {
    if (res.status === 401) openLoginModal();
    return;
  }
  const data = await res.json();
  const t = data.ticket;

  const detailDiv = document.getElementById('ticketDetail');
  detailDiv.innerHTML = `
    <div class="detail-card">
      <div style="display:flex; justify-content:space-between; align-items:flex-start;">
        <div>
          <span class="ticket-key" style="font-size:16px;">${escapeHtml(t.key)}</span>
          <span class="priority-badge p-${escapeHtml(t.priority)}" style="margin-left:8px;">${escapeHtml(t.priority)} (${escapeHtml(t.sla_target_hours)}h Target)</span>
          <h2 style="margin:8px 0 4px; font-size:18px;">${escapeHtml(t.title)}</h2>
          <div style="font-size:12px; color:#5e6c84;">
            Caller: <strong>${escapeHtml(t.caller_name)}</strong> (${escapeHtml(t.caller_email)}) &bull; Dept: <strong>${escapeHtml(t.department)}</strong>
          </div>
        </div>
        <div style="text-align:right;">
          <span style="display:inline-block; padding:4px 10px; background:#dfe1e6; border-radius:4px; font-size:12px; font-weight:700;">${escapeHtml(t.status)}</span>
          <div style="margin-top:6px; font-size:11px;" class="sla-badge ${t.sla_breached ? 'sla-breached' : (t.sla_at_risk ? 'sla-risk' : 'sla-ok')}">
            ${escapeHtml(t.sla_status)}: ${escapeHtml(t.elapsed_hours)}h elapsed
          </div>
        </div>
      </div>

      <div style="margin-top:16px; padding:12px; background:#f4f5f7; border-radius:4px; font-size:13px; line-height:1.5;">
        <strong>Description:</strong><br>${escapeHtml(t.description)}
      </div>

      ${t.resolution_notes ? `
        <div style="margin-top:12px; padding:12px; background:#e3fcef; border-left:4px solid #00875a; border-radius:4px; font-size:13px;">
          <strong>Technical Resolution Notes:</strong><br>${escapeHtml(t.resolution_notes)}
        </div>
      ` : ''}

      <div class="action-bar">
        <span style="font-size:12px; font-weight:600; line-height:28px;">Actions:</span>
        <button class="btn" onclick="updateTicketState('${escapeHtml(t.key)}', 'Assigned', 'Alex Chen')">Assign to Me</button>
        <button class="btn" onclick="updateTicketState('${escapeHtml(t.key)}', 'In Progress')">Start Progress</button>
        <button class="btn" onclick="updateTicketState('${escapeHtml(t.key)}', 'Waiting for Customer')">Wait for User</button>
        <button class="btn" onclick="updateTicketState('${escapeHtml(t.key)}', 'Waiting for Vendor')">Wait for Vendor</button>
        <button class="btn btn-success" onclick="promptResolve('${escapeHtml(t.key)}')">Resolve Ticket</button>
        <button class="btn" onclick="updateTicketState('${escapeHtml(t.key)}', 'Closed')">Close</button>
        ${(t.status === 'Resolved' || t.status === 'Closed') ? `<button class="btn" style="background:#ff8b00; color:white;" onclick="reopenTicket('${escapeHtml(t.key)}')">Reopen Ticket</button>` : ''}
      </div>
    </div>

    <div class="detail-card">
      <h3 style="margin-top:0; font-size:14px;">Activity & Communications Trail</h3>
      <div style="display:flex; gap:8px; margin-bottom:12px;">
        <textarea id="commentBox" rows="2" placeholder="Type public comment or internal technician work note..." style="flex:1; padding:8px; border:1px solid #dfe1e6; border-radius:4px; font-size:12px;"></textarea>
        <button class="btn btn-primary" onclick="postComment('${escapeHtml(t.key)}', 'CUSTOMER_COMMENT')">Add Public</button>
        <button class="btn" style="background:#ff8b00; color:white;" onclick="postComment('${escapeHtml(t.key)}', 'WORK_NOTE')">Work Note</button>
      </div>

      <div class="activity-log">
        ${(t.activities || []).map(a => `
          <div class="activity-item ${a.activity_type === 'WORK_NOTE' ? 'act-work-note' : ''}">
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
              <strong>${escapeHtml(a.author)}</strong>
              <span style="color:#5e6c84;">${escapeHtml(a.timestamp)} &bull; ${escapeHtml(a.activity_type)}</span>
            </div>
            <div>${escapeHtml(a.message)}</div>
          </div>
        `).join('')}
      </div>
    </div>
  `;
}

async function updateTicketState(key, status, assignee) {
  const payload = { key: key, status: status };
  if (assignee) payload.assigned_to = assignee;
  const res = await fetch('/api/ticket/update', {
    method: 'POST',
    headers: {'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest'},
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  if (!res.ok) {
    alert(data.message || 'Transition rejected');
    return;
  }
  await loadStats();
  await loadQueue(currentQueue);
  await selectTicket(key);
}

async function promptResolve(key) {
  const notes = prompt('Enter technical resolution notes (mandatory for ITIL compliance):');
  if (!notes) { alert('Resolution aborted: notes are mandatory'); return; }
  const res = await fetch('/api/ticket/update', {
    method: 'POST',
    headers: {'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest'},
    body: JSON.stringify({ key: key, status: 'Resolved', resolution_notes: notes })
  });
  const data = await res.json();
  if (!res.ok) {
    alert(data.message || 'Failed to resolve ticket');
    return;
  }
  await loadStats();
  await loadQueue(currentQueue);
  await selectTicket(key);
}

async function reopenTicket(key) {
  const reason = prompt('Enter reason for reopening ticket:');
  if (!reason) return;
  const res = await fetch('/api/ticket/update', {
    method: 'POST',
    headers: {'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest'},
    body: JSON.stringify({ key: key, status: 'In Progress', resolution_notes: null })
  });
  const data = await res.json();
  if (!res.ok) {
    alert(data.message || 'Failed to reopen ticket');
    return;
  }
  await postComment(key, 'WORK_NOTE', 'Ticket reopened by technician: ' + reason);
  await loadStats();
  await loadQueue(currentQueue);
  await selectTicket(key);
}

async function postComment(key, type, customMsg) {
  if (type === 'WORK_NOTE' && !currentUser) { openLoginModal(); return; }
  const msg = customMsg || document.getElementById('commentBox').value.trim();
  if (!msg) return;
  const res = await fetch('/api/ticket/comment', {
    method: 'POST',
    headers: {'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest'},
    body: JSON.stringify({ key: key, type: type, message: msg })
  });
  if (!res.ok) {
    const data = await res.json();
    alert(data.message || 'Failed to post comment');
    return;
  }
  if (!customMsg && document.getElementById('commentBox')) {
    document.getElementById('commentBox').value = '';
  }
  await selectTicket(key);
}

// Boot sequence
(async () => {
  await checkAuth();
  await loadStats();
  await loadQueue('all');
})();
</script>
</body>
</html>
"""
        self.send_response(200)
        self.send_security_headers('text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(html_content.encode('utf-8'))))
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

def run_server(host=DEFAULT_HOST, port=DEFAULT_PORT, db_path=DEFAULT_DB_FILE):
    init_db(db_path)
    ServiceDeskHandler.db_path = db_path
    
    server_address = (host, port)
    httpd = socketserver.TCPServer(server_address, ServiceDeskHandler)
    print(f"==================================================================")
    print(f"  NEXORA IT SERVICE DESK PLATFORM ONLINE (HARDENED)")
    print(f"  Host Binding:       {host}:{port} (Localhost Only)")
    print(f"  Customer Portal:    http://{host}:{port}/portal")
    print(f"  L1 Agent Console:   http://{host}:{port}/agent")
    print(f"  API Endpoint:       http://{host}:{port}/api/tickets")
    print(f"==================================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down service desk portal.")
        httpd.server_close()

if __name__ == "__main__":
    host = DEFAULT_HOST
    port = DEFAULT_PORT
    db = DEFAULT_DB_FILE
    
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.startswith("--port="):
                port = int(arg.split("=")[1])
            elif arg.startswith("--host="):
                host = arg.split("=")[1]
            elif arg.startswith("--db="):
                db = arg.split("=")[1]
                
    run_server(host=host, port=port, db_path=db)
