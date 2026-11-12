# Active Directory User Account Management Guide
**Document ID:** AD-002  
**Audience:** L1 Service Desk Analysts  
**Tools:** Active Directory Users and Computers (ADUC / `dsa.msc`), PowerShell `ActiveDirectory` Module

---

## 1. User Account Lifecycle Overview

As an L1 Service Desk Analyst, account administration is one of the highest-volume daily responsibilities:
- Creating new user accounts from approved HR requests.
- Unlocking locked accounts.
- Resetting forgotten passwords.
- Disabling departed employee accounts.
- Updating contact attributes (job title, phone number, department).

---

## 2. Managing Users via Graphical Interface (ADUC)

1. Launch **Active Directory Users and Computers** (`dsa.msc`).
2. Navigate to the appropriate OU: `nexora.local > Nexora-Users > [Department]`.
3. **Inspect Account Properties:**
   - Double-click user > **Account** tab.
   - Note fields: *User logon name* (`sAMAccountName` and `userPrincipalName`), *Account options* (*User must change password at next logon*, *Account is disabled*, *Account is locked out*).
4. **Unlocking an Account:**
   - On the **Account** tab, check the box **"Unlock account. This account is currently locked out on this Active Directory Domain Controller."**
   - Click **Apply**.
5. **Disabling an Account:**
   - Right-click user > click **Disable Account**. Account icon updates to show a small downward-pointing black arrow.

---

## 3. Managing Users via PowerShell (Automated L1 Scripts)

PowerShell provides faster, scriptable administration using the Microsoft `ActiveDirectory` module.

### Query User Account Details:
```powershell
Get-ADUser -Identity "kmurthy" -Properties DisplayName, Department, Title, Enabled, LockedOut, PasswordLastSet, MemberOf
```

### Create a New User Account:
```powershell
$Password = ConvertTo-SecureString "WelcomeNexora@2024!" -AsPlainText -Force
New-ADUser -Name "Kavitha Murthy" `
           -GivenName "Kavitha" `
           -Surname "Murthy" `
           -SamAccountName "kmurthy" `
           -UserPrincipalName "kmurthy@nexora.local" `
           -Path "OU=HR,OU=Nexora-Users,DC=nexora,DC=local" `
           -AccountPassword $Password `
           -Enabled $true `
           -ChangePasswordAtLogon $true `
           -Department "Human Resources" `
           -Title "HR Generalist" `
           -EmailAddress "kmurthy@nexora.local"
```

### Unlock an Account:
```powershell
Unlock-ADAccount -Identity "kmurthy"
```

### Disable an Account (Offboarding):
```powershell
Disable-ADAccount -Identity "kmurthy"
Set-ADUser -Identity "kmurthy" -Description "Account disabled per HR offboarding ticket SR0006 on 2024-11-12 by Sameer K."
```
