# Evaluation

Evaluation dilakukan dengan membandingkan hasil speech-to-speech
conversion pada beberapa aspek.

## Evaluation Criteria

### 1. Content Intelligibility
Apakah isi bahasa Indonesia masih dapat dipahami setelah conversion?

### 2. Accent Conversion
Apakah karakteristik aksen/gaya bicara target Yali terdengar pada output?

### 3. Voice Similarity
Seberapa dekat karakteristik suara output dengan reference Yali?

### 4. Audio Quality
Apakah output memiliki:
- noise
- clipping
- distortion
- robotic artifacts
- suara patah-patah

### 5. Overall Result
Penilaian keseluruhan terhadap hasil conversion.

## Experiment

Baseline:
Indonesia synthetic audio
+
Yali reference
→ Seed-VC V2
→ Output

Fine-tuned:
Indonesia synthetic audio
+
Yali reference
→ Fine-tuned Seed-VC V2
→ Output