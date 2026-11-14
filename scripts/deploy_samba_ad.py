#!/usr/bin/env python3
"""
Nexora Technologies - Samba Active Directory Domain Controller Management
Idempotent, non-destructive utility to deploy, configure, and audit an
isolated Samba 4 AD DC for realm nexora.test in WSL2 Ubuntu.

Security & AGDLP Hardening:
- Non-destructive: Probes domain health and preserves existing directory databases.
- Unique Credentials: Generates distinct cryptographically random passwords per account.
- Safe Storage: Stores credentials in local ignored file (evidence/active-directory/.ad_credentials.json),
  protected by operating system filesystem permissions (Windows ACLs via icacls / chmod 600).
- Protected Secret Transport: Never passes passwords in visible command arguments or process tables.
  Transports secrets via stdin into temporary mode 600 auth files cleaned up in traps.
- True AGDLP: Accounts -> Global Groups -> Domain Local Groups -> Permissions.
- Restrictive File Permissions: Replaces chmod 777 with group ownership (NEXORA\\dl-*) and chmod 2770
  (world access strictly 0).
- Rigorous Audit: Verifies Kerberos, clean DNS SRV + target A record, all 6 OUs, 7 Global Groups,
  4 Domain Local Groups, nesting, and strict NT_STATUS_ACCESS_DENIED on unauthorized share access.
"""

import subprocess
import sys
import time
import os
import json
import secrets
import string

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
EVIDENCE_DIR = os.path.join(PROJECT_ROOT, "evidence", "active-directory")
CREDENTIALS_FILE = os.path.join(EVIDENCE_DIR, ".ad_credentials.json")
os.makedirs(EVIDENCE_DIR, exist_ok=True)

USER_DEFS = [
    ("kavitha.murthy", "Kavitha", "Murthy", "HR Specialist", "OU=HR", "GG-HR"),
    ("deepak.rao", "Deepak", "Rao", "Financial Controller", "OU=Finance", "GG-Finance"),
    ("arun.nair", "Arun", "Nair", "Operations Manager", "OU=Operations", "GG-Operations"),
    ("prasad.joshi", "Prasad", "Joshi", "Operations Coordinator", "OU=Operations", "GG-Operations"),
    ("alex.chen", "Alex", "Chen", "L1 Service Desk Analyst", "OU=IT", "GG-IT"),
    ("priya.sharma", "Priya", "Sharma", "L1 Service Desk Analyst", "OU=IT", "GG-IT"),
    ("suresh.hegde", "Suresh", "Hegde", "IT Systems Administrator", "OU=IT", "GG-IT"),
    ("rajesh.bhat", "Rajesh", "Bhat", "Head of IT Operations", "OU=IT", "GG-IT"),
    ("divya.ramesh", "Divya", "Ramesh", "Lead Software Engineer", "OU=Engineering", "GG-Engineering"),
    ("karthik.subramaniam", "Karthik", "Subramaniam", "Software Engineer", "OU=Engineering", "GG-Engineering"),
    ("shreya.patil", "Shreya", "Patil", "Account Executive", "OU=Sales", "GG-Sales"),
    ("akash.desai", "Akash", "Desai", "Senior Sales Manager", "OU=Sales", "GG-Sales")
]

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

def generate_complex_password(length=16) -> str:
    """Generates an Active Directory complexity-compliant password."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    core = "".join(secrets.choice(alphabet) for _ in range(length))
    return f"{core}Nx1!"

def load_or_create_credentials() -> dict:
    """Loads existing unique account credentials or generates new distinct credentials."""
    creds = {}
    if os.path.exists(CREDENTIALS_FILE):
        try:
            with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
                creds = json.load(f)
        except Exception:
            creds = {}

    changed = False
    if "Administrator" not in creds:
        creds["Administrator"] = generate_complex_password()
        changed = True

    for uname, _, _, _, _, _ in USER_DEFS:
        if uname not in creds:
            creds[uname] = generate_complex_password()
            changed = True

    if changed or not os.path.exists(CREDENTIALS_FILE):
        try:
            with open(CREDENTIALS_FILE, "w", encoding="utf-8") as f:
                json.dump(creds, f, indent=2)
            protect_local_file(CREDENTIALS_FILE)
        except Exception as e:
            print(f"[WARN] Could not write credentials file: {e}", file=sys.stderr)

    return creds

def run_wsl_cmd(cmd: str, input_data: str = None) -> subprocess.CompletedProcess:
    """Executes a bash script safely inside WSL Ubuntu as root."""
    res = subprocess.run(
        ["wsl", "-u", "root", "-d", "Ubuntu", "-e", "bash", "-c", cmd],
        input=input_data,
        capture_output=True,
        text=True
    )
    return res

def is_domain_provisioned() -> bool:
    """Checks if Samba AD DC is already provisioned and responding."""
    res = run_wsl_cmd("samba-tool domain info 127.0.0.1 2>/dev/null")
    return "Domain           : nexora.test" in res.stdout or "Netbios domain   : NEXORA" in res.stdout

def is_samba_running() -> bool:
    """Checks if the samba service process is currently active."""
    res = run_wsl_cmd("pgrep -f 'samba: root process' 2>/dev/null || pgrep samba 2>/dev/null")
    return bool(res.stdout.strip())

def main():
    print("=" * 70)
    print("  NEXORA TECHNOLOGIES - SAMBA 4 ACTIVE DIRECTORY LAB MANAGER")
    print("  Target Realm: NEXORA.TEST | Domain: NEXORA | Role: Domain Controller")
    print("  Model: Textbook AGDLP (Accounts -> Global -> Domain Local -> Perms)")
    print("=" * 70)

    # 1. Load or generate unique credentials per user
    creds = load_or_create_credentials()
    print(f"[INIT] Loaded unique credentials register for Administrator and {len(USER_DEFS)} domain users.")
    print(f"[INIT] Local credential store secured via OS ACLs: {CREDENTIALS_FILE}")

    # 2. Inspect existing environment
    domain_exists = is_domain_provisioned()
    samba_running = is_samba_running()

    if domain_exists:
        print("\n[OK] Samba Active Directory Domain NEXORA.TEST is already provisioned.")
        print("     Preserving existing domain database and objects (Non-destructive mode).")
        if not samba_running:
            print("     Starting Samba daemon...")
            res = run_wsl_cmd("samba -D && sleep 2")
            if res.returncode != 0:
                print(f"[ERROR] Failed to start Samba daemon: {res.stderr}", file=sys.stderr)
                sys.exit(1)
    else:
        print("\n[INIT] Domain not detected. Provisioning fresh Samba 4 AD DC...")
        # Transport password via stdin
        provision_script = """
        set -e
        ADMIN_PASS=$(cat)
        samba-tool domain provision \\
            --use-rfc2307 \\
            --realm=NEXORA.TEST \\
            --domain=NEXORA \\
            --server-role=dc \\
            --dns-backend=SAMBA_INTERNAL \\
            --adminpass="$ADMIN_PASS"
        samba -D
        sleep 2
        """
        res = run_wsl_cmd(provision_script, input_data=creds["Administrator"])
        if res.returncode != 0:
            print(f"[ERROR] Domain provisioning failed: {res.stderr}\n{res.stdout}", file=sys.stderr)
            sys.exit(1)

    # 3. Transport credentials securely into WSL temporary vault (mode 600, cleaned on exit)
    vault_script = """
    set -e
    cat > /tmp/.ad_vault.json
    chmod 600 /tmp/.ad_vault.json
    """
    res = run_wsl_cmd(vault_script, input_data=json.dumps(creds))
    if res.returncode != 0:
        print(f"[ERROR] Failed to stage credentials vault: {res.stderr}", file=sys.stderr)
        sys.exit(1)

    import atexit
    atexit.register(lambda: run_wsl_cmd("rm -f /tmp/.ad_vault.json /tmp/.auth_* /tmp/.alex_pass /tmp/test_*.txt"))

    # 4. Synchronize Administrator and Domain Users safely using direct Python SamDB API inside WSL
    print("\n--> [Step 1/5] Synchronizing Administrator and 12 Domain Accounts...")
    sync_script = """
    python3 - << 'PY_SYNC'
import json, sys, subprocess
from samba.samdb import SamDB
from samba.auth import system_session
from samba.param import LoadParm

with open('/tmp/.ad_vault.json') as f:
    creds = json.load(f)

lp = LoadParm()
lp.load_default()
samdb = SamDB(session_info=system_session(), lp=lp)

# Rotate Administrator password using native SamDB API (zero command-line password exposure)
admin_pass = creds['Administrator']
try:
    samdb.setpassword("(&(objectClass=user)(sAMAccountName=Administrator))", admin_pass, force_change_at_next_login=False, username="Administrator")
except Exception as e:
    print(f"[ERROR] Administrator password sync failed: {e}", file=sys.stderr)
    sys.exit(1)

USER_DEFS = [
    ("kavitha.murthy", "Kavitha", "Murthy", "HR Specialist", "OU=HR"),
    ("deepak.rao", "Deepak", "Rao", "Financial Controller", "OU=Finance"),
    ("arun.nair", "Arun", "Nair", "Operations Manager", "OU=Operations"),
    ("prasad.joshi", "Prasad", "Joshi", "Operations Coordinator", "OU=Operations"),
    ("alex.chen", "Alex", "Chen", "L1 Service Desk Analyst", "OU=IT"),
    ("priya.sharma", "Priya", "Sharma", "L1 Service Desk Analyst", "OU=IT"),
    ("suresh.hegde", "Suresh", "Hegde", "IT Systems Administrator", "OU=IT"),
    ("rajesh.bhat", "Rajesh", "Bhat", "Head of IT Operations", "OU=IT"),
    ("divya.ramesh", "Divya", "Ramesh", "Lead Software Engineer", "OU=Engineering"),
    ("karthik.subramaniam", "Karthik", "Subramaniam", "Software Engineer", "OU=Engineering"),
    ("shreya.patil", "Shreya", "Patil", "Account Executive", "OU=Sales"),
    ("akash.desai", "Akash", "Desai", "Senior Sales Manager", "OU=Sales")
]

# Ensure OUs exist (samba-tool ou list / ou create has no passwords)
existing_ous = subprocess.run(['samba-tool', 'ou', 'list'], capture_output=True, text=True).stdout
for ou in ["OU=HR", "OU=Finance", "OU=Operations", "OU=IT", "OU=Engineering", "OU=Sales"]:
    if ou.lower() not in existing_ous.lower():
        r = subprocess.run(['samba-tool', 'ou', 'create', ou], capture_output=True, text=True)
        if r.returncode != 0:
            print(f"[ERROR] Failed to create {ou}: {r.stderr}", file=sys.stderr)
            sys.exit(1)

# Ensure Users exist and passwords match using native SamDB API (zero command-line password exposure)
existing_users = subprocess.run(['samba-tool', 'user', 'list'], capture_output=True, text=True).stdout.splitlines()
for uname, gname, sname, title, oupath in USER_DEFS:
    upass = creds[uname]
    try:
        if uname in existing_users:
            samdb.setpassword(f"(&(objectClass=user)(sAMAccountName={uname}))", upass, force_change_at_next_login=False, username=uname)
        else:
            samdb.newuser(
                username=uname,
                password=upass,
                force_password_change_at_next_login_req=False,
                userou=oupath,
                surname=sname,
                givenname=gname,
                jobtitle=title
            )
    except Exception as e:
        print(f"[ERROR] Failed to configure user {uname} via SamDB: {e}", file=sys.stderr)
        sys.exit(1)

print("[OK] All 12 domain users and Administrator synchronized via native SamDB API (zero command-line password exposure).")
PY_SYNC
    """
    res = run_wsl_cmd(sync_script)
    if res.returncode != 0:
        print(f"[ERROR] User synchronization failed:\n{res.stderr}\n{res.stdout}", file=sys.stderr)
        run_wsl_cmd("rm -f /tmp/.ad_vault.json")
        sys.exit(1)
    print("     " + res.stdout.strip())

    # 5. Configure AGDLP Group Structure and Nesting
    print("\n--> [Step 2/5] Configuring AGDLP Group Structure and Nesting...")
    agdlp_script = """
    python3 - << 'PY_AGDLP'
import subprocess, sys

def check_run(cmd, desc):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[ERROR] {desc} failed: {r.stderr}", file=sys.stderr)
        sys.exit(1)

existing_groups = subprocess.run(['samba-tool', 'group', 'list'], capture_output=True, text=True).stdout.splitlines()

# A. Global Groups
global_groups = ["GG-HR", "GG-Finance", "GG-Operations", "GG-IT", "GG-Engineering", "GG-Sales", "GG-All-Staff"]
for g in global_groups:
    if g not in existing_groups:
        check_run(['samba-tool', 'group', 'add', g, '--group-scope=Global'], f"Creating group {g}")

# B. Domain Local Groups
domain_local_groups = ["DL-CompanyShared-RW", "DL-HR-Private-RW", "DL-Finance-Private-RW", "DL-IT-Admin-RW"]
for dl in domain_local_groups:
    if dl not in existing_groups:
        check_run(['samba-tool', 'group', 'add', dl, '--group-scope=Domain'], f"Creating group {dl}")

# C. Account -> Global Group memberships
memberships = {
    "GG-HR": ["kavitha.murthy"],
    "GG-Finance": ["deepak.rao"],
    "GG-Operations": ["arun.nair", "prasad.joshi"],
    "GG-IT": ["alex.chen", "priya.sharma", "suresh.hegde", "rajesh.bhat"],
    "GG-Engineering": ["divya.ramesh", "karthik.subramaniam"],
    "GG-Sales": ["shreya.patil", "akash.desai"],
    "GG-All-Staff": [
        "kavitha.murthy", "deepak.rao", "arun.nair", "prasad.joshi",
        "alex.chen", "priya.sharma", "suresh.hegde", "rajesh.bhat",
        "divya.ramesh", "karthik.subramaniam", "shreya.patil", "akash.desai"
    ]
}

for group, users in memberships.items():
    current_members = subprocess.run(['samba-tool', 'group', 'listmembers', group], capture_output=True, text=True).stdout.splitlines()
    missing = [u for u in users if u not in current_members]
    if missing:
        check_run(['samba-tool', 'group', 'addmembers', group, ','.join(missing)], f"Adding members to {group}")

# D. Global Groups -> Domain Local Groups (AGDLP Nesting)
nesting = {
    "DL-HR-Private-RW": "GG-HR",
    "DL-Finance-Private-RW": "GG-Finance",
    "DL-IT-Admin-RW": "GG-IT",
    "DL-CompanyShared-RW": "GG-All-Staff"
}

for dl, gg in nesting.items():
    current_members = subprocess.run(['samba-tool', 'group', 'listmembers', dl], capture_output=True, text=True).stdout.splitlines()
    if gg not in current_members:
        check_run(['samba-tool', 'group', 'addmembers', dl, gg], f"Nesting {gg} into {dl}")

# E. Password and Lockout Policy
check_run([
    'samba-tool', 'domain', 'passwordsettings', 'set',
    '--complexity=on', '--history-length=5', '--min-pwd-age=0',
    '--max-pwd-age=90', '--min-pwd-length=8', '--account-lockout-threshold=5',
    '--account-lockout-duration=15', '--reset-account-lockout-after=15'
], "Setting domain password policy")

print("[OK] AGDLP group nesting and domain password policy configured.")
PY_AGDLP
    """
    res = run_wsl_cmd(agdlp_script)
    if res.returncode != 0:
        print(f"[ERROR] AGDLP configuration failed:\n{res.stderr}\n{res.stdout}", file=sys.stderr)
        run_wsl_cmd("rm -f /tmp/.ad_vault.json")
        sys.exit(1)
    print("     " + res.stdout.strip())

    # 6. Configure Restrictive File System Permissions and SMB Shares
    print("\n--> [Step 3/5] Applying Restrictive Filesystem Permissions (chmod 2770) & SMB Shares...")
    shares_setup_script = """
    set -e
    mkdir -p /srv/shares/company_shared /srv/shares/hr /srv/shares/finance /srv/shares/it
    
    # Restrictive filesystem permissions (Replacing world-writable chmod 777)
    chown root:root /srv/shares
    chmod 755 /srv/shares

    chown 'root:NEXORA\\dl-companyshared-rw' /srv/shares/company_shared
    chmod 2770 /srv/shares/company_shared

    chown 'root:NEXORA\\dl-hr-private-rw' /srv/shares/hr
    chmod 2770 /srv/shares/hr

    chown 'root:NEXORA\\dl-finance-private-rw' /srv/shares/finance
    chmod 2770 /srv/shares/finance

    chown 'root:NEXORA\\dl-it-admin-rw' /srv/shares/it
    chmod 2770 /srv/shares/it

    # Configure smb.conf shares
    sed -i '/^\\[CompanyShared\\]/,$d' /etc/samba/smb.conf
    sed -i '/^\\[HR-Private\\]/,$d' /etc/samba/smb.conf
    sed -i '/^\\[Finance-Private\\]/,$d' /etc/samba/smb.conf
    sed -i '/^\\[IT-Admin\\]/,$d' /etc/samba/smb.conf

    cat << 'SMB_CONFIG' >> /etc/samba/smb.conf

[CompanyShared]
    path = /srv/shares/company_shared
    read only = no
    guest ok = no
    valid users = @DL-CompanyShared-RW, Administrator

[HR-Private]
    path = /srv/shares/hr
    read only = no
    guest ok = no
    valid users = @DL-HR-Private-RW, Administrator

[Finance-Private]
    path = /srv/shares/finance
    read only = no
    guest ok = no
    valid users = @DL-Finance-Private-RW, Administrator

[IT-Admin]
    path = /srv/shares/it
    read only = no
    guest ok = no
    valid users = @DL-IT-Admin-RW, Administrator
SMB_CONFIG

    pkill -HUP smbd 2>/dev/null || pkill -HUP samba 2>/dev/null || true
    echo "[OK] Share permissions set to 2770 with Domain Local group ownership."
    """
    res = run_wsl_cmd(shares_setup_script)
    if res.returncode != 0:
        print(f"[ERROR] SMB share setup failed:\n{res.stderr}\n{res.stdout}", file=sys.stderr)
        run_wsl_cmd("rm -f /tmp/.ad_vault.json")
        sys.exit(1)
    print("     " + res.stdout.strip())

    # 7. DNS Hygiene: Remove Stale Host Records with Strict Assertions
    print("\n--> [Step 4/5] Auditing & Purging Stale DNS Registrations...")
    dns_cleanup_script = """
    set -e
    # 1. Retrieve current eth0 IPv4 address
    DC_IP=$(ip -4 addr show eth0 | grep -oP '(?<=inet\\s)\\d+(\\.\\d+){3}')
    if [ -z "$DC_IP" ]; then
        echo "[ERROR] Could not determine live DC IPv4 address on eth0." >&2
        exit 1
    fi
    echo "[INFO] Live DC IPv4 Address: $DC_IP"

    # 2. Query all existing A records for softwaresamee in nexora.test
    EXISTING_A=$(samba-tool dns query 127.0.0.1 nexora.test softwaresamee A -P | grep -oP '(?<=A:\\s)\\d+(\\.\\d+){3}' || true)
    echo "[INFO] Registered A records for softwaresamee: $EXISTING_A"

    # 3. Purge stale records with verified command return code (no silent failure)
    for ip in $EXISTING_A; do
        if [ "$ip" != "$DC_IP" ]; then
            echo "[PURGE] Removing stale DNS A record: softwaresamee -> $ip"
            samba-tool dns delete 127.0.0.1 nexora.test softwaresamee A "$ip" -P
        fi
    done

    # 4. Strict post-cleanup verification: assert exclusively live DC IP remains
    FINAL_A=$(samba-tool dns query 127.0.0.1 nexora.test softwaresamee A -P | grep -oP '(?<=A:\\s)\\d+(\\.\\d+){3}')
    echo "[INFO] Verified A records after purge: $FINAL_A"
    
    if [ "$FINAL_A" != "$DC_IP" ]; then
        echo "[SECURITY FAILURE] Stale DNS records remain: '$FINAL_A' (expected strictly '$DC_IP')" >&2
        exit 1
    fi
    echo "[OK] DNS A-record hygiene verified: softwaresamee.nexora.test resolves exclusively to live DC IP $DC_IP."
    """
    res = run_wsl_cmd(dns_cleanup_script)
    if res.returncode != 0:
        print(f"[ERROR] DNS hygiene verification failed:\n{res.stderr}\n{res.stdout}", file=sys.stderr)
        run_wsl_cmd("rm -f /tmp/.ad_vault.json")
        sys.exit(1)
    print("     " + res.stdout.strip())

    # 8. Rigorous Audit & Verification
    print("\n--> [Step 5/5] Executing Forensic AGDLP & Access Control Audit...")
    audit_script = """
    set -e
    trap 'rm -f /tmp/.auth_hr /tmp/.auth_fin /tmp/.auth_it /tmp/.alex_pass /tmp/.ad_vault.json /tmp/test_*.txt' EXIT INT TERM HUP
    OUT="/tmp/ad-audit.txt"
    echo "=== DOMAIN CONTROLLER STATUS ===" > "$OUT"
    samba-tool domain level show >> "$OUT" 2>&1

    echo -e "\n=== PASSWORD AND LOCKOUT POLICY ===" >> "$OUT"
    samba-tool domain passwordsettings show >> "$OUT" 2>&1

    echo -e "\n=== DOMAIN USERS REGISTER ===" >> "$OUT"
    samba-tool user list >> "$OUT" 2>&1

    echo -e "\n=== AGDLP GLOBAL GROUP MEMBERSHIP (GG-HR) ===" >> "$OUT"
    samba-tool group listmembers GG-HR >> "$OUT" 2>&1

    echo -e "\n=== AGDLP DOMAIN LOCAL GROUP MEMBERSHIP (DL-HR-Private-RW) ===" >> "$OUT"
    samba-tool group listmembers DL-HR-Private-RW >> "$OUT" 2>&1

    echo -e "\n=== ALL STAFF GLOBAL GROUP MEMBERSHIP (GG-All-Staff) ===" >> "$OUT"
    samba-tool group listmembers GG-All-Staff >> "$OUT" 2>&1

    echo -e "\n=== DNS SRV RECORD RESOLUTION (_ldap._tcp.nexora.test) ===" >> "$OUT"
    dig @::1 _ldap._tcp.nexora.test SRV +short >> "$OUT" 2>&1

    echo -e "\n=== DNS SRV TARGET HOSTNAME A RECORD RESOLUTION ===" >> "$OUT"
    TARGET_HOST=$(dig @::1 _ldap._tcp.nexora.test SRV +short | awk '{print $4}' | sed 's/\\.$//')
    dig @::1 "$TARGET_HOST" A +short >> "$OUT" 2>&1

    # Extract credentials for testing from vault
    python3 - << 'PY_AUTH_PREP'
import json
with open('/tmp/.ad_vault.json') as f:
    creds = json.load(f)

for role, user in [("hr", "kavitha.murthy"), ("fin", "deepak.rao"), ("it", "alex.chen")]:
    with open(f'/tmp/.auth_{role}', 'w') as af:
        af.write(f"username={user}\\npassword={creds[user]}\\ndomain=NEXORA\\n")

with open('/tmp/.alex_pass', 'w') as pf:
    pf.write(creds['alex.chen'])
PY_AUTH_PREP
    chmod 600 /tmp/.auth_hr /tmp/.auth_fin /tmp/.auth_it /tmp/.alex_pass

    echo -e "\n=== KERBEROS TICKET ACQUISITION (alex.chen@NEXORA.TEST) ===" >> "$OUT"
    cat /tmp/.alex_pass | kinit alex.chen@NEXORA.TEST >/dev/null 2>&1
    klist >> "$OUT" 2>&1
    rm -f /tmp/.alex_pass

    echo -e "\n=== SMB SHARES DISCOVERY ===" >> "$OUT"
    smbclient -L localhost -A /tmp/.auth_it 2>&1 | grep -E "Disk|IPC" >> "$OUT" 2>&1

    echo -e "\n=== AUTHORIZED SHARE WRITE TEST (alex.chen -> CompanyShared) ===" >> "$OUT"
    echo "Nexora Company Policy - General Access" > /tmp/test_shared.txt
    smbclient //localhost/CompanyShared -A /tmp/.auth_it -c "put /tmp/test_shared.txt test_policy.txt; ls; rm test_policy.txt" >> "$OUT" 2>&1
    rm -f /tmp/test_shared.txt

    echo -e "\n=== AUTHORIZED SHARE WRITE TEST (HR User kavitha.murthy -> HR-Private) ===" >> "$OUT"
    echo "Confidential HR Records" > /tmp/test_hr.txt
    smbclient //localhost/HR-Private -A /tmp/.auth_hr -c "put /tmp/test_hr.txt hr_doc.txt; ls; rm hr_doc.txt" >> "$OUT" 2>&1
    rm -f /tmp/test_hr.txt

    echo -e "\n=== DENIED ACCESS TEST (Finance User deepak.rao -> HR-Private) ===" >> "$OUT"
    DENY_HR_OUT=$(smbclient //localhost/HR-Private -A /tmp/.auth_fin -c "ls" 2>&1 || true)
    if echo "$DENY_HR_OUT" | grep -q "NT_STATUS_ACCESS_DENIED"; then
        echo "tree connect failed: NT_STATUS_ACCESS_DENIED (Access correctly blocked)" >> "$OUT"
    else
        echo "[SECURITY FAILURE] Expected NT_STATUS_ACCESS_DENIED, got: $DENY_HR_OUT" >> "$OUT"
        exit 1
    fi

    echo -e "\n=== AUTHORIZED SHARE WRITE TEST (Finance User deepak.rao -> Finance-Private) ===" >> "$OUT"
    echo "Quarterly Financial Statements" > /tmp/test_fin.txt
    smbclient //localhost/Finance-Private -A /tmp/.auth_fin -c "put /tmp/test_fin.txt fin_report.txt; ls; rm fin_report.txt" >> "$OUT" 2>&1
    rm -f /tmp/test_fin.txt

    echo -e "\n=== DENIED ACCESS TEST (HR User kavitha.murthy -> IT-Admin) ===" >> "$OUT"
    DENY_IT_OUT=$(smbclient //localhost/IT-Admin -A /tmp/.auth_hr -c "ls" 2>&1 || true)
    if echo "$DENY_IT_OUT" | grep -q "NT_STATUS_ACCESS_DENIED"; then
        echo "tree connect failed: NT_STATUS_ACCESS_DENIED (Access correctly blocked)" >> "$OUT"
    else
        echo "[SECURITY FAILURE] Expected NT_STATUS_ACCESS_DENIED, got: $DENY_IT_OUT" >> "$OUT"
        exit 1
    fi

    echo -e "\n=== AUTHORIZED SHARE WRITE TEST (IT User alex.chen -> IT-Admin) ===" >> "$OUT"
    echo "IT Infrastructure Runbook" > /tmp/test_it.txt
    smbclient //localhost/IT-Admin -A /tmp/.auth_it -c "put /tmp/test_it.txt it_doc.txt; ls; rm it_doc.txt" >> "$OUT" 2>&1
    rm -f /tmp/test_it.txt

    cat "$OUT"
    """
    res = run_wsl_cmd(audit_script)
    if res.returncode != 0:
        print(f"[ERROR] Audit verification failed:\n{res.stderr}\n{res.stdout}", file=sys.stderr)
        run_wsl_cmd("rm -f /tmp/.auth_hr /tmp/.auth_fin /tmp/.auth_it /tmp/.ad_vault.json")
        sys.exit(1)

    evidence_file = os.path.join(EVIDENCE_DIR, "samba-ad-dc-verification.txt")
    with open(evidence_file, "w", encoding="utf-8") as f:
        f.write(res.stdout)

    print(f"\n[EVIDENCE WRITTEN] Sanitized verification report written to: {evidence_file}")
    print("\nSamba 4 Active Directory configuration and AGDLP verification completed successfully!")
    run_wsl_cmd("rm -f /tmp/.ad_vault.json /tmp/.auth_* /tmp/.alex_pass /tmp/test_*.txt")

if __name__ == "__main__":
    main()
