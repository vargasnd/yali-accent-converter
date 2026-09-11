from pathlib import Path
import sys

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import shutil
import uuid


# =========================
# PROJECT PATH
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "app"

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


# =========================
# PIPELINE
# =========================

from pipeline import load_models, convert_speech


# =========================
# FASTAPI APP
# =========================

api = FastAPI(
    title="Yali Accent Converter API",
    description="Backend API untuk konversi karakter pengucapan Bahasa Indonesia.",
    version="1.0.0"
)


# =========================
# LOAD MODEL
# =========================

print("Loading models...")
load_models()
print("Models loaded successfully.")


# =========================
# HEALTH CHECK
# =========================

@api.get("/")
def root():
    return {
        "status": "online",
        "service": "Yali Accent Converter API"
    }


# =========================
# SPEECH CONVERSION
# =========================

@api.post("/convert")
async def convert_audio(
    file: UploadFile = File(...)
):

    input_dir = BASE_DIR / "server" / "temp"
    input_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    input_path = (
        input_dir
        / f"{uuid.uuid4().hex}_{file.filename}"
    )

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    try:

        transcription, output_audio = convert_speech(
            str(input_path)
        )

        return {
            "status": "success",
            "transcription": transcription,
            "audio_path": output_audio
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }

    finally:

        if input_path.exists():
            input_path.unlink()