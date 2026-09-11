from pathlib import Path


# Root project
PROJECT_ROOT = Path(__file__).resolve().parent.parent


# Data
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

REFERENCE_DIR = DATA_DIR / "reference"

SEGMENTS_DIR = PROCESSED_DIR / "segments"
TRAINING_CANDIDATE_DIR = PROCESSED_DIR / "training_candidate"

METADATA_FILE = PROCESSED_DIR / "metadata.csv"
QUALITY_REPORT_FILE = PROCESSED_DIR / "quality_report.csv"
MANUAL_REVIEW_FILE = PROCESSED_DIR / "manual_review.csv"
TRAINING_MANIFEST_FILE = PROCESSED_DIR / "training_manifest.csv"


# Input / output
INPUT_DIR = PROJECT_ROOT / "input"
OUTPUT_DIR = PROJECT_ROOT / "output"


# Model
MODEL_DIR = PROJECT_ROOT / "model"
SEED_VC_DIR = MODEL_DIR / "seed-vc"


# Important audio files
YALI_REFERENCE = REFERENCE_DIR / "yali_reference.wav"
INDONESIAN_INPUT = INPUT_DIR / "indonesia_synthetic.wav"