# Local User & Group Administration Hands-On Lab
**Document ID:** AD-LAB-001
**Audience:** L1 Support Engineer Candidate
**Environment:** Local Windows Host (Windows 10/11)
**Safety Classification:** Read-Only & Isolated Disposable Test Environment

---

## 1. Lab Objective & Architecture Distinction

In enterprise environments with an on-premises domain, user administration is conducted against Active Directory Domain Controllers (`dsa.msc`, `New-ADUser`). In standalone or workgroup machines, Windows uses the **Security Accounts Manager (SAM)** local database (`lusrmgr.msc`, `net user`).

> **Architectural Note:**
> This hands-on lab demonstrates account lifecycle principles, security groups, and NTFS Access Control Lists (ACLs) using Windows local administrative tools without requiring a resource-heavy Windows Server Domain Controller virtual machine.

---

## 2. Viewing Local Users and Groups via GUI & CLI

### Using Computer Management Console:
1. Press `Windows Key + R` > type `compmgmt.msc` > press Enter.
2. Navigate to **System Tools > Local Users and Groups** (`lusrmgr.msc`).
   - Click **Users** to view local accounts.
   - Click **Groups** to view built-in groups (`Administrators`, `Users`, `Remote Desktop Users`).

### Using PowerShell & Command Prompt:
List all local user accounts:
```cmd
net user
```

Inspect specific user details:
```cmd
net user %USERNAME%
```

Inspect local group membership:
```cmd
net localgroup Administrators
```

---

## 3. Practical Exercise: Isolated Disposable Permissions Lab

To safely demonstrate group-based access control and NTFS permissions without affecting production settings, execute this safe exercise in a disposable temporary directory (`$env:TEMP\nexora-test-share`):

### Step 1: Create Test Directory
```powershell
$LabDir = "$env:TEMP\nexora-test-share"
New-Item -ItemType Directory -Path $LabDir -Force | Out-Null
Set-Content -Path "$LabDir\confidential_finance.txt" -Value "Nexora Technologies Q4 Financial Summary - Strictly Confidential"
```

### Step 2: Inspect NTFS Access Control List (ACL) via `icacls`
```cmd
icacls "%TEMP%\nexora-test-share"
```
*Interpretation:* Observe inherited permissions:
- `NT AUTHORITY\SYSTEM:(OI)(CI)(F)` — Full control for OS
- `BUILTIN\Administrators:(OI)(CI)(F)` — Full control for Local Admins
- `BUILTIN\Users:(OI)(CI)(RX)` — Read & Execute for standard users
- `(OI)`: Object Inherit (files inherit permission)
- `(CI)`: Container Inherit (subfolders inherit permission)

### Step 3: Demonstrate AGDLP Permission Principle with PowerShell
```powershell
# Get existing ACL
$Acl = Get-Acl -Path $LabDir

# Display access rules cleanly in table format
$Acl.Access | Select-Object IdentityReference, FileSystemRights, AccessControlType, IsInherited | Format-Table -AutoSize
```

### Step 4: Cleanup Disposable Test Directory
```powershell
Remove-Item -Path $LabDir -Recurse -Force
```

---

## 4. Key Interview Talking Points
- **Q: What is the difference between an Active Directory account and a Local Windows account?**
  *A: "A local account is stored in the local machine's Security Accounts Manager (SAM) database in C:\Windows\System32\config\SAM and only grants access to that specific single computer. An Active Directory account is stored centrally in the ntds.dit database on a Domain Controller, allowing the user to sign in to any authorized domain-joined computer across the enterprise with a single identity and centrally enforced security policies."*
- **Q: What command-line tools can you use to manage accounts if the GUI is unavailable?**
  *A: "For local accounts, I use `net user <username>` to check status or reset passwords, and `net localgroup <group>` to view or modify group memberships. For domain environments, I use PowerShell cmdlets from the ActiveDirectory module: `Get-ADUser`, `Set-ADAccountPassword`, `Unlock-ADAccount`, and `Add-ADGroupMember`."*
