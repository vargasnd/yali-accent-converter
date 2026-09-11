from pathlib import Path
import uuid

import torch
import torchaudio as ta
import whisper

from huggingface_hub import hf_hub_download
from safetensors.torch import load_file
from chatterbox.tts import ChatterboxTTS


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "output" / "final"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Hugging Face repository milik project
HF_YALI_REPO = "vargasnd/yali-accent-model"

# Indonesian Chatterbox checkpoint
CHATTERBOX_REPO = "grandhigh/Chatterbox-TTS-Indonesian"
CHATTERBOX_CHECKPOINT = "t3_cfg.safetensors"


# ============================================================
# DEVICE
# ============================================================

if torch.cuda.is_available():
    DEVICE = "cuda"
else:
    DEVICE = "cpu"

print(f"Using device: {DEVICE}")


# ============================================================
# MODEL VARIABLES
# ============================================================

whisper_model = None
chatterbox_model = None
reference_audio = None


# ============================================================
# LOAD MODELS
# ============================================================

def load_models():
    global whisper_model
    global chatterbox_model
    global reference_audio

    print("=" * 60)
    print("Loading models...")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. Download Yali reference from Hugging Face
    # --------------------------------------------------------

    print("\n[1/3] Loading Yali reference audio...")

    reference_audio = hf_hub_download(
        repo_id=HF_YALI_REPO,
        filename="yali_reference.wav"
    )

    print(f"Yali reference: {reference_audio}")

    # --------------------------------------------------------
    # 2. Load Whisper
    # --------------------------------------------------------

    print("\n[2/3] Loading Whisper...")

    whisper_model = whisper.load_model(
        "base",
        device=DEVICE
    )

    print("Whisper loaded.")

    # --------------------------------------------------------
    # 3. Load Chatterbox
    # --------------------------------------------------------

    print("\n[3/3] Loading Chatterbox...")

    # Compatibility workaround for Perth
    from perth.perth_net.perth_net_implicit.perth_watermarker import (
        PerthImplicitWatermarker
    )

    import perth

    perth.PerthImplicitWatermarker = PerthImplicitWatermarker

    # Load base Chatterbox
    chatterbox_model = ChatterboxTTS.from_pretrained(
        device=DEVICE
    )

    print("Base Chatterbox loaded.")

    # --------------------------------------------------------
    # Load Indonesian fine-tuned checkpoint
    # --------------------------------------------------------

    print("Downloading Indonesian Chatterbox checkpoint...")

    checkpoint_path = hf_hub_download(
        repo_id=CHATTERBOX_REPO,
        filename=CHATTERBOX_CHECKPOINT
    )

    print(f"Checkpoint: {checkpoint_path}")

    print("Loading Indonesian checkpoint...")

    t3_state = load_file(
        checkpoint_path,
        device="cpu"
    )

    chatterbox_model.t3.load_state_dict(
        t3_state
    )

    print("Indonesian Chatterbox checkpoint loaded.")

    if DEVICE == "cuda":
        torch.cuda.empty_cache()

    print("\n" + "=" * 60)
    print("All models loaded successfully.")
    print("=" * 60)


# ============================================================
# SPEECH CONVERSION
# ============================================================

def convert_speech(input_audio):
    if whisper_model is None or chatterbox_model is None:
        raise RuntimeError(
            "Model belum di-load. Jalankan load_models() terlebih dahulu."
        )

    if not input_audio:
        raise ValueError(
            "Input audio tidak ditemukan."
        )

    if reference_audio is None:
        raise FileNotFoundError(
            "Reference audio Yali tidak ditemukan."
        )

    # --------------------------------------------------------
    # Speech-to-Text
    # --------------------------------------------------------

    print("\nTranscribing input audio...")

    result = whisper_model.transcribe(
        input_audio,
        language="id"
    )

    text = result["text"].strip()

    print("Transcription:")
    print(text)

    if not text:
        raise RuntimeError(
            "Whisper tidak menemukan ucapan pada audio."
        )

    # --------------------------------------------------------
    # Text-to-Speech / Yali-style conversion
    # --------------------------------------------------------

    print("\nGenerating Yali-style speech...")

    wav = chatterbox_model.generate(
        text,
        audio_prompt_path=reference_audio
    )

    # --------------------------------------------------------
    # Save output
    # --------------------------------------------------------

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