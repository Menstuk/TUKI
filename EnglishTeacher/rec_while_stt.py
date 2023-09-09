import io

import speech_recognition as sr
from datetime import datetime, timedelta
from queue import Queue
from time import sleep
import json
from colorama import Fore, Style

with open("configuration.json", "r") as f:
    cfg = json.load(f)

rws_params = cfg["rec_while_stt"]

def record_while_transcribing(audio_model, wait_time=rws_params["wait_time"], sample_rate=rws_params["sample_rate"]):

    # The last time a recording was retreived from the queue.
    phrase_time = None
    # Current raw audio bytes.
    last_sample = bytes()
    # Thread safe Queue for passing data from the threaded recording callback.
    data_queue = Queue()
    # We use SpeechRecognizer to record our audio because it has a nice feauture where it can detect when speech ends.
    recorder = sr.Recognizer()
    recorder.energy_threshold = rws_params["energy_threshold"]
    # Definitely do this, dynamic energy compensation lowers the energy threshold dramtically to a point where the SpeechRecognizer never stops recording.
    recorder.dynamic_energy_threshold = False

    source = sr.Microphone(sample_rate=sample_rate)

    record_timeout = rws_params["record_timeout"]
    phrase_timeout = rws_params["phrase_timeout"]

    transcription = ['']
    audio_lengths = []
    with source:
        recorder.adjust_for_ambient_noise(source)

    def record_callback(_, audio: sr.AudioData) -> None:
        """
        Threaded callback function to recieve audio data when recordings finish.
        audio: An AudioData containing the recorded bytes.
        """
        # Grab the raw bytes and push it into the thread safe queue.
        data = audio.get_raw_data()
        data_queue.put(data)

    # Create a background thread that will pass us raw audio bytes.
    # We could do this manually but SpeechRecognizer provides a nice helper.
    recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)

    # Cue the user that we're ready to go.
    print(Fore.RED+"Recording!")
    counter = 0
    print(Fore.CYAN + Style.BRIGHT + "<User>")
    while True:
        try:
            now = datetime.utcnow()
            # Pull raw recorded audio from the queue.
            if not data_queue.empty():
                phrase_complete = False
                # If enough time has passed between recordings, consider the phrase complete.
                # Clear the current working audio buffer to start over with the new data.
                if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                    last_sample = bytes()
                    phrase_complete = True
                # This is the last time we received new audio data from the queue.
                phrase_time = now

                # Concatenate our current audio data with the latest audio data.
                while not data_queue.empty():
                    data = data_queue.get()
                    last_sample += data

                audio_data = sr.AudioData(last_sample, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
                wav_data = io.BytesIO(audio_data.get_wav_data())
                audio_lengths.append(len(last_sample)/audio_data.sample_rate/audio_data.sample_width)
                # Read the transcription.
                segments, _ = audio_model.transcribe(wav_data, beam_size=5, language='en')
                segments = list(segments)
                text = ""
                for segment in segments:
                    text = text + segment.text.lstrip().replace(".", "")

                # If we detected a pause between recordings, add a new item to our transcription.
                # Otherwise edit the existing one.
                if phrase_complete:
                    transcription.append(text)
                else:
                    transcription[-1] = text

                print(Fore.CYAN + Style.NORMAL + transcription[-1].lower(), end=' ')
                counter = 0

            else:
                sleep(1)
                counter += 1
                if counter == wait_time:
                    break
        except KeyboardInterrupt:
            break
    print(Fore.RED + '\nRecording Stopped')
    ts = " ".join(transcription)
    words = len(ts.split(sep=' '))
    length = sum(audio_lengths)
    if length == 0:
        wps = 0
    else:
        wps = words/length
    return ts, wps
