# -*- coding: utf-8 -*-
import os, csv, wave, pyaudio, time, io

CSV_PATH    = "dataset/yoruba_commands.csv"
AUDIO_DIR   = "dataset/audio"
REPEATS     = 3
RECORD_SECS = 3
SAMPLE_RATE = 16000
CHANNELS    = 1
CHUNK       = 1024
FORMAT      = pyaudio.paInt16

os.makedirs(AUDIO_DIR, exist_ok=True)

def text_to_slug(text):
    return text.lower().strip().replace(" ", "_").replace("/", "-")

def record_clip(pa, duration, label):
    stream = pa.open(format=FORMAT, channels=CHANNELS, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK)
    print("  [REC] Recording '" + label + "'... (speak now)")
    frames = [stream.read(CHUNK, exception_on_overflow=False) for _ in range(int(SAMPLE_RATE / CHUNK * duration))]
    stream.stop_stream()
    stream.close()
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pa.get_sample_size(FORMAT))
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b"".join(frames))
    return buf.getvalue()

def get_next_index(slug):
    existing = [f for f in os.listdir(AUDIO_DIR) if f.startswith(slug + "_") and f.endswith(".wav")]
    if not existing:
        return 1
    indices = []
    for f in existing:
        try:
            indices.append(int(f.replace(slug + "_", "").replace(".wav", "")))
        except:
            pass
    return max(indices) + 1 if indices else 1

def load_commands():
    cmds = []
    with open(CSV_PATH, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            t = row["text"].strip()
            if t and t not in cmds:
                cmds.append(t)
    return cmds

commands = load_commands()
print("Loaded " + str(len(commands)) + " unique commands")
print("Recording each " + str(REPEATS) + " times (" + str(RECORD_SECS) + "s each)")
print("Press ENTER before each recording. Ctrl+C to stop.\n")

pa = pyaudio.PyAudio()
total = 0
try:
    for i, text in enumerate(commands, 1):
        slug = text_to_slug(text)
        print("\n[" + str(i) + "/" + str(len(commands)) + "] Command: " + text)
        for rep in range(1, REPEATS + 1):
            idx = get_next_index(slug)
            out = os.path.join(AUDIO_DIR, slug + "_" + str(idx).zfill(3) + ".wav")
            print("  Take " + str(rep) + "/" + str(REPEATS) + " -> " + os.path.basename(out))
            input("  Press ENTER when ready...")
            for c in range(3, 0, -1):
                print("  " + str(c) + "...", end=" ", flush=True)
                time.sleep(0.6)
            print()
            with open(out, "wb") as f:
                f.write(record_clip(pa, RECORD_SECS, text))
            total += 1
            print("  Saved: " + out)
            time.sleep(0.3)
except KeyboardInterrupt:
    print("\n\nStopped early.")
finally:
    pa.terminate()

print("\nDone! " + str(total) + " recordings saved to " + AUDIO_DIR)
print("Next step: python prepare_dataset.py")
