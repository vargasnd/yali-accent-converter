from pathlib import Path
import os
import shutil
import subprocess
import sys
import uuid

import torch
import whisper
from huggingface_hub import hf_hub_download


BASE_DIR = Path(__file__).resolve().parent.parent
SEED_VC_DIR = BASE_DIR / "seed-vc"
OUTPUT_DIR = BASE_DIR / "output" / "final"

HF_YALI_REPO = "vargasnd/yali-accent-model"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

whisper_model = None
reference_audio = None
cfm_checkpoint = None


def load_models():
    global whisper_model, reference_audio, cfm_checkpoint

    print(f"Device: {DEVICE}")

    print("Loading Whisper...")
    whisper_model = whisper.load_model("base", device=DEVICE)

    print("Downloading/loading Yali reference audio...")
    reference_audio = hf_hub_download(
        repo_id=HF_YALI_REPO,
        filename="yali_reference.wav"
    )

    print("Downloading/loading CFM checkpoint...")
    cfm_checkpoint = hf_hub_download(
        repo_id=HF_YALI_REPO,
        filename="yali_cfm_final.pth"
    )

    print("Models and assets ready.")


def convert_speech(input_audio):
    if whisper_model is None:
        load_models()

    input_audio = Path(input_audio)

    if not input_audio.exists():
        raise FileNotFoundError(
            f"Input audio tidak ditemukan: {input_audio}"
        )

    # ==========================================
    # 1. Speech-to-Text menggunakan Whisper
    # ==========================================

    print("Transcribing input audio...")

    result = whisper_model.transcribe(
        str(input_audio),
        language="id"
    )

    text = result["text"].strip()

    print(f"Transcription: {text}")

    if not text:
        raise ValueError(
            "Whisper tidak menghasilkan transkripsi."
        )

    # ==========================================
    # 2. Persiapan folder output
    # ==========================================

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    run_id = uuid.uuid4().hex[:8]

    run_output_dir = OUTPUT_DIR / f"run_{run_id}"

    run_output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # ==========================================
    # 3. Seed-VC V2 Inference
    # ==========================================

    diffusion_steps = "30"

    command = [
        sys.executable,
        str(SEED_VC_DIR / "inference_v2.py"),

        "--source",
        str(input_audio.resolve()),

        "--target",
        str(Path(reference_audio).resolve()),

        "--output",
        str(run_output_dir.resolve()),

        "--diffusion-steps",
        diffusion_steps,

        "--length-adjust",
        "1.0",

        "--intelligibility-cfg-rate",
        "1.0",

        "--similarity-cfg-rate",
        "0.7",

        "--top-p",
        "0.9",

        "--temperature",
        "1.0",

        "--repetition-penalty",
        "1.0",

        "--convert-style",
        "true",

        "--anonymization-only",
        "false",

        "--cfm-checkpoint-path",
        str(Path(cfm_checkpoint).resolve()),
    ]

    env = os.environ.copy()

    env["PYTHONPATH"] = str(SEED_VC_DIR)

    print("Starting Seed-VC V2 inference...")
    print(f"Seed-VC diffusion steps: {diffusion_steps}")

    subprocess.run(
        command,
        cwd=str(SEED_VC_DIR),
        env=env,
        check=True
    )

    # ==========================================
    # 4. Cari hasil audio
    # ==========================================

    wav_files = list(
        run_output_dir.glob("*.wav")
    )

    if not wav_files:
        raise FileNotFoundError(
            "Seed-VC selesai tetapi file output WAV tidak ditemukan."
        )

    generated_audio = max(
        wav_files,
        key=lambda p: p.stat().st_mtime
    )

    # ==========================================
    # 5. Copy hasil ke folder final
    # ==========================================

    filename = f"converted_{run_id}.wav"

    final_output = OUTPUT_DIR / filename

    # Tidak menggunakan torchaudio/TorchCodec.
    # Langsung copy file WAV hasil Seed-VC.
    shutil.copy2(
        generated_audio,
        final_output
    )

    print(f"Output: {final_output}")

    return text, str(final_output)