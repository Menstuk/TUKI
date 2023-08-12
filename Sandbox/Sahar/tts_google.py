from gtts import gTTS
from playsound import playsound
from io import BytesIO
import pygame.mixer
txt = "Hello everyone!"

# # convert wav to mp3                                                            
# sound = AudioSegment.from_mp3(src)
# sound.export(dst, format="wav")

# def speak(text, language='en'):
#     mp3_fo = BytesIO()
#     tts = gTTS(text, lang=language)
#     tts.write_to_fp(mp3_fo)
#     pygame.init()
#     pygame.mixer.init()
#     pygame.mixer.music.load(mp3_fo, 'mp3')
#     pygame.mixer.music.play()

# speak(txt)


def tts_check(txt, form = 'mp3', language = 'en', speed = False):
    tts = gTTS(txt, lang= language, slow = speed) # request to gtts
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_fp)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    # tts.save("h12.mp3")
    # sound = AudioSegment.from_mp3("h12.mp3")
    # sound.export("test.wav", format="wav")
    # if format != 'mp3': # convert to desired format
    #     sound = AudioSegment.from_mp3("hello_from_gtts.m  p3")
    #     sound.export(f"hello_from_gtts.{form}", format= form)
    # playsound("test.mp3")
form = 'mp3'
tts_check(txt, form, 'en', False)

