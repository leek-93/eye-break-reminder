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

<img width="855" height="669" alt="Image" src="https://github.com/user-attachments/assets/69dfe66a-add3-4222-a149-40dd441fef2d" />
<img width="469" height="373" alt="Image" src="https://github.com/user-attachments/assets/1086e372-05e6-4436-89b4-a935e4b61da9" />

Popup reminder every 20 minutes with rotating eye-care tips. Status window showing mode, language, startup option, and next reminder.

<img width="1107" height="446" alt="Image" src="https://github.com/user-attachments/assets/ 55fc0301-fe8b-4521-b736-cee4a54a00ad" />

Quick tray menu (Korean UI) with snooze, pause, language toggle, and startup options. Bilingual support – English UI for international users.

<img width="865" height="184" alt="Image" src="https://github.com/user-attachments/assets/72b4039a-0060-40ee-9317-bf4d76aa4150" />

Lightweight performance – only ~25MB RAM usage.

<img width="573" height="184" alt="Image" src="https://github.com/user-attachments/assets/223a0a24-a8d0-4a55-bf71-d731f17c6ffc" />

Auto-start with Windows for seamless background operation.

---

## License
MIT
