from pathlib import Path
import librosa
import soundfile as sf


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "raw" / "yali_audio"
WAV_DIR = PROJECT_ROOT / "data" / "processed" / "wav"
SEGMENT_DIR = PROJECT_ROOT / "data" / "processed" / "segments"

TARGET_SR = 16000

# Panjang segment
SEGMENT_DURATION = 15  # seconds

# Overlap antar segment
OVERLAP = 2  # seconds


# ============================================================
# CREATE DIRECTORIES
# ============================================================

WAV_DIR.mkdir(parents=True, exist_ok=True)
SEGMENT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# FIND AUDIO FILES
# ============================================================

SUPPORTED_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".flac",
    ".m4a",
    ".ogg",
    ".opus",
}


def find_audio_files(directory: Path):
    return sorted(
        [
            path
            for path in directory.rglob("*")
            if path.is_file()
            and path.suffix.lower() in SUPPORTED_EXTENSIONS
        ]
    )


# ============================================================
# CONVERT TO WAV
# ============================================================

def convert_to_wav(source_path: Path):

    output_path = WAV_DIR / f"{source_path.stem}.wav"

    if output_path.exists():
        print(f"[SKIP] WAV already exists: {output_path.name}")
        return output_path

    print(f"[CONVERT] {source_path.name}")

    audio, _ = librosa.load(
        source_path,
        sr=TARGET_SR,
        mono=True
    )

    sf.write(
        output_path,
        audio,
        TARGET_SR
    )

    return output_path


# ============================================================
# SEGMENT AUDIO
# ============================================================

def segment_audio(wav_path: Path):

    print(f"[SEGMENT] {wav_path.name}")

    audio, sr = librosa.load(
        wav_path,
        sr=TARGET_SR,
        mono=True
    )

    segment_samples = int(SEGMENT_DURATION * sr)
    overlap_samples = int(OVERLAP * sr)

    step = segment_samples - overlap_samples

    total_samples = len(audio)

    segment_number = 1
    start = 0

    while start < total_samples:

        end = start + segment_samples

        segment = audio[start:end]

        duration = len(segment) / sr

        # Abaikan potongan terlalu pendek di akhir
        if duration < 5:
            break

        output_name = (
            f"{wav_path.stem}_"
            f"{segment_number:03d}.wav"
        )

        output_path = SEGMENT_DIR / output_name

        sf.write(
            output_path,
            segment,
            sr
        )

        segment_number += 1
        start += step


# ============================================================
# MAIN
# ============================================================

def main():

    files = find_audio_files(RAW_DIR)

    print("=" * 60)
    print("YALI DATASET PREPROCESSING")
    print("=" * 60)

    print(f"Input directory : {RAW_DIR}")
    print(f"Files found     : {len(files)}")
    print(f"Target SR       : {TARGET_SR} Hz")
    print(f"Segment length  : {SEGMENT_DURATION} sec")
    print(f"Overlap         : {OVERLAP} sec")
    print("=" * 60)

    if not files:
        print("Tidak ada file audio ditemukan.")
        return

    for index, source_path in enumerate(files, start=1):

        print()
        print(f"[{index}/{len(files)}]")

        wav_path = convert_to_wav(source_path)

        segment_audio(wav_path)

    print()
    print("=" * 60)
    print("PREPROCESSING SELESAI")
    print("=" * 60)


if __name__ == "__main__":
    main()