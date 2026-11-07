# -*- coding: utf-8 -*-
# Data Augmentation Script for Yoruba Voice Dataset
# Expands your existing WAV files by 4-5x
# Run BEFORE prepare_dataset.py and training

import os
import numpy as np
import soundfile as sf
import random

AUDIO_DIR   = "dataset/audio"
OUTPUT_DIR  = "dataset/audio_augmented"
SAMPLE_RATE = 16000
SEED        = 42

random.seed(SEED)
np.random.seed(SEED)

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_audio(path):
    audio, sr = sf.read(path)
    if len(audio.shape) > 1:
        audio = audio.mean(axis=1)
    return audio.astype(np.float32)

def save_audio(audio, path):
    sf.write(path, audio, SAMPLE_RATE)

# ── AUGMENTATION FUNCTIONS ───────────────────────────────────

def add_noise(audio, noise_level=0.005):
    noise = np.random.randn(len(audio)) * noise_level
    return np.clip(audio + noise, -1.0, 1.0)

def change_speed(audio, speed_factor=None):
    if speed_factor is None:
        speed_factor = random.uniform(0.85, 1.15)
    indices = np.round(np.arange(0, len(audio), speed_factor)).astype(int)
    indices = indices[indices < len(audio)]
    return audio[indices]

def change_volume(audio, gain=None):
    if gain is None:
        gain = random.uniform(0.6, 1.4)
    return np.clip(audio * gain, -1.0, 1.0)

def change_pitch(audio, shift_steps=None):
    if shift_steps is None:
        shift_steps = random.randint(-2, 2)
    factor = 2 ** (shift_steps / 12.0)
    indices = np.round(np.arange(0, len(audio), factor)).astype(int)
    indices = indices[indices < len(audio)]
    stretched = audio[indices]
    if len(stretched) < len(audio):
        stretched = np.pad(stretched, (0, len(audio) - len(stretched)))
    else:
        stretched = stretched[:len(audio)]
    return stretched

def add_reverb(audio, decay=0.3):
    reverb = np.zeros(len(audio))
    delay  = int(SAMPLE_RATE * 0.02)
    reverb[delay:] = audio[:-delay] * decay
    return np.clip(audio + reverb, -1.0, 1.0)

def shift_time(audio, shift_ms=None):
    if shift_ms is None:
        shift_ms = random.randint(-200, 200)
    shift_samples = int(SAMPLE_RATE * shift_ms / 1000)
    if shift_samples > 0:
        return np.pad(audio, (shift_samples, 0))[:len(audio)]
    else:
        return np.pad(audio, (0, -shift_samples))[-shift_samples:]

# ── AUGMENTATION PIPELINE ────────────────────────────────────

AUGMENTATIONS = [
    ("noise",   lambda a: add_noise(a, noise_level=random.uniform(0.003, 0.008))),
    ("speed",   lambda a: change_speed(a)),
    ("volume",  lambda a: change_volume(a)),
    ("pitch",   lambda a: change_pitch(a)),
    ("reverb",  lambda a: add_reverb(a, decay=random.uniform(0.2, 0.4))),
]

# ── MAIN ─────────────────────────────────────────────────────

wav_files = sorted([f for f in os.listdir(AUDIO_DIR) if f.endswith(".wav")])
print("Original files  : " + str(len(wav_files)))
print("Augmentations   : " + str(len(AUGMENTATIONS)))
print("Expected output : " + str(len(wav_files) * (1 + len(AUGMENTATIONS))))
print("")

# Copy originals first
copied = 0
for fname in wav_files:
    src = os.path.join(AUDIO_DIR, fname)
    dst = os.path.join(OUTPUT_DIR, fname)
    audio = load_audio(src)
    save_audio(audio, dst)
    copied += 1

print("Copied originals: " + str(copied))

# Generate augmented versions
augmented = 0
failed    = 0

for fname in wav_files:
    src   = os.path.join(AUDIO_DIR, fname)
    base  = os.path.splitext(fname)[0]
    audio = load_audio(src)

    for aug_name, aug_fn in AUGMENTATIONS:
        try:
            aug_audio = aug_fn(audio.copy())
            # Normalise
            if np.abs(aug_audio).max() > 0:
                aug_audio = aug_audio / np.abs(aug_audio).max() * 0.95
            out_name = base + "_" + aug_name + ".wav"
            out_path = os.path.join(OUTPUT_DIR, out_name)
            save_audio(aug_audio, out_path)
            augmented += 1
        except Exception as e:
            print("FAILED: " + fname + " " + aug_name + " -> " + str(e))
            failed += 1

    if augmented % 500 == 0 and augmented > 0:
        print("Augmented: " + str(augmented))

print("")
print("=== AUGMENTATION COMPLETE ===")
print("Originals  : " + str(copied))
print("Augmented  : " + str(augmented))
print("Failed     : " + str(failed))
print("Total files: " + str(copied + augmented))
print("")
print("Next step: update prepare_dataset.py to use dataset/audio_augmented/")
