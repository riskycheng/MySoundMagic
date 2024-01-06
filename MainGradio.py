import gradio as gr
from gtts import gTTS
import os
import numpy as np
from Txt2SpeechUtils import Txt2SpeechUtils

ttsEngine = Txt2SpeechUtils()

def flip_text(input_text):
    return 'flip_text --> input_text'


def flip_image(image):
    return np.fliplr(image)


# Define two functions for each tab
with gr.Blocks() as demo:
    gr.Markdown(
        """
        # AI driven TTS and VC System
        Convert Text to Speech and Clone your Voice with AI.
        """)
    with gr.Tab("Text To Speech"):
        gr.Markdown(
            """
            This is a demo of a text-to-speech demo, you may train your own model with your own voice,
            with self-trained model, you can convert text to speech with your own voice.
            """)
        with gr.Tab("Train"):
            gr.Markdown(
                """
                ### Train
                Train a new model with your own voice.
                """)
            with gr.Column():
                text_input = gr.Textbox(label="Voice data path")
                text_output = gr.Textbox(label="Model save path")
                button_train = gr.Button("Train")

        # >>>>>>>> start conversion with TTS >>>>>>>>>>>>
        with gr.Tab("Convert"):
            gr.Markdown(
                """
                ### Convert
                Convert text to speech with your trained model.
                """)
            with gr.Column():
                model_input_selection_cvt = gr.Textbox(label="Model path")
                text_input_prompt_cvt = gr.Textbox(label="Text prompt", lines=8)
                text_output_cvt = gr.Textbox(label="Output audio")
                audio_output_cvt = gr.Audio(label="output audio")
                button_convert = gr.Button("Convert")

    button_convert.click(ttsEngine.tts_fn, inputs=[
        text_input_prompt_cvt,
    ], outputs=[text_output_cvt, audio_output_cvt])

    #  >>>>>>>>>>>>>>>>>>> Voice Clone fine-tuning >>>>>>>>>>>>>>>>>>>>>>>>>>>
    with gr.Tab("Voice Clone"):
        with gr.Row():
            vc_audio_input = gr.Audio(label="Input audio")
            vc_audio_output = gr.Audio(label="Output audio")
        button_vc_clone = gr.Button("Clone")

    button_vc_clone.click(flip_text, inputs=vc_audio_input, outputs=vc_audio_output)

demo.launch(share=True)
