from pathlib import Path

import librosa
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

SEGMENT_DIR = PROJECT_ROOT / "data" / "processed" / "segments"
OUTPUT_CSV = PROJECT_ROOT / "data" / "processed" / "quality_report.csv"


TARGET_SR = 16000


def calculate_features(path: Path):
    audio, sr = librosa.load(
        path,
        sr=TARGET_SR,
        mono=True
    )

    # RMS / loudness
    rms = librosa.feature.rms(y=audio)[0]

    mean_rms = float(np.mean(rms))

    # Convert RMS to approximate dB
    rms_db = 20 * np.log10(
        max(mean_rms, 1e-10)
    )

    # Silence ratio
    threshold = np.max(rms) * 0.1

    frame_rms = rms

    silence_ratio = float(
        np.mean(frame_rms < threshold)
    )

    # Clipping
    clipping_ratio = float(
        np.mean(np.abs(audio) >= 0.99)
    )

    # Zero crossing rate
    zcr = librosa.feature.zero_crossing_rate(
        audio
    )[0]

    mean_zcr = float(np.mean(zcr))

    return {
        "duration_sec": len(audio) / sr,
        "rms_db": rms_db,
        "silence_ratio": silence_ratio,
        "clipping_ratio": clipping_ratio,
        "zero_crossing_rate": mean_zcr,
    }


def assign_quality(row):

    score = 100

    # Terlalu banyak silence
    if row["silence_ratio"] > 0.50:
        score -= 30
    elif row["silence_ratio"] > 0.35:
        score -= 15

    # Terlalu pelan
    if row["rms_db"] < -35:
        score -= 25
    elif row["rms_db"] < -30:
        score -= 10

    # Clipping
    if row["clipping_ratio"] > 0.01:
        score -= 30
    elif row["clipping_ratio"] > 0.001:
        score -= 10

    score = max(0, score)

    if score >= 80:
        quality = "GOOD"
    elif score >= 60:
        quality = "REVIEW"
    else:
        quality = "BAD"

    return score, quality


def main():

    files = sorted(
        SEGMENT_DIR.glob("*.wav")
    )

    print("=" * 60)
    print("YALI AUDIO QUALITY CHECK")
    print("=" * 60)

    print(f"Segments found: {len(files)}")

    rows = []

    for index, path in enumerate(files, start=1):

        try:

            features = calculate_features(path)

            score, quality = assign_quality(
                features
            )

            row = {
                "filename": path.name,
                **features,
                "quality_score": score,
                "quality": quality
            }

            rows.append(row)

            print(
                f"[{index}/{len(files)}] "
                f"{path.name} → "
                f"{quality} ({score})"
            )

        except Exception as exc:

            print(
                f"[ERROR] {path.name}: {exc}"
            )

    df = pd.DataFrame(rows)

    df = df.sort_values(
        "quality_score",
        ascending=False
    )

    df.to_csv(
        OUTPUT_CSV,
        index=False,
        encoding="utf-8"
    )

    print()
    print("=" * 60)
    print("QUALITY CHECK SELESAI")
    print("=" * 60)

    print(df["quality"].value_counts())

    print()
    print(f"Report: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()