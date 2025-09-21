# blinkbuddy_tray_i18n.py
# - English Mode ON: 모든 UI/웰컴/버튼/트레이/상태창 영어
# - English Mode OFF: 모든 UI 한국어
import os, json, random, sys, time, platform, threading
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox

# ===== optional tray =====
TRAY_AVAILABLE = False
try:
    import pystray
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except Exception:
    TRAY_AVAILABLE = False

# ===== defaults =====
REMIND_EVERY_MIN = 20
SNOOZE_MIN = 5
POPUP_WIDTH = 420
POPUP_HEIGHT = 260

# work hours (Mon–Fri 09:00–18:00)
WORK_HOURS_ONLY = True
WORK_START_HOUR = 9
WORK_END_HOUR = 18
WORK_DAYS = set([0,1,2,3,4])  # Mon=0

# English UI/tips toggle (트레이에서 토글)
EN_MODE = False

# prefs path
PREFS_PATH = os.path.join(os.path.expanduser("~"), ".blinkbuddy.json")

# ===== i18n strings =====
I18N = {
    "ko": {
        "app_name": "BlinkBuddy",
        "title_reminder": "눈 휴식 알림 · BlinkBuddy",
        "headline": "⏰ 눈을 쉬어주세요!",
        "subtitle_base": "화면 과다 주시로 인한 눈의 피로를 예방해요.",
        "subtitle_workhours": " (업무시간에만 알림)",
        "btn_another": "다른 팁 보기",
        "btn_snooze": "스누즈 {mins}분",
        "btn_ok": "확인",
        "next_label": "다음 알림 예정: {dt}",
        "welcome_title": "BlinkBuddy • 시작하기",
        "welcome_head": "BlinkBuddy 시작하기",
        "welcome_desc": (
            "이 프로그램은 기본 설정으로 ‘업무시간(월–금 09:00–18:00)만’ 알림을 띄웁니다.\n"
            "업무시간 외에는 자동으로 일시 정지되며, 고장난 것이 아닙니다 🙂\n\n"
            "현재 모드: {mode}\n"
            "다음 알림 예정: {next_dt}"
        ),
        "welcome_mode_work": "업무시간만",
        "welcome_mode_always": "항상 작동",
        "welcome_dont_show": "다시 보지 않기",
        "welcome_disable_workhours": "업무시간 제한 끄기(항상 작동)",
        "status_title": "BlinkBuddy 상태",
        "status_mode": "모드: {mode}",
        "status_en": "영문 모드: {onoff}",
        "status_pause": "일시 정지: {yesno}",
        "status_next": "다음 알림 예정: {dt}",
        "yes": "예", "no": "아니오",
        "tray_show_now": "지금 팝업 열기 (Force)",
        "tray_snooze": "스누즈 {mins}분",
        "tray_pause": "일시 정지 30분",
        "tray_toggle_en": "English Mode: {onoff}",
        "tray_toggle_wh": "업무시간 알림: {onoff}",
        "tray_status": "상태 보기",
        "tray_quit": "종료",
        "on": "ON", "off": "OFF",
        "tray_title_base": "BlinkBuddy",
        "tray_title_paused": " — 일시 정지",
        "tray_title_ooh": " — 일시 정지(업무시간 외)",
        "tray_title_next": " — 다음까지 ~{mins}분",
        "msg_wh_disabled": "업무시간 제한을 끄고 항상 작동합니다.",
    },
    "en": {
        "app_name": "BlinkBuddy",
        "title_reminder": "Eye Break Reminder · BlinkBuddy",
        "headline": "⏰ Give your eyes a break!",
        "subtitle_base": "Prevent digital eye strain from prolonged screen time.",
        "subtitle_workhours": " (active only during work hours)",
        "btn_another": "Another tip",
        "btn_snooze": "Snooze {mins} min",
        "btn_ok": "OK",
        "next_label": "Next reminder: {dt}",
        "welcome_title": "BlinkBuddy • Welcome",
        "welcome_head": "Getting Started",
        "welcome_desc": (
            "By default, BlinkBuddy shows reminders only during work hours (Mon–Fri 09:00–18:00).\n"
            "Outside work hours it’s paused automatically — it’s not broken 🙂\n\n"
            "Current mode: {mode}\n"
            "Next reminder: {next_dt}"
        ),
        "welcome_mode_work": "Work-hours only",
        "welcome_mode_always": "Always on",
        "welcome_dont_show": "Don’t show again",
        "welcome_disable_workhours": "Turn off work-hours limit (Always on)",
        "status_title": "BlinkBuddy Status",
        "status_mode": "Mode: {mode}",
        "status_en": "English Mode: {onoff}",
        "status_pause": "Paused: {yesno}",
        "status_next": "Next reminder: {dt}",
        "yes": "Yes", "no": "No",
        "tray_show_now": "Open popup now (Force)",
        "tray_snooze": "Snooze {mins} min",
        "tray_pause": "Pause for 30 min",
        "tray_toggle_en": "English Mode: {onoff}",
        "tray_toggle_wh": "Work-hours only: {onoff}",
        "tray_status": "Show status",
        "tray_quit": "Quit",
        "on": "ON", "off": "OFF",
        "tray_title_base": "BlinkBuddy",
        "tray_title_paused": " — Paused",
        "tray_title_ooh": " — Paused (Out of hours)",
        "tray_title_next": " — Next in ~{mins}m",
        "msg_wh_disabled": "Work-hours limit is off. BlinkBuddy will run always.",
    }
}

# tips
TIPS_KO = [
    "20-20-20 룰: 20분마다 20피트(6m) 떨어진 곳을 20초간 바라보세요.",
    "깜빡임 10회: 가볍게 눈을 감았다 뜨기를 10번 반복해 눈물막을 회복하세요.",
    "포커스 훈련: 창밖의 먼 점 ▶️ 책상 위의 가까운 점을 10회 번갈아 보세요.",
    "눈꺼풀 마사지: 눈을 감고 눈두덩을 손끝으로 10–15초 아주 부드럽게 눌러주세요.",
    "눈이 건조하면 보존제 없는 인공눈물을 사용해 주세요(1일 4–6회 이내).",
    "자세 점검: 모니터 상단이 눈높이와 같거나 약간 낮게, 화면과 거리는 50–70cm.",
    "눈부심 줄이기: 화면 밝기를 주변과 비슷하게, 다크모드/블루라이트 필터 활용.",
    "1분 스트레칭: 목 좌우 5회, 어깨 으쓱 10회, 손목 돌리기 10회.",
    "미세 휴식: 매 20분마다 20–30초 시선을 화면에서 떼세요.",
    "수분 섭취: 매시간 물 150–200ml.",
]
TIPS_EN = [
    "20-20-20 rule: Every 20 minutes, look 20 feet (6 m) away for 20 seconds.",
    "Blink 10 times: gentle blinks to restore your tear film.",
    "Focus drill: switch near ↔ far targets about 10 times.",
    "Eyelid massage: with eyes closed, lightly press lids for 10–15 s.",
    "Dry eyes? Use preservative-free artificial tears (~4–6×/day).",
    "Ergonomics: monitor top at/below eye level; keep 50–70 cm distance.",
    "Reduce glare: match screen brightness; consider dark mode/blue-light filter.",
    "1-min stretch: neck side bends ×5, shoulder shrugs ×10, wrist circles ×10.",
    "Micro-breaks: every 20 minutes, look away for 20–30 seconds.",
    "Hydrate: ~150–200 ml of water per hour.",
]

def lang():
    return "en" if EN_MODE else "ko"

def t(key, **kwargs):
    s = I18N[lang()].get(key, key)
    return s.format(**kwargs) if kwargs else s

def is_within_work_hours(dt: datetime) -> bool:
    if not WORK_HOURS_ONLY:
        return True
    if dt.weekday() not in WORK_DAYS:
        return False
    return WORK_START_HOUR <= dt.hour < WORK_END_HOUR

def next_work_start_after(dt: datetime) -> datetime:
    today_start = dt.replace(hour=WORK_START_HOUR, minute=0, second=0, microsecond=0)
    if dt.weekday() in WORK_DAYS and dt < today_start:
        return today_start
    day = dt + timedelta(days=1)
    while day.weekday() not in WORK_DAYS:
        day += timedelta(days=1)
    return day.replace(hour=WORK_START_HOUR, minute=0, second=0, microsecond=0)

def humanize_dt(dt: datetime) -> str:
    # YYYY-MM-DD HH:MM (로컬)
    return dt.strftime("%Y-%m-%d %H:%M")

def load_prefs():
    global WORK_HOURS_ONLY, EN_MODE
    try:
        with open(PREFS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        WORK_HOURS_ONLY = bool(data.get("work_hours_only", WORK_HOURS_ONLY))
        EN_MODE = bool(data.get("en_mode", EN_MODE))
        return {"show_welcome": bool(data.get("show_welcome", True))}
    except Exception:
        return {"show_welcome": True}

def save_prefs(extra=None):
    data = {
        "work_hours_only": WORK_HOURS_ONLY,
        "en_mode": EN_MODE,
        "show_welcome": True,
    }
    if extra:
        data.update(extra)
    try:
        with open(PREFS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def center_window(win, width, height):
    win.update_idletasks()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = (sw // 2) - (width // 2)
    y = (sh // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

class BlinkBuddyApp:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()

        self.popup = None
        self.tip_label = None
        self.tip_index = None
        self.paused_until_ts = 0.0
        self.next_due_ts = self._compute_next_due(initial=True)

        # prefs
        self.prefs = load_prefs()

        # tray
        self.tray_icon = None
        if TRAY_AVAILABLE:
            self._init_tray()

        # welcome
        if self.prefs.get("show_welcome", True):
            self.root.after(300, self._show_welcome)

        self.root.after(500, self._tick)

    # -------- scheduling
    def _compute_next_due(self, initial=False):
        now_dt = datetime.now()
        if WORK_HOURS_ONLY and not is_within_work_hours(now_dt):
            return next_work_start_after(now_dt).timestamp()
        return time.time() + REMIND_EVERY_MIN * 60

    def _schedule_after(self, seconds: int):
        self.next_due_ts = time.time() + seconds

    def _next_alarm_dt(self) -> datetime:
        now_dt = datetime.now()
        if WORK_HOURS_ONLY and not is_within_work_hours(now_dt):
            return next_work_start_after(now_dt)
        return datetime.fromtimestamp(self.next_due_ts)

    # -------- tips/popup
    def _tips(self):
        return TIPS_EN if EN_MODE else TIPS_KO

    def _random_tip(self, avoid_index=None):
        tips = self._tips()
        idx_pool = list(range(len(tips)))
        if avoid_index is not None and len(tips) > 1 and avoid_index in idx_pool:
            idx_pool.remove(avoid_index)
        idx = random.choice(idx_pool)
        return idx, tips[idx]

    def _platform_beep(self):
        try:
            if platform.system() == "Windows":
                import winsound
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            else:
                sys.stdout.write('\a'); sys.stdout.flush()
        except Exception:
            pass

    def _show_popup(self, force=False):
        if not force:
            if WORK_HOURS_ONLY and not is_within_work_hours(datetime.now()):
                self.next_due_ts = self._compute_next_due()
                return
            if time.time() < self.paused_until_ts:
                return

        if self.popup is not None:
            try:
                self.popup.lift(); self.popup.focus_force(); return
            except tk.TclError:
                self.popup = None

        self._platform_beep()

        self.popup = tk.Toplevel(self.root)
        self.popup.title(t("title_reminder"))
        self.popup.attributes("-topmost", True)
        self.popup.resizable(False, False)
        try:
            self.popup.iconify(); self.popup.deiconify()
        except tk.TclError:
            pass

        style = ttk.Style(self.popup)
        try: style.theme_use("clam")
        except Exception: pass

        outer = ttk.Frame(self.popup, padding=16); outer.pack(fill="both", expand=True)
        ttk.Label(outer, text=t("headline"), font=("Segoe UI", 16, "bold")).pack(anchor="center", pady=(0,8))

        sub = t("subtitle_base")
        if WORK_HOURS_ONLY: sub += t("subtitle_workhours")
        ttk.Label(outer, text=sub, font=("Segoe UI", 10)).pack(anchor="center", pady=(0,12))

        self.tip_index, tip_text = self._random_tip()
        tip_box = ttk.Frame(outer); tip_box.pack(fill="both", expand=True)
        self.tip_label = ttk.Label(tip_box, text=tip_text, wraplength=POPUP_WIDTH-48, justify="left", font=("Segoe UI", 11))
        self.tip_label.pack(anchor="w")

        info = ttk.Label(outer, text=t("next_label", dt=humanize_dt(self._next_alarm_dt())), font=("Segoe UI", 9))
        info.pack(anchor="w", pady=(10,0))

        btns = ttk.Frame(outer); btns.pack(fill="x", pady=(16,0))
        ttk.Button(btns, text=t("btn_another"), command=self._show_another_tip).pack(side="left")
        ttk.Button(btns, text=t("btn_snooze", mins=SNOOZE_MIN), command=self._schedule_snooze).pack(side="left", padx=8)
        ttk.Button(btns, text=t("btn_ok"), command=self._confirm_and_schedule_next).pack(side="right")

        self.popup.bind("<Escape>", lambda e: self._confirm_and_schedule_next())
        self.popup.protocol("WM_DELETE_WINDOW", self._on_close_popup)

        center_window(self.popup, POPUP_WIDTH, POPUP_HEIGHT)
        try: self.popup.focus_force()
        except tk.TclError: pass

        if force:
            self._schedule_after(REMIND_EVERY_MIN * 60)

    def _show_another_tip(self):
        self.tip_index, txt = self._random_tip(avoid_index=self.tip_index)
        self.tip_label.configure(text=txt)

    def _schedule_snooze(self):
        self._schedule_after(SNOOZE_MIN * 60)
        self._on_close_popup()

    def _confirm_and_schedule_next(self):
        self._schedule_after(REMIND_EVERY_MIN * 60)
        self._on_close_popup()

    def _on_close_popup(self):
        if self.popup is not None:
            try: self.popup.destroy()
            except tk.TclError: pass
            self.popup = None

    # -------- welcome & status
    def _show_welcome(self):
        win = tk.Toplevel(self.root)
        win.title(t("welcome_title"))
        win.attributes("-topmost", True)
        win.resizable(False, False)

        frame = ttk.Frame(win, padding=16); frame.pack(fill="both", expand=True)
        ttk.Label(frame, text=t("welcome_head"), font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0,8))

        mode_text = t("welcome_mode_work") if WORK_HOURS_ONLY else t("welcome_mode_always")
        desc = t("welcome_desc", mode=mode_text, next_dt=humanize_dt(self._next_alarm_dt()))
        ttk.Label(frame, text=desc, justify="left").pack(anchor="w")

        dont_show = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text=t("welcome_dont_show"), variable=dont_show).pack(anchor="w", pady=(8,0))

        btns = ttk.Frame(frame); btns.pack(fill="x", pady=(12,0))
        def disable_workhours():
            global WORK_HOURS_ONLY
            WORK_HOURS_ONLY = False
            self.next_due_ts = time.time() + REMIND_EVERY_MIN * 60
            save_prefs({"show_welcome": dont_show.get()})
            self._update_tray_title()
            messagebox.showinfo(t("app_name"), t("msg_wh_disabled"))
        ttk.Button(btns, text=t("welcome_disable_workhours"), command=disable_workhours).pack(side="left")

        def ok_close():
            save_prefs({"show_welcome": dont_show.get()})
            win.destroy()
        ttk.Button(btns, text=t("btn_ok"), command=ok_close).pack(side="right")

        center_window(win, 560, 260)

    def _show_status(self):
        next_dt = self._next_alarm_dt()
        mode = t("welcome_mode_work") if WORK_HOURS_ONLY else t("welcome_mode_always")
        paused = time.time() < self.paused_until_ts
        msg = "\n".join([
            t("status_mode", mode=mode),
            t("status_en", onoff=t("on") if EN_MODE else t("off")),
            t("status_pause", yesno=t("yes") if paused else t("no")),
            t("status_next", dt=humanize_dt(next_dt)),
        ])
        messagebox.showinfo(t("status_title"), msg)

    # -------- tray
    def _make_tray_image(self, size=64):
        img = Image.new("RGBA", (size, size), (0,0,0,0))
        d = ImageDraw.Draw(img)
        d.ellipse((4, 12, size-4, size-12), fill=(255,255,255,255), outline=(40,40,40,255), width=2)
        d.ellipse((size//2-10, size//2-10, size//2+10, size//2+10), fill=(40,40,40,255))
        return img

    def _tray_title_text(self):
        now = datetime.now()
        base = t("tray_title_base")
        if time.time() < self.paused_until_ts:
            return base + t("tray_title_paused")
        if WORK_HOURS_ONLY and not is_within_work_hours(now):
            return base + t("tray_title_ooh")
        mins = int(max(0, (self._next_alarm_dt() - now).total_seconds() // 60))
        return base + t("tray_title_next", mins=mins)

    def _update_tray_title(self):
        if not self.tray_icon:
            return
        try:
            self.tray_icon.title = self._tray_title_text()
        except Exception:
            pass

    def _init_tray(self):
        def show_now(icon, item):
            self.root.after(0, lambda: self._show_popup(force=True))

        def snooze_5(icon, item):
            self.root.after(0, lambda: (self._schedule_after(SNOOZE_MIN*60), self._on_close_popup()))

        def pause_30(icon, item):
            self.root.after(0, lambda: (setattr(self, "paused_until_ts", time.time()+30*60), self._on_close_popup(), self._update_tray_title()))

        def toggle_workhours(icon, item):
            def _do():
                global WORK_HOURS_ONLY
                WORK_HOURS_ONLY = not WORK_HOURS_ONLY
                self.next_due_ts = self._compute_next_due()
                save_prefs()
                self._update_tray_title()
            self.root.after(0, _do)

        def toggle_en_mode(icon, item):
            def _do():
                global EN_MODE
                EN_MODE = not EN_MODE
                save_prefs()
                # 팝업이 열려 있으면 UI 문구 즉시 갱신
                try:
                    if self.popup and self.tip_label:
                        _, txt = self._random_tip(None)
                        # 상단 텍스트/버튼/레이블도 갱신
                        for w in self.popup.winfo_children():
                            w.destroy()
                        # 팝업을 다시 그려 가장 간단히 언어 전체 갱신
                        self._show_popup(force=True)
                    # 트레이 라벨/툴팁 갱신
                    self.tray_icon.menu = pystray.Menu(
                        pystray.MenuItem(t("tray_show_now"), show_now),
                        pystray.MenuItem(t("tray_snooze", mins=SNOOZE_MIN), snooze_5),
                        pystray.MenuItem(t("tray_pause"), pause_30),
                        pystray.MenuItem(lambda item: t("tray_toggle_en", onoff=t("on") if EN_MODE else t("off")), toggle_en_mode),
                        pystray.MenuItem(lambda item: t("tray_toggle_wh", onoff=t("on") if WORK_HOURS_ONLY else t("off")), toggle_workhours),
                        pystray.MenuItem(t("tray_status"), show_status),
                        pystray.MenuItem(t("tray_quit"), quit_app),
                    )
                except Exception:
                    pass
                self._update_tray_title()
            self.root.after(0, _do)

        def show_status(icon, item):
            self.root.after(0, self._show_status)

        def quit_app(icon, item):
            def _do():
                try:
                    if self.tray_icon is not None:
                        self.tray_icon.visible = False
                        self.tray_icon.stop()
                except Exception:
                    pass
                self.root.after(0, self.root.quit)
            self.root.after(0, _do)

        image = self._make_tray_image() if TRAY_AVAILABLE else None
        self.tray_icon = pystray.Icon(
            t("app_name"),
            image,
            t("app_name"),
            menu=pystray.Menu(
                pystray.MenuItem(t("tray_show_now"), show_now),
                pystray.MenuItem(t("tray_snooze", mins=SNOOZE_MIN), snooze_5),
                pystray.MenuItem(t("tray_pause"), pause_30),
                pystray.MenuItem(lambda item: t("tray_toggle_en", onoff=t("on") if EN_MODE else t("off")), toggle_en_mode),
                pystray.MenuItem(lambda item: t("tray_toggle_wh", onoff=t("on") if WORK_HOURS_ONLY else t("off")), toggle_workhours),
                pystray.MenuItem(t("tray_status"), show_status),
                pystray.MenuItem(t("tray_quit"), quit_app),
            )
        )
        threading.Thread(target=self.tray_icon.run, daemon=True).start()
        self.root.after(300, self._update_tray_title)

    # -------- loop
    def _tick(self):
        now = time.time()

        if now < self.paused_until_ts:
            if TRAY_AVAILABLE: self._update_tray_title()
            self.root.after(500, self._tick); return

        if WORK_HOURS_ONLY and not is_within_work_hours(datetime.now()):
            self.next_due_ts = self._compute_next_due()
            if TRAY_AVAILABLE: self._update_tray_title()
            self.root.after(500, self._tick); return

        if now >= self.next_due_ts:
            self._show_popup()
        if TRAY_AVAILABLE:
            self._update_tray_title()

        self.root.after(500, self._tick)

def main():
    root = tk.Tk()
    root.title("BlinkBuddy (background)")
    root.geometry("0x0+0+0")
    BlinkBuddyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
