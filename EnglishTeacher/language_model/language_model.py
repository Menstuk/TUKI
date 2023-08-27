import os
import re

import google.generativeai as palm

from language_model.examples import *


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

def extract_grade(input_string):
    # Find the first numeric substring in the string under the assumption that there will be no more than one
    # number in LLM response
    match = re.search(r'\d+', input_string)
    if match:
        number = int(match.group())
        return number
    else:
        return False


class LanguageModel:
    def __init__(self):
        self.api_key = os.getenv("PALM_API_KEY")
        palm.configure(api_key=self.api_key)
        self.chat_context = """You are tasked with chatting with the user in a friendly manner.
        You respond with an informative, yet brief response. A response CANNOT be longer than 100 words.
        Every response should intrigue the user to continue the conversation.
        """
        self.chat_examples = [(
            "What are your favorite movies?", CHAT_EXAMPLE_RESPONSE)]
        self.palm = None
        self.grammar_palm = None
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
        self.grammar_context = """
You are now a language evaluator with a specific focus on grading grammar and verb conjugation mistakes in \
text (ignore punctuation while grading the text). Your main task is to assess the provided paragraphs and \
assign them a grade from 1 to 5 based on their grammar and verb conjugation accuracy. You should consider \
both the correctness of grammar and the appropriate usage of verb conjugations in your evaluation. The \
general instructions for the grade are: \
1 - The text has severe grammar and verb conjugation mistakes that significantly impair its clarity and coherence. \
2 - The text contains noticeable grammar and verb conjugation errors that might affect its readability and understanding. \
3 - The text has some grammar and verb conjugation issues, but they don't heavily detract from the overall meaning. \
4 - The text contains only minor grammar and verb conjugation errors that have a minimal impact on its quality. \
5 - The text demonstrates impeccable grammar and verb conjugation usage, with no or only very minor errors. \
Make sure you answer in the following format - The grade is: x. Where x is the grade you choose from 1-5 \
based on grammar and verb conjugation so x will represent the level of english as desribed by grading scale. \
Please stick to the guidelines."""
        self.grammar_examples = [(GRAMMAR_EXAMPLE_1_USER_GOOD_YOUNG, GRAMMAR_EXAMPLE_1_RESPONSE_GOOD_YOUNG),
                                 (GRAMMAR_EXAMPLE_2_USER_GOOD_ADULT, GRAMMAR_EXAMPLE_2_RESPONSE_GOOD_ADULT),
                                 (GRAMMAR_EXAMPLE_3_USER_MEDIUM_YOUNG, GRAMMAR_EXAMPLE_3_RESPONSE_MEDIUM_YOUNG),
                                 (GRAMMAR_EXAMPLE_4_USER_MEDIUM_ADULT, GRAMMAR_EXAMPLE_4_RESPONSE_MEDIUM_ADULT),
                                 (GRAMMAR_EXAMPLE_5_USER_BAD_YOUNG, GRAMMAR_EXAMPLE_5_RESPONSE_BAD_YOUNG),
                                 (GRAMMAR_EXAMPLE_6_USER_BAD_ADULT, GRAMMAR_EXAMPLE_6_RESPONSE_BAD_ADULT)]

    def init_chat(self, offer_topics: bool = True):
        if offer_topics:
            res = palm.chat(
                context=self.chat_context,
                messages=[{'author': '0', 'content': f"Start the conversation, offer 3 topics to discuss, but allow more to be raised."}],
            )
            self.palm = res
        else:
            res = palm.chat(
                context=self.chat_context,
                messages=[{'author': '0', 'content': f"Start."}],
                examples=self.chat_examples
            )
            res.messages[1] = {'author': '1', 'content': "Hello! Feel free to ask or say anything."}
            self.palm = res

        return self.palm.last

    def get_chat_response(self, prompt):
        if self.palm is None:
            self.init_chat()
        self.palm = self.palm.reply(prompt)
        answer = self.palm.last
        return answer

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

    def grade_grammar(self, prompt: str):
        """
        Grades the speech based on it's grammar and verb conjugation from 1 to 5 using the LLM.
        """
        start_prompt = "Grade the next text as I explained before in the context. Text: "
        final_prompt = start_prompt + prompt
        for i in range(5):
            res_grammar = palm.chat(
                context=self.grammar_context,
                examples=self.grammar_examples,
                messages=final_prompt
            )
            answer = res_grammar.last
            print(answer)
            grammar_grade = extract_grade(answer)
            if grammar_grade:
                return answer, grammar_grade
            else:
                print("Failed to extract a grade from LLM answer")
                print(f"Attempt number {i+1} out of {5}")
                

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