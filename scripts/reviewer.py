from pathlib import Path
import pandas as pd
import streamlit as st


# ============================================================
# PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SEGMENT_DIR = PROJECT_ROOT / "data" / "processed" / "segments"
REPORT = PROJECT_ROOT / "data" / "processed" / "quality_report.csv"
REVIEW_FILE = PROJECT_ROOT / "data" / "processed" / "manual_review.csv"


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="Yali Audio Reviewer",
    layout="centered"
)


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(REPORT)

# Urutkan berdasarkan score teknis
df = df.sort_values(
    "quality_score",
    ascending=False
).reset_index(drop=True)


# ============================================================
# LOAD EXISTING REVIEW
# ============================================================

if REVIEW_FILE.exists():

    review_df = pd.read_csv(
        REVIEW_FILE
    )

else:

    review_df = pd.DataFrame(
        columns=[
            "filename",
            "decision",
            "notes"
        ]
    )


reviewed_files = set(
    review_df["filename"].tolist()
)


# ============================================================
# ONLY UNREVIEWED FILES
# ============================================================

remaining = df[
    ~df["filename"].isin(reviewed_files)
].reset_index(drop=True)


# ============================================================
# HEADER
# ============================================================

st.title("Yali Audio Reviewer")

st.write(
    "Dengarkan audio Yali lalu tentukan apakah "
    "audio tersebut layak digunakan untuk training."
)

st.write(
    f"Sudah direview: **{len(reviewed_files)}** / **{len(df)}**"
)

st.progress(
    min(len(reviewed_files) / len(df), 1.0)
)


# ============================================================
# FINISHED
# ============================================================

if len(remaining) == 0:

    st.success(
        "Semua audio sudah selesai direview."
    )

    st.write(
        review_df["decision"].value_counts()
    )

    st.stop()


# ============================================================
# CURRENT AUDIO
# ============================================================

current = remaining.iloc[0]

filename = current["filename"]

audio_path = SEGMENT_DIR / filename


st.divider()

st.subheader(
    f"Audio berikutnya"
)

st.write(
    f"**{filename}**"
)

st.caption(
    f"Technical score: {current['quality_score']} | "
    f"Duration: {current['duration_sec']:.2f} detik"
)


# ============================================================
# AUDIO PLAYER
# ============================================================

if audio_path.exists():

    st.audio(
        str(audio_path),
        format="audio/wav"
    )

else:

    st.error(
        f"File tidak ditemukan: {audio_path}"
    )

    st.stop()


# ============================================================
# DECISION
# ============================================================

decision = st.radio(
    "Bagaimana kualitas audio ini?",
    [
        "GOOD",
        "BAD",
        "SKIP"
    ],
    horizontal=True
)


notes = st.text_input(
    "Catatan (opsional)",
    placeholder="Contoh: ada musik, noise, speaker lain, dll."
)


# ============================================================
# SAVE
# ============================================================

if st.button(
    "Simpan & Next",
    type="primary",
    use_container_width=True
):

    new_row = pd.DataFrame([{
        "filename": filename,
        "decision": decision,
        "notes": notes
    }])

    review_df = pd.concat(
        [
            review_df,
            new_row
        ],
        ignore_index=True
    )

    review_df.to_csv(
        REVIEW_FILE,
        index=False,
        encoding="utf-8"
    )

    st.rerun()


# ============================================================
# SUMMARY
# ============================================================

st.divider()

st.subheader("Progress")

if len(review_df) > 0:

    counts = review_df["decision"].value_counts()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "GOOD",
            counts.get("GOOD", 0)
        )

    with col2:
        st.metric(
            "BAD",
            counts.get("BAD", 0)
        )

    with col3:
        st.metric(
            "SKIP",
            counts.get("SKIP", 0)
        )