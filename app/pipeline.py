from pathlib import Path
import os
import subprocess
import sys
import uuid

import torch
import torchaudio as ta
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
    global whisper_model
    global reference_audio
    global cfm_checkpoint

    print("===================================")
    print(" Yali Accent Converter")
    print("===================================")
    print(f"Device: {DEVICE}")

    if not SEED_VC_DIR.exists():
        raise FileNotFoundError(f"Folder Seed-VC tidak ditemukan:\n{SEED_VC_DIR}")

    inference_file = SEED_VC_DIR / "inference_v2.py"

    if not inference_file.exists():
        raise FileNotFoundError(f"inference_v2.py tidak ditemukan:\n{inference_file}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Mengambil reference Yali...")

    reference_audio = hf_hub_download(
        repo_id=HF_YALI_REPO, filename="yali_reference.wav"
    )

    print("Mengambil model CFM Yali...")

    cfm_checkpoint = hf_hub_download(
        repo_id=HF_YALI_REPO, filename="yali_cfm_final.pth"
    )

    print("Memuat Whisper...")

    whisper_model = whisper.load_model("base", device=DEVICE)

    print("Semua model siap.")
    print("===================================")


def convert_speech(input_audio):

    if whisper_model is None:
        raise RuntimeError("Whisper belum di-load.")

    if reference_audio is None:
        raise RuntimeError("Reference Yali belum tersedia.")

    if cfm_checkpoint is None:
        raise RuntimeError("Model CFM Yali belum tersedia.")

    if not input_audio:
        raise ValueError("Input audio tidak ditemukan.")

    input_audio = Path(input_audio).resolve()

    if not input_audio.exists():
        raise FileNotFoundError(f"File audio tidak ditemukan:\n{input_audio}")

    print(f"Input: {input_audio}")

    # =========================
    # 1. TRANSKRIPSI
    # =========================

    print("Transkripsi audio...")

    result = whisper_model.transcribe(str(input_audio), language="id")

    text = result["text"].strip()

    if not text:
        raise RuntimeError("Tidak ada ucapan yang terdeteksi.")

    print(f"Transkripsi: {text}")

    # =========================
    # 2. OUTPUT DIRECTORY
    # =========================

    run_id = uuid.uuid4().hex[:8]

    run_output_dir = OUTPUT_DIR / f"run_{run_id}"

    run_output_dir.mkdir(parents=True, exist_ok=True)

    # =========================
    # 3. DIFFUSION STEPS
    # =========================

    diffusion_steps = "30"

    print(f"Seed-VC diffusion steps: " f"{diffusion_steps}")

    # =========================
    # 4. SEED-VC
    # =========================

    command = [
        sys.executable,
        str(SEED_VC_DIR / "inference_v2.py"),
        "--source",
        str(input_audio),
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

    print("Menjalankan Seed-VC...")

    subprocess.run(command, cwd=str(SEED_VC_DIR), env=env, check=True)

    # =========================
    # 5. CARI OUTPUT
    # =========================

    wav_files = list(run_output_dir.glob("*.wav"))

    if not wav_files:
        raise RuntimeError("Seed-VC selesai tetapi " "file output tidak ditemukan.")

    generated_audio = max(wav_files, key=lambda p: p.stat().st_mtime)

    # =========================
    # 6. SALIN KE OUTPUT FINAL
    # =========================

    filename = f"converted_{run_id}.wav"

    final_output = OUTPUT_DIR / filename

    waveform, sample_rate = ta.load(str(generated_audio))

    ta.save(str(final_output), waveform, sample_rate)

    print(f"Output: {final_output}")

    return text, str(final_output)
