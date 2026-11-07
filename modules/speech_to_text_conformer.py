# -*- coding: utf-8 -*-
import torch, tempfile, os
import sounddevice, soundfile
import numpy as np
import nemo.collections.asr as nemo_asr

MODEL_PATH  = "models/conformer_yoruba/conformer_yoruba.nemo"
SAMPLE_RATE = 16000
MAX_DURATION   = 10
SILENCE_THRESH = 0.01
SILENCE_LIMIT  = 1.5
CHUNK_SIZE     = 1024

_model = None

def load_conformer():
    global _model
    if _model is None:
        print("Loading Conformer model...")
        _model = nemo_asr.models.EncDecCTCModel.restore_from(MODEL_PATH)
        _model.eval()
        print("Conformer loaded!")
    return _model

def listen(backend="conformer", **kwargs):
    try:
        model = load_conformer()
        print("Listening... (speak now)")
        frames = []
        silent_chunks = 0
        max_chunks = int(SAMPLE_RATE / CHUNK_SIZE * MAX_DURATION)
        silence_chunks = int(SAMPLE_RATE / CHUNK_SIZE * SILENCE_LIMIT)
        speaking = False
        with sounddevice.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32", blocksize=CHUNK_SIZE) as stream:
            for _ in range(max_chunks):
                chunk, _ = stream.read(CHUNK_SIZE)
                volume = float(np.abs(chunk).mean())
                frames.append(chunk)
                if volume > SILENCE_THRESH:
                    speaking = True
                    silent_chunks = 0
                elif speaking:
                    silent_chunks += 1
                    if silent_chunks >= silence_chunks:
                        break
        print("Processing...")
        audio = np.concatenate(frames, axis=0).flatten()
        tmp = tempfile.mktemp(suffix=".wav")
        soundfile.write(tmp, audio, SAMPLE_RATE)
        result = model.transcribe([tmp])
        os.remove(tmp)
        text = result[0] if isinstance(result[0], str) else result[0].text
        text = text.strip().lower()
        print("Heard: " + text)
        return text
    except Exception as e:
        print("Conformer STT error: " + str(e))
        return ""