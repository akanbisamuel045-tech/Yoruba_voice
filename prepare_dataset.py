# -*- coding: utf-8 -*-
import os, json, wave, random, csv

AUDIO_DIR      = "dataset/audio_augmented"
CSV_PHONE      = "dataset/labels_phone.csv"
TRAIN_MANIFEST = "dataset/train.jsonl"
VAL_MANIFEST   = "dataset/val.jsonl"
VAL_SPLIT      = 0.15
RANDOM_SEED    = 42

def get_duration(path):
    with wave.open(path, "r") as wf:
        return round(wf.getnframes() / wf.getframerate(), 3)

def load_label_map():
    mapping = {}
    with open(CSV_PHONE, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            fname = row["filename"].strip()
            text  = row["text"].strip().lower()
            base  = os.path.splitext(fname)[0]
            mapping[fname] = text
            # Also map augmented versions
            for aug in ["noise", "speed", "volume", "pitch", "reverb"]:
                mapping[base + "_" + aug + ".wav"] = text
    return mapping

def slug_to_text(fname):
    name = os.path.splitext(fname)[0]
    # Remove augmentation suffix
    for aug in ["_noise", "_speed", "_volume", "_pitch", "_reverb"]:
        name = name.replace(aug, "")
    parts = name.split("_")
    if parts and parts[-1].isdigit():
        parts = parts[:-1]
    return " ".join(parts).lower()

phone_labels = load_label_map()
wav_files    = sorted([f for f in os.listdir(AUDIO_DIR) if f.endswith(".wav")])

print("Total WAV files: " + str(len(wav_files)))

entries = []
skipped = 0

for fname in wav_files:
    path     = os.path.join(AUDIO_DIR, fname)
    abs_path = os.path.abspath(path).replace(chr(92), chr(47))
    text     = phone_labels.get(fname, slug_to_text(fname))

    if not text:
        skipped += 1
        continue

    try:
        duration = get_duration(path)
    except Exception as e:
        skipped += 1
        continue

    if duration < 0.3:
        skipped += 1
        continue

    entries.append({"audio_filepath": abs_path, "duration": duration, "text": text})

random.seed(RANDOM_SEED)
random.shuffle(entries)
split      = int(len(entries) * (1 - VAL_SPLIT))
train_data = entries[:split]
val_data   = entries[split:]

nl = chr(10)
for fpath, data, label in [(TRAIN_MANIFEST, train_data, "train"), (VAL_MANIFEST, val_data, "val")]:
    with open(fpath, "w", encoding="utf-8") as f:
        for entry in data:
            f.write(json.dumps(entry, ensure_ascii=False) + nl)
    print(label + ": " + str(len(data)) + " entries -> " + fpath)

print("Skipped: " + str(skipped))
print("Total  : " + str(len(entries)))
print("Ready for training!")
