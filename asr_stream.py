# asr_stream.py

import whisper
import sounddevice as sd
import numpy as np
from queue import Queue

# ─── CONFIG ─────────────────────────────────────────────────
sd.default.device = 3     # ← MacBook Pro Mic
_SAMPLE_RATE = 16000
_BUFFER_SEC  = 5          # chunk length
# ────────────────────────────────────────────────────────────

q = Queue()
model = whisper.load_model("base")  # you’re on CPU now

def start_audio_stream():
    """Begin capturing mic audio and stuffing it into q."""
    stream = sd.InputStream(
        samplerate=_SAMPLE_RATE,
        channels=1,
        callback=lambda indata, *_: q.put(indata.copy())
    )
    stream.start()
    return stream

def transcribe_loop(on_asr):
    """Buffer up _BUFFER_SEC of audio, run Whisper, then call on_asr(text)."""
    buffer = np.zeros((0,1), dtype=np.float32)
    while True:
        chunk = q.get()
        buffer = np.concatenate([buffer, chunk])
        if buffer.shape[0] >= _SAMPLE_RATE * _BUFFER_SEC:
            audio = buffer.flatten()
            text = model.transcribe(audio, language="en")["text"].strip()
            if text:
                on_asr(text)
            buffer = np.zeros((0,1), dtype=np.float32)