from pathlib import Path
import csv
import soundfile as sf


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "training_candidate"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "training_manifest.csv"
)


def main():

    files = sorted(DATASET_DIR.glob("*.wav"))

    rows = []

    for file in files:

        audio, sample_rate = sf.read(file)

        duration = len(audio) / sample_rate

        rows.append({
            "path": str(file.resolve()),
            "filename": file.name,
            "duration_sec": round(duration, 3),
            "sample_rate": sample_rate,
        })

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "path",
                "filename",
                "duration_sec",
                "sample_rate",
            ]
        )

        writer.writeheader()
        writer.writerows(rows)

    print("=" * 60)
    print("TRAINING MANIFEST")
    print("=" * 60)

    print(f"Files      : {len(rows)}")
    print(f"Manifest   : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()