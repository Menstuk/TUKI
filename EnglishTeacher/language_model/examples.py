CHAT_EXAMPLE_RESPONSE = """Of course! My favorite movies are:

The Dark Knight
The Shawshank Redemption
The Godfather Part II
Pulp Fiction
Forrest Gump
And many more!

Notice that the correct phrasing should be "What are your favorite movies?".
"""

ANSWER_EXAMPLE_1_USER = """Answer the following-

Text:
Hey, I am Omri, I'm 26 years old living in Tel-Aviv.

Questions:
1. What is the speaker's name?
2. What is the speaker's age?
3. Where does the speaker live?"""

ANSWER_EXAMPLE_1_RESPONSE = """1. Omri.
2. 26.
3. Tel-Aviv."""

ANSWER_EXAMPLE_2_USER = """Answer the following-

Text:
Hey, I am Yael, I'm 22 years old. In my free time I like to work out and watch TV

Questions:
1. What is the speaker's name?
2. What does the speaker do for a living?
3. What are some of the speaker's hobbies?"""

ANSWER_EXAMPLE_2_RESPONSE = """1. Yael.
2. NONE
3. Working out, watching TV."""

COMPARE_EXAMPLE_1_USER = """Correct questions and answers:
1.Q: What is the speaker's name?
A:Omri
2.Q: What is the speaker's age?
A: 26
3. Q: Where does the speaker live?
A: Tel Aviv

Student answers:
1. Omri
2. 26 years old.
3. Tel Aviv-Yaffo"""
COMPARE_EXAMPLE_1_RESPONSE ="""1. CORRECT
2. CORRECT
3. CORRECT  """


COMPARE_EXAMPLE_2_USER = """Correct questions and answers:
1. Q: What is the speaker's name?
A: Omri
2. Q: What does the speaker do for a living?
A: Software Engineer
3. Q: What are some of the speaker's hobbies?
A: Working out, watching TV.

Student answers:
1. Sahar
2. Software Engineer
3. NONE"""
COMPARE_EXAMPLE_2_RESPONSE = """1. INCORRECT
2. CORRECT
3. INCORRECT"""


COMPARE_EXAMPLE_3_USER = """Correct questions and answers:
1.Q: What is the speaker's name?
A:Yam
2.Q: What is the speaker's age?
A: 24
3. Q: Where does the speaker live?
A: Yaffo

Student answers:
1. Yama
2. 20 years old.
3. Rosh Haayin"""
COMPARE_EXAMPLE_3_RESPONSE = """1. INCORRECT
2. INCORRECT
3. INCORRECT"""