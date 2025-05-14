# Live Meeting AI Scribe

A real‑time in‑room meeting summarizer that listens to your MacBook Pro microphone (or any supported input), transcribes speech with OpenAI’s Whisper, summarizes discussion every 10 seconds via GPT‑3.5‑turbo, and writes rolling notes to an Obsidian vault.

---

## 🔥 Features

* **Offline capture:** Works with your built‑in or USB mic—no Zoom/Teams required.
* **Free transcription:** Uses open‑source Whisper (base model) locally, zero per‑minute fees.
* **Fast summaries:** Calls GPT‑3.5‑turbo for incremental updates every \~10 s.
* **Obsidian integration:** Automatically overwrites a Markdown note in your vault so you can glance at live summaries.
* **Easy Ctrl+C shutdown:** Clean exit on SIGINT/SIGTERM.

---

## 🛠️ Prerequisites

* **macOS/Linux** machine.
* **Conda** (or Miniconda/Mambaforge) installed.
* **Python 3.10** (managed by Conda). 
* An **OpenAI API key** (for GPT‑3.5 calls).
* OPTIONAL:  **Obsidian** installed with a vault on your filesystem.

---

## ⚙️ Installation & Setup

1. **Clone this repo** or download the scripts into a folder (e.g. `meet-env`).

2. **Create a Conda environment**:

   ```bash
   conda create -n meet-env python=3.10 -y
   conda activate meet-env
   ```

3. **Install native deps** (FFmpeg, PortAudio) and Python libraries:

   ```bash
   conda install -c conda-forge ffmpeg libsndfile portaudio cffi -y
   pip install openai-whisper sounddevice numpy scipy python-dotenv requests torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
   ```

4. **Configure environment variables**:

    * Copy `.env.example` to `.env` (or create a new `.env` file).
    * Add your OpenAI key and Obsidian vault path:

      ```dotenv
      OPENAI_API_KEY=sk-<YOUR_OPENAI_KEY>
      # If you are not using Obsidian, then just put it anywhere you want.
      VAULT_PATH=/absolute/path/to/your/Obsidian/Vault
      NOTE_NAME=Live Meeting Summary.md
      ```

---

## 🎙️ Finding & Setting Your Audio Device

By default, the script uses `sd.default.device = 3`, which on a MacBook Pro is usually the built‑in mic. To discover your system’s device index:

```bash
python - <<EOF
import sounddevice as sd
print(sd.query_devices())
EOF
```

Look for the **Input** device you want (e.g. “MacBook Pro Microphone”) and note its index number.

In both `test_record.py` and `asr_stream.py`, set:

```python
import sounddevice as sd
sd.default.device = <YOUR_DEVICE_INDEX>
```

---

## 📁 Project Structure

```
meet-env/
├─ .env
├─ asr_stream.py      # audio capture + Whisper transcription
├─ summarizer.py      # OpenAI GPT-3.5 summarizer + Obsidian sync
├─ run_meet.py        # orchestrator (starts audio & summarizer)
├─ test_record.py     # simple mic test & WAV recorder
└─ Live Meeting Summary.md  # your live-updated Obsidian note
```

---

## 🚀 Usage

1. **Test your mic**:

   ```bash
   python test_record.py
   afplay test.wav   # (macOS) or play test.wav on Linux
   ```
2. **Run the pipeline** in foreground:

   ```bash
   python run_meet.py
   ```

   You should see logs:

   ```
   ✅ Audio stream started.
   ✅ Transcription thread started.
   📝 ASR chunk: Hello everyone…
   ```
3. **Check Obsidian**: Open `Live Meeting Summary.md` in your vault, watch rolling summaries.
4. **Background mode** (optional):

   ```bash
   nohup python run_meet.py &> meet.log &
   tail -f meet.log
   ```
5. **Shutdown**: Press `Ctrl+C` once—script catches SIGINT and exits cleanly.

---

## 🐞 Troubleshooting

* **Segmentation fault**: Ensure you installed the CPU‑only PyTorch wheel. Run the import tests:

  ```bash
  python - <<EOF
  import torch, whisper, sounddevice
  print(torch.__version__, whisper.load_model("base").device)
  EOF
  ```
* **Silent audio**: Confirm your device index & enable **Terminal** mic permissions under **System Preferences → Privacy → Microphone**.
* **OpenAI errors**: Check your API key in `.env`, and inspect `meet.log` for HTTP/status errors.
