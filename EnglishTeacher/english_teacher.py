import os
import sys
import pathlib
import shutil
import queue
import threading as th
import mysql.connector

from colorama import Fore, Style
from faster_whisper import WhisperModel
from language_model.language_model import LanguageModel
from grammar_check.grammar_check import GrammarChecker
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
        self.session_directory = pathlib.Path(path / "session")
        self.mic = Recorder(self.session_directory)
        # self.llm = LanguageModel()
        # self.grammar = GrammarChecker()
        self.stt = WhisperModel("medium.en", device="cpu", compute_type="int8")
        self.tts = TextToSpeech()
        self.menu = Menu()
        self.signing = Signing()
        self.stop_words = ['Quit.', 'Stop.', 'Exit.', 'Bye.', 'Bye-bye.']
        self.bard_queue = queue.Queue() # Thread-safe queue for bard response
        self.grammar_queue = queue.Queue() # Thread-safe queue for grammar response
        self.bard_reply_queue = queue.Queue() # Thread-safe queue for grammar response
        self.grammar_reply_queue = queue.Queue() # Thread-safe queue for grammar response
        self.terminate_queue = queue.Queue() # Thread-safe queue for terminate threads
        # self.bard_thread = th.Thread(target=self.llm.get_response, args=(self.bard_queue, self.bard_reply_queue, self.terminate_queue,), name='bard_thread')
        self.grammar_thread = th.Thread(target=self.grammar.grammar_response, args=(self.grammar_queue, self.grammar_reply_queue, self.terminate_queue,), name='grammar_thread')
        self.logged_in = False
        self.user_name = None

    def menu(self):
        if self.logged_in:
            while True:
                self.Menu.print_main_menu_in()
                choice = input("    Choose mode: ")
                index = int(choice)
                if index == 0:
                    return
                if index == 1:
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Welcome To Learning Mode!")
                    # Start Here the learning mode (grammar correction and rephrased sentences)
                if index == 2:
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Welcome To Test Mode!")
                    # Start here the test mode
                if index == 3:
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Starting Free Conversation!")
                    # Start here the free conversation
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Welcome To Conversation Mode!")
                    # self.free_conversation()
                else:
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Invalid input! Please select one of the options below")

        else:
            while not self.logged_in:
                self.Menu.print_main_menu_out()
                choice = input("    Choose option: ")
                index = int(choice)
                if index == 0:
                    return
                if index == 1:
                    self.user_name = self.signing.sign_up()
                    self.logged_in = True
                if index == 2:
                    signed_in, self.user_name = self.signing.sign_in()
                    self.logged_in = signed_in
                else:
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Invalid input! Please select one of the options below")

    
    def free_conversation(self):
        # Handling the flow of a free conversation between the user and bard. 
        # Record the conversation in self.conversation for future use. 
        self.llm.init_teacher()
        msg = "Hello! Feel free to ask or say anything."
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "<Assistant>")
        print(Fore.LIGHTBLUE_EX + Style.NORMAL + msg)
        self.tts.read_aloud(text=msg)
        while True:
            try:
                # audio = self.mic.record()
                # prompt = self.stt.get_transcription(audio=audio).lstrip()
                prompt = record_while_transcribing(audio_model=self.stt)
                # print(Fore.CYAN + Style.BRIGHT + "<User>")
                # print(Fore.CYAN + Style.NORMAL + prompt)
                self.conversation.append({"type": "user", "content": prompt})

                if prompt in self.stop_words:
                    break
                if prompt == '':
                    msg = "No audio detected! Ending Conversation, Bye-bye!"
                    print(Fore.RED + Style.BRIGHT + msg)
                    self.tts.read_aloud(text=msg)
                    break
                response = self.llm.get_response_simple(prompt= prompt)
                self.conversation.append({"type": "assistant", "content": response})
                print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "<Assistant>")
                print(Fore.LIGHTBLUE_EX + Style.NORMAL + response)
                self.tts.read_aloud(text=response)

            except WaitTimeoutError:
                msg = "No audio detected! Ending Conversation, Bye-bye!"
                print(Fore.RED + Style.BRIGHT + msg)
                self.tts.read_aloud(text=msg)
                break
        

    def teach(self):
        # self.llm.init_teacher()
        msg = "Hello! Feel free to ask or say anything."
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "<Assistant>")
        print(Fore.LIGHTBLUE_EX + Style.NORMAL + msg)
        self.tts.read_aloud(text=msg)
        self.grammar_thread.start()
        # self.bard_thread.start()

        while True:
            try:
                # audio = self.mic.record()
                # prompt = self.stt.get_transcription(audio=audio).lstrip()
                prompt = record_while_transcribing(audio_model=self.stt)
                # print(Fore.CYAN + Style.BRIGHT + "<User>")
                # print(Fore.CYAN + Style.NORMAL + prompt)
                self.conversation.append({"type": "user", "content": prompt})

                if prompt in self.stop_words:
                    break
                if prompt == '':
                    msg = "No audio detected! Ending Conversation, Bye-bye!"
                    print(Fore.RED + Style.BRIGHT + msg)
                    self.tts.read_aloud(text=msg)
                    break

                # response = self.llm.get_response(prompt=prompt)
                # self.conversation.append({"type": "assistant", "content": response})
                # print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "<Assistant>")
                # print(Fore.LIGHTBLUE_EX + Style.NORMAL + response)
                # self.tts.read_aloud(text=response)
                self.grammar_queue.put(prompt)
                # self.bard_queue.put(prompt)
                try:
                    grammar_reply = self.grammar_reply_queue.get(block=True, timeout=10)
                    num_mistakes, grammar_response = grammar_reply[0], grammar_reply[1]
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "<Grammar Feedback>")
                    grammar_say_aloud = None
                    if num_mistakes == 0:
                        grammar_say_aloud = "No grammar mistakes detected! Well Done!"
                        print(Fore.LIGHTBLUE_EX + Style.NORMAL + grammar_say_aloud)
                    else:
                        grammar_say_aloud = str(num_mistakes) + " grammar mistakes detected "
                        print(Fore.LIGHTBLUE_EX + Style.NORMAL + grammar_say_aloud)
                        print(Fore.LIGHTBLUE_EX + Style.NORMAL + "Grammatically correct sentence:", grammar_response)
                    self.tts.read_aloud(text=grammar_say_aloud) 
                except queue.Empty:
                    pass

                # try:
                    # bard_reply = self.bard_reply_queue.get()
                    # self.conversation.append({"type": "assistant", "content": bard_reply})
                    # print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "<Assistant>")
                    # print(Fore.LIGHTBLUE_EX + Style.NORMAL + bard_reply)
                    # self.tts.read_aloud(text=bard_reply)
                # except queue.Empty:
                    # pass
            except WaitTimeoutError:
                msg = "No audio detected! Ending Conversation, Bye-bye!"
                print(Fore.RED + Style.BRIGHT + msg)
                self.tts.read_aloud(text=msg)
                self.terminate_queue.put(1)
                self.grammar_thread.join()
                # self.bard_thread.join()
                break


if __name__ == '__main__':
    # db = DB_connect.connect_db
    db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'password123'
    )
    cursor = db.cursor()
    DB_connect.create_database(cursor)
    DB_connect.create_users_table(cursor)

    teacher = EnglishTeacher(pathlib.Path().absolute(), db, cursor)
    teacher.menu()
    # teacher.teach()
    print(Fore.RED + Style.BRIGHT + "Hope you learned something new! See you next time!")
    # Close the cursor and the connection
    cursor.close()
    db.close()
    exit()
