# Active Directory Domain Services (AD DS) Fundamentals for L1 Support
**Document ID:** AD-001  
**Audience:** L1 Support Engineers / Service Desk Analysts  
**Scope:** Core Directory Concepts, Architecture, Authentication, Group Policy

---

## 1. What is Active Directory?

Active Directory Domain Services (AD DS) is Microsoft's directory service and identity platform used by enterprises to centrally manage:
- **User Accounts:** Identities, passwords, permissions, department information.
- **Computer Accounts:** Workstations, laptops, servers joined to the domain.
- **Security Groups:** Access control lists for shared folders, applications, and VPNs.
- **Group Policy Objects (GPOs):** Automated system and security configuration pushed across thousands of machines.

In a domain environment, users do not have separate local accounts on each machine. Instead, they authenticate against a centralized **Domain Controller (DC)** using their domain credentials (e.g., `NEXORA\kmurthy` or `kmurthy@nexora.test`).

---

## 2. Nexora Technologies Domain Architecture

```
Forest: nexora.test
  │
  └── Domain: nexora.test
        │
        ├── Domain Controllers:
        │     ├── NEX-DC01 (Primary Domain Controller & DNS - 192.168.20.10)
        │     └── NEX-DC02 (Secondary Domain Controller - 192.168.20.11)
        │
        └── Organizational Units (OU Structure):
              ├── Nexora-Users
              │     ├── HR
              │     ├── Finance
              │     ├── Operations
              │     └── IT-Support
              ├── Nexora-Computers
              │     ├── Laptops
              │     └── Desktops
              ├── Nexora-Groups
              │     ├── Security-Groups
              │     └── Distribution-Lists
              └── Nexora-Servers
```

---

## 3. How Authentication Works: Kerberos vs. NTLM

Understanding the authentication flow is essential for diagnosing access issues:

1. **User logs in:** Enters username and password at the Windows logon screen.
2. **Contact Key Distribution Center (KDC):** The client workstation contacts the Domain Controller (running the Kerberos KDC service on UDP/TCP port 88).
3. **Authentication Ticket (TGT):** If the password hash matches, the KDC issues an encrypted **Ticket Granting Ticket (TGT)** to the workstation.
4. **Service Ticket:** When the user accesses an internal resource (e.g., file server `\\nexfs01\finance` using SMB on port 445), the workstation presents the TGT to the KDC to obtain a **Service Ticket** for that specific file server.
5. **Session Established:** Workstation presents Service Ticket to the file server, which grants access without ever asking the user to type their password again (Single Sign-On).
6. **NTLM Fallback:** If Kerberos fails (e.g., accessing server via raw IP address instead of FQDN, or clock skew > 5 minutes), Windows falls back to older NTLM challenge-response authentication.

---

## 4. Group Policy Basics for L1 Support

Group Policy Objects (GPOs) configure computer and user settings centrally:
- **Computer Configuration:** Applies when the machine boots up (e.g., BitLocker enforcement, Windows Defender firewall rules, corporate Wi-Fi certificates).
- **User Configuration:** Applies when the user logs in (e.g., mapped drive letters, desktop wallpaper, browser bookmarks).

### Essential L1 Group Policy Commands:
Force immediate policy update without waiting for the 90-minute refresh cycle:
```cmd
gpupdate /force
```

Generate a detailed report of all applied GPOs:
```cmd
gpresult /r
```
*Output tells you:* Which GPOs were applied, which were filtered out, and which security groups the current user belongs to.

Export full HTML diagnostic Group Policy report:
```cmd
gpresult /h "C:\Temp\gpresult_report.html"
```
