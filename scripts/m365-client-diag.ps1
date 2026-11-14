# Nexora Technologies - Microsoft 365 Client Diagnostics & Endpoint Verification
# Document ID: M365-DIAG-001
# Host: Windows 11 Enterprise | L1 Service Desk Diagnostic Script

$ErrorActionPreference = "SilentlyContinue"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$output = @()

$output += "======================================================================"
$output += "  NEXORA TECHNOLOGIES - MICROSOFT 365 CLIENT DIAGNOSTIC REPORT"
$output += "  Executed: $timestamp"
$output += "======================================================================"

# 1. Office / M365 Click-to-Run Installation
$output += "`n[1. Office Click-to-Run & Suite Detection]"
$c2r = Get-ItemProperty "HKLM:\Software\Microsoft\Office\ClickToRun\Configuration" -ErrorAction SilentlyContinue
if ($c2r) {
    $output += "  Status: Installed (Click-to-Run)"
    $output += "  VersionToReport: $($c2r.VersionToReport)"
    $output += "  ProductReleaseIDs: $($c2r.ProductReleaseIDs)"
    $output += "  UpdateChannel: $($c2r.UpdateChannel)"
} else {
    $output += "  Status: Checking standard Office installation..."
    $officeApp = Get-ItemProperty "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*" | Where-Object { $_.DisplayName -like "*Microsoft Office*" -or $_.DisplayName -like "*Microsoft 365*" } | Select-Object -First 1
    if ($officeApp) {
        $output += "  Detected Suite: $($officeApp.DisplayName) (v$($officeApp.DisplayVersion))"
    } else {
        $output += "  Status: No traditional Click-to-Run suite detected."
    }
}

# 2. Outlook Configuration & Registry Profiles
$output += "`n[2. Outlook Profile Status & Registry Detection]"
$profiles = Get-ChildItem "HKCU:\Software\Microsoft\Office\16.0\Outlook\Profiles" -ErrorAction SilentlyContinue
if ($profiles) {
    $profileNames = ($profiles | ForEach-Object { $_.PSChildName }) -join ", "
    $output += "  Outlook Profiles Configured: $profileNames"
} else {
    $output += "  Outlook Profiles: Default profile uninitialized or managed via cloud identity."
}

# 3. Microsoft Teams Client Detection & Cache Location
$output += "`n[3. Microsoft Teams Client & Cache Inspection]"
$teamsProcess = Get-Process -Name "ms-teams", "Teams" -ErrorAction SilentlyContinue
if ($teamsProcess) {
    $output += "  Teams Process: Running (PID: $($teamsProcess[0].Id), WorkingSet: $([math]::Round($teamsProcess[0].WorkingSet/1MB,2)) MB)"
} else {
    $output += "  Teams Process: Stopped (Idle)"
}
$newTeamsPath = "$env:LOCALAPPDATA\Packages\MSTeams_8wekyb3d8bbwe\LocalCache"
$classicTeamsPath = "$env:APPDATA\Microsoft\Teams"
$output += "  New Teams LocalCache Path: $newTeamsPath (Exists: $(Test-Path $newTeamsPath))"
$output += "  Classic Teams Cache Path:  $classicTeamsPath (Exists: $(Test-Path $classicTeamsPath))"

# 4. OneDrive Synchronization Health
$output += "`n[4. Microsoft OneDrive Sync Client Health]"
$oneDriveProcess = Get-Process -Name "OneDrive" -ErrorAction SilentlyContinue
if ($oneDriveProcess) {
    $output += "  OneDrive Client: Running (PID: $($oneDriveProcess[0].Id))"
} else {
    $output += "  OneDrive Client: Not currently running"
}
$oneDriveFolder = "$env:USERPROFILE\OneDrive"
$output += "  Local OneDrive Directory: $oneDriveFolder (Exists: $(Test-Path $oneDriveFolder))"

# 5. Live Cloud Endpoint TCP Connectivity Verification
$output += "`n[5. Microsoft 365 Cloud Endpoint Connectivity (Port 443)]"
$endpoints = @(
    "login.microsoftonline.com",
    "outlook.office.com",
    "teams.microsoft.com"
)
foreach ($ep in $endpoints) {
    $t = Test-NetConnection -ComputerName $ep -Port 443 -WarningAction SilentlyContinue
    $status = if ($t.TcpTestSucceeded) { "SUCCESS (Reachable)" } else { "FAILED (Blocked/Timeout)" }
    $output += "  Endpoint: $($ep.PadRight(28)) | Port: 443 | Status: $status | RTT: $($t.PingReplyDetails.RoundtripTime)ms"
}

$output += "`n======================================================================"
$output += "  END OF M365 CLIENT DIAGNOSTIC REPORT"
$output += "======================================================================"

$output | Out-String
