# -*- coding: utf-8 -*-
import os, random
import nemo.collections.asr as nemo_asr

MODEL_PATH = "models/yoruba_conformer/yoruba_asr_final.nemo"
AUDIO_DIR  = "dataset/audio"

print("Loading trained model...")
model = nemo_asr.models.EncDecCTCModel.restore_from(MODEL_PATH)
model.eval()

files = [os.path.join(AUDIO_DIR, f) for f in os.listdir(AUDIO_DIR) if f.endswith(".wav")]
samples = random.sample(files, min(10, len(files)))

print("=== TRANSCRIPTION TEST ===")
correct = 0
for path in samples:
    fname = os.path.basename(path)
    expected = " ".join(fname.replace(".wav","").split("_")[:-1])
    result = model.transcribe([path])
    predicted = result[0] if isinstance(result[0], str) else result[0].text
    match = predicted.strip() == expected.strip()
    if match: correct += 1
    status = "PASS" if match else "FAIL"
    print(f"[{status}] Expected: {expected}")
    print(f"       Got     : {predicted}")
    print("---")
print(f"Score: {correct}/10")