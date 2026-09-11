from pathlib import Path
import csv
import soundfile as sf


PROJECT_ROOT = Path(__file__).resolve().parents[1]

SEGMENT_DIR = PROJECT_ROOT / "data" / "processed" / "segments"
OUTPUT_CSV = PROJECT_ROOT / "data" / "processed" / "metadata.csv"


def main():

    files = sorted(SEGMENT_DIR.glob("*.wav"))

    rows = []

    for file in files:

        audio, sample_rate = sf.read(file)

        duration = len(audio) / sample_rate

        rows.append({
            "filename": file.name,
            "duration_sec": round(duration, 3),
            "sample_rate": sample_rate,
            "channels": 1
        })

    with open(
        OUTPUT_CSV,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "filename",
                "duration_sec",
                "sample_rate",
                "channels"
            ]
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"Metadata saved: {OUTPUT_CSV}")
    print(f"Total segments: {len(rows)}")


if __name__ == "__main__":
    main()