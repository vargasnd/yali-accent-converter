from pathlib import Path
import librosa


PROJECT_ROOT = Path(__file__).resolve().parents[1]

REFERENCE = PROJECT_ROOT / "data" / "reference" / "yali_reference.wav"
SOURCE = PROJECT_ROOT / "input" / "indonesia_synthetic.wav"


def inspect_audio(path: Path):
    print("=" * 60)
    print(f"FILE: {path.name}")
    print("=" * 60)

    if not path.exists():
        print("ERROR: file tidak ditemukan")
        return

    audio, sample_rate = librosa.load(
        path,
        sr=None,
        mono=False
    )

    if audio.ndim == 1:
        channels = 1
        samples = len(audio)
    else:
        channels = audio.shape[0]
        samples = audio.shape[1]

    duration = samples / sample_rate

    print(f"Sample rate : {sample_rate} Hz")
    print(f"Channels    : {channels}")
    print(f"Samples     : {samples}")
    print(f"Duration    : {duration:.2f} seconds")
    print()


def main():
    inspect_audio(REFERENCE)
    inspect_audio(SOURCE)


if __name__ == "__main__":
    main()