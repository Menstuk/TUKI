import google.generativeai as palm
import os

API_KEY = "AIzaSyCC0ZIUhEEd75I_NNFNbzYAfZ5Q8ENFW4M"
palm.configure(api_key=API_KEY)


CONTEXT = """
You an English teacher who is tasked with chatting with the user, while fixing their grammar mistakes.
The fixes will be given while maintaining a conversation.
"""


res = palm.chat(
    context=CONTEXT,
    messages="Hello, me omri, me will go to see movie yesterday."
)

print(res)

