# eye-break-reminder (aka BlinkBuddy)

A lightweight desktop tray application that helps reduce eye strain by reminding users to take regular breaks.

---

## Features
- 20-minute reminders with rotating eye-exercise tips
- Snooze function (postpone reminder by 5 minutes)
- Work hours mode (Mon–Fri, 9am–6pm) with optional overtime support
- Auto-start at Windows login and uninstall option
- Bilingual support: English / Korean toggle
- Status window to check current settings and app state

---

## Tech Stack
- Python 3.13
- `pystray`, `PIL`, `tkinter`, `threading`
- Windows Registry APIs (startup/uninstall integration)
- Packaged with PyInstaller (`.exe` for easy installation)

---

## Challenges & Solutions
- Issue: Duplicate tray icons appeared when adding startup/uninstall features  
- Fix: Debugged `_init_tray` function and removed redundant code → confirmed stable single-icon behavior

---

## Performance
- Stable runtime: 1 week continuous use  
- Memory footprint: ~25MB  
- Power usage: negligible

---

## Future Roadmap
- Currently stable with no additional features planned  
- Open to community feedback for additional languages or custom reminder settings

---

## Screenshots


---

## License
MIT
