import io
import pathlib

from colorama import Fore
from pydub import AudioSegment
import speech_recognition as sr
from datetime import datetime

def record2(output_path: pathlib.Path, threshold = 3):
    r = sr.Recognizer()
    r.pause_threshold = threshold
    with sr.Microphone(sample_rate=8000) as mic:
        r.adjust_for_ambient_noise(mic)
        print(Fore.RED + 'Recording!')
        audio = r.listen(mic)
        audio = io.BytesIO(audio.get_wav_data())
        audio = AudioSegment.from_file(audio)
        dt_string = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        filename = f"{dt_string}.wav"
        full_path = output_path / filename
        audio.export(full_path.as_posix(), format='wav')

        return full_path
if __name__ == '__main__':

    audio_name = record2(pathlib.Path("E:\GitHub\TUKI\Sandbox\Omri"))
    print(audio_name)