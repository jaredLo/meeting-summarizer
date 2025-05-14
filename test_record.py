import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

# ➤ Set MacBook Pro mic as default input (index 3 from your list)
sd.default.device = 3

fs, duration = 16000, 3  # 16 kHz × 3 s
print(f"🎤 Recording {duration}s on device #{sd.default.device} ({sd.query_devices(sd.default.device)['name']})")

rec = sd.rec(int(fs * duration), samplerate=fs, channels=1)
sd.wait()
write("test.wav", fs, rec)
print("💾 Saved test.wav – play with `afplay test.wav`")