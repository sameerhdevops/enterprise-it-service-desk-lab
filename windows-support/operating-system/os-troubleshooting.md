# Windows Operating System Troubleshooting Guide
**Document ID:** WIN-OS-001  
**Audience:** L1 Service Desk Analysts  
**Scope:** Windows 11 Enterprise & Windows 10 Pro

---

## 1. Windows Update Failures & Corrupted Cache

### Common Error Codes
- `0x80070002` / `0x80070003`: File not found in update cache.
- `0x80240034`: Windows Update download failed.
- `0x800f081f`: Source files for component repair could not be found.

### The Complete L1 Windows Update Reset Procedure
Execute in an elevated Command Prompt or PowerShell:
```cmd
:: 1. Stop background update services
net stop wuauserv
net stop cryptSvc
net stop bits
net stop msiserver

:: 2. Rename software distribution and catroot2 folders
ren C:\Windows\SoftwareDistribution SoftwareDistribution.old
ren C:\Windows\System32\catroot2 catroot2.old

:: 3. Restart services
net start wuauserv
net start cryptSvc
net start bits
net start msiserver
```
*Result:* Windows builds a fresh, uncorrupted update catalog and resumes downloads cleanly.

---

## 2. System File Integrity Repair (SFC & DISM)

When Windows exhibits unexplained stability issues, explorer crashes, or corrupted system icons, run the two-tier native Microsoft repair sequence:

### Tier 1: DISM (Deployment Image Servicing and Management)
Repairs the underlying Windows Component Store (`C:\Windows\WinSxS`) using Windows Update as the clean source:
```cmd
DISM.exe /Online /Cleanup-image /Restorehealth
```

### Tier 2: SFC (System File Checker)
Scans all protected operating system files and replaces corrupted files with cached copies from the repaired Component Store:
```cmd
sfc /scannow
```

*Expected Output:*  
`Windows Resource Protection found corrupt files and successfully repaired them.`

---

## 3. Blue Screen of Death (BSOD) Triage for L1

L1 support engineers are not expected to reverse-engineer kernel memory dumps in WinDbg, but are expected to capture the critical triage information before escalating or resolving:

1. **Record the Stop Code:**
   - `CRITICAL_PROCESS_DIED`: Essential system process terminated unexpectedly.
   - `PAGE_FAULT_IN_NONPAGED_AREA`: Memory requested that was not in RAM (often bad RAM or faulty driver).
   - `SYSTEM_SERVICE_EXCEPTION`: Malfunctioning third-party driver attempting illegal memory operation.
   - `INACCESSIBLE_BOOT_DEVICE`: Storage controller driver mismatch or corrupted BCD (Boot Configuration Data).
2. **Record the Faulting Driver:** Often displayed below the stop code (e.g., `nvlddmkm.sys` for Nvidia, `Netwtw10.sys` for Intel Wi-Fi).
3. **Check Reliability Monitor:** Run `perfmon /rel` to correlate the BSOD timestamp with recently installed drivers or updates.
4. **Boot into Windows Recovery Environment (WinRE):**
   - Hold `Shift` while clicking **Restart**.
   - Navigate to Troubleshoot > Advanced options > **Startup Repair** or **Uninstall Updates**.
