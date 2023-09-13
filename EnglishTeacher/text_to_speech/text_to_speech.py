import pathlib
import time
from io import BytesIO

import librosa
import numpy as np
import pydub.effects
from gtts import gTTS
import json
import os

from pydub import AudioSegment

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import re

with open(pathlib.Path().absolute().parent / "configuration.json", "r") as f:
    cfg = json.load(f)

tts_params = cfg["text_to_speech"]

class TextToSpeech:
    def __init__(self, slow=bool(tts_params["slow"]), language=tts_params["language"]):
        pygame.init()
        pygame.mixer.init(frequency=44100)
        self.slow = slow
        self.language = language

    def read_aloud(self, text, speed=1.2):
        text = remove_special_characters(text)
        tts = gTTS(text, lang=self.language, slow=self.slow)
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        sound = AudioSegment.from_file(mp3_fp)
        speed_sound = pydub.effects.speedup(sound, speed)
        temp = speed_sound.export()
        pygame.mixer.music.load(temp)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)


def remove_special_characters(input_string):
    pattern = r'[*\-|\\#$)<>"\'`]'  # Characters to remove: *, -, |, \, #, $, < >)
    cleaned_string = re.sub(pattern, '', input_string)
    return cleaned_string


