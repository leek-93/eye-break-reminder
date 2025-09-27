# check_startup.py
import os, sys
import winreg

NAME = "BlinkBuddy"

try:
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run")
    val, typ = winreg.QueryValueEx(key, NAME)
    winreg.CloseKey(key)
    print(f"[OK] Registered value:\n  {val}")
    # 실행 파일/인터프리터 경로가 실제 존재하는지 대략 확인
    cmd = val.strip().strip('"')
    path = cmd.split('"')[1] if cmd.startswith('"') and cmd.count('"')>=2 else cmd.split(' ')[0]
    print(f"Exists on disk?: {os.path.exists(path)}")
except FileNotFoundError:
    print("[X] Not registered")
