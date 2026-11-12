# IT Asset Management (ITAM) Standard Operating Procedure
**Document ID:** ITAM-001  
**Audience:** L1 Service Desk Analysts  
**Scope:** Hardware Asset Lifecycle, Software Licensing, Tracking, Disposal

---

## 1. The IT Asset Lifecycle

In Nexora Technologies, every physical compute device and peripheral follows a 5-stage lifecycle:

```
[1. Procurement] ──> [2. Receiving & Tagging] ──> [3. Deployment / In Use]
                                                          │
                                         ┌────────────────┴────────────────┐
                                         ▼                                 ▼
                             [4. Maintenance / Repair]           [5. Retirement / Disposal]
                                (Spare issuance / RMA)             (Wipe / E-Waste recycling)
```

---

## 2. L1 Responsibilities in Asset Management

### A. Tagging & Ingestion (Stage 2)
When new hardware arrives at the office:
1. Inspect packaging for physical transit damage.
2. Affix tamper-evident barcode asset label: Format `NXT-AST-0XX`.
3. Record hardware specifications in the Asset Register (`asset-inventory.csv` or ServiceNow `alm_hardware` table):
   - Asset Tag, Serial Number (Service Tag), Model, MAC Address, Purchase Date, Warranty Expiration Date.
4. Escrow BitLocker recovery key into Active Directory / Intune during initial imaging.

### B. Deployment & Assignment (Stage 3)
1. Issue laptop to employee along with standard accessory bundle (charger, laptop bag, wireless mouse).
2. Employee signs physical or digital **Asset Acceptance Form**.
3. Update Asset Status in register from `In Stock` to `Active`, setting `AssignedTo` and `Department`.

### C. Repair & Spare Handling (Stage 4)
- When a laptop suffers hardware failure (e.g., motherboard failure in INC0001):
  - Check warranty status in `asset-inventory.csv`.
  - If under warranty: Log service ticket with vendor (HP/Dell/Lenovo).
  - Move faulty asset status to `In Repair`.
  - Issue pre-configured loaner laptop (e.g., `NXT-AST-015`) to employee so work is uninterrupted.
  - Record loaner asset issuance in ticket work notes.

### D. Secure Disposal & Offboarding (Stage 5)
- Prior to decommissioning or returning a leased laptop:
  - Perform DoD 5220.22-M compliant disk sanitize or NVMe Cryptographic Erase.
  - Remove asset from Active Directory and Intune.
  - Status updated to `Decommissioned` / `Disposed`.
