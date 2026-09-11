from pathlib import Path
import soundfile as sf


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "raw"


SUPPORTED_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".flac",
    ".m4a",
    ".ogg",
    ".opus",
}


def get_audio_files(directory: Path):
    return [
        path
        for path in directory.rglob("*")
        if path.is_file()
        and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]


def main():
    files = get_audio_files(RAW_DIR)

    print("=" * 60)
    print("YALI DATASET INSPECTION")
    print("=" * 60)

    print(f"Dataset directory : {RAW_DIR}")
    print(f"Audio files       : {len(files)}")
    print()

    for index, file in enumerate(files, start=1):
        print(f"{index:03d}. {file.name}")

    print("=" * 60)


if __name__ == "__main__":
    main()