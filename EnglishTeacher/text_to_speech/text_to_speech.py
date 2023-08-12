from io import BytesIO
from gtts import gTTS
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


class TextToSpeech:
    def __init__(self, slow=False, language='en'):
        pygame.init()
        pygame.mixer.init()
        self.slow = slow
        self.language = language

    def read_aloud(self, text):
        tts = gTTS(text, lang=self.language, slow=self.slow)
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        pygame.mixer.music.load(mp3_fp)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

