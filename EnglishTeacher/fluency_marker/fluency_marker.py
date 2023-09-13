import json
import os
import pathlib
import random
import time
from colorama import Fore, Style
from pydub import AudioSegment
from EnglishTeacher.recorder.recorder import Recorder
from EnglishTeacher.speech_to_text.speech_to_text import SpeechToText
from EnglishTeacher.language_model.language_model import LanguageModel

with open(pathlib.Path().absolute().parent / "configuration.json", "r") as f:
    cfg = json.load(f)

fm_params = cfg["fluency_marker"]


class FluencyMarker:
    def __init__(self, recorder: Recorder, speech_to_text: SpeechToText):
        self.recorder = recorder
        self.stt = speech_to_text
        self.questions = None
        self.model_questions = None
        self.qna_pairs = None
        self.grade = None
        self.speech_rate = None
        self.speech_grade = None
        self.grammar_score = None
        self.speech = None
        self.audio_length = None
        self.llm = LanguageModel()

    def collect_questions(self, user_level: str):
        pool_path = pathlib.Path(r"E:\GitHub\TUKI\EnglishTeacher\fluency_marker") / 'question_pool'
        topics = os.listdir(pool_path)
        all_questions = []
        chosen_questions = []

        for topic in topics:
            with open(pool_path / topic, 'r') as f:
                questions_json = json.load(f)
            all_questions.append(questions_json["questions"])

        if user_level == 'low':
            topic_index = random.randint(0, (len(all_questions)-1))
            chosen_topic = all_questions[topic_index]
            while len(chosen_questions) < 5:
                question_index = random.randint(0, (len(chosen_topic)-1))
                chosen_questions.append(chosen_topic.pop(question_index))

        elif user_level == 'medium':
            while len(chosen_questions) < 5:
                topic_index = random.randint(0, (len(all_questions) - 1))
                chosen_topic = all_questions[topic_index]
                for i in range(2):
                    question_index = random.randint(0, (len(chosen_topic) - 1))
                    chosen_questions.append(chosen_topic.pop(question_index))
                all_questions.pop(topic_index)
            q_to_remove = random.randint(0, (len(chosen_questions) - 1))
            chosen_questions.pop(q_to_remove)

        elif user_level == 'high':
            while len(chosen_questions) < 5:
                topic_index = random.randint(0, (len(all_questions) - 1))
                chosen_topic = all_questions[topic_index]
                question_index = random.randint(0, (len(chosen_topic) - 1))
                chosen_questions.append(chosen_topic.pop(question_index))
                all_questions.pop(topic_index)

        self.questions = [question["display"] for question in chosen_questions]
        self.model_questions = [question["model"] for question in chosen_questions]

    def ask_questions(self):
        qna_pairs = []
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Answer the following questions in a concise manner:")
        time.sleep(3)
        for i, question in enumerate(self.questions):
            answer = input(Fore.LIGHTBLUE_EX + Style.NORMAL + f"{question} ")
            qna_pairs.append({"question": self.model_questions[i], "answer": answer})
        self.qna_pairs = qna_pairs

    def get_speech(self):
        print(Fore.LIGHTGREEN_EX + Style.NORMAL + "\nTo evaluate your fluency, you are required to speak about yourself.")
        time.sleep(5)
        print(Fore.LIGHTGREEN_EX + Style.NORMAL + "You will be recorded and evaluated according to this recording.")
        time.sleep(5)
        print(Fore.LIGHTGREEN_EX + Style.NORMAL + "When speaking, include all the information you provided at the beginning.")
        time.sleep(5)
        path = self.recorder.record()
        audio = AudioSegment.from_file(path)
        self.audio_length = audio.duration_seconds
        self.speech = self.stt.get_transcription(audio=path.as_posix()).lstrip()
        print("\n" + Fore.CYAN + Style.BRIGHT + "User Speech:")
        print(Fore.CYAN + Style.NORMAL + self.speech + "\n")

    def evaluate(self):
        model_answers = self.llm.answer_questions(text=self.speech, questions=self.questions)
        grades = self.llm.compare_answers(qna_pairs=self.qna_pairs, model_answers=model_answers)
        questions_answered = sum([1 for grade in grades if grade == "CORRECT"])
        num_words = len(self.speech.split(sep=' '))
        self.speech_rate = round(num_words / self.audio_length, 3)  # save audio length differently
        self.grade = questions_answered

        text_answer, self.grammar_score = self.llm.grade_grammar(prompt=self.speech)
        print(Fore.LIGHTYELLOW_EX + Style.NORMAL + text_answer + "\n")
        if self.speech_rate <= fm_params["1to2"]:
            self.speech_grade = 1
        elif fm_params["1to2"] < self.speech_rate <= fm_params["2to3"]:
            self.speech_grade = 2
        elif fm_params["2to3"] < self.speech_rate <= fm_params["3to4"]:
            self.speech_grade = 3
        elif fm_params["3to4"] < self.speech_rate <= fm_params["4to5"]:
            self.speech_grade = 4
        else:
            self.speech_grade = 5


if __name__ == '__main__':
    import time
    start = time.time()
    stt = SpeechToText()
    rec = Recorder()
    fm = FluencyMarker(recorder=rec, speech_to_text=stt)
    fm.collect_questions("low")
    fm.ask_questions()
    fm.get_speech()
    fm.evaluate()
    print(f"\n{fm.speech}\n")
    print(f"You speak at a rate of: {fm.speech_rate} words per second")
    print(f"Your questions grade is: {fm.grade}")
    print(f"Your grammar score is: {fm.grammar_score}")
    end = time.time()
    print(f"Time passed {end-start}")