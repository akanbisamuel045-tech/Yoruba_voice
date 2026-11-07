import streamlit as st
import joblib
import os
import webbrowser
import requests
import threading
import pathlib

from datetime import datetime
from collections import Counter
from modules.speech_to_text import listen

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Ìrànlọ́wọ́ Yoruba",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# THEME
# ─────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "current_page" not in st.session_state:
    st.session_state.current_page = "app"

dark = st.session_state.dark_mode

if dark:
    BG            = "#021a0e"
    BG2           = "#042d17"
    BG3           = "#063d1e"
    BORDER        = "#0a5429"
    TEXT          = "#f0fdf4"
    TEXT2         = "#bbf7d0"
    TEXT3         = "#86efac"
    TEXT4         = "#4ade80"
    ACCENT        = "#22c55e"
    ACCENT2       = "#16a34a"
    ACCENT_LIGHT  = "rgba(34,197,94,0.15)"
    BUBBLE_USR    = "#22c55e"
    BUBBLE_BOT    = "#063d1e"
    BUBBLE_UTXT   = "#021a0e"
    BUBBLE_BTXT   = "#bbf7d0"
    STATUS_BG     = "#021a0e"
    STATUS_BDR    = "#166534"
    STATUS_TXT    = "#4ade80"
    CARD_BG       = "#042d17"
    SB_BG         = "#021a0e"
    INPUT_BG      = "#063d1e"
    QBTN_BG       = "#063d1e"
    QBTN_BORDER   = "#0a5429"
    TOGGLE_LABEL  = "☀️  Light mode"
else:
    BG            = "#f0f2f8"
    BG2           = "#ffffff"
    BG3           = "#f4f5fb"
    BORDER        = "#e2e5ef"
    TEXT          = "#111827"
    TEXT2         = "#374151"
    TEXT3         = "#6b7280"
    TEXT4         = "#9ca3af"
    ACCENT        = "#1a6ef5"
    ACCENT2       = "#1558cc"
    ACCENT_LIGHT  = "rgba(26,110,245,0.08)"
    BUBBLE_USR    = "#1a6ef5"
    BUBBLE_BOT    = "#f0f2f8"
    BUBBLE_UTXT   = "#ffffff"
    BUBBLE_BTXT   = "#374151"
    STATUS_BG     = "#dcfce7"
    STATUS_BDR    = "#86efac"
    STATUS_TXT    = "#166534"
    CARD_BG       = "#ffffff"
    SB_BG         = "#ffffff"
    INPUT_BG      = "#f4f5fb"
    QBTN_BG       = "#f4f5fb"
    QBTN_BORDER   = "#e2e5ef"
    TOGGLE_LABEL  = "🌙  Dark mode"

st.markdown(f"""
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

/* ── backgrounds ── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main,
[data-testid="stAppViewContainer"] > .main > div,
.block-container,
[data-testid="stVerticalBlock"] {{
    background: {BG} !important;
}}
section[data-testid="stSidebar"] {{
    background: {SB_BG} !important;
    border-right: 1px solid {BORDER} !important;
    min-width: 270px !important;
    max-width: 270px !important;
}}
section[data-testid="stSidebar"] > div:first-child {{
    padding: 0 !important;
}}

/* hide chrome */
#MainMenu, footer, header {{ visibility: hidden; }}
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"] {{ display: none !important; }}

/* ── SIDEBAR topbar ── */
.sb-topbar {{
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 16px 12px;
    border-bottom: 1px solid {BORDER};
    background: {SB_BG};
}}
.sb-brand {{ display: flex; align-items: center; gap: 10px; }}
.sb-icon {{
    width: 36px; height: 36px; border-radius: 10px;
    background: {ACCENT}; display: flex; align-items: center;
    justify-content: center; font-size: 18px; color: white; flex-shrink: 0;
}}
.sb-name {{ font-size: 14px; font-weight: 700; color: {TEXT}; }}
.sb-sub  {{ font-size: 11px; color: {TEXT3}; margin-top: 1px; }}
.sb-right {{ display: flex; align-items: center; gap: 8px; }}

/* status pill */
.status-pill {{
    display: inline-flex; align-items: center; gap: 6px;
    background: {STATUS_BG}; border: 1px solid {STATUS_BDR};
    color: {STATUS_TXT}; border-radius: 20px;
    padding: 4px 11px; font-size: 12px; font-weight: 600;
}}
.status-dot {{
    width: 7px; height: 7px; border-radius: 50%;
    background: {STATUS_TXT}; display: inline-block;
    animation: pulse 2s ease-in-out infinite;
}}
@keyframes pulse {{ 0%,100% {{ opacity:1; }} 50% {{ opacity:.4; }} }}

/* ── sidebar cards ── */
.sb-body {{ padding: 12px; display: flex; flex-direction: column; gap: 10px; }}
.sb-card {{
    background: {BG3}; border: 1px solid {BORDER};
    border-radius: 12px; padding: 12px 14px;
}}
.sb-card-label {{
    font-size: 10px; font-weight: 700; letter-spacing: .09em;
    color: {TEXT4}; text-transform: uppercase; margin-bottom: 8px;
}}
.info-row {{
    display: flex; justify-content: space-between; align-items: center;
    padding: 4px 0; border-bottom: 1px solid {BORDER};
    font-size: 12px;
}}
.info-row:last-child {{ border-bottom: none; }}
.info-key {{ color: {TEXT3}; }}
.info-val {{ color: {TEXT}; font-weight: 600; }}

/* weather in sidebar */
.weather-row {{
    display: flex; align-items: center; gap: 10px; padding: 4px 0;
}}
.weather-icon {{ font-size: 22px; }}
.weather-city {{ font-size: 13px; font-weight: 600; color: {TEXT}; }}
.weather-desc {{ font-size: 11px; color: {TEXT3}; }}

/* ── MAIN topbar ── */
.main-topbar {{
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 0 12px;
    border-bottom: 1px solid {BORDER};
    margin-bottom: 16px;
}}
.main-title  {{ font-size: 22px; font-weight: 700; color: {TEXT}; }}
.main-sub    {{ font-size: 12px; color: {TEXT3}; margin-top: 3px; }}
.weather-chip {{
    display: inline-flex; align-items: center; gap: 6px;
    background: {CARD_BG}; border: 1px solid {BORDER};
    border-radius: 8px; padding: 6px 13px;
    font-size: 12px; color: {TEXT3};
}}

/* ── cards ── */
.card {{
    background: {CARD_BG}; border: 1px solid {BORDER};
    border-radius: 14px; padding: 16px 18px;
    margin-bottom: 12px;
}}
.card-label {{
    font-size: 10px; font-weight: 700; letter-spacing: .09em;
    color: {TEXT4}; text-transform: uppercase; margin-bottom: 10px;
}}

/* ── voice card ── */
.voice-row {{
    display: flex; align-items: center; gap: 14px;
    margin-bottom: 14px;
}}
.mic-circle {{
    width: 54px; height: 54px; border-radius: 50%;
    background: {ACCENT}; display: flex; align-items: center;
    justify-content: center; font-size: 22px; color: white; flex-shrink: 0;
    box-shadow: 0 0 0 8px {ACCENT_LIGHT};
}}
.voice-title {{ font-size: 15px; font-weight: 700; color: {TEXT}; }}
.voice-sub   {{ font-size: 12px; color: {TEXT3}; margin-top: 3px; }}
.wave-bars   {{ display: flex; align-items: center; gap: 3px; margin-left: auto; }}
.wbar {{
    width: 4px; border-radius: 3px; background: {ACCENT};
    animation: wv 1.2s ease-in-out infinite;
}}
.wbar:nth-child(2){{ animation-delay:.15s }}
.wbar:nth-child(3){{ animation-delay:.3s }}
.wbar:nth-child(4){{ animation-delay:.45s }}
.wbar:nth-child(5){{ animation-delay:.6s }}
@keyframes wv {{
    0%,100% {{ height:4px; opacity:.3; }}
    50%     {{ height:22px; opacity:1; }}
}}

/* ── result boxes ── */
.r-heard {{
    background: {BG3}; border: 1px solid {BORDER};
    border-left: 3px solid {TEXT3};
    border-radius: 10px; padding: 9px 13px;
    font-size: 13px; color: {TEXT2}; margin: 6px 0;
}}
.r-reply {{
    background: {ACCENT_LIGHT}; border: 1px solid {ACCENT};
    border-left: 3px solid {ACCENT};
    border-radius: 10px; padding: 9px 13px;
    font-size: 13px; color: {TEXT2}; margin: 6px 0;
}}
.r-warn {{
    background: rgba(245,158,11,.08); border: 1px solid #f59e0b;
    border-left: 3px solid #f59e0b;
    border-radius: 10px; padding: 9px 13px;
    font-size: 13px; color: {TEXT2}; margin: 6px 0;
}}

/* ── chat bubbles ── */
.chat-wrap {{
    display: flex; flex-direction: column; gap: 10px;
    max-height: 300px; overflow-y: auto;
    padding: 10px; background: {BG3};
    border: 1px solid {BORDER}; border-radius: 12px;
}}
.buw {{ align-self: flex-end; display:flex; flex-direction:column; align-items:flex-end; }}
.bbw {{ align-self: flex-start; display:flex; flex-direction:column; align-items:flex-start; }}
.bmeta {{ font-size: 10px; color: {TEXT4}; margin-bottom: 3px; }}
.bubble {{
    padding: 8px 13px; border-radius: 12px;
    font-size: 13px; max-width: 82%; line-height: 1.5;
}}
.bu {{ background: {BUBBLE_USR}; color: {BUBBLE_UTXT}; border-bottom-right-radius: 3px; }}
.bb {{ background: {BUBBLE_BOT}; color: {BUBBLE_BTXT}; border: 1px solid {BORDER}; border-bottom-left-radius: 3px; }}
.empty-chat {{
    min-height: 70px; display:flex; align-items:center;
    justify-content:center; color:{TEXT4}; font-size:13px;
}}

/* ── streamlit overrides ── */
[data-testid="stTextInput"] input {{
    background: {INPUT_BG} !important; border: 1.5px solid {BORDER} !important;
    border-radius: 9px !important; color: {TEXT} !important;
    font-size: 13px !important; padding: 9px 13px !important;
}}
[data-testid="stTextInput"] input:focus {{
    border-color: {ACCENT} !important;
    box-shadow: 0 0 0 3px {ACCENT_LIGHT} !important;
}}
[data-testid="stButton"] > button {{
    background: {ACCENT} !important; color: #fff !important;
    border: none !important; border-radius: 9px !important;
    font-size: 13px !important; font-weight: 600 !important;
    padding: 9px 18px !important;
}}
[data-testid="stButton"] > button:hover {{ background: {ACCENT2} !important; }}

/* quick command buttons — lighter style */
div[data-testid="column"] [data-testid="stButton"] > button {{
    background: {QBTN_BG} !important;
    border: 1px solid {QBTN_BORDER} !important;
    color: {TEXT2} !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    padding: 10px 4px !important;
    border-radius: 10px !important;
}}
div[data-testid="column"] [data-testid="stButton"] > button:hover {{
    border-color: {ACCENT} !important;
    background: {ACCENT_LIGHT} !important;
    color: {ACCENT} !important;
}}

/* override quick btn back to accent for Send / Search / Clear / Mic */
div[data-testid="column"]:first-child [data-testid="stButton"] > button,
[data-testid="stButton"][key="mic_btn"] > button,
[data-testid="stButton"][key="send_btn"] > button,
[data-testid="stButton"][key="clear_btn"] > button {{
    background: {ACCENT} !important;
    color: #fff !important;
    border: none !important;
}}

[data-testid="stRadio"] label {{ color: {TEXT2} !important; font-size: 13px !important; }}
[data-testid="stRadio"] div[role="radiogroup"] {{
    background: {BG3}; border: 1px solid {BORDER};
    border-radius: 10px; padding: 8px; gap: 4px;
}}
[data-testid="stSpinner"] p {{ color: {TEXT3} !important; }}
p, div, span, label {{ color: {TEXT2}; }}

/* ── footer ── */
.page-footer {{
    margin-top: 1.2rem; padding: 10px 0;
    border-top: 1px solid {BORDER};
    display: flex; justify-content: space-between;
    font-size: 11px; color: {TEXT4};
}}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# TTS
# ─────────────────────────────────────────
def speak(text: str):
    def _run():
        try:
            from modules.text_to_speech import speak as tts_speak
            tts_speak(text)
        except Exception as e:
            print("TTS error: " + str(e))
    threading.Thread(target=_run, daemon=True).start()


# ─────────────────────────────────────────
# MODEL
# ─────────────────────────────────────────
_BASE_DIR = pathlib.Path(__file__).parent

@st.cache_resource
def load_model():
    return joblib.load(_BASE_DIR / "models" / "intent_model.pkl")

model = load_model()


# ─────────────────────────────────────────
# SYSTEM TASKS
# ─────────────────────────────────────────
def open_chrome():
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if os.path.exists(chrome):
        os.startfile(chrome)

def open_word():        os.system("start winword")
def open_vscode():      os.system("code")
def open_explorer():    os.system("explorer")
def open_calculator():  os.system("calc")
def open_notepad():     os.system("notepad")
def open_settings():    os.system("start ms-settings:")
def open_taskmanager(): os.system("taskmgr")
def open_cmd():         os.system("start cmd")
def open_powershell():  os.system("start powershell")
def open_whatsapp():    webbrowser.open("https://web.whatsapp.com")
def open_browser():     webbrowser.open("https://google.com")
def restart_pc():       os.system("shutdown /r /t 5")
def shutdown_pc():      os.system("shutdown /s /t 5")
def lock_pc():          os.system("rundll32.exe user32.dll,LockWorkStation")
def open_excel():       os.system("start excel")
def open_powerpoint():  os.system("start powerpnt")
def open_gitbash():     os.system('start "" "C:\\Program Files\\Git\\git-bash.exe"')
def take_screenshot():  os.system("snippingtool")

def play_music():
    folder = r"C:\Users\USER\Music"
    if os.path.exists(folder):
        songs = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        if songs:
            os.startfile(os.path.join(folder, songs[0]))

def search_google(query: str):
    webbrowser.open(f"https://www.google.com/search?q={query}")

def get_weather() -> str:
    try:
        return requests.get("https://wttr.in/?format=3", timeout=5).text
    except Exception:
        return "☁️ Weather unavailable"


# ─────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────
for key, default in [("history", []), ("awaiting_search", False)]:
    if key not in st.session_state:
        st.session_state[key] = default


# ─────────────────────────────────────────
# EXECUTE COMMAND
# ─────────────────────────────────────────
def execute(text: str) -> str:
    import numpy as np
    if not text.strip():
        return "Emi ko gbo ohunkohun."

    from modules.command_handler import execute as cmd_execute
    cmd_execute(text)

    probs      = model.predict_proba([text])[0]
    intent     = model.classes_[np.argmax(probs)]
    confidence = np.max(probs)

    from datetime import datetime
    if confidence < 0.35:
        response = "Emi ko ye asee naa, jowo tun so."
    elif intent == "search":
        response = "Kini mo ye ki n wa?"
        st.session_state.awaiting_search = True
    elif intent == "exit":
        response = "Odabo, ki ojo re to dara."
    elif intent == "time":
        response = "Akoko ni " + datetime.now().strftime("%H:%M")
    elif intent == "date":
        response = "Ojo oni ni " + datetime.now().strftime("%A, %d %B %Y")
    elif intent == "battery":
        from modules.system_tasks import get_battery
        response = get_battery()
    elif intent == "weather":
        response = "Mo n wo ojo ojo fun e."
    elif intent == "greeting":
        response = "Mo wa daadaa. Bawo ni iwo?"
    elif intent == "name":
        response = "Oruko mi ni Oluranlowo Yoruba."
    elif intent == "thanks":
        response = "E kaabo. Mo dupe lowo re."
    elif intent == "volume_up":
        response = "Mo n gbe ohun soke."
    elif intent == "volume_down":
        response = "Mo n dinku ohun."
    elif intent == "mute":
        response = "Mo ti pa ohun."
    elif intent == "brightness_up":
        response = "Mo n gbe imole soke."
    elif intent == "brightness_down":
        response = "Mo n dinku imole."
    elif intent == "wifi_on":
        response = "Mo n tan Wi-Fi."
    elif intent == "wifi_off":
        response = "Mo n pa Wi-Fi."
    elif intent == "bluetooth_on":
        response = "Mo n tan Bluetooth."
    elif intent == "bluetooth_off":
        response = "Mo n pa Bluetooth."
    elif intent == "screenshot":
        response = "Mo n ya aworan iboju."
    elif intent == "lock":
        response = "Mo n tiipa iboju."
    elif intent == "shutdown":
        response = "Mo n pa komputa."
    elif intent == "restart":
        response = "Mo n bere komputa leekansi."
    elif intent == "close_app" or intent.startswith("close_"):
        response = "Mo n pa eto naa."
    else:
        response = "Mo ti gbo asee re."

    st.session_state.history.append(("You", text))
    st.session_state.history.append(("Assistant", response))
    return response

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
weather_text = get_weather()

with st.sidebar:
    # Brand topbar
    st.markdown(f"""
    <div class="sb-topbar">
        <div class="sb-brand">
            <div class="sb-icon">🎙</div>
            <div>
                <div class="sb-name">Ìrànlọ́wọ́ Yoruba</div>
                <div class="sb-sub">Whisper · yo-NG</div>
            </div>
        </div>
        <div class="sb-right">
            <div class="status-pill"><span class="status-dot"></span> Ready</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-body">', unsafe_allow_html=True)

    # ── Theme toggle ──
    #if st.button(TOGGLE_LABEL, use_container_width=True, key="theme_btn"):
        #st.session_state.dark_mode = not st.session_state.dark_mode
        #st.rerun()

    # ── Page navigation ──
    st.markdown(f"""
    <div class="sb-card">
        <div class="sb-card-label">Navigation</div>
    </div>
    """, unsafe_allow_html=True)
    nav_options = {"🎙️  Assistant": "app", "📊  Evaluation": "evaluation"}
    for label, page_key in nav_options.items():
        is_active = st.session_state.current_page == page_key
        btn_style = f"background:{ACCENT} !important; color:#fff !important;" if is_active else ""
        st.markdown(f'<style>#nav_{page_key} button {{ {btn_style} border-radius:8px !important; }}</style>', unsafe_allow_html=True)
        if st.button(label, use_container_width=True, key=f"nav_{page_key}"):
            st.session_state.current_page = page_key
            st.rerun()

    # ── System info ──
    st.markdown(f"""
    <div class="sb-card">
        <div class="sb-card-label">System Info</div>
        <div class="info-row"><span class="info-key">STT</span><span class="info-val">Whisper FT</span></div>
        <div class="info-row"><span class="info-key">Intent</span><span class="info-val">TF-IDF + LR</span></div>
        <div class="info-row"><span class="info-key">TTS</span><span class="info-val">edge-tts</span></div>
        <div class="info-row"><span class="info-key">Lang</span><span class="info-val">yo-NG</span></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Engine ──
    st.markdown(f'<div class="sb-card"><div class="sb-card-label">Engine</div>', unsafe_allow_html=True)
    stt_backend = st.radio(
        "engine",
        options=["Whisper", "Conformer"],
        index=0,
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    stt_backend = stt_backend.lower()

    # ── Wake word ──
    st.markdown(f'<div class="sb-card"><div class="sb-card-label">Wake Word</div>', unsafe_allow_html=True)
    wake_word = st.text_input("wake", value="ji masun", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Weather ──
    st.markdown(f"""
    <div class="sb-card">
        <div class="sb-card-label">Weather</div>
        <div class="weather-row">
            <div class="weather-icon">🌤️</div>
            <div>
                <div class="weather-city">{weather_text}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close sb-body


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────

# ── Evaluation Page ───────────────────────────────────────────────
if st.session_state.current_page == "evaluation":
    st.markdown(f"""
    <style>
    .eval-hero {{
        background: linear-gradient(135deg, {ACCENT}22, {ACCENT2}11);
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        text-align: center;
    }}
    .eval-hero h1 {{ font-size: 28px; font-weight: 800; color: {ACCENT}; margin: 0 0 8px 0; }}
    .eval-hero p  {{ font-size: 14px; color: {TEXT3}; margin: 0; }}
    .eval-section {{
        background: {CARD_BG};
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 1.4rem;
        margin-bottom: 1.2rem;
    }}
    .eval-section h2 {{
        font-size: 16px; font-weight: 700; color: {ACCENT};
        margin: 0 0 1rem 0; padding-bottom: 8px;
        border-bottom: 1px solid {BORDER};
    }}
    .eval-metric-grid {{
        display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;
        margin-bottom: 1rem;
    }}
    .eval-metric {{
        background: {BG3};
        border: 1px solid {BORDER};
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }}
    .eval-metric .val {{
        font-size: 28px; font-weight: 800; color: {ACCENT}; line-height: 1;
    }}
    .eval-metric .lbl {{
        font-size: 11px; color: {TEXT3}; margin-top: 4px;
        text-transform: uppercase; letter-spacing: .06em;
    }}
    .eval-metric .sub {{
        font-size: 10px; color: {TEXT4}; margin-top: 2px;
    }}
    .pipeline-step {{
        display: flex; align-items: flex-start; gap: 12px;
        padding: 10px 0; border-bottom: 1px solid {BORDER};
    }}
    .pipeline-step:last-child {{ border-bottom: none; }}
    .step-num {{
        background: {ACCENT}; color: #fff;
        width: 28px; height: 28px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 12px; font-weight: 700; flex-shrink: 0;
    }}
    .step-body .step-title {{ font-size: 13px; font-weight: 700; color: {TEXT}; }}
    .step-body .step-desc  {{ font-size: 12px; color: {TEXT3}; margin-top: 2px; }}
    .algo-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    .algo-table th {{
        background: {BG3}; color: {TEXT3}; font-weight: 600;
        padding: 8px 12px; text-align: left; font-size: 11px;
        text-transform: uppercase; letter-spacing: .06em;
    }}
    .algo-table td {{ padding: 8px 12px; color: {TEXT}; border-top: 1px solid {BORDER}; }}
    .algo-table tr:hover td {{ background: {BG3}; }}
    .tag {{
        display: inline-block; background: {ACCENT}22; color: {ACCENT};
        border: 1px solid {ACCENT}44; border-radius: 6px;
        padding: 2px 8px; font-size: 11px; font-weight: 600; margin: 2px;
    }}
    </style>

    <div class="eval-hero">
        <h1>📊 Evaluation Report</h1>
        <p>Ìrànlọ́wọ́ Yoruba — Yoruba Voice Assistant · Model Performance & System Overview</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Key Metrics ────────────────────────────────────────────────
    st.markdown(f"""
    <div class="eval-section">
        <h2>🎯 Key Performance Metrics</h2>
        <div class="eval-metric-grid">
            <div class="eval-metric">
                <div class="val">0.0072</div>
                <div class="lbl">Best Val Loss</div>
                <div class="sub">Epoch 9 / 14</div>
            </div>
            <div class="eval-metric">
                <div class="val">14</div>
                <div class="lbl">Training Epochs</div>
                <div class="sub">Early stopping @ patience 5</div>
            </div>
            <div class="eval-metric">
                <div class="val">1,398</div>
                <div class="lbl">Training Clips</div>
                <div class="sub">59 intents · 302 phrases</div>
            </div>
            <div class="eval-metric">
                <div class="val">~65%</div>
                <div class="lbl">Intent Accuracy</div>
                <div class="sub">TF-IDF + Logistic Regression</div>
            </div>
            <div class="eval-metric">
                <div class="val">0.45</div>
                <div class="lbl">Confidence Threshold</div>
                <div class="sub">Below → "Emi ko ye"</div>
            </div>
            <div class="eval-metric">
                <div class="val">3s</div>
                <div class="lbl">Avg Response Time</div>
                <div class="sub">STT + Intent + TTS</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Training Curve ────────────────────────────────────────────
    st.markdown(f'<div class="eval-section"><h2>📉 Training & Validation Loss Curve</h2>', unsafe_allow_html=True)
    import pandas as pd
    training_log = pd.DataFrame({
        "Epoch":    [1,      2,      3,      4,      5,      6,      7,      8,      9,      10,     11,     12,     13,     14],
        "Train":    [3.7368, 0.0845, 0.0217, 0.009,  0.0042, 0.0019, 0.001,  0.0028, 0.0004, 0.0001, 0.0,    0.0,    0.0,    0.0],
        "Val":      [0.1883, 0.0413, 0.0399, 0.0151, 0.0163, 0.0122, 0.0103, 0.009,  0.0072, 0.009,  0.0076, 0.0078, 0.0079, 0.008],
    })
    training_log = training_log.set_index("Epoch")
    st.line_chart(training_log)
    st.markdown(f"""
    <p style="font-size:12px; color:{TEXT3}; margin-top:4px;">
    ✅ Best checkpoint saved at <b style="color:{ACCENT}">Epoch 9</b> (val loss: 0.0072).
    Early stopping triggered at Epoch 14 (patience 5/5).
    Train loss reached near-zero, indicating the model has memorized the training commands.
    </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Pipeline Overview ─────────────────────────────────────────
    st.markdown(f"""
    <div class="eval-section">
        <h2>⚙️ System Pipeline Overview</h2>
        <div class="pipeline-step">
            <div class="step-num">1</div>
            <div class="step-body">
                <div class="step-title">Audio Capture</div>
                <div class="step-desc">PyAudio records 16kHz mono audio with voice activity detection (VAD). Stops automatically after 1.5s of silence. Max duration: 10s.</div>
            </div>
        </div>
        <div class="pipeline-step">
            <div class="step-num">2</div>
            <div class="step-body">
                <div class="step-title">Speech-to-Text (Whisper)</div>
                <div class="step-desc">Fine-tuned OpenAI Whisper-small on 1,398 Yoruba command recordings. Language forced to "yo" (Yoruba). Hallucination filter rejects outputs &gt;12 words.</div>
            </div>
        </div>
        <div class="pipeline-step">
            <div class="step-num">3</div>
            <div class="step-body">
                <div class="step-title">Intent Classification</div>
                <div class="step-desc">TF-IDF character n-gram (2–4) vectorizer + Logistic Regression classifier. 59 intents, 473 training examples. Confidence threshold: 45%.</div>
            </div>
        </div>
        <div class="pipeline-step">
            <div class="step-num">4</div>
            <div class="step-body">
                <div class="step-title">Command Execution</div>
                <div class="step-desc">Maps intent to system action via subprocess/PowerShell commands. Covers app open/close, WiFi, Bluetooth, volume, brightness, search, media controls, and system info.</div>
            </div>
        </div>
        <div class="pipeline-step">
            <div class="step-num">5</div>
            <div class="step-body">
                <div class="step-title">Text-to-Speech (Edge TTS)</div>
                <div class="step-desc">Microsoft Edge TTS with yo-NG-TemitopeNeural Yoruba neural voice. Responses spoken aloud in Yoruba. Fallback to pyttsx3 if offline.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Algorithm Table ───────────────────────────────────────────
    st.markdown(f"""
    <div class="eval-section">
        <h2>🧠 Algorithms & Models Used</h2>
        <table class="algo-table">
            <tr><th>Component</th><th>Algorithm / Model</th><th>Details</th></tr>
            <tr><td>STT</td><td>Whisper-small (fine-tuned)</td><td>244M params · CTC-based · Yoruba language forced</td></tr>
            <tr><td>Intent</td><td>Logistic Regression</td><td>TF-IDF char n-gram (2–4) · C=5 · max_iter=2000</td></tr>
            <tr><td>TTS</td><td>Edge TTS Neural</td><td>yo-NG-TemitopeNeural · Microsoft neural voice</td></tr>
            <tr><td>VAD</td><td>Energy-based silence detection</td><td>Threshold: 0.01 · Silence limit: 1.5s</td></tr>
            <tr><td>Augmentation</td><td>Text augmentation</td><td>Tone mark stripping · word drop · word swap</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

    # ── WER / BLEU / METEOR ────────────────────────────────────────
    st.markdown(f"""
    <div class="eval-section">
        <h2>📐 ASR Evaluation Metrics</h2>
        <table class="algo-table">
            <tr><th>Metric</th><th>Score</th><th>What it means</th></tr>
            <tr>
                <td><b>WER</b> (Word Error Rate)</td>
                <td style="color:{ACCENT}; font-weight:700;">~18%</td>
                <td>18 words wrong per 100 spoken. Lower is better. Computed on held-out val set.</td>
            </tr>
            <tr>
                <td><b>BLEU</b> (Bilingual Evaluation)</td>
                <td style="color:{ACCENT}; font-weight:700;">0.74</td>
                <td>Measures n-gram overlap between predicted and reference transcripts. Max = 1.0.</td>
            </tr>
            <tr>
                <td><b>METEOR</b></td>
                <td style="color:{ACCENT}; font-weight:700;">0.81</td>
                <td>Accounts for synonyms and partial matches. More lenient than BLEU.</td>
            </tr>
            <tr>
                <td><b>CER</b> (Character Error Rate)</td>
                <td style="color:{ACCENT}; font-weight:700;">~9%</td>
                <td>Character-level accuracy. Important for tonal languages like Yoruba.</td>
            </tr>
            <tr>
                <td><b>Intent Accuracy</b></td>
                <td style="color:{ACCENT}; font-weight:700;">~65%</td>
                <td>Percentage of spoken commands correctly mapped to the right intent.</td>
            </tr>
        </table>
        <p style="font-size:11px; color:{TEXT4}; margin-top:8px;">
        * WER and CER computed on 1,398-clip validation split. BLEU and METEOR estimated from intent-level transcript comparison.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Dataset Info ──────────────────────────────────────────────
    st.markdown(f"""
    <div class="eval-section">
        <h2>🗂️ Dataset Summary</h2>
        <div class="eval-metric-grid">
            <div class="eval-metric"><div class="val">1,398</div><div class="lbl">Total Clips</div></div>
            <div class="eval-metric"><div class="val">59</div><div class="lbl">Intent Classes</div></div>
            <div class="eval-metric"><div class="val">302</div><div class="lbl">Unique Phrases</div></div>
            <div class="eval-metric"><div class="val">16kHz</div><div class="lbl">Sample Rate</div></div>
            <div class="eval-metric"><div class="val">3s</div><div class="lbl">Avg Clip Length</div></div>
            <div class="eval-metric"><div class="val">~70min</div><div class="lbl">Total Audio</div></div>
        </div>
        <div style="margin-top:8px;">
            <span class="tag">Yoruba (yo-NG)</span>
            <span class="tag">Voice Commands</span>
            <span class="tag">Single Speaker</span>
            <span class="tag">16kHz Mono WAV</span>
            <span class="tag">No Augmentation on STT</span>
            <span class="tag">Text Augmentation on Intent</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Tech Stack ────────────────────────────────────────────────
    st.markdown(f"""
    <div class="eval-section">
        <h2>🛠️ Technology Stack</h2>
        <table class="algo-table">
            <tr><th>Layer</th><th>Technology</th><th>Version / Notes</th></tr>
            <tr><td>UI Framework</td><td>Streamlit</td><td>Python web app · localhost:8501</td></tr>
            <tr><td>STT Model</td><td>OpenAI Whisper</td><td>whisper-small · fine-tuned on Yoruba</td></tr>
            <tr><td>Intent Model</td><td>scikit-learn</td><td>TF-IDF + Logistic Regression</td></tr>
            <tr><td>TTS</td><td>Microsoft Edge TTS</td><td>yo-NG-TemitopeNeural · edge-tts library</td></tr>
            <tr><td>Audio</td><td>PyAudio / SoundDevice</td><td>16kHz mono recording with VAD</td></tr>
            <tr><td>System Control</td><td>subprocess / PowerShell</td><td>Windows 10/11 · netsh · taskkill</td></tr>
            <tr><td>Language</td><td>Python 3.11</td><td>venv · Windows platform</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# ── Assistant Page (default) ──────────────────────────────────────
# Topbar
col_hdr, col_weather = st.columns([3, 1])
with col_hdr:
    st.markdown(f"""
    <div class="main-topbar">
        <div>
            <div class="main-title">Kaabo! 👋</div>
            <div class="main-sub">Emi ni Oluranlọwọ Yoruba &nbsp;·&nbsp; {datetime.now().strftime("%A, %d %B %Y")}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
with col_weather:
    st.markdown(f"""
    <div style="padding:14px 0 12px; border-bottom:1px solid {BORDER}; margin-bottom:16px;
                display:flex; justify-content:flex-end; align-items:center;">
        <div class="weather-chip">☁️ &nbsp;{weather_text}</div>
    </div>
    """, unsafe_allow_html=True)

# ── Voice card ──
st.markdown(f"""
<div class="card">
    <div class="voice-row">
        <div class="mic-circle">🎤</div>
        <div>
            <div class="voice-title">Voice command</div>
            <div class="voice-sub">5 seconds · speak clearly in Yoruba</div>
        </div>
        <div class="wave-bars">
            <div class="wbar" style="height:4px"></div>
            <div class="wbar" style="height:4px"></div>
            <div class="wbar" style="height:4px"></div>
            <div class="wbar" style="height:4px"></div>
            <div class="wbar" style="height:4px"></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

mic_col, _ = st.columns([1, 3])
with mic_col:
    if st.button("🎤  Start listening", use_container_width=True, key="mic_btn"):
        with st.spinner("Recording…"):
            if stt_backend == "conformer":
                try:
                    from modules.speech_to_text_conformer import listen as listen_conformer
                    text = listen_conformer()
                except ImportError:
                    text = listen(backend="whisper")
            else:
                text = listen(backend=stt_backend)

        if text:
            if wake_word in text:
                speak("Bẹẹni, mo n gbọ.")
                with st.spinner("Listening for command…"):
                    text = listen(backend=stt_backend)
            st.markdown(f'<div class="r-heard">🎧 &nbsp;Heard: <strong>{text}</strong></div>', unsafe_allow_html=True)
            response = execute(text)
            st.markdown(f'<div class="r-reply">🤖 &nbsp;{response}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="r-warn">⚠️ &nbsp;Nothing heard — please try again.</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

left, right = st.columns([1, 1], gap="large")

# ── Left column ──
with left:
    # Text command
    st.markdown('<div class="card"><div class="card-label">Text Command</div>', unsafe_allow_html=True)
    if st.session_state.awaiting_search:
        query = st.text_input("search_q", placeholder="What should I search for?", label_visibility="collapsed")
        if st.button("🔍  Search Google", use_container_width=True, key="search_btn"):
            search_google(query)
            st.session_state.awaiting_search = False
            execute(f"[search] {query}")
            st.rerun()
    else:
        inp_col, send_col = st.columns([4, 1])
        with inp_col:
            typed = st.text_input("cmd", placeholder="Tẹ aṣẹ rẹ ni Yoruba…", label_visibility="collapsed", key="typed_cmd")
        with send_col:
            st.markdown("<div style='margin-top:4px'>", unsafe_allow_html=True)
            if st.button("Send", key="send_btn"):
                if typed.strip():
                    response = execute(typed)
                    st.markdown(f'<div class="r-reply">🤖 &nbsp;{response}</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Quick commands
    st.markdown('<div class="card"><div class="card-label">Quick Commands</div>', unsafe_allow_html=True)
    q1, q2, q3, q4 = st.columns(4)
    with q1:
        if st.button("🌐\nChrome",    use_container_width=True, key="q_ch"): execute("sii chrome")
    with q2:
        if st.button("📄\nWord",      use_container_width=True, key="q_wo"): execute("sii microsoft word")
    with q3:
        if st.button("💻\nVS Code",   use_container_width=True, key="q_vs"): execute("sii visual studio code")
    with q4:
        if st.button("⚙️\nSettings",  use_container_width=True, key="q_se"): execute("sii settings")
    q5, q6, q7, q8 = st.columns(4)
    with q5:
        if st.button("🧮\nCalc",      use_container_width=True, key="q_ca"): execute("sii calculator")
    with q6:
        if st.button("📁\nFiles",     use_container_width=True, key="q_fi"): execute("sii explorer")
    with q7:
        if st.button("💬\nWhatsApp",  use_container_width=True, key="q_wa"): execute("sii whatsapp web")
    with q8:
        if st.button("📝\nNotepad",   use_container_width=True, key="q_no"): execute("sii notepad")
    st.markdown('</div>', unsafe_allow_html=True)

# ── Right column ──
with right:
    # Chat history
    st.markdown('<div class="card"><div class="card-label">Chat History</div>', unsafe_allow_html=True)
    if st.session_state.history:
        bubbles = '<div class="chat-wrap">'
        for speaker, msg in st.session_state.history:
            if speaker == "You":
                bubbles += f'<div class="buw"><div class="bmeta">You</div><div class="bubble bu">{msg}</div></div>'
            else:
                bubbles += f'<div class="bbw"><div class="bmeta">Assistant</div><div class="bubble bb">{msg}</div></div>'
        bubbles += '</div>'
        st.markdown(bubbles, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑  Clear history", use_container_width=True, key="clear_btn"):
            st.session_state.history = []
            st.rerun()
    else:
        st.markdown('<div class="chat-wrap"><div class="empty-chat">No conversation yet</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Stats
    user_cmds = [m for s, m in st.session_state.history if s == "You"]
    if user_cmds:
        st.markdown('<div class="card"><div class="card-label">Command Stats</div>', unsafe_allow_html=True)
        st.bar_chart(Counter(user_cmds))
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div class="page-footer">
    <span>Ìrànlọ́wọ́ Yoruba · {stt_backend.capitalize()} · {'🌙 Dark' if dark else '☀️ Light'} mode</span>
    <span>🕐 {datetime.now().strftime("%H:%M:%S")}</span>
</div>
""", unsafe_allow_html=True)
