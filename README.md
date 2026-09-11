# Yali Accent Converter

Yali Accent Converter adalah prototype sistem konversi karakter pengucapan
Bahasa Indonesia berdasarkan referensi suara Yali.

Sistem ini tidak melakukan penerjemahan Bahasa Indonesia ke Bahasa Yali.
Bahasa dan isi ucapan tetap dipertahankan dalam Bahasa Indonesia, sedangkan
karakter suara dihasilkan berdasarkan referensi suara Yali.

## Tujuan

Sistem dikembangkan sebagai prototype untuk mengeksplorasi pemanfaatan
teknologi Speech-to-Speech dan Text-to-Speech dalam menghasilkan karakter
pengucapan yang berbeda dari suara masukan.

## Alur Sistem

Input suara Bahasa Indonesia
        ↓
Speech Recognition (Whisper)
        ↓
Teks Bahasa Indonesia
        ↓
Chatterbox TTS
+ Referensi suara Yali
        ↓
Output suara dengan karakter pengucapan Yali

## Teknologi

- Python
- OpenAI Whisper
- Chatterbox TTS
- Gradio
- PyTorch
- CUDA

## Model

### Speech Recognition

Whisper digunakan untuk mengubah input suara menjadi teks Bahasa Indonesia.

### Speech Generation

Chatterbox TTS digunakan untuk menghasilkan kembali suara berdasarkan teks
hasil transkripsi dan audio referensi Yali.

Audio referensi digunakan untuk memberikan karakter gaya, prosodi, dan
karakteristik suara pada hasil keluaran.

## Dataset

Audio referensi berasal dari rekaman Bahasa Yali yang diperoleh dari
Global Recordings Network (GRN).

Dataset kemudian melalui proses:

1. Konversi audio ke format WAV.
2. Resampling audio.
3. Segmentasi audio.
4. Pemeriksaan kualitas audio.
5. Review manual.
6. Pemilihan audio yang dianggap sesuai sebagai kandidat training/reference.

## Evaluasi

Evaluasi dilakukan menggunakan dua pendekatan:

### Evaluasi Otomatis

Word Error Rate (WER) digunakan untuk melihat tingkat kesesuaian isi ucapan
antara teks referensi dan hasil konversi.

### Evaluasi Subjektif

Output dinilai berdasarkan:

- Clarity
- Karakter/style pengucapan
- Naturalness

Pada pengujian prototype terhadap lima kalimat, Chatterbox memperoleh:

| Aspek | Rata-rata |
|---|---:|
| Clarity | 4.2/5 |
| Style | 4.2/5 |
| Naturalness | 3.8/5 |

Rata-rata WER hasil konversi adalah 41.71%.

## Catatan

Sistem ini merupakan prototype dan belum ditujukan untuk menghasilkan
aksen Yali yang autentik secara linguistik.

Karakter pengucapan yang dihasilkan merupakan pendekatan berdasarkan audio
referensi yang tersedia.

## Menjalankan Sistem

Aplikasi membutuhkan environment dengan GPU yang kompatibel untuk menjalankan
model secara optimal.

Jalankan:

```bash
python app/app.py