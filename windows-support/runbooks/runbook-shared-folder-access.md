# Troubleshooting Runbook: Shared Folder Access Denied
**Incident ID:** INC-W012  
**Category:** Windows Support / Network & Security  
**Target Systems:** Windows 11 / Windows 10 (SMB Network Shares)  

---

### 1. Reported Symptom
User reports: *"When I try to open our team shared folder `\\nexfs01\finance` from File Explorer, a Windows Security dialog appears saying: 'Windows cannot access \\nexfs01\finance. You do not have permission to access \\nexfs01\finance. Contact your network administrator to request access'."*

### 2. User Impact
User cannot access departmental spreadsheets, monthly accounts, or customer contracts. Productivity blocked. Priority: P2/P3.

### 3. Initial Questions
1. Is this a new share you are trying to access for the first time, or have you been accessing it previously?
2. Are other colleagues in your department able to access this shared folder right now?
3. Did you recently change your domain password or change your job title/department?
4. Are you connected to the office LAN or connecting from home via VPN?

### 4. Investigation Sequence
1. Check basic network connectivity to file server (`ping nexfs01`).
2. Test SMB port connectivity (TCP port 445).
3. Check the user's current Active Directory group memberships using `whoami /groups`.
4. Distinguish between **Share Permissions** and **NTFS (Security) Permissions** (the most restrictive permission wins).
5. Inspect Windows Credential Manager (`control keymgr.dll`) for stale cached passwords.
6. Check for Kerberos token expiration or unrefreshed group security identifiers (SIDs).

### 5. Tools Required
- Command Prompt / PowerShell (`whoami`, `net use`, `klist`)
- Windows Credential Manager (`control keymgr.dll`)
- File Explorer / Network Map Drive

### 6. Commands & Output Interpretation
Inspect current user's security token and group memberships:
```cmd
whoami /groups
```
*Interpretation:* Review the list of group SIDs. If the required group (e.g., `NEXORA\FIN-SharedDrive-RW`) is missing, the user has not been added in AD, or they have not logged off since being added.

Test SMB port 445 connectivity to the file server:
```powershell
Test-NetConnection -ComputerName nexfs01 -Port 445
```
*Interpretation:* If `TcpTestSucceeded` is `False`, network firewalls or VPN routing are blocking SMB traffic.

List cached Kerberos tickets and purge to refresh without rebooting:
```cmd
klist
klist purge
```
*Interpretation:* `klist purge` deletes cached Kerberos ticket-granting tickets (TGT), forcing Windows to request a fresh ticket containing updated group SIDs upon next network access.

Inspect mapped network drives and disconnect stale sessions:
```cmd
net use
net use \\nexfs01\finance /delete
```
*Interpretation:* Clears any open SMB session authenticated under an old or invalid credential context.

### 7. Expected Observations
- Healthy: Folder opens immediately in File Explorer, displaying directory listings.
- Fault: Error code `0x80070005` (Access Denied) or continuous password prompt.

### 8. Possible Root Causes
1. **Missing AD Security Group Membership:** User was never added to the designated security group granting access to the share.
2. **Unrefreshed Kerberos Token:** User was added to the group in AD, but has not logged off and logged back on (Kerberos token is generated only at logon).
3. **Stale Credentials in Credential Manager:** Old password cached for `nexfs01` after a password change.
4. **NTFS vs. Share Permission Conflict:** Share permission is Full Control, but NTFS folder permission lacks user read/write access.
5. **VPN / Network Firewall:** Client is on guest Wi-Fi or VPN profile that blocks SMB port 445.

### 9. Corrective Action
1. **Verify Group Membership in AD:** If missing, initiate Service Request approval and add user to the designated security group in Active Directory Users and Computers (ADUC).
2. **Refresh Security Token:** Instruct the user to **Sign Out** of Windows (`shutdown /l`) and sign back in. (Or run `klist purge`).
3. **Clear Cached Credentials:** Open Windows Credential Manager (`control keymgr.dll`) > Windows Credentials > remove any stored entries for `nexfs01`.
4. **Remap Network Drive:**
   ```cmd
   net use Z: \\nexfs01\finance /persistent:yes
   ```

### 10. Verification Procedure
- Open File Explorer and browse to `\\nexfs01\finance`.
- Verify user can view files, open an existing document, and create a test text file to confirm write permissions.
- Delete the test file to confirm delete permissions.

### 11. Escalation Conditions
- Escalate to **L2 Systems / Storage Administrator** if NTFS folder permissions on the file server need restructuring or if the SMB file server service is unresponsive.

### 12. Ticket Resolution Notes
> *"Investigated Access Denied error on \\nexfs01\finance for user in Finance department. Validated via `whoami /groups` that user was absent from FIN-SharedDrive-RW security group following departmental transfer. Verified manager approval and added user to group in Active Directory. Purged cached Kerberos tickets using `klist purge` and instructed user to re-sign into Windows. Verified read and write access restored."*

### 13. Interview Questions & Defensible Answers
- **Q: What is the difference between Share permissions and NTFS permissions, and what happens when they conflict?**  
  *A: "Share permissions apply when a folder is accessed over the network (e.g., via SMB \\server\share), whereas NTFS permissions apply both over the network and when someone logs onto the machine locally. When a user accesses a shared folder over the network, Windows evaluates both Share permissions and NTFS permissions, and the MOST RESTRICTIVE permission always wins. For example, if Share permission is Full Control but NTFS is Read-Only, the user can only read."*
- **Q: If you add a user to an Active Directory security group to give them access to a shared drive, why can't they access it immediately?**  
  *A: "Because group memberships are embedded into the user's Kerberos Ticket Granting Ticket (TGT) when they log on to Windows. If they are already logged in, their existing token does not contain the new group SID. They must sign out and sign back in (or lock/unlock or run `klist purge`) so Windows requests a new Kerberos token reflecting their updated group memberships."*
