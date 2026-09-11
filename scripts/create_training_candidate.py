from pathlib import Path
import shutil
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

SEGMENT_DIR = PROJECT_ROOT / "data" / "processed" / "segments"
REVIEW_FILE = PROJECT_ROOT / "data" / "processed" / "manual_review.csv"

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "training_candidate"


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df = pd.read_csv(REVIEW_FILE)

    good = df[
        df["decision"].str.upper() == "GOOD"
    ]

    print("=" * 60)
    print("CREATE TRAINING CANDIDATE")
    print("=" * 60)

    print(f"GOOD files: {len(good)}")

    copied = 0
    missing = 0

    for _, row in good.iterrows():

        filename = row["filename"]

        source = SEGMENT_DIR / filename
        destination = OUTPUT_DIR / filename

        if not source.exists():

            print(f"[MISSING] {filename}")
            missing += 1
            continue

        if destination.exists():
            print(f"[SKIP] {filename}")
            continue

        shutil.copy2(
            source,
            destination
        )

        copied += 1

    print()
    print("=" * 60)
    print("SELESAI")
    print("=" * 60)

    print(f"Copied  : {copied}")
    print(f"Missing : {missing}")
    print(f"Output  : {OUTPUT_DIR}")


if __name__ == "__main__":
    main()