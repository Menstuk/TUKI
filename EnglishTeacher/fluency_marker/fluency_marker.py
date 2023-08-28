import time

from pydub import AudioSegment

from recorder.recorder import Recorder
from speech_to_text.speech_to_text import SpeechToText
from language_model.language_model import LanguageModel


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
        self.model_questions = [
            "What is the speaker's age?",
            "How many siblings does the speaker have?",
            "What does the speaker's father do for a living?",
            "What does the speaker's mother do for a living?",
            "What was the speaker's favorite class in high-school?"
        ]
        self.qna_pairs = None
        self.grade = None
        self.speech_rate = None
        self.speech_grade = None
        self.grammar_score = None
        self.speech = None
        self.audio_length = None
        self.llm = LanguageModel()

    def ask_questions(self):
        qna_pairs = []
        print("Answer the following questions in a concise manner:")
        for i, question in enumerate(self.questions):
            answer = input(f"{question} ")
            qna_pairs.append({"question": self.model_questions[i], "answer": answer})
        self.qna_pairs = qna_pairs

    def get_speech(self):
        print("\nTo evaluate your fluency, you are required to speak about yourself.")
        time.sleep(5)
        print("You will be recorded and evaluated according to this recording.")
        time.sleep(5)
        print("When speaking, include all the information you provided at the beginning.")
        time.sleep(5)
        path = self.recorder.record()
        audio = AudioSegment.from_file(path)
        self.audio_length = audio.duration_seconds
        self.speech = self.stt.get_transcription(audio=path.as_posix()).lstrip()
        print("Speech of the user:")
        print(self.speech)

    def evaluate(self):
        model_answers = self.llm.answer_questions(text=self.speech, questions=self.questions)
        grades = self.llm.compare_answers(qna_pairs=self.qna_pairs, model_answers=model_answers)
        questions_answered = sum([1 for grade in grades if grade == "CORRECT"])
        num_words = len(self.speech.split(sep=' '))
        self.speech_rate = num_words / self.audio_length # save audio length differently
        self.grade = (questions_answered / len(self.questions))
        text_answer, self.grammar_score = self.llm.grade_grammar(prompt=self.speech)
        if self.speech_rate <= 1.0:
            self.speech_grade = 1
        elif 1 < self.speech_rate <= 1.5:
            self.speech_grade = 2
        elif 1.5 < self.speech_rate <= 2.0:
            self.speech_grade = 3
        elif 2 < self.speech_rate <= 2.4:
            self.speech_grade = 4
        else:
            self.speech_grade = 5


if __name__ == '__main__':
    import time
    start = time.time()
    stt = SpeechToText()
    rec = Recorder()
    fm = FluencyMarker(recorder=rec, speech_to_text=stt)
    fm.ask_questions()
    fm.get_speech()
    fm.evaluate()
    print(f"\n{fm.speech}\n")
    print(f"You speak at a rate of: {fm.speech_rate} words per second")
    print(f"Your questions grade is: {fm.grade}")
    print(f"Your grammar score is: {fm.grammar_score}")
    end = time.time()
    print(f"Time passed {end-start}")