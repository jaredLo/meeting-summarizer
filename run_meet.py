import os
import time
import threading
import signal, os
import sys

from dotenv import load_dotenv
from asr_stream import start_audio_stream, transcribe_loop
from summarizer import update_summary

load_dotenv()
RAW_LOG = os.getenv("RAW_LOG_PATH", "transcript.log")

def log_raw(text: str):
    """Append raw ASR text with timestamp to RAW_LOG."""
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(RAW_LOG, "a") as f:
        f.write(f"{ts} | {text}\n")

def on_asr(text: str):
    # 1) Dump raw transcription
    log_raw(text)
    # 2) Feed into your summarizer
    update_summary(text)

def shutdown(signum, frame):
    print("\n🛑 Shutting down…")
    try: stream.stop()
    except: pass
    os._exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT,  shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    # start mic → queue
    stream = start_audio_stream()
    print("✅ Audio stream started.")

    # transcription thread drives on_asr
    t = threading.Thread(target=transcribe_loop, args=(on_asr,), daemon=True)
    t.start()
    print("✅ Transcription thread started.")

    # live input loop (or idle)
    while True:
        time.sleep(1)