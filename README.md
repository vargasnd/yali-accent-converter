# Yali Accent Conversion

Sistem speech-to-speech untuk mengubah karakteristik aksen/gaya bicara
bahasa Indonesia menjadi aksen/gaya bicara yang terinspirasi dari
bahasa Yali menggunakan teknologi Voice Conversion.

## Tujuan

Sistem ini bertujuan untuk melakukan konversi suara dari:

Input:
- Bahasa Indonesia

Target:
- Karakteristik aksen/gaya bicara Yali

Sistem tidak melakukan penerjemahan bahasa Indonesia ke bahasa Yali.

## Teknologi

- Python
- Seed-VC V2
- Librosa
- SoundFile
- Streamlit
- PyTorch
- Git

## Struktur Project

```text
yali_accent/
├── app/
├── data/
│   ├── raw/
│   ├── processed/
│   └── reference/
├── input/
├── model/
│   └── seed-vc/
├── output/
├── scripts/
└── README.md