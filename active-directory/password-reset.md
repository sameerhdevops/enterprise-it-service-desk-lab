# Active Directory Password Reset & Account Recovery Runbook
**Document ID:** AD-004  
**Audience:** L1 Service Desk Analysts  
**Scope:** Password Policy, Identity Verification, Reset Procedures, Self-Service Concepts

---

## 1. Security First: Mandatory Identity Verification

> **SECURITY DIRECTIVE:**  
> Never perform a password reset without formally verifying the caller's identity. Social engineering attacks frequently target service desk analysts by pretending to be executives or remote employees.

### Mandatory Verification Checklist (Must confirm 2 of 3):
1. **Employee ID Number:** Match against HR database.
2. **Manager Name & Department:** Match against organizational chart.
3. **Out-of-Band Callback:** Hang up and call the employee back on their official registered corporate mobile number listed in HR records (never accept an alternate number provided on the call).

---

## 2. Password Reset Procedure via GUI (ADUC)

1. Open **Active Directory Users and Computers** (`dsa.msc`).
2. Search for the user: Press `Ctrl + F`, enter username (e.g., `kmurthy`).
3. Right-click the user account > select **Reset Password...**
4. Enter a temporary password conforming to Nexora's password complexity policy:
   - Minimum 12 characters.
   - At least 1 uppercase letter, 1 lowercase letter, 1 number, and 1 symbol (e.g., `<TEMPORARY_PASSWORD>`).
5. **CHECK:** **"User must change password at next logon"**.
6. **UNCHECK:** **"Account is locked out"** (if the user was locked out, this unfreezes the account simultaneously).
7. Communicate the temporary password securely to the user via phone or encrypted SMS (never email it to an unverified address).

---

## 3. Password Reset via PowerShell

```powershell
# Reset password and require change on next logon
$TempPassword = ConvertTo-SecureString "<TEMPORARY_PASSWORD>" -AsPlainText -Force
Set-ADAccountPassword -Identity "kmurthy" -NewPassword $TempPassword -Reset
Set-ADUser -Identity "kmurthy" -ChangePasswordAtLogon $true
Unlock-ADAccount -Identity "kmurthy"
```

---

## 4. Nexora Corporate Password Policy (Simulated Fine-Grained Policy)

| Policy Setting | Standard User Policy | IT Privileged Admin Policy |
|---|---|---|
| Minimum Password Length | 12 characters | 16 characters |
| Password Complexity | Enabled (3 of 4 character classes) | Enabled (all 4 classes) |
| Maximum Password Age | 90 days | 60 days |
| Minimum Password Age | 1 day (prevents rapid recycling) | 1 day |
| Password History | 24 passwords remembered | 24 passwords remembered |
| Account Lockout Threshold | 5 invalid attempts | 3 invalid attempts |
| Lockout Duration | 30 minutes | Requires manual IT unlock |
| Reset Lockout Counter After | 30 minutes | 30 minutes |
