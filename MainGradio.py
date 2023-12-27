import gradio as gr
from gtts import gTTS
import os
import numpy as np


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
        text_input = gr.Textbox()
        text_output = gr.Textbox()
        text_button = gr.Button("Convert")
    with gr.Tab("Voice Clone"):
        with gr.Row():
            image_input = gr.Image()
            image_output = gr.Image()
        image_button = gr.Button("Clone")

    text_button.click(flip_text, inputs=text_input, outputs=text_output)
    image_button.click(flip_image, inputs=image_input, outputs=image_output)

demo.launch()
