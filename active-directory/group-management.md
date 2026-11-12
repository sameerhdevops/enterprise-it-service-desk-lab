# Active Directory Group Management & Access Control
**Document ID:** AD-003  
**Audience:** L1 Service Desk Analysts  
**Scope:** Security Groups vs. Distribution Groups, Group Scopes, AGDLP Principle

---

## 1. Group Types: Security vs. Distribution

| Group Type | Purpose & Scope | Can Assign Permissions? | Example |
|---|---|---|---|
| **Security Group** | Used to assign access rights to network resources (shared folders, printers, VPN, SharePoint). Can also be used as an email distribution list if mail-enabled. | **YES** (Listed in NTFS and Share Access Control Lists / ACLs). | `FIN-SharedDrive-RW`, `VPN-RemoteUsers`, `IT-Admins` |
| **Distribution Group** | Used exclusively for broadcasting emails to multiple recipients via Microsoft Exchange / Exchange Online. | **NO** (Cannot be added to NTFS ACLs or file permissions). | `All-Employees@nexora.com`, `HR-Announcements@nexora.com` |

---

## 2. Nexora Technologies Group Naming Conventions

Nexora enforces standardized prefixes to ensure clarity during audits:

- `SEC-`: General security roles (e.g., `SEC-MFA-Exempt-Temporary`, `SEC-USB-Storage-Allowed`).
- `DEPT-`: Departmental baseline groups (e.g., `DEPT-Finance`, `DEPT-HR`, `DEPT-Operations`).
- `SHARE-`: File share access permissions (e.g., `SHARE-Finance-ReadWrite`, `SHARE-HR-ReadOnly`).
- `APP-`: Application access roles (e.g., `APP-SAP-GeneralUsers`, `APP-Salesforce-Standard`).
- `DL-`: Distribution lists (e.g., `DL-Bengaluru-Office`).

---

## 3. The AGDLP Best-Practice Principle

When assigning file permissions, ITIL and Microsoft best practices dictate **AGDLP**:
- **A**ccounts are added to...
- **G**lobal groups (representing job roles, e.g., `Global-Finance-Accountants`), which are added to...
- **D**omain **L**ocal groups (representing resource access, e.g., `DL-SharedDrive-Finance-RW`), which receive...
- **P**ermissions (NTFS Read/Write assigned directly to the Domain Local group).

*Why this matters in L1 interviews:* "Using AGDLP means we never assign individual user accounts directly to folder permissions. When a new accountant joins, we simply add their user account to the Global Finance group, and all required shared folder permissions are inherited automatically."

---

## 4. Managing Groups via PowerShell

### Add User to a Group:
```powershell
Add-ADGroupMember -Identity "SHARE-Finance-ReadWrite" -Members "kmurthy"
```

### Remove User from a Group:
```powershell
Remove-ADGroupMember -Identity "SHARE-Finance-ReadWrite" -Members "kmurthy" -Confirm:$false
```

### List All Members of a Group:
```powershell
Get-ADGroupMember -Identity "SHARE-Finance-ReadWrite" | Select-Object Name, SamAccountName, ObjectClass
```
