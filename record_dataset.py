"""
Yoruba Voice Assistant — Dataset Recording Tool (Stage 1)
=========================================================
Run in your VS Code terminal:
    py -3.11 record_dataset.py

- Walks you through every command phrase one by one
- Press Enter to record, [s] to skip, [q] to quit anytime
- Auto-saves into dataset/recordings/<intent>/ folder
- Resume anytime — shows existing clip count per intent
"""

import os
import wave
import time
import pyaudio

# ── Recording settings ────────────────────────────────────────────
SAMPLE_RATE  = 16000
CHANNELS     = 1
CHUNK        = 1024
FORMAT       = pyaudio.paInt16
RECORD_SECS  = 3        # seconds per clip
REPS         = 5        # recordings per phrase
OUTPUT_DIR   = "dataset/recordings"
# ─────────────────────────────────────────────────────────────────

COMMANDS = {

    # ── STAGE 1: Identity & Conversation ─────────────────────────
    "greeting": [
        "kaabo",
        "bawo ni",
        "e kaaro",
        "e kaasan",
        "e kale",
        "nle o",
        "pele o",
        "se alaafia ni",
        "bawo lo se wa",
        "hello",
    ],
    "name": [
        "ki ni oruko re",
        "ta ni o",
        "oruko re ni kini",
        "se robot ni e",
        "tani oluranlowo",
        "ki ni e npe e",
    ],
    "self_intro": [
        "mo je iranlowo re",
        "oruko mi ni iranlo wo yoruba",
        "mo wa nibi lati ran e lowo",
        "emi ni oluranlowo yoruba re",
        "bawo ni mo se le ran e lowo",
    ],
    "what_can_you_do": [
        "kini o le se",
        "kini iṣẹ re",
        "ise wo ni o le se",
        "ran mi lowo pelu kini",
        "se o le ran mi lowo",
    ],
    "thanks": [
        "e ṣeun",
        "o seun",
        "thank you",
        "o dara",
        "daadaa",
        "mo dupẹ",
    ],
    "apology": [
        "e pele",
        "e ma binu",
        "sorry",
        "e jẹ ki a tun gbiyanju",
        "e tun so",
    ],
    "exit": [
        "jade",
        "odabo",
        "bye",
        "fi mi sile",
        "pari",
        "da duro",
    ],
    "confirm": [
        "beeni",
        "yes",
        "mo gba",
        "se e",
        "oya se",
    ],
    "cancel": [
        "rara",
        "no",
        "ma se",
        "fi sile",
        "da duro",
    ],

    # ── STAGE 2: Time & Date ──────────────────────────────────────
    "time": [
        "kini ago",
        "ago melo ni",
        "so akoko fun mi",
        "ki ni akoko bayi",
        "what time is it",
    ],
    "date": [
        "kini ojo oni",
        "ojo wo ni oni",
        "so ojo oni",
        "ki ni date oni",
        "what day is today",
    ],
    "weather": [
        "kini ojo loni",
        "bawo ni ojo ojo",
        "se ojo yoo ro",
        "iwo otutu",
        "what is the weather",
    ],

    # ── STAGE 3: Open Apps ────────────────────────────────────────
    "chrome": [
        "sii chrome",
        "si chrome",
        "mo fe chrome",
        "gbe chrome soke",
        "open chrome",
    ],
    "whatsapp": [
        "sii whatsapp",
        "si whatsapp",
        "mo fe whatsapp",
        "gbe whatsapp soke",
        "open whatsapp",
    ],
    "word": [
        "sii word",
        "si word",
        "mo fe word",
        "sii microsoft word",
        "open word",
    ],
    "excel": [
        "sii excel",
        "si excel",
        "mo fe excel",
        "sii microsoft excel",
        "open excel",
    ],
    "powerpoint": [
        "sii powerpoint",
        "si powerpoint",
        "mo fe powerpoint",
        "sii slides",
        "open powerpoint",
    ],
    "notepad": [
        "sii notepad",
        "si notepad",
        "mo fe notepad",
        "tan notepad",
        "open notepad",
    ],
    "calculator": [
        "sii isiro",
        "si isiro",
        "mo fe isiro",
        "tan isiro",
        "open calculator",
    ],
    "vscode": [
        "sii vscode",
        "si vscode",
        "mo fe vscode",
        "tan vscode",
        "open vscode",
    ],
    "settings": [
        "sii eto",
        "si eto",
        "mo fe eto",
        "tan settings",
        "open settings",
    ],
    "explorer": [
        "sii faili",
        "si faili",
        "mo fe faili",
        "gbe explorer soke",
        "open file explorer",
    ],
    "store": [
        "sii microsoft store",
        "si store",
        "mo fe store",
        "open store",
        "sii store",
    ],
    "taskmanager": [
        "sii task manager",
        "tan task manager",
        "mo fe task manager",
        "open task manager",
        "si task manager",
    ],
    "camera": [
        "sii kamera",
        "si kamera",
        "mo fe kamera",
        "tan kamera",
        "open camera",
    ],

    # ── STAGE 4: Close Apps ───────────────────────────────────────
    "close_chrome": [
        "pa chrome",
        "da chrome duro",
        "close chrome",
        "fi chrome sile",
        "pa google chrome",
    ],
    "close_whatsapp": [
        "pa whatsapp",
        "da whatsapp duro",
        "close whatsapp",
        "fi whatsapp sile",
        "jade kuro ninu whatsapp",
    ],
    "close_word": [
        "pa word",
        "da word duro",
        "close word",
        "fi word sile",
        "pa microsoft word",
    ],
    "close_excel": [
        "pa excel",
        "da excel duro",
        "close excel",
        "fi excel sile",
        "pa microsoft excel",
    ],
    "close_notepad": [
        "pa notepad",
        "da notepad duro",
        "close notepad",
        "fi notepad sile",
        "jade kuro ninu notepad",
    ],
    "close_app": [
        "pa app yii",
        "da app duro",
        "close this app",
        "jade kuro ninu app",
        "pa ohun ti o ṣii",
    ],

    # ── STAGE 5: System Controls ──────────────────────────────────
    "wifi_on": [
        "tan wifi",
        "mu wifi soke",
        "fi wifi sii",
        "turn on wifi",
        "enable wifi",
    ],
    "wifi_off": [
        "pa wifi",
        "da wifi duro",
        "pa wifi run",
        "turn off wifi",
        "disable wifi",
    ],
    "bluetooth_on": [
        "tan bluetooth",
        "mu bluetooth soke",
        "fi bluetooth sii",
        "turn on bluetooth",
        "enable bluetooth",
    ],
    "bluetooth_off": [
        "pa bluetooth",
        "da bluetooth duro",
        "turn off bluetooth",
        "disable bluetooth",
        "pa bluetooth run",
    ],
    "volume_up": [
        "gbe volume soke",
        "gbe ohun soke",
        "mu ohun ga",
        "soke",
        "louder",
    ],
    "volume_down": [
        "gbe volume wale",
        "gbe ohun wale",
        "dinku ohun",
        "wale",
        "quieter",
    ],
    "mute": [
        "pa ohun",
        "dake",
        "mu ohun dake",
        "mute",
        "silence",
    ],
    "brightness_up": [
        "gbe imole soke",
        "mu imole ga",
        "increase brightness",
        "imole soke",
        "brighter",
    ],
    "brightness_down": [
        "gbe imole wale",
        "dinku imole",
        "decrease brightness",
        "imole wale",
        "dimmer",
    ],
    "screenshot": [
        "ya foto iboju",
        "ya screenshot",
        "se screenshot",
        "take screenshot",
        "capture screen",
    ],
    "lock": [
        "tiipa iboju",
        "tiipa kọmputa",
        "lock screen",
        "pa iboju",
        "lock computer",
    ],
    "sleep": [
        "sun",
        "pa iboju run",
        "se sleep",
        "hibernate",
        "sleep computer",
    ],
    "shutdown": [
        "pa kọmputa",
        "pa ẹrọ",
        "turn off computer",
        "shutdown",
        "power off",
    ],
    "restart": [
        "bẹrẹ kọmputa leẹkansi",
        "restart",
        "reboot",
        "start again",
        "bẹrẹ leẹkansi",
    ],

    # ── STAGE 6: System Info ──────────────────────────────────────
    "battery": [
        "bawo ni batiri mi se wa",
        "kini ipele batiri mi",
        "battery level",
        "check battery",
        "batiri melo ni mo ku",
    ],
    "storage": [
        "bawo ni ipamọ mi se wa",
        "kini aaye ti o ku ninu kọmputa",
        "check storage",
        "how much storage",
        "ipamọ melo ni o ku",
    ],
    "ram": [
        "bawo ni memory mi se wa",
        "kini ipele ram mi",
        "check ram",
        "how much ram",
        "ram melo ni mo lo",
    ],
    "cpu": [
        "bawo ni processor mi se wa",
        "kini ipele cpu mi",
        "check cpu",
        "cpu usage",
        "processor melo ni mo lo",
    ],

    # ── STAGE 7: Search & Browser ─────────────────────────────────
    "search": [
        "wa fun mi",
        "search for",
        "wa lori google",
        "google it",
        "wa lori intanẹẹti",
    ],
    "search_youtube": [
        "wa lori youtube",
        "search on youtube",
        "youtube",
        "wa fideo lori youtube",
        "ṣe wiwa lori youtube",
    ],
    "new_tab": [
        "ṣii taabu titun",
        "open new tab",
        "new tab",
        "taabu titun",
        "ṣii tab titun",
    ],
    "close_tab": [
        "pa taabu yii",
        "close this tab",
        "close tab",
        "pa tab yii",
        "da taabu duro",
    ],
    "go_back": [
        "pada sẹhin",
        "go back",
        "back",
        "pada",
        "lo sẹhin",
    ],
    "refresh": [
        "tun gbe",
        "refresh",
        "reload",
        "tun load",
        "tun ṣe",
    ],

    # ── STAGE 8: Media Controls ───────────────────────────────────
    "music": [
        "tan orin",
        "mu orin wa",
        "play music",
        "sii spotify",
        "se orin",
    ],
    "pause_music": [
        "da orin duro",
        "pause music",
        "da orin duro fun igba diẹ",
        "pause",
        "duro",
    ],
    "next_song": [
        "orin to tẹle",
        "next song",
        "skip song",
        "gbe orin to tẹle",
        "next",
    ],
    "prev_song": [
        "orin ti o koja",
        "previous song",
        "go back song",
        "orin sẹhin",
        "previous",
    ],
}

# ─────────────────────────────────────────────────────────────────


def record_clip(filepath):
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=FORMAT, channels=CHANNELS,
        rate=SAMPLE_RATE, input=True,
        frames_per_buffer=CHUNK,
    )
    frames = []
    for _ in range(int(SAMPLE_RATE / CHUNK * RECORD_SECS)):
        frames.append(stream.read(CHUNK, exception_on_overflow=False))
    stream.stop_stream()
    stream.close()
    pa.terminate()

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    pa2 = pyaudio.PyAudio()
    with wave.open(filepath, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pa2.get_sample_size(FORMAT))
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b''.join(frames))
    pa2.terminate()


def count_existing(intent):
    folder = os.path.join(OUTPUT_DIR, intent)
    if not os.path.exists(folder):
        return 0
    return len([f for f in os.listdir(folder) if f.endswith('.wav')])


def next_filepath(intent, phrase, rep):
    clean = phrase.lower().replace(' ', '_')
    clean = ''.join(c for c in clean if c.isalnum() or c in '_ọẹṣị')
    existing = count_existing(intent)
    folder = os.path.join(OUTPUT_DIR, intent)
    return os.path.join(folder, f"{clean}_{existing+rep+1:03d}.wav")


def print_summary():
    print("\n" + "="*60)
    print("  RECORDING SUMMARY")
    print("="*60)
    total = 0
    for intent in COMMANDS:
        count = count_existing(intent)
        total += count
        bar = "█" * (count // 5)
        print(f"  {intent:<25} {count:>3} clips  {bar}")
    print(f"\n  TOTAL: {total} clips recorded")
    print("="*60)


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*60)
    print("  YORUBA VOICE ASSISTANT — DATASET RECORDER")
    print("="*60)

    total_intents = len(COMMANDS)
    total_phrases = sum(len(p) for p in COMMANDS.values())
    total_clips   = total_phrases * REPS

    print(f"\n  {total_intents} intents | {total_phrases} phrases | ~{total_clips} total clips")
    print(f"  Output: {OUTPUT_DIR}")
    print(f"  {RECORD_SECS}s per clip | {REPS} reps per phrase\n")
    print("  Controls:")
    print("  [Enter]   = record")
    print("  [s]       = skip this phrase")
    print("  [i]       = skip this entire intent")
    print("  [q]       = quit and show summary")
    print("  [summary] = show progress so far\n")

    input("  Press Enter to start...")

    intent_num = 0
    for intent, phrases in COMMANDS.items():
        intent_num += 1
        existing = count_existing(intent)

        print(f"\n{'='*60}")
        print(f"  [{intent_num}/{total_intents}] INTENT: {intent.upper()}")
        print(f"  Already recorded: {existing} clips")
        print(f"{'='*60}")

        skip_intent = False
        for phrase_idx, phrase in enumerate(phrases):
            if skip_intent:
                break

            print(f"\n  📢 Say this in Yoruba:")
            print(f"  \"{phrase}\"")
            print(f"  (phrase {phrase_idx+1} of {len(phrases)})")

            for rep in range(REPS):
                filepath = next_filepath(intent, phrase, rep)
                prompt = input(f"\n  Rep {rep+1}/{REPS} → [Enter]=record [s]=skip [i]=skip intent [q]=quit: ").strip().lower()

                if prompt == 'q':
                    print_summary()
                    return
                elif prompt == 'i':
                    print(f"  Skipping entire intent: {intent}")
                    skip_intent = True
                    break
                elif prompt == 's':
                    print("  Phrase skipped.")
                    break
                elif prompt == 'summary':
                    print_summary()
                    continue

                print(f"\n  🔴 Get ready...")
                time.sleep(0.8)
                print(f"  🎤 Recording now! Say: \"{phrase}\"")
                record_clip(filepath)
                print(f"  ✅ Saved → {os.path.basename(filepath)}")

        if not skip_intent:
            print(f"\n  ✅ '{intent}' complete! ({count_existing(intent)} clips)")

        nxt = input("\n  [Enter]=next intent  [q]=quit: ").strip().lower()
        if nxt == 'q':
            break

    print_summary()


if __name__ == "__main__":
    main()
