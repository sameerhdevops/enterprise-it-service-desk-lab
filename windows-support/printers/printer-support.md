# Enterprise Printer Setup & Support Guide
**Document ID:** WIN-PRN-001  
**Audience:** L1 Service Desk Analysts  
**Scope:** Network Shared Printers, Print Servers, Drivers (PCL6 vs PostScript)

---

## 1. Network Printing Architecture at Nexora

In an enterprise environment, printers are rarely shared directly from a user's workstation. Printing follows one of two models:

```
Model A: Centralized Print Server (Preferred Enterprise Model)
[Client Workstation] ──SMB──> [Windows Print Server \\NEX-PRN01] ──RAW 9100──> [Physical MFD Printer]

Model B: Direct IP Printing (Branch / Small Office Model)
[Client Workstation] ──────────────────Standard TCP/IP Port (9100)─────────────> [Physical MFD Printer]
```

---

## 2. Printer Driver Selection: PCL6 vs. PostScript (PS)

| Feature | PCL6 (Printer Command Language) | PostScript (PS) |
|---|---|---|
| **Developer** | Hewlett-Packard | Adobe Systems |
| **Best Used For** | General daily business documents (Word, Excel, Outlook, text, invoices). | High-end graphic design, desktop publishing, precise color reproduction (PDFs, Illustrator). |
| **Speed & Overhead** | Fast spooling, smaller spool file sizes, processed rapidly by printer firmware. | Slower processing, larger spool files, higher printer memory requirements. |
| **Enterprise Standard** | Default recommended driver for 95% of corporate workstations. | Installed on-demand for Marketing and Creative users. |

---

## 3. Adding a Network Printer via PowerShell (Direct IP)

When setting up a printer without a print server, avoid using the Windows "Add a device" discovery wizard (which binds unreliable WSD ports). Use explicit PowerShell scripting:

```powershell
# Step 1: Create a Standard TCP/IP Printer Port
Add-PrinterPort -Name "IP_192.168.10.25" -PrinterHostAddress "192.168.10.25"

# Step 2: Install the manufacturer driver into the DriverStore (if not pre-installed)
Add-PrinterDriver -Name "HP Universal Printing PCL 6"

# Step 3: Install the Printer and bind to the TCP/IP Port
Add-Printer -Name "HR-LaserJet-01" -DriverName "HP Universal Printing PCL 6" -PortName "IP_192.168.10.25"

# Step 4: Set as Default Printer
(New-Object -ComObject WScript.Network).SetDefaultPrinter("HR-LaserJet-01")
```

---

## 4. Common Printing Faults Checklist for L1
- **Faded Print / Streaks:** Low toner cartridge or dirty laser optical glass / drum unit.
- **Paper Jams:** Remove paper following the printer's internal guide numbering (1, 2, 3); never yank paper backwards through rollers as torn scraps lock mechanical optical sensors.
- **Wrong Paper Size Error:** Ensure tray paper guides physically match the size setting (A4 vs Letter) in Printer Properties > Device Settings > Form To Tray Assignment.
