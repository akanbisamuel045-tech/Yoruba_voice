# -*- coding: utf-8 -*-
import joblib
import numpy as np
from datetime import datetime
from modules.text_to_speech import speak
from modules.system_tasks import *

model = joblib.load("models/intent_model.pkl")

CONFIDENCE_THRESHOLD = 0.30

def execute(text: str):
    if not text.strip():
        return

    probs      = model.predict_proba([text])[0]
    confidence = np.max(probs)
    intent     = model.classes_[np.argmax(probs)]

    print("Intent: " + intent + " (" + str(round(confidence * 100)) + "%)")

    if confidence < CONFIDENCE_THRESHOLD:
        speak("Emi ko ye ibeere naa. E jowo tun so.")
        return

    # ── GREETINGS & SOCIAL ──────────────────────────────────
    if intent == "greeting":
        speak("Mo wa daadaa. Bawo ni iwo?")

    elif intent == "name":
        speak("Oruko mi ni Oluranlowo Yoruba.")

    elif intent == "self_intro":
        speak("Emi ni Oluranlowo Yoruba, eto iranlowo ohun ede Yoruba.")

    elif intent == "what_can_you_do":
        speak("Mo le ṣi awọn eto, wa alaye, ṣakoso kọmputa re, ati dahun ibeere re.")

    elif intent == "thanks":
        speak("E kaabo. Mo dupe lowo re.")

    elif intent == "apology":
        speak("Ẹ ma binu. Mo gba itẹwọgba re.")

    elif intent == "confirm":
        speak("Beeni, mo gbo.")

    elif intent == "cancel":
        speak("O dara, mo fagilee.")

    elif intent == "help":
        speak("Mo wa nibi lati ran ọ lọwọ. Kini o nilo?")

    elif intent == "learn":
        speak("Mo n kọ lati awọn ọrọ rẹ lojoojumọ.")

    # ── TIME & DATE ──────────────────────────────────────────
    elif intent == "time":
        current = datetime.now().strftime("%H:%M")
        speak("Akoko ni " + current)

    elif intent == "date":
        today = datetime.now().strftime("%A, %d %B %Y")
        speak("Ojo oni ni " + today)

    elif intent == "alarm":
        speak("Mo n seto alarinrin fun iṣẹju marun.")
        set_alarm(5)

    elif intent == "reminder":
        speak("Iṣẹ iranti ko ti wa ni ipo siṣẹ patapata.")

    elif intent == "calendar":
        speak("Mo n ṣi kalẹnda.")
        run("start outlookcal:")

    # ── OPEN APPS ────────────────────────────────────────────
    elif intent == "chrome":
        speak("Mo n ṣi Google Chrome.")
        open_chrome()

    elif intent == "browser":
        speak("Mo n ṣi aṣawakiri.")
        open_browser()

    elif intent == "explorer":
        speak("Mo n ṣi File Explorer.")
        open_explorer()

    elif intent == "calculator":
        speak("Mo n ṣi Calculator.")
        open_calculator()

    elif intent == "notepad":
        speak("Mo n ṣi Notepad.")
        open_notepad()

    elif intent == "word":
        speak("Mo n ṣi Microsoft Word.")
        open_word()

    elif intent == "excel":
        speak("Mo n ṣi Microsoft Excel.")
        open_excel()

    elif intent == "powerpoint":
        speak("Mo n ṣi PowerPoint.")
        open_powerpoint()

    elif intent == "vscode":
        speak("Mo n ṣi VS Code.")
        open_vscode()

    elif intent == "whatsapp":
        speak("Mo n ṣi WhatsApp.")
        open_whatsapp()

    elif intent == "settings":
        speak("Mo n ṣi Settings.")
        open_settings()

    elif intent == "taskmanager":
        speak("Mo n ṣi Task Manager.")
        open_task_manager()

    elif intent == "cmd":
        speak("Mo n ṣi Command Prompt.")
        open_cmd()

    elif intent == "powershell":
        speak("Mo n ṣi PowerShell.")
        open_powershell()

    elif intent == "gitbash":
        speak("Mo n ṣi Git Bash.")
        open_gitbash()

    elif intent == "store":
        speak("Mo n ṣi Microsoft Store.")
        open_store()

    elif intent == "camera":
        speak("Mo n ṣi Camera.")
        open_camera()

    elif intent == "email":
        speak("Mo n ṣi imeeli.")
        open_email()

    elif intent == "music":
        speak("Mo n ṣe orin.")
        open_music()

    # ── CLOSE APPS ───────────────────────────────────────────
    elif intent == "close_app":
        speak("Mo n pa eto ti o wa ni iwaju.")
        close_current_app()

    elif intent == "close_chrome":
        speak("Mo n pa Google Chrome.")
        close_chrome()

    elif intent == "close_word":
        speak("Mo n pa Microsoft Word.")
        close_word()

    elif intent == "close_excel":
        speak("Mo n pa Microsoft Excel.")
        close_excel()

    elif intent == "close_notepad":
        speak("Mo n pa Notepad.")
        close_notepad()

    elif intent == "close_whatsapp":
        speak("Mo n pa WhatsApp.")
        close_whatsapp()

    elif intent == "close_tab":
        speak("Mo n pa tab yi.")
        close_current_tab()

    # ── VOLUME ───────────────────────────────────────────────
    elif intent == "volume_up":
        speak("Mo n gbe ohun soke.")
        volume_up()

    elif intent == "volume_down":
        speak("Mo n dinku ohun.")
        volume_down()

    elif intent == "mute":
        speak("Mo ti pa ohun.")
        mute_volume()

    # ── BRIGHTNESS ───────────────────────────────────────────
    elif intent == "brightness_up":
        speak("Mo n gbe imole soke.")
        brightness_up()

    elif intent == "brightness_down":
        speak("Mo n dinku imole.")
        brightness_down()

    # ── WI-FI ────────────────────────────────────────────────
    elif intent == "wifi_on":
        speak("Mo n tan Wi-Fi.")
        wifi_on()

    elif intent == "wifi_off":
        speak("Mo n pa Wi-Fi.")
        wifi_off()

    # ── BLUETOOTH ────────────────────────────────────────────
    elif intent == "bluetooth_on":
        speak("Mo n tan Bluetooth.")
        bluetooth_on()

    elif intent == "bluetooth_off":
        speak("Mo n pa Bluetooth.")
        bluetooth_off()

    # ── SYSTEM CONTROLS ──────────────────────────────────────
    elif intent == "shutdown":
        speak("Mo n pa kọmputa. O dabo.")
        shutdown()

    elif intent == "restart":
        speak("Mo n bere kọmputa leekansi.")
        restart()

    elif intent == "lock":
        speak("Mo n tiipa iboju.")
        lock_screen()

    elif intent == "sleep":
        speak("Mo n fi kọmputa sun.")
        sleep_computer()

    elif intent == "screenshot":
        speak("Mo n ya aworan iboju.")
        path = take_screenshot()
        speak("Aworan iboju ti wa ni fipamo.")

    # ── SYSTEM INFO ──────────────────────────────────────────
    elif intent == "battery":
        info = get_battery()
        speak(info)

    elif intent == "storage":
        info = get_storage()
        speak(info)

    elif intent == "ram":
        info = get_ram()
        speak(info)

    elif intent == "cpu":
        info = get_cpu()
        speak(info)

    # ── SEARCH ───────────────────────────────────────────────
    elif intent == "search":
        speak("Kini mo yẹ ki n wa?")
        query = input("Search Query: ")
        search_google(query)

    elif intent == "search_youtube":
        speak("Kini mo yẹ ki n wa lori YouTube?")
        query = input("YouTube Search: ")
        search_youtube(query)

    elif intent == "weather":
        speak("Mo n wo ojo ojo.")
        check_weather()

    # ── BROWSER CONTROLS ─────────────────────────────────────
    elif intent == "new_tab":
        speak("Mo n ṣi tab titun.")
        open_new_tab()

    elif intent == "close_tab":
        speak("Mo n pa tab yi.")
        close_current_tab()

    elif intent == "go_back":
        speak("Mo n pada sehin.")
        go_back()

    elif intent == "refresh":
        speak("Mo n tun gba oju opo.")
        refresh_page()

    # ── MEDIA CONTROLS ───────────────────────────────────────
    elif intent == "pause_music":
        speak("Mo ti da orin duro.")
        pause_music()

    elif intent == "next_song":
        speak("Mo n lo si orin to n bo.")
        next_song()

    elif intent == "prev_song":
        speak("Mo n pada si orin ti o koja.")
        prev_song()

    # ── SMART HOME ───────────────────────────────────────────
    elif intent == "smart_home":
        speak("Iṣẹ smart home ko ti wa ni ipo siṣẹ.")

    # ── EXIT ─────────────────────────────────────────────────
    elif intent == "exit":
        speak("O dabo. Ki ojo re o dara.")
        exit()

    # ── FALLBACK ─────────────────────────────────────────────
    else:
        speak("Emi ko ye ibeere naa. E jowo tun so.")
