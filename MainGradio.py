import gradio as gr
from gtts import gTTS
import os
import numpy as np
import json

import MyUtils
from Txt2SpeechUtils import Txt2SpeechUtils

ttsEngine = Txt2SpeechUtils()

roles = []
models = {}


def refresh_models_bert_vits2_list():
    models_dic = MyUtils.refreshAvailableRolesList()
    models.clear()
    roles.clear()
    # Access information for all roles in BERT_VITS2
    bert_vits2_roles = models_dic.get("BERT_VITS2", {})
    for role, details in bert_vits2_roles.items():
        d_model_path = details.get("D_model", "N/A")
        print(f"{role}'s D_model path:", d_model_path)
        roles.append(role)
        models[role] = d_model_path
    return gr.Dropdown(choices=roles)


def refresh_models_bert_vits2_config_yml(selectedModelPath):
    MyUtils.updateModelSelectionInConfigYaml(selectedModelPath, models)


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
                with gr.Row():
                    dropdown_infer_model = gr.Dropdown(
                        label="选择推理模型",
                        info="默认选择预处理阶段配置的文件夹内容; 也可以自己输入路径。",
                        interactive=True,
                        allow_custom_value=True,
                    )
                    button_refresh_model_list = gr.Button("Refresh")
                    button_confirm_select_model = gr.Button("Confirm")
                text_input_prompt_cvt = gr.Textbox(label="Text prompt", lines=8)
                text_output_cvt = gr.Textbox(label="Output audio")
                audio_output_cvt = gr.Audio(label="output audio")
                button_convert = gr.Button("Convert")

    button_refresh_model_list.click(refresh_models_bert_vits2_list, inputs=[], outputs=[dropdown_infer_model])

    button_confirm_select_model.click(refresh_models_bert_vits2_config_yml, inputs=[dropdown_infer_model], outputs=[])

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

demo.launch(share=False)
# if "__main__" == __name__:
#     print("Start Gradio server...")
#     refresh_models_bert_vits2_list()
#     print("Gradio server started.")
