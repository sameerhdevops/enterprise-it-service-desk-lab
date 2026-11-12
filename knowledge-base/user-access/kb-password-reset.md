# Standard Knowledge Base Article: Employee Account Password Reset Procedure
**KB ID:** KB0007  
**Category:** User Access / Active Directory  
**Author:** Sameer Kulkarni (L1 Support)  
**Last Reviewed:** 2024-11-12  

---

### Symptoms
- Employee calls or messages: "I forgot my password" or "My password expired over the weekend."
- Windows login screen displays: "The user name or password is incorrect" or "The referenced account is currently locked out."

### Applicable Systems
- Active Directory Domain Services (`nexora.local`), Azure AD / Entra ID, Microsoft 365.

### Prerequisites
- L1 Service Desk credentials delegated with password reset permissions in `OU=Nexora-Users`.
- **MANDATORY:** Completed caller identity verification.

### Identity Verification Checklist (Security Pre-Check)
Before performing any reset, verify the caller by:
1. Asking for Employee ID number (cross-reference in HR database).
2. Verifying reporting manager's name and department.
3. If caller identity is uncertain, call them back on their registered corporate mobile phone number on file.

### Troubleshooting & Reset Steps
1. Open **Active Directory Users and Computers** (`dsa.msc`).
2. Search for the user account (`Ctrl + F`), entering their username (e.g., `kmurthy`).
3. Right-click the user account > select **Reset Password...**
4. Enter temporary password complying with policy (min 12 characters, uppercase, lowercase, numbers, symbols, e.g., `Nexora#Nov2024!`).
5. **CHECK:** **"User must change password at next logon"**.
6. **UNCHECK:** **"Account is locked out"** (clears any active lockout flags).
7. Click **OK**.

### PowerShell Alternative:
```powershell
$TempPass = ConvertTo-SecureString "Nexora#Nov2024!" -AsPlainText -Force
Set-ADAccountPassword -Identity "kmurthy" -NewPassword $TempPass -Reset
Set-ADUser -Identity "kmurthy" -ChangePasswordAtLogon $true
Unlock-ADAccount -Identity "kmurthy"
```

### Resolution
- Verbally communicate the temporary password to the employee over the verified phone call.
- Instruct employee to enter temporary password at Windows login screen.
- Windows will immediately prompt: *"The user's password must be changed before signing in."*
- User sets their private permanent password.

### Verification
- Confirm user successfully logs into Windows desktop.
- Confirm user can access corporate Outlook and intranet without further credential prompts.

### Escalation Instructions
- Escalate to **IT Security Operations** if an account experiences repeated lockouts from unauthorized IP addresses or suspicious geographic locations.

### Related Incidents
- SR0004, INC-W013, AD-004
