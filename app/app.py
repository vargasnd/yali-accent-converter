import gradio as gr

from pipeline import convert_speech


def process_audio(audio):
    try:
        transcription, output_audio = convert_speech(audio)

        return transcription, output_audio

    except Exception as e:
        print("ERROR:", e)

        return (
            f"Terjadi kesalahan: {str(e)}",
            None
        )


demo = gr.Interface(
    fn=process_audio,

    inputs=gr.Audio(
        sources=["upload", "microphone"],
        type="filepath",
        label="Input Suara Bahasa Indonesia"
    ),

    outputs=[
        gr.Textbox(
            label="Hasil Transkripsi"
        ),

        gr.Audio(
            label="Hasil Konversi Yali"
        )
    ],

    title="Yali Accent Converter",

    description=(
        "Sistem konversi karakter pengucapan "
        "bahasa Indonesia berdasarkan referensi "
        "suara Yali."
    ),

    submit_btn="Convert",
    clear_btn="Clear"
)


if __name__ == "__main__":
    demo.launch()