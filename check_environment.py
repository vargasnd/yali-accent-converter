import importlib
import sys

REQUIRED_MODULES = {
    "torch": "torch",
    "torchaudio": "torchaudio",
    "gradio": "gradio",
    "whisper": "openai-whisper",
    "transformers": "transformers",
    "huggingface_hub": "huggingface-hub",
    "einops": "einops",
    "soundfile": "soundfile",
    "librosa": "librosa",
    "scipy": "scipy",
    "munch": "munch",
    "hydra": "hydra-core",
    "omegaconf": "omegaconf",
    "yaml": "pyyaml",
    "matplotlib": "matplotlib",
    "funasr": "funasr",
    "modelscope": "modelscope",
    "resemblyzer": "resemblyzer",
    "descript_audio_codec": "descript-audio-codec",
}

print("Checking Python dependencies...")
print()

failed = []

for module, package in REQUIRED_MODULES.items():
    try:
        importlib.import_module(module)
        print(f"[OK] {package}")
    except Exception as e:
        print(f"[FAIL] {package}")
        print(f"      {e}")
        failed.append(package)

print()

# FFmpeg
import shutil

if shutil.which("ffmpeg"):
    print("[OK] FFmpeg")
else:
    print("[FAIL] FFmpeg")
    failed.append("FFmpeg")

print()

if failed:
    print("Some dependencies are missing:")
    for item in failed:
        print(f" - {item}")
    sys.exit(1)

print("===================================")
print(" ALL DEPENDENCIES ARE READY")
print("===================================")