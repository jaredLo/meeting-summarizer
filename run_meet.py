import threading
import time
import signal
import os   # ← added

from asr_stream import start_audio_stream, transcribe_loop
from summarizer import update_summary

def on_asr(text):
    print("📝 ASR chunk:", text)
    update_summary(text)

def shutdown(signum, frame):
    print("\n🛑 Shutting down…")
    try:
        stream.stop()
    except Exception:
        pass
    os._exit(0)   # HARD KILL: no mercy

if __name__ == "__main__":
    # Catch Ctrl+C and kill signals
    signal.signal(signal.SIGINT,  shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    # 1) Start audio
    stream = start_audio_stream()
    print("✅ Audio stream started.")

    # 2) Launch transcription thread
    t = threading.Thread(
        target=transcribe_loop,
        args=(on_asr,),
        daemon=True
    )
    t.start()
    print("✅ Transcription thread started.")

    # 3) Hang out until we’re zapped
    while True:
        time.sleep(1)