"""
system_tasks.py — All system functions with visible error output
"""

import os
import subprocess
import webbrowser


# ─────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────

def run(cmd: str):
    """Run a shell command and print any errors."""
    try:
        result = subprocess.run(
            cmd, shell=True,
            capture_output=True, text=True
        )
        if result.returncode != 0 and result.stderr:
            print(f"⚠️ Command warning: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False

def run_ps(cmd: str):
    """Run a PowerShell command and print any errors."""
    try:
        result = subprocess.run(
            ['powershell', '-NonInteractive', '-WindowStyle', 'Hidden', '-Command', cmd],
            capture_output=True, text=True
        )
        if result.stderr:
            print(f"⚠️ PS warning: {result.stderr.strip()[:100]}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ PowerShell error: {e}")
        return False


# ─────────────────────────────────────────
# OPEN APPS
# ─────────────────────────────────────────

def open_chrome():
    paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for p in paths:
        if os.path.exists(p):
            subprocess.Popen([p])
            print("✅ Chrome opened")
            return
    run("start chrome")

def open_explorer():
    subprocess.Popen(['explorer'])
    print("✅ Explorer opened")

def open_calculator():
    subprocess.Popen(['calc'])
    print("✅ Calculator opened")

def open_notepad():
    subprocess.Popen(['notepad'])
    print("✅ Notepad opened")

def open_word():
    run("start winword")
    print("✅ Word opened")

def open_excel():
    run("start excel")
    print("✅ Excel opened")

def open_powerpoint():
    run("start powerpnt")
    print("✅ PowerPoint opened")

def open_vscode():
    run("code")
    print("✅ VS Code opened")

def open_whatsapp():
    webbrowser.open("https://web.whatsapp.com")
    print("✅ WhatsApp opened")

def open_settings():
    subprocess.Popen(['start', 'ms-settings:'], shell=True)
    print("✅ Settings opened")

def open_task_manager():
    subprocess.Popen(['taskmgr'])
    print("✅ Task Manager opened")

def open_cmd():
    subprocess.Popen(['start', 'cmd'], shell=True)
    print("✅ CMD opened")

def open_powershell():
    subprocess.Popen(['start', 'powershell'], shell=True)
    print("✅ PowerShell opened")

def open_store():
    subprocess.Popen(['start', 'ms-windows-store:'], shell=True)
    print("✅ Store opened")

def open_camera():
    subprocess.Popen(['start', 'microsoft.windows.camera:'], shell=True)
    print("✅ Camera opened")

def open_telegram():
    webbrowser.open("https://web.telegram.org")
    print("✅ Telegram opened")

def open_zoom():
    subprocess.Popen(['start', 'zoommtg:'], shell=True)
    print("✅ Zoom opened")

def open_browser():
    webbrowser.open("https://google.com")
    print("✅ Browser opened")

def open_music():
    music_folder = os.path.join(os.path.expanduser("~"), "Music")
    if os.path.exists(music_folder):
        songs = [f for f in os.listdir(music_folder)
                 if f.endswith(('.mp3', '.wav', '.m4a', '.flac'))]
        if songs:
            os.startfile(os.path.join(music_folder, songs[0]))
            print("✅ Music playing")
            return
    webbrowser.open("https://open.spotify.com")
    print("✅ Spotify opened")


# ─────────────────────────────────────────
# CLOSE APPS
# ─────────────────────────────────────────

def close_app_by_name(process_name: str):
    result = subprocess.run(
        ['taskkill', '/f', '/im', process_name],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"✅ {process_name} closed")
    else:
        print(f"⚠️ Could not close {process_name}: {result.stderr.strip()}")

def close_chrome():      close_app_by_name("chrome.exe")
def close_word():        close_app_by_name("winword.exe")
def close_excel():       close_app_by_name("excel.exe")
def close_powerpoint():  close_app_by_name("powerpnt.exe")
def close_notepad():     close_app_by_name("notepad.exe")
def close_vscode():      close_app_by_name("code.exe")
def close_taskmanager(): close_app_by_name("taskmgr.exe")

def close_whatsapp():
    try:
        import pyautogui
        pyautogui.hotkey('ctrl', 'w')
        print("✅ WhatsApp tab closed")
    except:
        close_app_by_name("chrome.exe")

def close_current_app():
    try:
        import pyautogui
        pyautogui.hotkey('alt', 'F4')
        print("✅ Current app closed")
    except Exception as e:
        print(f"❌ close_current_app error: {e}")

def close_current_tab():
    try:
        run_ps("Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('^w')")
        print("Tab closed")
    except Exception as e:
        print("close_tab error: " + str(e))


# ─────────────────────────────────────────
# VOLUME — using nircmd or PowerShell WScript
# ─────────────────────────────────────────

def _send_key(key_code: int, times: int = 1):
    """Send a virtual key press via PowerShell WScript."""
    script = f"""
    $wsh = New-Object -ComObject WScript.Shell
    for ($i=0; $i -lt {times}; $i++) {{
        $wsh.SendKeys([char]{key_code})
        Start-Sleep -Milliseconds 50
    }}
    """
    result = subprocess.run(
        ['powershell', '-NonInteractive', '-Command', script],
        capture_output=True, text=True
    )
    return result.returncode == 0

def volume_up():
    # Key code 175 = VK_VOLUME_UP
    if _send_key(175, 5):
        print("✅ Volume increased")
    else:
        # fallback via nircmd
        run("nircmd.exe changesysvolume 5000")

def volume_down():
    # Key code 174 = VK_VOLUME_DOWN
    if _send_key(174, 5):
        print("✅ Volume decreased")
    else:
        run("nircmd.exe changesysvolume -5000")

def mute_volume():
    # Key code 173 = VK_VOLUME_MUTE
    if _send_key(173):
        print("✅ Volume muted/unmuted")
    else:
        run("nircmd.exe mutesysvolume 2")

def unmute_volume():
    mute_volume()


# ─────────────────────────────────────────
# BRIGHTNESS — via PowerShell WMI
# ─────────────────────────────────────────

def _get_brightness():
    try:
        result = subprocess.run(
            ['powershell', '-Command',
             '(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness'],
            capture_output=True, text=True, timeout=5
        )
        return int(result.stdout.strip())
    except:
        return 50

def _set_brightness(level: int):
    level = max(0, min(100, level))
    result = subprocess.run(
        ['powershell', '-Command',
         f'(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})'],
        capture_output=True, text=True, timeout=5
    )
    if result.returncode == 0:
        print(f"✅ Brightness set to {level}%")
    else:
        print(f"⚠️ Brightness error: {result.stderr.strip()[:80]}")

def brightness_up():
    current = _get_brightness()
    _set_brightness(current + 20)

def brightness_down():
    current = _get_brightness()
    _set_brightness(current - 20)


# ─────────────────────────────────────────
# WI-FI — via netsh
# ─────────────────────────────────────────

def wifi_on():
    result = subprocess.run(
        'netsh interface set interface "Wi-Fi" enable',
        shell=True, capture_output=True, text=True
    )
    if result.returncode == 0:
        print("✅ WiFi enabled")
    else:
        # Try alternate interface names
        for name in ["WiFi", "Wireless Network Connection", "Wi-Fi 2"]:
            r = subprocess.run(
                f'netsh interface set interface "{name}" enable',
                shell=True, capture_output=True, text=True
            )
            if r.returncode == 0:
                print(f"✅ WiFi enabled ({name})")
                return
        print(f"⚠️ WiFi enable failed: {result.stderr.strip()}")

def wifi_off():
    result = subprocess.run(
        'netsh interface set interface "Wi-Fi" disable',
        shell=True, capture_output=True, text=True
    )
    if result.returncode == 0:
        print("✅ WiFi disabled")
    else:
        for name in ["WiFi", "Wireless Network Connection", "Wi-Fi 2"]:
            r = subprocess.run(
                f'netsh interface set interface "{name}" disable',
                shell=True, capture_output=True, text=True
            )
            if r.returncode == 0:
                print(f"✅ WiFi disabled ({name})")
                return
        print(f"⚠️ WiFi disable failed: {result.stderr.strip()}")

def get_wifi_status():
    result = subprocess.run(
        'netsh interface show interface "Wi-Fi"',
        shell=True, capture_output=True, text=True
    )
    if 'Connected' in result.stdout or 'Enabled' in result.stdout:
        return "Wi-Fi wa ni ipo sisẹ."
    return "Wi-Fi wa ni ipo pa."


# ─────────────────────────────────────────
# BLUETOOTH — via PowerShell
# ─────────────────────────────────────────

def bluetooth_on():
    script = """
    $bt = Get-PnpDevice -Class Bluetooth -ErrorAction SilentlyContinue
    if ($bt) {
        $bt | Enable-PnpDevice -Confirm:$false -ErrorAction SilentlyContinue
        Write-Output "OK"
    } else {
        Write-Output "NO_BT"
    }
    """
    result = subprocess.run(
        ['powershell', '-NonInteractive', '-Command', script],
        capture_output=True, text=True, timeout=10
    )
    if "OK" in result.stdout:
        print("✅ Bluetooth enabled")
    elif "NO_BT" in result.stdout:
        print("⚠️ No Bluetooth device found")
    else:
        print(f"⚠️ Bluetooth on failed: {result.stderr.strip()[:80]}")

def bluetooth_off():
    script = """
    $bt = Get-PnpDevice -Class Bluetooth -ErrorAction SilentlyContinue
    if ($bt) {
        $bt | Disable-PnpDevice -Confirm:$false -ErrorAction SilentlyContinue
        Write-Output "OK"
    } else {
        Write-Output "NO_BT"
    }
    """
    result = subprocess.run(
        ['powershell', '-NonInteractive', '-Command', script],
        capture_output=True, text=True, timeout=10
    )
    if "OK" in result.stdout:
        print("✅ Bluetooth disabled")
    elif "NO_BT" in result.stdout:
        print("⚠️ No Bluetooth device found")
    else:
        print(f"⚠️ Bluetooth off failed: {result.stderr.strip()[:80]}")


# ─────────────────────────────────────────
# SCREENSHOT
# ─────────────────────────────────────────

def take_screenshot():
    import time
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    pics = os.path.join(os.path.expanduser("~"), "Pictures")
    os.makedirs(pics, exist_ok=True)
    save_path = os.path.join(pics, f"screenshot_{timestamp}.png").replace("\\", "\\\\")
    script = f"""
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing
    $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    $bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
    $bitmap.Save('{save_path}')
    Write-Output "SAVED"
    """
    result = subprocess.run(
        ['powershell', '-NonInteractive', '-Command', script],
        capture_output=True, text=True, timeout=10
    )
    if "SAVED" in result.stdout:
        print(f"✅ Screenshot saved: {save_path}")
    else:
        print(f"⚠️ Screenshot failed: {result.stderr.strip()[:80]}")
        # Fallback: use Snipping Tool
        subprocess.Popen(['snippingtool'])


# ─────────────────────────────────────────
# LOCK / SLEEP / SHUTDOWN / RESTART
# ─────────────────────────────────────────

def lock_screen():
    result = subprocess.run(
        ['rundll32.exe', 'user32.dll,LockWorkStation'],
        capture_output=True, text=True
    )
    print("✅ Screen locked")

def sleep_computer():
    result = subprocess.run(
        ['rundll32.exe', 'powrprof.dll,SetSuspendState', '0,1,0'],
        capture_output=True, text=True
    )
    print("✅ Computer sleeping")

def shutdown():
    result = subprocess.run(
        ['shutdown', '/s', '/t', '5'],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print("✅ Shutting down in 5 seconds")
    else:
        print(f"⚠️ Shutdown failed: {result.stderr.strip()}")

def restart():
    result = subprocess.run(
        ['shutdown', '/r', '/t', '5'],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print("✅ Restarting in 5 seconds")
    else:
        print(f"⚠️ Restart failed: {result.stderr.strip()}")


# ─────────────────────────────────────────
# SYSTEM INFO
# ─────────────────────────────────────────

def get_battery():
    try:
        import psutil
        b = psutil.sensors_battery()
        if b:
            status = "ti o n gba agbara" if b.power_plugged else "ko si lori ina"
            return f"Batiri re wa ni ipele {int(b.percent)} ogorun, {status}."
        return "Emi ko le ri alaye nipa batiri re."
    except Exception as e:
        return f"Emi ko le se ayewo batiri: {e}"

def get_storage():
    try:
        import psutil
        d = psutil.disk_usage('C:\\')
        free_gb  = d.free  / (1024**3)
        total_gb = d.total / (1024**3)
        return f"Ipamo re: {free_gb:.1f} GB free ninu {total_gb:.1f} GB lapapọ."
    except Exception as e:
        return f"Emi ko le se ayewo ipamo: {e}"

def get_ram():
    try:
        import psutil
        r = psutil.virtual_memory()
        used_gb  = r.used  / (1024**3)
        total_gb = r.total / (1024**3)
        return f"Memory re: {used_gb:.1f} GB lo ninu {total_gb:.1f} GB lapapọ."
    except Exception as e:
        return f"Emi ko le se ayewo memory: {e}"

def get_cpu():
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=1)
        return f"Processor re n lo {cpu:.0f} ogorun agbara lọwọlọwọ."
    except Exception as e:
        return f"Emi ko le se ayewo processor: {e}"


# ─────────────────────────────────────────
# SEARCH & BROWSER
# ─────────────────────────────────────────

def search_google(query: str):
    webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
    print(f"✅ Searching Google: {query}")

def search_youtube(query: str):
    webbrowser.open(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
    print(f"✅ Searching YouTube: {query}")

def open_new_tab():
    try:
        import pyautogui
        pyautogui.hotkey('ctrl', 't')
        print("✅ New tab opened")
    except:
        webbrowser.open("https://google.com")

def go_back():
    try:
        import pyautogui
        pyautogui.hotkey('alt', 'left')
        print("✅ Went back")
    except Exception as e:
        print(f"❌ go_back error: {e}")

def refresh_page():
    try:
        import pyautogui
        pyautogui.hotkey('ctrl', 'r')
        print("✅ Page refreshed")
    except Exception as e:
        print(f"❌ refresh error: {e}")

def check_weather():
    webbrowser.open("https://www.google.com/search?q=weather")
    print("✅ Weather opened")


# ─────────────────────────────────────────
# MEDIA CONTROLS
# ─────────────────────────────────────────

def pause_music():
    if _send_key(179):
        print("✅ Music paused/resumed")

def next_song():
    if _send_key(176):
        print("✅ Next song")

def prev_song():
    if _send_key(177):
        print("✅ Previous song")
