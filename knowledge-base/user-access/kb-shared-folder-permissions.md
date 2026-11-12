# Standard Knowledge Base Article: Troubleshooting Shared Folder Access Denied
**KB ID:** KB0010  
**Category:** User Access / Network Shares  
**Author:** Nexora IT Service Desk (L1 Support)  
**Last Reviewed:** 2024-11-12  

---

### Symptoms
- User attempts to access a network drive or UNC path (e.g., `\\nexfs01\finance`) and receives:  
  *"Windows cannot access \\nexfs01\finance. You do not have permission to access \\nexfs01\finance. Contact your network administrator to request access."*
- User prompted repeatedly for network credentials that are rejected.

### Applicable Systems
- Windows 10/11 Enterprise domain endpoints accessing Windows Server SMB file shares (`NEX-FS01`).

### Prerequisites
- Active Directory Users and Computers (ADUC) delegation to inspect and modify security group memberships.

### Troubleshooting Steps
1. **Verify User Group Membership:**
   - On the user workstation, open Command Prompt and run:
     ```cmd
     whoami /groups
     ```
   - Check if the required security group (e.g., `NEXORA\SHARE-Finance-ReadWrite`) is listed in the output.
2. **If Group is Missing in Active Directory:**
   - Confirm manager approval in the service ticket.
   - Open ADUC (`dsa.msc`), locate the user account, go to **Member Of** tab > click **Add...** > add `SHARE-Finance-ReadWrite`.
3. **If Group Was Recently Added in AD but Not Active on PC:**
   - The user's local Kerberos security token has not refreshed.

### Resolution
- **Purge Cached Kerberos Security Tokens:**
  Run in Command Prompt:
  ```cmd
  klist purge
  ```
- **Clear Stale Cached Credentials:**
  - Open `control keymgr.dll` > Windows Credentials > remove any stored passwords for `nexfs01`.
- **Force Kerberos Token Refresh:**
  - Instruct user to **Sign Out** of Windows (`shutdown /l`) and sign back in.
  - (Logging off and back on destroys the old Kerberos ticket-granting ticket and requests a new token containing all updated group SIDs from the Domain Controller).

### Verification
- Open File Explorer and browse to `\\nexfs01\finance`.
- Confirm folder opens immediately without permission error dialogs.
- Create and delete a test text file to confirm write permissions.

### Escalation Instructions
- Escalate to **L3 Infrastructure / Storage Team** if NTFS permissions on the file server folder have lost inheritance or if server SMB services are unresponsive.

### Related Incidents
- INC0002, INC-W012, AD-003
