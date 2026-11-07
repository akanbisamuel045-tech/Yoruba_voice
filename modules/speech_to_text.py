# -*- coding: utf-8 -*-
import whisper, torch, tempfile, os
import sounddevice, soundfile
import numpy as np

DEVICE      = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_PATH  = "models/whisper_yoruba/whisper_yoruba_best.pt"
SAMPLE_RATE = 16000
MAX_DURATION   = 10
SILENCE_LIMIT  = 1.5
SILENCE_THRESH = 0.01
CHUNK_SIZE     = 1024

_model = None

def load_whisper():
    global _model
    if _model is None:
        print("Loading fine-tuned Whisper model...")
        _model = whisper.load_model("small").to(DEVICE)
        if os.path.exists(MODEL_PATH):
            _model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
            print("Fine-tuned Yoruba weights loaded!")
        else:
            print("Warning: fine-tuned weights not found.")
        _model.eval()
    return _model

def _record_with_vad():
    print("Listening... (speak now)")
    frames=[]; silent_chunks=0; speaking=False; total_chunks=0
    max_chunks=int(SAMPLE_RATE/CHUNK_SIZE*MAX_DURATION)
    silence_chunks=int(SAMPLE_RATE/CHUNK_SIZE*SILENCE_LIMIT)
    with sounddevice.InputStream(samplerate=SAMPLE_RATE,channels=1,dtype="float32",blocksize=CHUNK_SIZE) as stream:
        while total_chunks < max_chunks:
            chunk,_=stream.read(CHUNK_SIZE)
            frames.append(chunk.copy())
            total_chunks+=1
            volume=float(np.abs(chunk).mean())
            if volume > SILENCE_THRESH:
                speaking=True; silent_chunks=0
            else:
                if speaking:
                    silent_chunks+=1
                    if silent_chunks >= silence_chunks:
                        print("Processing...")
                        break
    if not frames: return None
    audio=np.concatenate(frames,axis=0)
    return audio.flatten()

def listen(backend="whisper", **kwargs):
    try:
        model=load_whisper()
        audio=_record_with_vad()
        if audio is None or len(audio)==0:
            print("No audio recorded.")
            return ""
        if np.abs(audio).max() > 0:
            audio=audio/np.abs(audio).max()
        # Add 0.3s silence padding at start - fixes Whisper missing first word
        padding = np.zeros(int(SAMPLE_RATE * 0.2), dtype=np.float32)
        audio   = np.concatenate([padding, audio, padding])
        tmp=tempfile.mktemp(suffix=".wav")
        soundfile.write(tmp,audio,SAMPLE_RATE)
        result=model.transcribe(
            tmp,
            language="yo",
            fp16=False,
            temperature=0.0,
            no_speech_threshold=0.6,
            condition_on_previous_text=False,
        )
        os.remove(tmp)
        text=result["text"].strip().lower()
        clean="".join(c for c in text if ord(c)<1000 or c in "seo")
        clean=clean.strip()
        # Filter hallucinations - only filter if VERY repetitive (5+ same words)
        words = clean.split()
        if len(words) > 5:
            unique = set(words)
            if len(unique) == 1:
                print("Hallucination detected - ignoring.")
                return ""
        # Filter extremely long outputs only
        if len(words) > 15:
            print("Output too long - ignoring.")
            return ""
        # Filter hallucinations - only filter if VERY repetitive (5+ same words)
        words = clean.split()
        if len(words) > 5:
            unique = set(words)
            if len(unique) == 1:
                print("Hallucination detected - ignoring.")
                return ""
        # Filter extremely long outputs only
        if len(words) > 15:
            print("Output too long - ignoring.")
            return ""
        if clean: print("Heard: "+clean)
        else: print("Could not understand.")
        return clean
    except Exception as e:
        print("STT error: "+str(e))
        return ""
