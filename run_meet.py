# run_meet.py

import threading, time
from asr_stream import start_audio_stream, transcribe_loop
from summarizer import update_summary

def on_asr(text):
    print("📝 ASR chunk:", text)     # debug/logging
    update_summary(text)             # push into Obsidian note

if __name__ == "__main__":
    # 1) Start capturing
    stream = start_audio_stream()
    print("✅ Audio stream started.")

    # 2) Spin up the transcriber
    t = threading.Thread(target=transcribe_loop, args=(on_asr,), daemon=True)
    t.start()
    print("✅ Transcription thread started.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        stream.stop()    # if you want to cleanly stop PortAudio
        # optionally join the thread here
        exit(0)

    # 3) Keep main alive
    while True:
        time.sleep(1)