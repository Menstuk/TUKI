import os
import re

import google.generativeai as palm
import queue

from EnglishTeacher.language_model.examples import *


def parse_grades_list(input_list):
    output_list = []
    for item in input_list:
        match = re.search(r'\b(CORRECT|INCORRECT)\b', item)
        if match:
            output_list.append(match.group())
        else:
            output_list.append(item)
    return output_list


def parse_numbered_list(input_string):
    lines = input_string.strip().split('\n')
    numbered_list = []

    for line in lines:
        if re.match(r'^\d+\.', line.strip()):
            item_text = re.sub(r'^\d+\.', '', line.strip()).strip()
            numbered_list.append(item_text)

    return numbered_list


class LanguageModel:
    def __init__(self):
        self.api_key = os.getenv("PALM_API_KEY")
        palm.configure(api_key=self.api_key)
        self.chat_context = """You an English teacher who is tasked with chatting with the user, while fixing their grammar mistakes.
        The fixes will be given while maintaining a conversation.
        Do not contain any signs such as |,-,* in your responses.
        Punctuation is allowed, and even appreciated.
        """
        self.chat_examples = [(
            "what u favorite movies.", CHAT_EXAMPLE_RESPONSE)]
        self.palm = None
        self.answer_context = """You are a student tasked with answering a test about an unseen text.
        You are given the full text and a set of questions.
        For each question you reply with with an answer from the information in the text.
        If the question is impossible to answer with the given information, the answer should be "NONE".
        """
        self.answer_examples = [
            (ANSWER_EXAMPLE_1_USER, ANSWER_EXAMPLE_1_RESPONSE),
            (ANSWER_EXAMPLE_2_USER, ANSWER_EXAMPLE_2_RESPONSE)
        ]
        self.compare_context = """You are a teaching assistant tasked with grading a students answers.
You are given the correct questions and answers, as well as the student's answers and you need to grade the students' answers as either CORRECT or INCORRECT.
The answers might not be worded exactly the same, but if the general idea of the answer is the same, the answer should be graded as CORRECT.
If the given student answer is "NONE" then the grade should be INCORRECT.
Your response should be a list of grades, no need for explanations."""
        self.compare_examples = [
            (COMPARE_EXAMPLE_1_USER, COMPARE_EXAMPLE_1_RESPONSE),
            (COMPARE_EXAMPLE_2_USER, COMPARE_EXAMPLE_2_RESPONSE),
            (COMPARE_EXAMPLE_3_USER, COMPARE_EXAMPLE_3_RESPONSE)
        ]

    def get_chat_response(self, palm_queue, palm_reply_queue, terminate_queue):
        while terminate_queue.empty():
            try:
                if self.palm is None:
                    res = palm.chat(
                        context=self.chat_context,
                        messages=[{'author': '0', 'content': f"Start."}],
                        examples=self.chat_examples
                    )
                    res.messages[1] = {'author': '1', 'content': "Hello! Feel free to ask or say anything."}
                    self.palm = res
                prompt = palm_queue.get(block=True, timeout=1)
                self.palm = self.palm.reply(prompt)
                answer = self.palm.last
                palm_reply_queue.put(answer)
            except queue.Empty:
                pass

    def answer_questions(self, text, questions):
        prompt = "Answer the following-\n\n"
        prompt += f"Text:\n{text}\n\n"
        prompt += "Questions:\n"
        for i, q in enumerate(questions):
            prompt += f"{i+1}. {q}\n"

        for i in range(5):
            res = palm.chat(
                context=self.answer_context,
                examples=self.answer_examples,
                messages=prompt
            )
            try:
                response = parse_numbered_list(res.last)
                return response
            except:
                print(f"Parsing response failed. Try {i+1}/5")
                continue

    def compare_answers(self, qna_pairs, model_answers):
        prompt = "Correct questions and answers:\n"
        for i, pair in enumerate(qna_pairs):
            prompt += f"{i+1}. Q: {pair['question']}\n A: {pair['answer']}\n"

        prompt += "\nStudent answers:\n"
        for i, answer in enumerate(model_answers):
            prompt += f"{i+1}. {answer}\n"

        for i in range(5):
            res = palm.chat(
                context=self.compare_context,
                examples=self.compare_examples,
                messages=prompt
            )
            try:
                response = parse_numbered_list(res.last)
                response = parse_grades_list(response)
                return response
            except:
                print(f"Parsing response failed. Try {i + 1}/5")
                continue

    def get_rephrase_response(self, palm_queue, palm_reply_queue, terminate_queue):
        while terminate_queue.empty():
            try:
                prompt = "I will provide you a sentence in this prompt, your task is to rephrase it \
                    in two ways with only one option for each way: causal and formal. The format is: \
                    Casual: (insert here the casual rephrase text) Formal: (insert here the formal rephrase text). \
                    Please don't add any additional text to your answer, only one casual and one formal \
                    alternatives. The sentence you need to rephrase is: "
                prompt += palm_queue.get(block=True, timeout=1)
                answer = self.model.get_answer(prompt)["content"]
                palm_reply_queue.put(answer)
            except queue.Empty:
                pass


if __name__ == '__main__':
    questions = [
        "What is your age?",
        "How many siblings do you have?",
        "What does your father do for a living?",
        "What does your mother do for a living?",
        "What was your favorite class in high-school?"
    ]
    qna_pairs = [
        {
            "question": "What is your age?",
            "answer": "26"
        },
        {
            "question": "How many siblings do you have?",
            "answer": "2"
        },
        {
            "question": "What does your father do for a living??",
            "answer": "teacher"
        },
        {
            "question": "What does your mother do for a living??",
            "answer": "teacher"
        },
        {
            "question": "What was your favorite class in high-school?",
            "answer": "biology"
        },
    ]

    text = "My name is Omri. I am 20 years old. I have one brother and one sister and both my parents are teachers."
    llm = LanguageModel()
    model_answers = llm.answer_questions(text=text, questions=questions)
    grades = llm.compare_answers(qna_pairs=qna_pairs, model_answers=model_answers)