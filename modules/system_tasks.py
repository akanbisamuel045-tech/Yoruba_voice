"""
system_tasks.py — Fixed WiFi, Bluetooth, Brightness
"""

import os
import subprocess
import webbrowser


# ─────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────

def run(cmd: str, shell: bool = True):
    subprocess.Popen(cmd, shell=shell,
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)

def run_ps(cmd: str):
    subprocess.Popen(
        ['powershell', '-NonInteractive', '-WindowStyle', 'Hidden', '-Command', cmd],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def run_ps_output(cmd: str) -> str:
    result = subprocess.run(
        ['powershell', '-NonInteractive', '-Command', cmd],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def run_as_admin(cmd: str):
    """Run a command with admin privileges via PowerShell."""
    subprocess.Popen(
        ['powershell', '-Command',
         f'Start-Process powershell -ArgumentList "-Command {cmd}" -Verb RunAs -WindowStyle Hidden'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


# ─────────────────────────────────────────
# OPEN APPS
# ─────────────────────────────────────────

def open_chrome():
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if os.path.exists(chrome):
        run(f'"{chrome}"')
    else:
        run("start chrome")

def open_explorer():   run("explorer")
def open_calculator(): run("calc")
def open_notepad():    run("notepad")
def open_word():       run("start winword")
def open_excel():      run("start excel")
def open_powerpoint(): run("start powerpnt")
def open_vscode():     run("code")
def open_settings():   run("start ms-settings:")
def open_task_manager(): run("taskmgr")
def open_cmd():        run("start cmd")
def open_powershell(): run("start powershell")
def open_store():      run("start ms-windows-store:")
def open_camera():     run("start microsoft.windows.camera:")
def open_email():      run("start outlookmail:")
def open_browser():    webbrowser.open("https://google.com")
def open_whatsapp():   webbrowser.open("https://web.whatsapp.com")

def open_gitbash():
    for p in [r"C:\Program Files\Git\git-bash.exe",
              r"C:\Program Files (x86)\Git\git-bash.exe"]:
        if os.path.exists(p):
            run(f'"{p}"')
            return
    run("start git-bash")

def open_music():
    music_folder = os.path.expanduser("~/Music")
    if os.path.exists(music_folder):
        songs = [f for f in os.listdir(music_folder)
                 if f.endswith(('.mp3', '.wav', '.m4a', '.flac'))]
        if songs:
            os.startfile(os.path.join(music_folder, songs[0]))
            return
    webbrowser.open("https://open.spotify.com")


# ─────────────────────────────────────────
# CLOSE APPS
# ─────────────────────────────────────────

def close_app_by_name(process_name: str):
    run(f"taskkill /f /im {process_name}")

def close_chrome():      close_app_by_name("chrome.exe")
def close_word():        close_app_by_name("winword.exe")
def close_excel():       close_app_by_name("excel.exe")
def close_powerpoint():  close_app_by_name("powerpnt.exe")
def close_notepad():     close_app_by_name("notepad.exe")
def close_whatsapp():    close_chrome()
def close_vscode():      close_app_by_name("code.exe")
def close_taskmanager(): close_app_by_name("taskmgr.exe")

def close_current_app():
    run_ps("""
    Add-Type @'
    using System;
    using System.Runtime.InteropServices;
    public class WinAPI {
        [DllImport("user32.dll")]
        public static extern IntPtr GetForegroundWindow();
        [DllImport("user32.dll")]
        public static extern bool PostMessage(IntPtr hWnd, uint Msg, IntPtr wParam, IntPtr lParam);
    }
'@
    $hwnd = [WinAPI]::GetForegroundWindow()
    [WinAPI]::PostMessage($hwnd, 0x0010, [IntPtr]::Zero, [IntPtr]::Zero)
    """)

def close_current_tab():
    run_ps("""
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.SendKeys]::SendWait("^w")
    """)

def close_tab():
    close_current_tab()


# ─────────────────────────────────────────
# VOLUME
# ─────────────────────────────────────────

def volume_up():
    run_ps("$wsh = New-Object -ComObject WScript.Shell; 1..5 | ForEach-Object { $wsh.SendKeys([char]175) }")

def volume_down():
    run_ps("$wsh = New-Object -ComObject WScript.Shell; 1..5 | ForEach-Object { $wsh.SendKeys([char]174) }")

def mute_volume():
    run_ps("$wsh = New-Object -ComObject WScript.Shell; $wsh.SendKeys([char]173)")

def unmute_volume():
    mute_volume()


# ─────────────────────────────────────────
# BRIGHTNESS — fixed for external monitors
# Uses keyboard brightness keys via SendKeys
# ─────────────────────────────────────────

def brightness_up():
    # Try WMI first (works on laptops)
    result = run_ps_output(
        '(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness'
    )
    try:
        current = int(result)
        level   = min(100, current + 20)
        run_ps(f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})")
        return
    except:
        pass
    # Fallback: use Windows display settings
    run("start ms-settings:display")

def brightness_down():
    result = run_ps_output(
        '(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness'
    )
    try:
        current = int(result)
        level   = max(0, current - 20)
        run_ps(f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})")
        return
    except:
        pass
    run("start ms-settings:display")


# ─────────────────────────────────────────
# WI-FI — fixed with admin elevation
# ─────────────────────────────────────────

def wifi_on():
    # Try without admin first
    result = subprocess.run(
        'netsh interface set interface "Wi-Fi" enable',
        shell=True, capture_output=True, text=True
    )
    if result.returncode != 0:
        # Elevate with admin
        run_as_admin('netsh interface set interface \\"Wi-Fi\\" enable')

def wifi_off():
    result = subprocess.run(
        'netsh interface set interface "Wi-Fi" disable',
        shell=True, capture_output=True, text=True
    )
    if result.returncode != 0:
        run_as_admin('netsh interface set interface \\"Wi-Fi\\" disable')

def get_wifi_status() -> str:
    result = subprocess.run(
        'netsh interface show interface "Wi-Fi"',
        shell=True, capture_output=True, text=True
    )
    if 'Connected' in result.stdout:
        return "Wi-Fi wa ni ipo sisẹ ati ti sopọ."
    elif 'Enabled' in result.stdout:
        return "Wi-Fi wa ni ipo sisẹ sugbon ko ti sopọ."
    return "Wi-Fi wa ni ipo pa."


# ─────────────────────────────────────────
# BLUETOOTH — fixed to target Intel radio only
# ─────────────────────────────────────────

def bluetooth_on():
    # Target the Intel Bluetooth radio specifically
    run_ps("""
    $bt = Get-PnpDevice | Where-Object { $_.FriendlyName -like '*Intel*Bluetooth*' -or $_.FriendlyName -like '*Wireless Bluetooth*' }
    if ($bt) {
        $bt | Enable-PnpDevice -Confirm:$false -ErrorAction SilentlyContinue
    } else {
        Get-PnpDevice -Class Bluetooth | Where-Object { $_.Status -ne 'Unknown' } | Enable-PnpDevice -Confirm:$false -ErrorAction SilentlyContinue
    }
    """)

def bluetooth_off():
    run_ps("""
    $bt = Get-PnpDevice | Where-Object { $_.FriendlyName -like '*Intel*Bluetooth*' -or $_.FriendlyName -like '*Wireless Bluetooth*' }
    if ($bt) {
        $bt | Disable-PnpDevice -Confirm:$false -ErrorAction SilentlyContinue
    } else {
        Get-PnpDevice -Class Bluetooth | Where-Object { $_.Status -ne 'Unknown' } | Disable-PnpDevice -Confirm:$false -ErrorAction SilentlyContinue
    }
    """)


# ─────────────────────────────────────────
# SCREENSHOT
# ─────────────────────────────────────────

def take_screenshot():
    import time
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    save_path = os.path.join(os.path.expanduser("~"), "Pictures",
                             f"screenshot_{timestamp}.png")
    run_ps(f"""
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing
    $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    $bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
    $bitmap.Save('{save_path}')
    """)
    return save_path


# ─────────────────────────────────────────
# LOCK / SLEEP / SHUTDOWN / RESTART
# ─────────────────────────────────────────

def lock_screen():    run("rundll32.exe user32.dll,LockWorkStation")
def sleep_computer(): run("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
def shutdown():       run("shutdown /s /t 5")
def restart():        run("shutdown /r /t 5")


# ─────────────────────────────────────────
# SYSTEM INFO
# ─────────────────────────────────────────

def get_battery() -> str:
    try:
        import psutil
        b = psutil.sensors_battery()
        if b:
            status = "ti o n gba agbara" if b.power_plugged else "ko si lori ina"
            return f"Batiri re wa ni ipele {int(b.percent)} ogorun, {status}."
        return "Emi ko le ri alaye nipa batiri re."
    except:
        return "Emi ko le se ayewo batiri."

def get_storage() -> str:
    try:
        import psutil
        d = psutil.disk_usage('C:\\')
        return f"Ipamo re: {d.free/(1024**3):.1f} GB free ninu {d.total/(1024**3):.1f} GB lapapọ."
    except:
        return "Emi ko le se ayewo ipamo."

def get_ram() -> str:
    try:
        import psutil
        r = psutil.virtual_memory()
        return f"Memory re: {r.used/(1024**3):.1f} GB lo ninu {r.total/(1024**3):.1f} GB lapapọ."
    except:
        return "Emi ko le se ayewo memory."

def get_cpu() -> str:
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=1)
        return f"Processor re n lo {cpu:.0f} ogorun agbara lọwọlọwọ."
    except:
        return "Emi ko le se ayewo processor."


# ─────────────────────────────────────────
# SEARCH & BROWSER
# ─────────────────────────────────────────

def search_google(query: str):
    webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")

def search_youtube(query: str):
    webbrowser.open(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")

def open_new_tab():
    run_ps("Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('^t')")

def go_back():
    run_ps("Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('%{LEFT}')")

def refresh_page():
    run_ps("Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('^r')")

def check_weather():
    webbrowser.open("https://www.google.com/search?q=weather")


# ─────────────────────────────────────────
# MEDIA CONTROLS
# ─────────────────────────────────────────

def pause_music(): run_ps("$wsh = New-Object -ComObject WScript.Shell; $wsh.SendKeys([char]179)")
def next_song():   run_ps("$wsh = New-Object -ComObject WScript.Shell; $wsh.SendKeys([char]176)")
def prev_song():   run_ps("$wsh = New-Object -ComObject WScript.Shell; $wsh.SendKeys([char]177)")


# ─────────────────────────────────────────
# ALARM
# ─────────────────────────────────────────

def set_alarm(minutes: int = 5):
    run_ps(f"""
    $time = (Get-Date).AddMinutes({minutes})
    $action = New-ScheduledTaskAction -Execute 'powershell' -Argument '-Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show(\"Akoko ti to!\", \"Alarinrin\")"'
    $trigger = New-ScheduledTaskTrigger -Once -At $time
    Register-ScheduledTask -Action $action -Trigger $trigger -TaskName 'YorubaAlarm' -Force
    """)

def cancel_alarm():
    run_ps("Unregister-ScheduledTask -TaskName 'YorubaAlarm' -Confirm:$false -ErrorAction SilentlyContinue")

def smart_home_on():  return "Iṣẹ smart home ko ti wa ni ipo sisẹ."
def smart_home_off(): return "Iṣẹ smart home ko ti wa ni ipo sisẹ."
