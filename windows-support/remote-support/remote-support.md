# Remote Support Tools & Best Practices
**Document ID:** WIN-REM-001  
**Audience:** L1 Service Desk Analysts  
**Scope:** Microsoft Quick Assist, Remote Desktop (RDP), Remote Assistance

---

## 1. Remote Support Tool Matrix

| Tool | Architecture | User Experience | Admin / Elevation Capability | Best Used For |
|---|---|---|---|---|
| **Microsoft Quick Assist** | Cloud-relayed (HTTPS/WebRTC) via Microsoft Services. | User generates or enters a 6-digit code. Sees technician's screen actions live. | Prompts for elevation; technician can view/input UAC credentials if allowed by policy. | Primary tool for ad-hoc remote support of hybrid/work-from-home users across internet. |
| **Remote Desktop (RDP)** | Direct Layer 4 TCP connection over port 3389. | Locks local console; full interactive session for technician only. | Full administrative access matching logged-on account. | Connecting to headless servers (`NEX-DC01`, `NEX-FS01`) or configuring unattended PCs. |
| **Windows Remote Assistance (MSRA)** | Peer-to-peer over local LAN (port 3389 / dynamic DCOM). | User invites technician or technician offers assistance via LAN. | Prompts user to allow screen sharing and control. | Internal office LAN support when internet access is degraded. |

---

## 2. Using Microsoft Quick Assist (L1 Procedure)

### Step-by-Step Connection Flow:
1. **Technician Action:**
   - Press `Windows Key + Ctrl + Q` to launch Quick Assist.
   - Click **Help someone**.
   - Sign in with corporate Microsoft 365 credentials.
   - Provide the generated 6-digit security code (valid for 10 minutes) to the user verbally over phone or via secure chat.
2. **End-User Action:**
   - User launches Quick Assist (`Windows Key + Ctrl + Q`).
   - Enters the 6-digit code provided by technician.
   - Clicks **Share screen**.
3. **Technician Control:**
   - Choose **Take full control** (or **View screen** for training).
   - User receives permission prompt and clicks **Allow**.
   - Both parties now see the workstation screen with a blue border indicating an active session.

---

## 3. Remote Support Professional Etiquette (Golden Rules)

1. **Explicit Permission Before Connection:** Never attempt unattended remote connection to a user workstation without their explicit verbal or ticket-documented consent.
2. **Warn Before Closing Applications or Rebooting:** Always inform the user before terminating a process or triggering a restart: *"Akash, I need to restart the machine now to apply the network fix. Please save any open browser tabs."*
3. **Privacy Awareness:** If user has private windows (personal email, bank account, WhatsApp) open on screen, pause control and politely ask them to close those windows before proceeding: *"Please take a moment to minimize or close any personal documents while I pause our session."*
4. **Narrate Your Actions:** Explain what you are checking as you navigate: *"I am opening the Services console right now to verify whether the Print Spooler is running."*
5. **Formal Handover & Disconnect:** Always confirm resolution before disconnecting: *"Everything appears to be functioning normally now. Is there anything else you need before I disconnect this remote session?"*
