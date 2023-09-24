import io
import pathlib
from datetime import datetime
from colorama import Fore
from pydub import AudioSegment
import speech_recognition as sr
from speech_recognition.exceptions import WaitTimeoutError
import json

with open(pathlib.Path().absolute().parent / "configuration.json", "r") as f:
    cfg = json.load(f)

rec_params = cfg["recorder"]


class Recorder:
    def __init__(self):
        pass

    def record(self, threshold=rec_params["threshold"], sample_rate=rec_params["sample_rate"], timeout=rec_params["timeout"]) -> pathlib.Path:
        r = sr.Recognizer()
        r.pause_threshold = threshold
        with sr.Microphone(sample_rate=sample_rate) as mic:
            r.adjust_for_ambient_noise(mic)
            print(Fore.RED + 'Recording!')
            audio = r.listen(mic, timeout=timeout)
            audio = io.BytesIO(audio.get_wav_data())
            audio = AudioSegment.from_file(audio)
            full_path = pathlib.Path().absolute().parent / "main" / "session" / f"{self._get_datetime()}.wav"
            audio.export(full_path.as_posix(), format='wav')
            print(Fore.RED + 'Recording Stopped')
            return full_path

    def _get_datetime(self):
        return str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
