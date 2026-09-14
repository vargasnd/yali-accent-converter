# Yali Accent Converter

Prototype aplikasi konversi karakter pengucapan Bahasa Indonesia dengan pendekatan **Voice & Accent Conversion** menggunakan referensi suara Yali.

Sistem ini **bukan penerjemah Bahasa Indonesia ke Bahasa Yali**. Bahasa dan isi ucapan tetap Bahasa Indonesia, sedangkan sistem berusaha mengubah karakter pengucapan suara agar memiliki karakter yang dipengaruhi oleh referensi suara Yali.

## Instalasi

Pastikan tersedia:

- Python 3.11
- Git
- Koneksi internet

Clone repository:

    git clone <REPOSITORY_GITHUB>
    cd yali_accent

Buat virtual environment:

    python -m venv .venv

Aktifkan virtual environment pada Windows:

    .venv\Scripts\activate

Install dependency:

    pip install -r requirements-local.txt

## Menjalankan Aplikasi

Jalankan:

    python app.py

Setelah aplikasi berjalan, buka alamat Gradio yang ditampilkan pada terminal, biasanya:

    http://127.0.0.1:7860

## Alur Sistem

    Audio Bahasa Indonesia
            |
            v
       OpenAI Whisper
            |
            v
    Transkripsi Bahasa Indonesia
            |
            v
       Seed-VC V2
            |
            +---- Referensi Suara Yali
            |
            +---- Model CFM yang telah di-fine-tune
            |
            v
    Audio dengan Karakter Pengucapan Yali

## Teknologi

- Python
- Gradio
- OpenAI Whisper
- Seed-VC V2
- PyTorch
- Hugging Face Hub

## Model dan Aset

File model berukuran besar tidak disimpan di repository GitHub.

Model dan referensi suara akan diunduh secara otomatis dari Hugging Face:

    vargasnd/yali-accent-model

Repository model tersebut digunakan untuk menyediakan:

- Model CFM hasil fine-tuning
- Referensi suara Yali

Model Whisper juga akan diunduh secara otomatis saat pertama kali digunakan dan disimpan pada cache lokal.

## Seed-VC

Project ini menggunakan **Seed-VC V2** sebagai dasar sistem Voice & Accent Conversion.

Source code Seed-VC disertakan di dalam repository agar aplikasi dapat dijalankan secara lokal tanpa perlu melakukan instalasi repository Seed-VC secara terpisah.

Beberapa bagian source code Seed-VC telah disesuaikan agar kompatibel dengan environment yang digunakan pada prototype ini.

## Inference

Konversi menggunakan konfigurasi utama berikut:

- Diffusion steps: 30
- Length adjustment: 1.0
- Intelligibility CFG: 1.0
- Similarity CFG: 0.7
- Top-p: 0.9
- Temperature: 1.0
- Repetition penalty: 1.0
- Convert style: aktif

Penggunaan 30 diffusion steps dipilih untuk mempertahankan kualitas hasil konversi pada prototype.

## Hardware

GPU NVIDIA direkomendasikan untuk mempercepat proses inference.

Aplikasi tetap dapat dijalankan menggunakan CPU, tetapi proses konversi dapat membutuhkan waktu yang cukup lama karena Seed-VC melakukan proses voice conversion berbasis diffusion.

## Dataset

Model CFM dikembangkan menggunakan data referensi suara Yali yang telah melalui proses seleksi dan preprocessing.

Dataset yang digunakan pada tahap fine-tuning terdiri dari 43 segmen audio dengan total durasi sekitar 10 menit.

Data tersebut digunakan untuk eksperimen prototype dan bukan sebagai representasi lengkap dari keseluruhan bahasa atau dialek Yali.

## Batasan Sistem

Prototype ini memiliki beberapa keterbatasan:

- Hasil konversi belum dapat dianggap sebagai representasi autentik atau standar fonetik Bahasa Yali.
- Karakter pengucapan dipengaruhi oleh kualitas dan karakteristik data referensi yang tersedia.
- Kualitas output dapat berbeda tergantung pada input audio.
- Inference pada CPU membutuhkan waktu yang cukup lama.
- Model masih merupakan hasil eksperimen prototype dan belum ditujukan untuk penggunaan produksi.

## Status

**Prototype**

Sistem dikembangkan sebagai prototype untuk menguji pendekatan konversi karakter pengucapan Bahasa Indonesia menggunakan referensi suara Yali.