import gradio as gr
from gtts import gTTS
import IPython.display as ipd
import os


# Define the function to generate speech
def generate_speech(text):
    tts = gTTS(text)
    tts.save("output.mp3")
    return "output.mp3"


# Define the Gradio interface
with gr.Blocks() as demo:
    with gr.Row():
        name = gr.Textbox(label="Text")
        pitch_btn = gr.Button("Pitch")
        speed_btn = gr.Button("Speed")
        emotion_btn = gr.Button("Emotion")
        generate_btn = gr.Button("Generate")
        output = gr.Audio(sources=["microphone", "upload"])

demo.launch()
