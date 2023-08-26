import os
import sys
import pathlib
import shutil
import queue
import threading as th
import mysql.connector

from colorama import Fore, Style
from faster_whisper import WhisperModel

from EnglishTeacher.fluency_marker.fluency_marker import FluencyMarker
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
    def __init__(self, path: Union[pathlib.Path, str], db, cursor):
        self.db = db
        self.cursor = cursor
        self.conversation = []
        if os.path.exists(path / "session"):
            shutil.rmtree(path / "session")
        os.mkdir(path / "session")
        self.mic = Recorder()
        self.llm = LanguageModel()
        self.whisper = WhisperModel("medium.en", device="cpu", compute_type="int8")
        self.stt = SpeechToText()
        self.tts = TextToSpeech()
        self.menu = Menu()
        self.signing = Signing()
        self.stop_words = ['Quit.', 'Stop.', 'Exit.', 'Bye.', 'Bye-bye.']
        self.logged_in = False
        self.user_name = "Sign in or sign up first :)"
        self.wps = []

    def menu_navigation(self):
        """
        General main_menu that handles user sign up/in and navigation in the program.
        After verifying the user, the function will proceed the interaction with him and the mode he desires
        to practice.
        """
        while True:  # Continue until user chooses to exit program
            if self.logged_in:  # Check if user already logged in and behave accordingly
                self.menu.print_main_menu_in()
                choice = input("Choose mode: ")
                index = int(choice)
                if index == 0:
                    break
                elif index == 1:
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Welcome To Learning Mode!")
                    # Start Here the learning mode (grammar correction and rephrased sentences)
                elif index == 2:
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Welcome To Test Mode!")
                    self.test_mode()
                elif index == 3:
                    # Start here the free conversation
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Welcome To Conversation Mode!")
                    self.free_conversation()
                elif index == 4:
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Signing Out...")
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Bye Bye " + self.user_name)
                    self.user_name = "Sign in or sign up first :)"
                    self.logged_in = False
                else:
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Invalid input! Please select one of the options below")

            else:  # If user still not logged in, present him two options, sign up or sign in
                self.menu.print_main_menu_out()
                choice = input("Choose option: ")
                index = int(choice)
                if index == 0:
                    break
                elif index == 1:
                    self.user_name = self.signing.sign_up(self.db, self.cursor)
                    self.logged_in = True
                elif index == 2:
                    signed_in, self.user_name = self.signing.sign_in(self.db, self.cursor)
                    self.logged_in = signed_in
                else:
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Invalid input! Please select one of the options below")

    def test_mode(self):
        fm = FluencyMarker(recorder=self.mic, speech_to_text=self.stt)
        fm.ask_questions()
        fm.get_speech()
        fm.evaluate()
        grade = fm.grade
        wps = fm.speech_rate
        self.db.insert_user_metrics(cursor=self.cursor, username=self.user_name, speech_rate=wps, correct_answers_metric=grade)

    def free_conversation(self):
        """
        Handling the flow of a free conversation between the user and bard. 
        Record the conversation in "self.conversation" for future use.
        """
        msg = self.llm.init_chat(True)
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "<Assistant>")
        print(Fore.LIGHTBLUE_EX + Style.NORMAL + msg)
        self.tts.read_aloud(text=msg)
        self.wps = []
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
                print(Fore.LIGHTBLUE_EX + Style.NORMAL + response)
                self.tts.read_aloud(text=response)
                self.wps.append(wps)
            except WaitTimeoutError:
                msg = "No audio detected! Ending Conversation, Bye-bye!"
                print(Fore.RED + Style.BRIGHT + msg)
                self.tts.read_aloud(text=msg)
                break


if __name__ == '__main__':
    # db = DB_connect.connect_db
    db = DB_connect()  # Create an instance of DB_connect
    # db = mysql.connector.connect(
    # host = 'localhost',
    # user = 'root',
    # passwd = 'password123'
    # )
    mydb = db.connect_db()
    cursor = mydb.cursor()
    db.create_database(cursor)
    db.create_users_table(cursor)

    teacher = EnglishTeacher(pathlib.Path().absolute(), mydb, cursor)
    teacher.menu_navigation()
    # teacher.teach()
    print(Fore.RED + Style.BRIGHT + "Hope you learned something new! See you next time!")
    # Close the cursor and the connection
    cursor.close()
    mydb.close()
    exit()
