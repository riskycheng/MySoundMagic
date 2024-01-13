import os
import logging
import re_matching

import torch
import utils
from infer import infer, latest_version, get_net_g
import gradio as gr
import webbrowser
import numpy as np
from config import updateConfig


class Txt2SpeechUtils:
    def __init__(self):
        self.hps = None
        self.device = None
        self.net_g = None

    def init(self):
        config = updateConfig()
        if config.webui_config.debug:
            logger.info("Enable DEBUG-LEVEL log")
            logging.basicConfig(level=logging.DEBUG)
        self.hps = utils.get_hparams_from_file(config.webui_config.config_path)
        version = self.hps.version if hasattr(self.hps, "version") else latest_version

        self.device = config.webui_config.device
        if self.device == "mps":
            os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

        self.net_g = get_net_g(
            model_path=config.webui_config.model, version=version, device=self.device, hps=self.hps
        )

        speaker_ids = self.hps.data.spk2id
        speakers = list(speaker_ids.keys())
        languages = ["ZH", "JP", "EN", "mix", "auto"]

    def generate_audio(self,
            slices,
            sdp_ratio,
            noise_scale,
            noise_scale_w,
            length_scale,
            speaker,
            language,
    ):
        audio_list = []
        silence = np.zeros(self.hps.data.sampling_rate // 2, dtype=np.int16)
        with torch.no_grad():
            for piece in slices:
                audio = infer(
                    piece,
                    sdp_ratio=sdp_ratio,
                    noise_scale=noise_scale,
                    noise_scale_w=noise_scale_w,
                    length_scale=length_scale,
                    sid=speaker,
                    language=language,
                    hps=self.hps,
                    net_g=self.net_g,
                    device=self.device,
                )
                audio16bit = gr.processing_utils.convert_to_16_bit_wav(audio)
                audio_list.append(audio16bit)
                audio_list.append(silence)  # 将静音添加到列表中
        return audio_list

    def tts_fn(self,
               text,
               speaker="Vo_Jay",
               sdp_ratio=0.2,
               noise_scale=0.8,
               noise_scale_w=0.6,
               length_scale=1.0,
               language="ZH"):
        audio_list = []
        if language == "mix":
            bool_valid, str_valid = re_matching.validate_text(text)
            if not bool_valid:
                return str_valid, (
                    self.hps.data.sampling_rate,
                    np.concatenate([np.zeros(self.hps.data.sampling_rate // 2)]),
                )
            result = re_matching.text_matching(text)
            for one in result:
                _speaker = one.pop()
                for lang, content in one:
                    audio_list.extend(
                        generate_audio(
                            content.split("|"),
                            sdp_ratio,
                            noise_scale,
                            noise_scale_w,
                            length_scale,
                            _speaker,
                            lang,
                        )
                    )
        elif language.lower() == "auto":
            sentences_list = split_by_language(text, target_languages=["zh", "ja", "en"])
            for sentences, lang in sentences_list:
                lang = lang.upper()
                if lang == "JA":
                    lang = "JP"
                sentences = sentence_split(sentences, max=250)
                for content in sentences:
                    audio_list.extend(
                        generate_audio(
                            content.split("|"),
                            sdp_ratio,
                            noise_scale,
                            noise_scale_w,
                            length_scale,
                            speaker,
                            lang,
                        )
                    )
        else:
            audio_list.extend(
                self.generate_audio(
                    text.split("|"),
                    sdp_ratio,
                    noise_scale,
                    noise_scale_w,
                    length_scale,
                    speaker,
                    language,
                )
            )

        audio_concat = np.concatenate(audio_list)
        return "Success", (self.hps.data.sampling_rate, audio_concat)
