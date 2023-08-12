import os
import shutil

import requests
import time
from bardapi import Bard
from faster_whisper import WhisperModel
from gtts import gTTS
import logging
from io import BytesIO
import io
import pygame.mixer
import pyaudio
import wave
import pathlib
import threading as th
from datetime import datetime
from colorama import Style, Fore
# logging.basicConfig()
# logging.getLogger("faster_whisper").setLevel(logging.DEBUG)
from pydub import AudioSegment
import speech_recognition as sr
keep_going = True


def key_capture_thread():
    global keep_going
    input()
    keep_going = False


def record(output_path: pathlib.Path):

    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    frames = []

    print(Fore.RED+'Recording!')
    print(Fore.RED+'Press ENTER to stop recording', end=' ')
    th.Thread(target=key_capture_thread, args=(), name='key_capture_thread', daemon=True).start()
    while keep_going:
        data = stream.read(1024)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print(Fore.RED+'>Recording stopped')
    dt_string = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    filename = f"{dt_string}.m4a"
    full_path = output_path / filename
    sound_file = wave.open(full_path.as_posix(), "wb")
    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()

    return full_path


def record2(output_path: pathlib.Path, threshold=1.5):
    r = sr.Recognizer()
    r.pause_threshold = threshold
    with sr.Microphone(sample_rate=8000) as mic:
        r.adjust_for_ambient_noise(mic)
        print(Fore.RED + 'Recording!')
        audio = r.listen(mic, timeout=10)
        audio = io.BytesIO(audio.get_wav_data())
        audio = AudioSegment.from_file(audio)
        dt_string = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        filename = f"{dt_string}.wav"
        full_path = output_path / filename
        audio.export(full_path.as_posix(), format='wav')
        print(Fore.RED + 'Recording Stopped')
        return full_path

def stt_run(audio_name, whisper_model):
    '''
    Input: audio file path
    return: text after stt faster-whisper model
    '''
    segments, _ = whisper_model.transcribe(audio_name, beam_size=5, language='en')
    # With VAD filter and an option to control the silence length to be removed 
    # segments, _ = model.transcribe(
    #     "audio.mp3",
    #     vad_filter=True,
    #     vad_parameters=dict(min_silence_duration_ms=500),
    # )
    # for segment in segments:
    #     print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

    segments = list(segments)  # The transcription will actually run here.
    txt = ""
    for segment in segments:
        txt = txt + segment.text
    return txt

def get_bard_answer(prompt):
    '''
    Input: promt as string
    return: bard answer
    '''
    resp = bard.get_answer(prompt)['content']
    return resp

def tts_run(txt, form = 'mp3', language = 'en', speed = False):
    '''
    Input:
        txt: text to speak
        form: audio format to export
        language: desired language to speak 
        speed: True for speaking slowly
    return: text after stt faster-whisper model
    '''

    tts = gTTS(txt, lang=language, slow=speed) # request to gtts
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    pygame.mixer.music.load(mp3_fp)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


# FasterWhisper initialization
model_size = "large-v2"
whisper_model = WhisperModel(model_size, device="cpu", compute_type="int8")

# Bard initialization
# os.environ['_BARD_API_KEY'] = 'xxxxxxx'

# UPDATE TOKEN IF NEEDED!
# sahar's token = 'YAjGbfRdaqH2_VbideTcafHBuxNbWvkA3PFGNAmC2Ihz-RtqtRnLweJQxfCzgRIHUSZS-A.'
token = "Ygh8Ku1Ufjys-A7Tu09G9iDKfLuMHoAUJrrQLjaz4YARY38oAVkVsct9k5vLNm5ePrrL9w."
session = requests.Session()
session.headers = {
            "Host": "bard.google.com",
            "X-Same-Domain": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "https://bard.google.com",
            "Referer": "https://bard.google.com/",
        }

# session.cookies.set("__Secure-1PSID", os.getenv("_BARD_API_KEY")) 
session.cookies.set("__Secure-1PSID", token) 

bard = Bard(token=token, session=session, timeout=30)

# STT initialization
pygame.init()
pygame.mixer.init()

# Start program

start = time.time()

form = 'M4A'
stop_words = ['Quit.', 'Stop.', 'Exit.', 'Bye.', 'Bye-bye.']
conversation = []

# starting_prompt = "In the next prompts you will have a conversation with a student to practice \
# his speaking abilities. Adjust your answers to his English level based on his prompts. Make sure \
# your answers are short and  make it feel more like a phone call conversation. I need you to answer \
# in a short manner. No more than two sentences per answer. \
# Please follow this instructions for the entire session until it ends. "

starting_prompt = "In the next prompts you will have a casual conversation. You will answer in a short manner, " \
                  "no more than one sentences per answer. Please follow this instructions for the entire session until it ends."
print(bard.get_answer(starting_prompt)['content'])

wd = pathlib.Path("E:\GitHub\TUKI\Sandbox\Omri")
if os.path.exists(wd / "session"):
    shutil.rmtree(wd / "session")
os.mkdir(wd / "session")

while True:

    audio_name = record2(wd / "session")
    prompt = stt_run(audio_name.as_posix(), whisper_model).lstrip()
    print(Fore.CYAN+Style.BRIGHT+ "<User>")
    print(Fore.CYAN + Style.NORMAL + prompt)
    if prompt in stop_words:
        break
    resp = bard.get_answer(prompt)['content']
    # resp = get_bard_answer(prompt)
    conversation.append({"type": "user", "content": prompt})
    conversation.append({"type": "assistant", "content": resp})
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "<Assistant>")
    print(Fore.LIGHTBLUE_EX + Style.NORMAL + resp)
    tts_run(resp, form, 'en', False)
    keep_going = True


# Continued conversation without set new session (example)
# resp = bard.get_answer("repeat my last prompt")['content']
# print(resp)
#
# tts_run(resp, form, 'en', False)

print(f"\nRuntime: {time.time()-start}")