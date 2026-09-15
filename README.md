# Yali Accent Converter

Prototype aplikasi konversi karakter pengucapan Bahasa Indonesia dengan pendekatan **Voice & Accent Conversion** menggunakan referensi suara Yali.

Sistem ini **bukan penerjemah Bahasa Indonesia ke Bahasa Yali**. Bahasa dan isi ucapan tetap Bahasa Indonesia, sedangkan sistem berusaha mengubah karakter pengucapan suara agar memiliki karakter yang dipengaruhi oleh referensi suara Yali.

## Instalasi

Pastikan tersedia:

- Python 3.11
- Git
- FFmpeg
- Koneksi internet
- GPU NVIDIA direkomendasikan untuk mempercepat inference

Untuk instalasi, jalankan perintah berikut pada PowerShell secara berurutan:

    git clone <REPOSITORY_GITHUB>
    cd yali_accent

    python -m venv .venv
    .venv\Scripts\activate

    python -m pip install --upgrade pip

    python -m pip install torch torchaudio torchvision --index-url https://download.pytorch.org/whl/cu126

    python -m pip install -r requirements-local.txt

    python check_environment.py

Jika komputer tidak memiliki NVIDIA GPU, gunakan instalasi PyTorch CPU sebagai pengganti perintah instalasi PyTorch CUDA:

    python -m pip install torch torchaudio torchvision

FFmpeg diperlukan untuk pemrosesan audio. Pastikan FFmpeg telah terpasang dan dapat dijalankan melalui terminal:

    ffmpeg -version

Jika perintah `ffmpeg` tidak ditemukan, install FFmpeg terlebih dahulu dan tambahkan folder `bin` FFmpeg ke Windows PATH.

Setelah seluruh dependency terpasang, `check_environment.py` digunakan untuk memastikan dependency Python dan FFmpeg yang diperlukan sudah tersedia.

Jika muncul:

    ALL DEPENDENCIES ARE READY

maka environment sudah siap digunakan.

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

Pengguna tidak perlu mengunduh model secara manual.

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
- Anonymization only: tidak

Penggunaan 30 diffusion steps dipilih untuk mempertahankan kualitas hasil konversi pada prototype.

## Dependency

Dependency utama yang digunakan project antara lain:

- PyTorch
- TorchAudio
- TorchVision
- OpenAI Whisper
- Transformers
- Hugging Face Hub
- Librosa
- SoundFile
- SciPy
- SoundDevice
- Pydub
- Munch
- Einops
- Descript Audio Codec
- Accelerate
- Hydra
- OmegaConf
- PyYAML
- FunASR
- ModelScope
- Resemblyzer
- Matplotlib
- Jiwer
- Python Dotenv

PyTorch di-install secara terpisah dari `requirements-local.txt` agar versi PyTorch dapat disesuaikan dengan GPU dan CUDA pada komputer pengguna.

**TorchCodec tidak diperlukan oleh aplikasi.**

Output audio dari Seed-VC langsung digunakan setelah proses conversion selesai tanpa melakukan decode dan encode ulang menggunakan TorchCodec.

## Hardware

GPU NVIDIA direkomendasikan untuk mempercepat proses inference.

Aplikasi tetap dapat dijalankan menggunakan CPU, tetapi proses konversi dapat membutuhkan waktu yang cukup lama karena Seed-VC melakukan proses voice conversion berbasis diffusion.

Kecepatan inference juga bergantung pada spesifikasi komputer dan durasi audio input.

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
- Model saat ini belum dapat mempertahankan karakter suara female/perempuan dengan baik.

## Troubleshooting

Jika muncul error `ModuleNotFoundError`, pastikan virtual environment sudah aktif kemudian jalankan:

    .venv\Scripts\activate
    python -m pip install -r requirements-local.txt
    python check_environment.py

Jika muncul error terkait FFmpeg, cek:

    ffmpeg -version

Jika GPU tidak terdeteksi, cek:

    python -c "import torch; print(torch.cuda.is_available())"

Jika hasilnya `False`, aplikasi tetap dapat berjalan menggunakan CPU, tetapi proses inference akan lebih lambat.

Jika muncul Windows Symlink Warning seperti:

    To support symlinks on Windows, you either need to activate Developer Mode...

pesan tersebut merupakan warning dari Hugging Face cache dan bukan error yang menghentikan aplikasi. Aplikasi tetap dapat berjalan tanpa mengaktifkan Developer Mode.

## Struktur Project

    yali_accent/
    │
    ├── app/
    │   ├── __init__.py
    │   ├── app.py
    │   └── pipeline.py
    │
    ├── seed-vc/
    │   └── ...
    │
    ├── output/
    │
    ├── .gitignore
    ├── app.py
    ├── check_environment.py
    ├── requirements-local.txt
    └── README.md

Model dan checkpoint berukuran besar tidak disimpan di repository GitHub dan akan diunduh secara otomatis dari Hugging Face saat aplikasi dijalankan.

## Status

**Prototype**

Sistem dikembangkan sebagai prototype untuk menguji pendekatan konversi karakter pengucapan Bahasa Indonesia menggunakan referensi suara Yali.