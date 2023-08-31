import os
import sys
import pathlib
import shutil
import queue
import threading as th
import mysql.connector
import numpy as np

from colorama import Fore, Style
from faster_whisper import WhisperModel

from fluency_marker.fluency_marker import FluencyMarker
from language_model.language_model import LanguageModel
from recorder.recorder import Recorder, WaitTimeoutError
from speech_to_text.speech_to_text import SpeechToText
from text_to_speech.text_to_speech import TextToSpeech
from typing import Union
from rec_while_stt import record_while_transcribing
from menu.menu_prints import Menu
from menu.sign_handler import Signing
from database.db_handler import DB_connect


class EnglishTeacher:
    def __init__(self, path: Union[pathlib.Path, str], db_handler):
        self.conversation = []
        if os.path.exists(path / "session"):
            shutil.rmtree(path / "session")
        os.mkdir(path / "session")
        self.mic = Recorder()
        self.llm = LanguageModel()
        self.whisper = WhisperModel(model_size_or_path="medium.en", device="cpu", compute_type="int8")
        self.stt = SpeechToText()
        self.tts = TextToSpeech()
        self.db_handler = db_handler
        self.db = db_handler.db
        self.cursor = db_handler.cursor
        self.menu = Menu()
        self.signing = Signing()
        self.stop_words = ['Quit.', 'Stop.', 'Exit.', 'Bye.', 'Bye-bye.']
        self.logged_in = False
        self.user_name = "Sign in or sign up first :)"
        self.user_level = None
        self.wps = []

    def valid_choice(self, choice):
        """
        Validate that the input consist of one number (int) alone for navigating in menu"""
        try:
            number = int(choice) 
            return True
        except ValueError:
            return False

    def menu_navigation(self):
        """
        General main_menu that handles user sign up/in and navigation in the program.
        After verifying the user, the function will proceed the interaction with him and the mode he desires
        to practice.
        """
        while True:  # Continue until user chooses to exit program
            if self.logged_in:  # Check if user already logged in and behave accordingly
                self.menu.print_main_menu_in()
                while True:
                    choice = input("Choose mode: ")
                    if self.valid_choice(choice):
                        break
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Please enter your choice again.")
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Make sure your choice consist of numbers alone")
                index = int(choice)
                if index == 0:
                    break
                elif index == 1:
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Welcome To Test Mode!")
                    self.test_mode()
                elif index == 2:
                    # Start here the free conversation
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Welcome To Conversation Mode!")
                    self.free_conversation()
                elif index == 3:
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Signing Out...")
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Bye Bye " + self.user_name)
                    self.user_name = "Sign in or sign up first :)"
                    self.logged_in = False
                else:
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Invalid input! \
                         Please select one of the options below")

            else:  # If user still not logged in, present him two options, sign up or sign in
                self.menu.print_main_menu_out()
                while True:
                    choice = input("Choose mode: ")
                    if self.valid_choice(choice):
                        break
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Please enter your choice again.")
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Make sure your choice consist of numbers alone")
                index = int(choice) 
                if index == 0:
                    break
                elif index == 1:
                    self.user_name = self.signing.sign_up(self.db, self.cursor)
                    self.logged_in = True
                elif index == 2:
                    self.logged_in, self.user_name, self.user_level = self.signing.sign_in(self.db, self.cursor)
                    print(f"Right now your English level is {self.user_level}")
                else:
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Invalid input! \
                          Please select one of the options below")

    def test_mode(self):
        fm = FluencyMarker(recorder=self.mic, speech_to_text=self.stt)
        fm.ask_questions()
        fm.get_speech()
        fm.evaluate()
        grade = fm.grade
        wps = fm.speech_rate
        speech_rate_score = fm.speech_grade
        grammar_score = fm.grammar_score
        self.db_handler.insert_user_stats(
            cursor=self.cursor,
            username=self.user_name,
            speech_rate=wps,
            speech_rate_score=speech_rate_score,
            questions_score=grade,
            grammar_score=grammar_score,
        )

    def free_conversation(self):
        """
        Handling the flow of a free conversation between the user and bard. 
        Record the conversation in "self.conversation" for future use.
        """
        msg = self.llm.init_chat(True)
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "<Assistant>")
        print(Fore.LIGHTBLUE_EX + Style.NORMAL + msg)
        self.tts.read_aloud(text=msg)
        while True:
            try:
                prompt, wps = record_while_transcribing(audio_model=self.whisper)
                self.conversation.append({"type": "user", "content": prompt})
                if prompt in self.stop_words:
                    break
                if prompt == '':
                    msg = "No audio detected! Ending Conversation, Bye-bye!"
                    print(Fore.RED + Style.BRIGHT + msg)
                    self.tts.read_aloud(text=msg)
                    break
                response = self.llm.get_chat_response(prompt=prompt)
                self.conversation.append({"type": "assistant", "content": response})
                print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "<Assistant>")
                print(Fore.LIGHTBLUE_EX + Style.NORMAL + str(response))
                self.tts.read_aloud(text=response)
                if wps != 0:
                    self.wps.append(wps)
            except WaitTimeoutError:
                msg = "No audio detected! Ending Conversation, Bye-bye!"
                print(Fore.RED + Style.BRIGHT + msg)
                self.tts.read_aloud(text=msg)
                break
        if len(self.wps) > 0:
            print(Fore.GREEN + Style.DIM + f"This conversation's average speech rate was {sum(self.wps) / len(self.wps)} WPS\n")
        else:
            print(Fore.GREEN + Style.DIM + f"This conversation's average speech rate was 0 WPS\n")

if __name__ == '__main__':
    db_obj = DB_connect()  # Create an instance of DB_connect
    # db_obj.drop_database(cursor=db_obj.cursor, database_name="EnglishTeacher")
    db_obj.create_database(cursor=db_obj.cursor)
    db_obj.create_all_tables(cursor=db_obj.cursor)

    teacher = EnglishTeacher(pathlib.Path().absolute(), db_obj)

    teacher.menu_navigation()

    print(Fore.RED + Style.BRIGHT + "Hope you learned something new! See you next time!")

    db_obj.cursor.close()
    db_obj.db.close()
    exit()
