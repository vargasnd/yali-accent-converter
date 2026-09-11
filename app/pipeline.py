from pathlib import Path
import uuid

import whisper
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS


# =========================
# PATH CONFIGURATION
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

REFERENCE_AUDIO = (
    BASE_DIR / "data" / "reference" / "yali_reference.wav"
)

OUTPUT_DIR = (
    BASE_DIR / "output" / "final"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =========================
# MODEL
# =========================

whisper_model = whisper.load_model(
    "base",
    device="cuda"
)

chatterbox_model = ChatterboxTTS.from_pretrained(
    device="cuda"
)


def load_models():
    """
    Load Whisper dan Chatterbox.

    Model dijalankan pada GPU jika tersedia.
    """

    global whisper_model
    global chatterbox_model

    print("Loading Whisper...")

    whisper_model = whisper.load_model(
        "base",
        device="cuda"
    )

    print("Whisper loaded.")

    print("Loading Chatterbox...")

    chatterbox_model = ChatterboxTTS.from_pretrained(
        device="cuda"
    )

    print("Chatterbox loaded.")


# =========================
# SPEECH-TO-SPEECH
# =========================

def convert_speech(input_audio):
    """
    Pipeline:

    Indonesian Speech
          ↓
       Whisper
          ↓
    Indonesian Text
          ↓
     Chatterbox
          +
    Yali Reference
          ↓
      Output Audio
    """

    if whisper_model is None or chatterbox_model is None:
        raise RuntimeError(
            "Model belum di-load. Jalankan load_models() terlebih dahulu."
        )

    if not input_audio:
        raise ValueError("Input audio tidak ditemukan.")

    if not REFERENCE_AUDIO.exists():
        raise FileNotFoundError(
            f"Reference audio tidak ditemukan: {REFERENCE_AUDIO}"
        )

    # -------------------------
    # 1. Speech → Text
    # -------------------------

    print("Transcribing...")

    result = whisper_model.transcribe(
        input_audio,
        language="id"
    )

    text = result["text"].strip()

    print("Transcription:")
    print(text)

    # -------------------------
    # 2. Text → Yali-style Speech
    # -------------------------

    print("Generating Yali-style speech...")

    wav = chatterbox_model.generate(
        text,
        audio_prompt_path=str(REFERENCE_AUDIO)
    )

    # -------------------------
    # 3. Save output
    # -------------------------

    filename = (
        f"converted_{uuid.uuid4().hex[:8]}.wav"
    )

    output_path = OUTPUT_DIR / filename

    ta.save(
        str(output_path),
        wav,
        chatterbox_model.sr
    )

    print("Output:")
    print(output_path)

    return text, str(output_path)