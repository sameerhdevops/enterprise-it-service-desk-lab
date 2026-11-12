# Standard Knowledge Base Article: Resolving Microsoft Teams Audio & Microphone Issues
**KB ID:** KB0006  
**Category:** Microsoft 365 / Teams  
**Author:** Sameer Kulkarni (L1 Support)  
**Last Reviewed:** 2024-11-12  

---

### Symptoms
- User can hear meeting attendees, but attendees cannot hear the user speaking ("You are on mute" or zero microphone pickup).
- Audio drops out or robotic screeching occurs during calls.
- Teams displays banner: "Your microphone isn't working. Please switch to another device."

### Applicable Systems
- Microsoft Teams (New Teams / Classic Teams) on Windows 11/10 with USB or 3.5mm headsets.

### Prerequisites
- Standard user access.

### Troubleshooting Steps
1. **Verify Physical Hardware & Mute Buttons:**
   - Check inline hardware mute switch on the USB headset cable (ensure red LED mute light is off).
   - Test headset in a different USB port directly on laptop chassis (bypass docking station).
2. **Configure Teams In-App Device Settings:**
   - In Teams, click three dots `...` next to profile picture > **Settings > Devices**.
   - Under **Audio devices**, ensure custom headset is selected for both **Speaker** and **Microphone** (do NOT use "PC Mic and Speakers").
   - Click **Make a test call**. Record a 5-second message; listen for playback confirmation.
3. **Check Windows OS Microphone Privacy Permissions:**
   - Open Windows Settings > Privacy & security > **Microphone**.
   - Verify **"Microphone access"** is ON.
   - Verify **"Let desktop apps access your microphone"** is ON and Teams is listed.
4. **Disable Exclusive Mode Conflict in Sound Control Panel:**
   - Run `mmsys.cpl` > **Recording** tab > double-click microphone > **Advanced** tab.
   - UNCHECK: **"Allow applications to take exclusive control of this device"**.

### Resolution
- If Teams audio driver interface remains frozen, clear Teams application cache:
  ```cmd
  taskkill /F /IM ms-teams.exe
  rmdir /S /Q "%LOCALAPPDATA%\Packages\MSTeams_8wekyb3d8bbwe\LocalCache"
  ```
- Relaunch Teams.

### Verification
- Execute "Make a test call" inside Teams; confirm successful audio playback with clear voice quality.
- Join a live test meeting with IT support; confirm bidirectional clear audio.

### Escalation Instructions
- Escalate to **L2 Desktop Support** if hardware microphone fails Windows Voice Recorder test across multiple ports (physical hardware failure requiring headset replacement).

### Related Incidents
- INC-W011, M365-TMS-001
