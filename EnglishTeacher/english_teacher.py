import os
import sys
import pathlib
import shutil
import queue
import threading as th

from colorama import Fore, Style
from faster_whisper import WhisperModel
from language_model.language_model import LanguageModel
from grammar_check.grammar_check import GrammarChecker
from recorder.recorder import Recorder, WaitTimeoutError
from speech_to_text.speech_to_text import SpeechToText
from text_to_speech.text_to_speech import TextToSpeech
from typing import Union
from rec_while_stt import record_while_transcribing

class EnglishTeacher:
    def __init__(self, path: Union[pathlib.Path, str]):
        self.conversation = []
        if os.path.exists(path / "session"):
            shutil.rmtree(path / "session")
        os.mkdir(path / "session")
        self.mic = Recorder()
        self.llm = LanguageModel()
        self.grammar = GrammarChecker()
        self.stt = WhisperModel("medium.en", device="cpu", compute_type="int8")
        self.tts = TextToSpeech()
        self.stop_words = ['Quit.', 'Stop.', 'Exit.', 'Bye.', 'Bye-bye.']
        self.palm_queue = queue.Queue() # Thread-safe queue for palm response
        self.grammar_queue = queue.Queue() # Thread-safe queue for grammar response
        self.palm_reply_queue = queue.Queue() # Thread-safe queue for grammar response
        self.grammar_reply_queue = queue.Queue() # Thread-safe queue for grammar response
        self.terminate_queue = queue.Queue() # Thread-safe queue for terminate threads
        self.palm_thread = th.Thread(target=self.llm.get_response, args=(self.palm_queue, self.palm_reply_queue, self.terminate_queue,), name='palm_thread')


    def teach(self):
        msg = "Hello! Feel free to ask or say anything."
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "<Assistant>")
        print(Fore.LIGHTBLUE_EX + Style.NORMAL + msg)
        self.tts.read_aloud(text=msg)
        self.palm_thread.start()
        while True:
            try:
                prompt = record_while_transcribing(audio_model=self.stt)
                self.conversation.append({"type": "user", "content": prompt})
                if prompt in self.stop_words:
                    break
                if prompt == '':
                    msg = "No audio detected! Ending Conversation, Bye-bye!"
                    print(Fore.RED + Style.BRIGHT + msg)
                    self.tts.read_aloud(text=msg)
                    break
                self.palm_queue.put(prompt)

                try:
                    palm_reply = self.palm_reply_queue.get()
                    self.conversation.append({"type": "assistant", "content": palm_reply})
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "<Assistant>")
                    print(Fore.LIGHTBLUE_EX + Style.NORMAL + palm_reply)
                    self.tts.read_aloud(text=palm_reply)
                except queue.Empty:
                    pass
            except WaitTimeoutError:
                msg = "No audio detected! Ending Conversation, Bye-bye!"
                print(Fore.RED + Style.BRIGHT + msg)
                self.tts.read_aloud(text=msg)
                self.terminate_queue.put(1)
                self.palm_thread.join()
                break


if __name__ == '__main__':
    teacher = EnglishTeacher(pathlib.Path().absolute())
    teacher.teach()
    exit()
