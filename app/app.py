import gradio as gr
from pipeline import convert_speech


def process_audio(audio):
    if audio is None:
        return "", None, "Silakan masukkan atau rekam suara terlebih dahulu."

    try:
        transcription, output_audio = convert_speech(audio)

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
#title {
    text-align: center;
    margin-bottom: 5px;
}

#subtitle {
    text-align: center;
    max-width: 750px;
    margin: 0 auto 25px auto;
}

#convert-btn {
    min-height: 48px;
    font-size: 16px;
    font-weight: 600;
}

.result-box {
    min-height: 120px;
}
"""


with gr.Blocks(
    title="Yali Accent Converter",
    css=custom_css,
    theme=gr.themes.Soft()
) as demo:

    gr.Markdown(
        """
        # Yali Accent Converter
        """,
        elem_id="title"
    )

    gr.Markdown(
        """
        Sistem konversi karakter pengucapan Bahasa Indonesia
        berdasarkan referensi suara Yali.
        
        **Sistem ini bukan penerjemah Bahasa Indonesia ke Bahasa Yali.**
        Teks dan makna ucapan tetap menggunakan Bahasa Indonesia.
        """,
        elem_id="subtitle"
    )

    with gr.Row():

        with gr.Column():
            gr.Markdown("### Input Suara")

            input_audio = gr.Audio(
                sources=["upload", "microphone"],
                type="filepath",
                label="Rekam atau Upload Suara Bahasa Indonesia"
            )

            convert_button = gr.Button(
                "Convert Speech",
                variant="primary",
                elem_id="convert-btn"
            )

        with gr.Column():
            gr.Markdown("### Hasil Konversi")

            output_audio = gr.Audio(
                label="Audio dengan Karakter Pengucapan Yali",
                type="filepath"
            )

    gr.Markdown("### Hasil Transkripsi")

    transcription = gr.Textbox(
        label="Teks yang Terdeteksi",
        placeholder="Hasil transkripsi akan muncul di sini...",
        lines=3,
        interactive=False,
        elem_classes="result-box"
    )

    status = gr.Markdown(
        "Siap digunakan."
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


if __name__ == "__main__":
    demo.launch()