from pathlib import Path
import sys
import shutil
import uuid

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles


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
# OUTPUT DIRECTORY
# =========================

OUTPUT_DIR = BASE_DIR / "output" / "final"
OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================
# FASTAPI
# =========================

api = FastAPI(
    title="Yali Accent Converter API",
    description="Backend API untuk konversi karakter pengucapan Bahasa Indonesia.",
    version="1.0.0"
)


# =========================
# STATIC OUTPUT
# =========================

api.mount(
    "/outputs",
    StaticFiles(directory=str(OUTPUT_DIR)),
    name="outputs"
)


# =========================
# LOAD MODELS
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
# CONVERT AUDIO
# =========================

@api.post("/convert")
async def convert_audio(
    file: UploadFile = File(...)
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Nama file tidak ditemukan."
        )

    input_dir = BASE_DIR / "server" / "temp"

    input_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    input_path = (
        input_dir
        / f"{uuid.uuid4().hex}_{file.filename}"
    )

    try:

        # Simpan input sementara
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        print(f"Processing: {file.filename}")

        # Jalankan pipeline
        transcription, output_audio = convert_speech(
            str(input_path)
        )

        output_path = Path(output_audio)

        if not output_path.exists():
            raise RuntimeError(
                "File hasil konversi tidak ditemukan."
            )

        return {
            "status": "success",
            "transcription": transcription,
            "audio_url": f"/outputs/{output_path.name}"
        }

    except Exception as e:

        print("ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        # Hapus input sementara
        if input_path.exists():
            input_path.unlink()