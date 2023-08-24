import os
import re

import google.generativeai as palm

API_KEY = os.getenv("PALM_API_KEY")
palm.configure(api_key=API_KEY)

CONTEXT = """
You are now a language evaluator with a specific focus on grading grammar and verb conjugation mistakes in text.\
Your main task is to assess the provided paragraphs and assign them a grade from 1 to 5 based on their grammar \
and verb conjugation accuracy. You should consider both the correctness of grammar and the appropriate usage \
of verb conjugations in your evaluation. Grading Scale: \
1: The text has severe grammar and verb conjugation mistakes that significantly impair its clarity and coherence. \
2: The text contains noticeable grammar and verb conjugation errors that affect its readability and understanding. \
3: The text has some grammar and verb conjugation issues, but they don't heavily detract from the overall meaning. \
4: The text contains only minor grammar and verb conjugation errors that have a minimal impact on its quality. \
5: The text demonstrates impeccable grammar and verb conjugation usage, with no or only very minor errors. \
Make sure your answer is only the number of the grade: 1, 2, 3, 4 or 5."""

GRAMMAR_EXAMPLE_1_USER_GOOD_YOUNG = """
The sun goes down, and like, it makes the sea look all shiny and pretty. The waves were like, \
gentle on the beach, and it feels really calm, you know? People were walking on the sand, \
and you could hear their happy voices mixing with the sounds of nature.
"""
GRAMMAR_EXAMPLE_1_RESPONSE_GOOD_YOUNG = """The grade is: 4"""

GRAMMAR_EXAMPLE_2_USER_GOOD_ADULT = """
So as the sun dips below the horizon, it kind of casts this warm, golden glow across the sea, \
you know what I'm saying? The waves were gently lapping against the shore, creating this sense \
of tranquility. And you had people just strolling along the beach, and their laughter, \
it mixed so nicely with the soothing sounds of nature.
"""
GRAMMAR_EXAMPLE_2_RESPONSE_GOOD_ADULT = """The grade is: 5"""

GRAMMAR_EXAMPLE_3_USER_MEDIUM_YOUNG = """
The sun goes down, and like, it make the sea look shiny and pretty. The waves was gentle on the beach, \
and it feel real calm, you know? People was walking on the sand, \
and you could hear their happy voices mixing with nature sounds.
"""
GRAMMAR_EXAMPLE_3_RESPONSE_MEDIUM_YOUNG = """The grade is: 3"""

GRAMMAR_EXAMPLE_4_USER_MEDIUM_ADULT = """
So, as the sun dips below the horizon, it kind of casted this warm, golden glow across the sea, \
you know what I'm saying? The waves was gently lapping against the shore, \
creating this sense of tranquility. And you had people just strolling along the beach, \
and their laughter, it mixed so nice with the soothing sounds of nature.
"""
GRAMMAR_EXAMPLE_4_RESPONSE_MEDIUM_ADULT = """The grade is: 3"""

GRAMMAR_EXAMPLE_5_USER_BAD_YOUNG = """
The sun, it go down, and, um, it make the sea, you know, look all shiny and pretty? \
The waves, they're like, gentle on the beach, and it's like, really calm and stuff. \
People, you know, they walk on the sand, and, uh, their happy voices mix with, um, nature sounds.
"""
GRAMMAR_EXAMPLE_5_RESPONSE_BAD_YOUNG = """The grade is: 2"""

GRAMMAR_EXAMPLE_6_USER_BAD_ADULT = """
So, like, the sun is, you know, dipping below the horizon? And it's casting this warm, golden, like, \
glow across, um, the sea? And, like, the waves are, you know, gently lapping against the shore, \
creating this, um, sense of tranquility? And, um, people are just, you know, strolling along the beach, \
and their laughter, it's, like, mixing really nicely with, um, the soothing sounds of nature.
"""
GRAMMAR_EXAMPLE_6_RESPONSE_BAD_ADULT = """The grade is: 1"""

grammar_examples = [(GRAMMAR_EXAMPLE_1_USER_GOOD_YOUNG, GRAMMAR_EXAMPLE_1_RESPONSE_GOOD_YOUNG),
                                 (GRAMMAR_EXAMPLE_2_USER_GOOD_ADULT, GRAMMAR_EXAMPLE_2_RESPONSE_GOOD_ADULT),
                                 (GRAMMAR_EXAMPLE_3_USER_MEDIUM_YOUNG, GRAMMAR_EXAMPLE_3_RESPONSE_MEDIUM_YOUNG),
                                 (GRAMMAR_EXAMPLE_4_USER_MEDIUM_ADULT, GRAMMAR_EXAMPLE_4_RESPONSE_MEDIUM_ADULT),
                                 (GRAMMAR_EXAMPLE_5_USER_BAD_YOUNG, GRAMMAR_EXAMPLE_5_RESPONSE_BAD_YOUNG),
                                 (GRAMMAR_EXAMPLE_6_USER_BAD_ADULT, GRAMMAR_EXAMPLE_6_RESPONSE_BAD_ADULT)]

def grade_grammar(prompt: str):
        for i in range(5):
            res = palm.chat(
                context=CONTEXT,
                examples=grammar_examples,
                messages="You are now a language evaluator with a specific focus on grading grammar and \
verb conjugation mistakes in text. Your main task is to assess the provided paragraphs and assign them a \
grade from 1 to 5 based on their grammar and verb conjugation accuracy. You should consider both the \
correctness of grammar and the appropriate usage of verb conjugations in your evaluation. Grading Scale: \
1: The text has severe grammar and verb conjugation mistakes that significantly impair its clarity and coherence. \
2: The text contains noticeable grammar and verb conjugation errors that affect its readability and understanding. \
3: The text has some grammar and verb conjugation issues, but they don't heavily detract from the overall meaning. \
4: The text contains only minor grammar and verb conjugation errors that have a minimal impact on its quality. \
5: The text demonstrates impeccable grammar and verb conjugation usage, with no or only very minor errors. \
Make sure you answer in the following format - The grade is: x. Where x is the grade you choose from 1-5 \
based on grammar and verb conjugation so x will represent the level of english as desribed by grading scale. \
We will strat from the next prompt, stick to the guidelines please."
            )
            res = res.reply(prompt)
            answer = res.last
            print(answer)
            grammar_grade = extract_number_and_convert_to_int(answer)
            if grammar_grade:
                return answer, grammar_grade
            else:
                print("Failed to extract a grade from LLM answer")

def extract_number_and_convert_to_int(input_string):
    # Find the first numeric substring in the string under the assumption that there will be no more than one
    # number in LLM response
    match = re.search(r'\d+', input_string)
    
    if match:
        number = int(match.group())
        return number
    else:
        return False

prompt = 'So, about my age, I\'m currently 28 years old. As for siblings, I\'ve got two of them. My father,\
    he\'s an engineer and works at a tech company. My mother, on the other hand, is a teacher at a local school.\
    When it comes to high school, I have to say my favorite class was definitely English literature. \
    I\'ve always enjoyed reading and analyzing different literary works.'

# res = palm.chat(
#     context=CONTEXT,
#     examples=grammar_examples,
#     messages=prompt
# )

# answer = res.last

answer, grammar_grade = grade_grammar(prompt)
print("Grammar score:")
print(grammar_grade)
# print(answer)

