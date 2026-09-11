from pathlib import Path
import subprocess
import sys

from project_config import (
    PROJECT_ROOT,
    SEED_VC_DIR,
    INDONESIAN_INPUT,
    YALI_REFERENCE,
    OUTPUT_DIR,
)


def main():
    inference_script = SEED_VC_DIR / "inference_v2.py"

    # Check required files
    required_files = {
        "Seed-VC inference script": inference_script,
        "Indonesian input": INDONESIAN_INPUT,
        "Yali reference": YALI_REFERENCE,
    }

    for name, path in required_files.items():
        if not path.exists():
            raise FileNotFoundError(
                f"{name} tidak ditemukan:\n{path}"
            )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    command = [
        sys.executable,
        str(inference_script),

        "--source",
        str(INDONESIAN_INPUT),

        "--target",
        str(YALI_REFERENCE),

        "--output",
        str(OUTPUT_DIR),

        "--diffusion-steps",
        "30",

        "--length-adjust",
        "1.0",

        "--intelligibility-cfg-rate",
        "0.7",

        "--similarity-cfg-rate",
        "0.7",

        "--top-p",
        "0.9",

        "--temperature",
        "1.0",

        "--repetition-penalty",
        "1.0",

        "--convert-style",
        "true",

        "--anonymization-only",
        "false",
    ]

    print("Running Seed-VC V2 baseline...")
    print()
    print("Source    :", INDONESIAN_INPUT)
    print("Reference :", YALI_REFERENCE)
    print("Output    :", OUTPUT_DIR)
    print()

    subprocess.run(
        command,
        cwd=SEED_VC_DIR,
        check=True,
    )


if __name__ == "__main__":
    main()