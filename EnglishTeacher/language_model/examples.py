CHAT_EXAMPLE_RESPONSE = """My favorite movies are:

The Dark Knight
The Shawshank Redemption
The Godfather Part II
Pulp Fiction
Forrest Gump
And many more!

Movies are a great visual medium in my opinion. What are your favorite movies?
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
COMPARE_EXAMPLE_1_RESPONSE = """1. CORRECT
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

GRAMMAR_EXAMPLE_1_USER_GOOD_YOUNG = """
The sun goes down, and like, it makes the sea look all shiny and pretty. The waves were like, \
gentle on the beach, and it feels really calm, you know? People were walking on the sand, \
and you could hear their happy voices mixing with the sounds of nature.
"""
GRAMMAR_EXAMPLE_1_RESPONSE_GOOD_YOUNG = """4
"""

GRAMMAR_EXAMPLE_2_USER_GOOD_ADULT = """
So as the sun dips below the horizon, it kind of casts this warm, golden glow across the sea, \
you know what I'm saying? The waves were gently lapping against the shore, creating this sense \
of tranquility. And you had people just strolling along the beach, and their laughter, \
it mixed so nicely with the soothing sounds of nature.
"""
GRAMMAR_EXAMPLE_2_RESPONSE_GOOD_ADULT = """5"""

GRAMMAR_EXAMPLE_3_USER_MEDIUM_YOUNG = """
The sun goes down, and like, it make the sea look shiny and pretty. The waves was gentle on the beach, \
and it feel real calm, you know? People was walking on the sand, \
and you could hear their happy voices mixing with nature sounds.
"""
GRAMMAR_EXAMPLE_3_RESPONSE_MEDIUM_YOUNG = """3"""

GRAMMAR_EXAMPLE_4_USER_MEDIUM_ADULT = """
So, as the sun dips below the horizon, it kind of casted this warm, golden glow across the sea, \
you know what I'm saying? The waves was gently lapping against the shore, \
creating this sense of tranquility. And you had people just strolling along the beach, \
and their laughter, it mixed so nice with the soothing sounds of nature.
"""
GRAMMAR_EXAMPLE_4_RESPONSE_MEDIUM_ADULT = """3"""

GRAMMAR_EXAMPLE_5_USER_BAD_YOUNG = """
The sun, it go down, and, um, it make the sea, you know, look all shiny and pretty? \
The waves, they're like, gentle on the beach, and it's like, really calm and stuff. \
People, you know, they walk on the sand, and, uh, their happy voices mix with, um, nature sounds.
"""
GRAMMAR_EXAMPLE_5_RESPONSE_BAD_YOUNG = """2"""

GRAMMAR_EXAMPLE_6_USER_BAD_ADULT = """
So, like, the sun is, you know, dipping below the horizon? And it's casting this warm, golden, like, \
glow across, um, the sea? And, like, the waves are, you know, gently lapping against the shore, \
creating this, um, sense of tranquility? And, um, people are just, you know, strolling along the beach, \
and their laughter, it's, like, mixing really nicely with, um, the soothing sounds of nature.
"""
GRAMMAR_EXAMPLE_6_RESPONSE_BAD_ADULT = """1"""
