# Troubleshooting Runbook: Windows Login Problem
**Incident ID:** INC-W013  
**Category:** Windows Support / Authentication & Access  
**Target Systems:** Windows 11 / Windows 10 (Domain & Local Accounts)  

---

### 1. Reported Symptom
User reports: *"I cannot log in to my laptop this morning. When I enter my password, it says: 'The user name or password is incorrect' or 'The referenced account is currently locked out and may not be logged on to'."*

### 2. User Impact
User completely locked out of workstation and cannot work. High individual urgency (Priority: P2/P3).

### 3. Initial Questions
1. Did you recently change your password on another device (e.g., your smartphone or tablet for company email)?
2. Is the laptop connected to the office network via Ethernet/Wi-Fi or are you working offline at home?
3. Is your Caps Lock or Num Lock key enabled on the keyboard?
4. What is the exact error message displayed on the Windows logon screen?

### 4. Investigation Sequence
1. Confirm identity of caller using standard company verification (Employee ID, Manager Name).
2. Check account status in Active Directory (or local accounts database if standalone):
   - Is the account locked out?
   - Has the password expired?
   - Is the account disabled?
3. If user is remote, check if cached credentials are out of sync (requires connecting to corporate VPN before logon or using "Network sign-in").
4. Check keyboard layout (e.g., accidental switch to UK/Dvorak layout changing special characters).
5. Inspect Security Event log for Event ID 4625 (Failed Logon) to identify failure reason.

### 5. Tools Required
- Active Directory Users and Computers (`dsa.msc`) or Active Directory Administrative Center
- PowerShell ActiveDirectory module (`Get-ADUser`, `Unlock-ADAccount`)
- Local Account tools (`net user`, `lusrmgr.msc`)
- Event Viewer (`eventvwr.msc`)

### 6. Commands & Output Interpretation
Inspect domain user account status via PowerShell:
```powershell
Get-ADUser -Identity "kmurthy" -Properties LockedOut, AccountExpirationDate, PasswordExpired, BadLogonCount, LastBadPasswordAttempt
```
*Interpretation:*
- `LockedOut: True` indicates too many consecutive incorrect password attempts (triggered account lockout policy).
- `PasswordExpired: True` indicates 90-day password aging threshold reached.

Unlock an account via PowerShell:
```powershell
Unlock-ADAccount -Identity "kmurthy"
```
*Interpretation:* Clears the lockout flag immediately on the Domain Controller.

Check local account status (on standalone/lab test machine):
```cmd
net user kmurthy
```
*Interpretation:* Look for `Account active`, `Account expires`, and `Password last set`.

### 7. Expected Observations
- Normal: User enters password, Windows validates with DC (or cached hash), profile loads desktop.
- Fault: Account lockout message appears; BadLogonCount increments in AD.

### 8. Possible Root Causes
1. **Account Lockout:** User typed incorrect password 5+ times, triggering account lockout policy.
2. **Stale Stored Credentials (The Mobile Device Trap):** User changed domain password on laptop, but their mobile phone or iPad is still attempting to sync corporate email using the old password, continuously locking the account every 15 minutes.
3. **Password Expired:** 90-day password policy elapsed while user was on leave.
4. **Cached Credentials Mismatch:** Remote user reset password on web portal, but offline laptop still expects the old cached password because it has not communicated with the domain controller.
5. **Accidental Caps Lock / Keyboard Language Switch:** `Shift + Alt` accidentally pressed, swapping key characters.

### 9. Corrective Action
1. **Verify Identity & Unlock Account:**
   - In ADUC, right-click user > Properties > **Account** tab > Check **"Unlock account"** > click Apply.
2. **Perform Password Reset if Forgotten:**
   - Right-click user > **Reset Password**.
   - Set temporary compliant password.
   - Check **"User must change password at next logon"**.
3. **Resolve Remote Cached Credential Desynchronization:**
   - Instruct remote user to enter their **OLD** password to log into the cached local Windows profile.
   - Once logged in, connect to corporate VPN.
   - Press `Ctrl + Alt + Del` > **Change a password** (or lock and unlock screen) to force synchronization with Domain Controller.
4. **Identify Lockout Source:**
   - If account locks again repeatedly, check the user's smartphone, tablet, or mapped network drives for stored outdated passwords.

### 10. Verification Procedure
- User enters new password at Windows logon screen.
- Verify desktop environment loads cleanly.
- Check AD BadLogonCount resets to 0.

### 11. Escalation Conditions
- Escalate to **L2/Security Operations** if repeated lockouts occur from external IP addresses or unrecognized hostnames (potential brute-force attack).

### 12. Ticket Resolution Notes
> *"Assisted user locked out of domain account. Verified user identity via Employee ID and manager confirmation. Discovered account was locked in Active Directory with BadLogonCount = 6. Unlocked account and performed temporary password reset with 'User must change password at next logon' enforced. Discovered user's personal smartphone was persistently attempting Exchange ActiveSync using old credentials; updated mobile password. Confirmed user logged into laptop successfully."*

### 13. Interview Questions & Defensible Answers
- **Q: An employee calls and says their account keeps getting locked out every 15 minutes even after you unlock it. What is causing this?**  
  *A: "This is a classic IT support scenario. When an account repeatedly locks out after being unlocked, it is almost always caused by a background device or service continually authenticating with an old, cached password. Common culprits include: a mobile phone or tablet trying to sync corporate email/Wi-Fi with an old password, a mapped network drive with saved credentials, or a scheduled task/Windows service configured with user credentials. I would ask the user to temporarily turn off Wi-Fi on their phone, check Event Viewer Event ID 4740 on the Domain Controller to identify the Caller Computer Name, and update the stored credentials on that device."*
