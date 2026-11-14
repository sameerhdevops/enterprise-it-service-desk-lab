# Nexora Technologies - Microsoft 365 / Office Client Diagnostics and Troubleshooting
# Document ID: M365-DIAG-001
# Host: Windows 11 Enterprise | L1 Service Desk Diagnostic Script
# Scope: Local Office Client Installation, Profiles, Process State, Local Cache & TCP 443 Reachability
# Note: Client-side diagnostics only (Does not assert tenant-level administration)

$ErrorActionPreference = "SilentlyContinue"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$output = @()

$output += "======================================================================"
$output += "  NEXORA TECHNOLOGIES - M365 / OFFICE CLIENT DIAGNOSTIC REPORT"
$output += "  Scope: Local Client Diagnostics & Endpoint Reachability Verification"
$output += "  Execution: [REDACTED_TIMESTAMP] | Host: [CLIENT_WORKSTATION] (Windows 11)"
$output += "======================================================================"

# 1. Office / M365 Click-to-Run Installation State
$output += "`n[1. Office Click-to-Run Suite Detection]"
$c2r = Get-ItemProperty "HKLM:\Software\Microsoft\Office\ClickToRun\Configuration" -ErrorAction SilentlyContinue
if ($c2r -and $c2r.VersionToReport) {
    $output += "  Installation State: INSTALLED (Click-to-Run)"
    $output += "  VersionToReport:    $($c2r.VersionToReport)"
    $output += "  ProductReleaseIDs:  $($c2r.ProductReleaseIDs)"
    $output += "  UpdateChannel:      $($c2r.UpdateChannel)"
} else {
    $officeApp = Get-ItemProperty "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*" -ErrorAction SilentlyContinue | Where-Object { $_.DisplayName -like "*Microsoft Office*" -or $_.DisplayName -like "*Microsoft 365*" } | Select-Object -First 1
    if ($officeApp) {
        $output += "  Installation State: INSTALLED (Traditional/MSI)"
        $output += "  Detected Suite:     $($officeApp.DisplayName) (v$($officeApp.DisplayVersion))"
    } else {
        $output += "  Installation State: NOT DETECTED (No Office C2R configuration found in registry)"
    }
}

# 2. Outlook Profile State & Registry Inspection
$output += "`n[2. Outlook Profile & Configuration State]"
$profiles = Get-ChildItem "HKCU:\Software\Microsoft\Office\16.0\Outlook\Profiles" -ErrorAction SilentlyContinue
if ($profiles -and $profiles.Count -gt 0) {
    $profileNames = ($profiles | ForEach-Object { $_.PSChildName }) -join ", "
    $output += "  Profile State:      CONFIGURED ($($profiles.Count) local profile(s) detected)"
    $output += "  Profile Names:      $profileNames"
} else {
    $output += "  Profile State:      NOT INITIALIZED (No Outlook 16.0 registry profile configured for user; mailbox access not tested)"
}

# 3. Microsoft Teams Process & Cache Inspection
$output += "`n[3. Microsoft Teams Process & Local Cache State]"
$teamsProcess = Get-Process -Name "ms-teams", "Teams" -ErrorAction SilentlyContinue
if ($teamsProcess) {
    $proc = $teamsProcess[0]
    $output += "  Process State:      RUNNING (PID: $($proc.Id), Memory WorkingSet: $([math]::Round($proc.WorkingSet/1MB,2)) MB)"
} else {
    $output += "  Process State:      STOPPED / IDLE (Teams communication services not active/tested)"
}
$newTeamsPath = "$env:LOCALAPPDATA\Packages\MSTeams_8wekyb3d8bbwe\LocalCache"
$classicTeamsPath = "$env:APPDATA\Microsoft\Teams"
$output += "  New Teams LocalCache: $(if (Test-Path $newTeamsPath) { 'PRESENT (%LOCALAPPDATA%\Packages\MSTeams_8wekyb3d8bbwe\LocalCache)' } else { 'ABSENT' })"
$output += "  Classic Teams Cache:  $(if (Test-Path $classicTeamsPath) { 'PRESENT (%APPDATA%\Microsoft\Teams)' } else { 'ABSENT' })"

# 4. OneDrive Process & Sync State
$output += "`n[4. Microsoft OneDrive Process & Sync Directory State]"
$oneDriveProcess = Get-Process -Name "OneDrive" -ErrorAction SilentlyContinue
if ($oneDriveProcess) {
    $output += "  Process State:      RUNNING (PID: $($oneDriveProcess[0].Id))"
} else {
    $output += "  Process State:      STOPPED / IDLE"
}
$oneDriveFolder = "$env:USERPROFILE\OneDrive"
$output += "  Local Sync Path:    $(if (Test-Path $oneDriveFolder) { 'PRESENT (%USERPROFILE%\OneDrive - Process active; sync state unverified)' } else { 'ABSENT' })"

# 5. Live Cloud Endpoint TCP Port 443 Socket Connect & Latency
$output += "`n[5. Microsoft 365 Cloud Endpoint TCP Socket Reachability (Port 443)]"
$endpoints = @(
    "login.microsoftonline.com",
    "outlook.office.com",
    "teams.microsoft.com"
)

foreach ($ep in $endpoints) {
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $tcpClient = New-Object System.Net.Sockets.TcpClient
    try {
        $tcpClient.Connect($ep, 443)
        $sw.Stop()
        $latency = [math]::Round($sw.Elapsed.TotalMilliseconds, 1)
        $tcpClient.Close()
        $output += "  Endpoint: $($ep.PadRight(28)) | Port: 443 | Status: SUCCESS (Reachable) | TCP Connect: ${latency} ms"
    } catch {
        $sw.Stop()
        $output += "  Endpoint: $($ep.PadRight(28)) | Port: 443 | Status: FAILED ($($_.Exception.Message))"
    }
}

$output += "`n======================================================================"
$output += "  END OF M365 CLIENT DIAGNOSTIC REPORT (CLIENT-SIDE VERIFIED)"
$output += "======================================================================"

$fullReport = $output -join "`r`n"
Write-Output $fullReport

# Save to evidence
$evidencePath = Join-Path $PSScriptRoot "..\evidence\microsoft-365\m365-client-diagnostics-output.txt"
$fullReport | Out-File -FilePath $evidencePath -Encoding utf8
