import time

from pydub import AudioSegment

from EnglishTeacher.language_model.language_model import LanguageModel
from queue import Queue
import threading as th
import pyaudio
from EnglishTeacher.recorder.recorder import Recorder
from EnglishTeacher.speech_to_text.speech_to_text import SpeechToText


class FluencyMarker:
    def __init__(self, recorder: Recorder, speech_to_text: SpeechToText):
        self.recorder = recorder
        self.stt = speech_to_text
        self.questions = [
            "What is your age?",
            "How many siblings do you have?",
            "What does your father do for a living?",
            "What does your mother do for a living?",
            "What was your favorite class in high-school?"
        ]
        self.qna_pairs = None
        self.grade = None
        self.speech_rate = None
        self.speech = None
        self.audio_length = None

    def ask_questions(self):
        qna_pairs = []
        print("Answer the following questions in a concise manner:")
        for question in self.questions:
            answer = input(f"{question} ")
            qna_pairs.append({"question": question, "answer": answer})
        self.qna_pairs = qna_pairs

    def get_speech(self):
        print("To evaluate your fluency, you are required to speak about yourself.")
        time.sleep(5)
        print("You will be recorded and evaluated according to this recording.")
        time.sleep(5)
        print("When speaking, include all the information you provided at the beginning.")
        time.sleep(5)
        path = self.recorder.record()
        audio = AudioSegment.from_file(path)
        self.audio_length = audio.duration_seconds
        self.speech = self.stt.get_transcription(audio=path.as_posix()).lstrip()

    def evaluate(self):
        # Chuck for LLM processing of Q&As with speech
        questions_answered = 5
        num_words = len(self.speech.split(sep=' '))
        self.speech_rate = num_words / self.audio_length
        self.grade = (questions_answered / len(self.questions)) * self.speech_rate

if __name__ == '__main__':
    stt = SpeechToText()
    rec = Recorder()
    fm = FluencyMarker(recorder=rec, speech_to_text=stt)
    fm.ask_questions()
    fm.get_speech()
    fm.evaluate()
    print(f"\n{fm.speech}\n")
    print(f"You speak at a rate of {fm.speech_rate} words per second")
    print(f"Your grade is {fm.grade}")
