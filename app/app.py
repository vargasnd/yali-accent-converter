import gradio as gr

from .pipeline import (
    convert_speech,
    load_models,
    DEVICE
)


print("Initializing models...")
load_models()


def process_audio(audio, progress=gr.Progress()):
    if audio is None:
        return "", None, "Silakan masukkan atau rekam suara terlebih dahulu."

    try:
        progress(0, desc="Menyiapkan audio...")
        progress(0.2, desc="Mendeteksi ucapan...")

        transcription, output_audio = convert_speech(audio)

        progress(1.0, desc="Konversi selesai.")

        return (
            transcription,
            output_audio,
            "Konversi berhasil."
        )

    except Exception as e:
        print("ERROR:", e)

        return (
            "",
            None,
            f"Terjadi kesalahan: {str(e)}"
        )


custom_css = """
body {
    font-family: Arial, sans-serif;
}

#main-title {
    text-align: center;
    font-size: 34px;
    font-weight: 700;
    margin-bottom: 5px;
}

#subtitle {
    text-align: center;
    max-width: 760px;
    margin: 0 auto 30px auto;
    font-size: 16px;
}

#convert-btn {
    min-height: 50px;
    font-size: 16px;
    font-weight: 600;
}

#status {
    text-align: center;
    margin-top: 15px;
}

.footer {
    text-align: center;
    margin-top: 30px;
    opacity: 0.7;
    font-size: 13px;
}
"""


with gr.Blocks(
    title="Yali Accent Converter",
    css=custom_css,
    theme=gr.themes.Soft()
) as demo:

    gr.Markdown(
        "# Yali Accent Converter",
        elem_id="main-title"
    )

    gr.Markdown(
        """
        Sistem konversi karakter pengucapan Bahasa Indonesia
        berdasarkan referensi suara Yali.
        
        Sistem mempertahankan **bahasa dan isi ucapan** dalam Bahasa Indonesia,
        kemudian menghasilkan suara dengan karakter pengucapan yang berbeda.
        """,
        elem_id="subtitle"
    )

    with gr.Row():

        # INPUT
        with gr.Column():
            gr.Markdown("### Input Suara")

            input_audio = gr.Audio(
                sources=["upload", "microphone"],
                type="filepath",
                label="Rekam atau Upload Suara"
            )

            convert_button = gr.Button(
                "Convert Speech",
                variant="primary",
                elem_id="convert-btn"
            )

        # OUTPUT
        with gr.Column():
            gr.Markdown("### Hasil Konversi")

            output_audio = gr.Audio(
                label="Hasil Suara",
                type="filepath"
            )

    gr.Markdown("### Hasil Transkripsi")

    transcription = gr.Textbox(
        label="Teks yang Terdeteksi",
        placeholder="Hasil transkripsi akan muncul setelah proses konversi...",
        lines=3,
        interactive=False
    )

    status = gr.Markdown(
    f"Siap digunakan. Device: `{DEVICE}`",
    elem_id="status"
)

    convert_button.click(
        fn=process_audio,
        inputs=input_audio,
        outputs=[
            transcription,
            output_audio,
            status
        ]
    )

    gr.Markdown(
        """
        Yali Accent Converter — Prototype Sistem Konversi Suara
        """,
        elem_classes="footer"
    )