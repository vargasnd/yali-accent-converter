# Yali Accent Converter

Prototype aplikasi konversi karakter pengucapan Bahasa Indonesia berdasarkan referensi suara Yali. Sistem ini bukan penerjemah Bahasa Indonesia ke Bahasa Yali; bahasa dan isi ucapan tetap Bahasa Indonesia, kemudian suara dihasilkan dengan karakter pengucapan yang dipengaruhi oleh referensi suara Yali.

## Instalasi & Menjalankan

Pastikan Python 3.11 dan koneksi internet tersedia.

    git clone <REPOSITORY_GITHUB>
    cd yali_accent
    python -m venv .venv

Windows:

    .venv\Scripts\activate

Install dependency:

    pip install -r requirements-local.txt

Jalankan aplikasi:

    python app.py

Kemudian buka alamat Gradio lokal yang ditampilkan, biasanya:

    http://127.0.0.1:7860

## Teknologi

Python, Gradio, OpenAI Whisper, Chatterbox TTS, PyTorch, dan Hugging Face Hub.

## Alur Sistem

    Audio Input
        ↓
      Whisper
        ↓
    Teks Bahasa Indonesia
        ↓
    Chatterbox TTS
    + Referensi Suara Yali
        ↓
    Audio Hasil Konversi

## Model

File model dan aset berukuran besar tidak disimpan di repository GitHub. Referensi suara Yali diambil otomatis dari Hugging Face:

vargasnd/yali-accent-model

Model Chatterbox Indonesian:

grandhigh/Chatterbox-TTS-Indonesian

Model Whisper juga akan diunduh otomatis saat pertama kali digunakan dan disimpan pada cache lokal.

## Catatan

NVIDIA GPU direkomendasikan untuk mempercepat inference. Aplikasi tetap dapat berjalan menggunakan CPU, tetapi proses konversi akan lebih lambat.

Hasil konversi merupakan pendekatan karakter pengucapan berdasarkan referensi suara dan bukan representasi linguistik atau fonetik resmi Bahasa Yali.

## Status

Prototype