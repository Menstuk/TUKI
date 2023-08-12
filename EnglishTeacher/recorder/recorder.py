import io
import pathlib
from datetime import datetime
from colorama import Fore
from pydub import AudioSegment
import speech_recognition as sr
from speech_recognition.exceptions import WaitTimeoutError


class Recorder:
    def __init__(self, output_path: pathlib.Path):
        self.output_path = pathlib.Path(output_path)

    def record(self, threshold=1.5, sample_rate=8000, timeout=10):
        r = sr.Recognizer()
        r.pause_threshold = threshold
        with sr.Microphone(sample_rate=sample_rate) as mic:
            r.adjust_for_ambient_noise(mic)
            print(Fore.RED + 'Recording!')
            audio = r.listen(mic, timeout=timeout)
            audio = io.BytesIO(audio.get_wav_data())
            # audio = AudioSegment.from_file(audio)
            # full_path = self.output_path / f"{self._get_datetime()}.wav"
            # audio.export(full_path.as_posix(), format='wav')
            print(Fore.RED + 'Recording Stopped')
            return audio

    def _get_datetime(self):
        return str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))

