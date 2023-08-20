import google.generativeai as palm
import os

API_KEY = os.getenv("PALM_API_KEY")
a = palm.configure(api_key=API_KEY)


CONTEXT = """
You an English teacher who is tasked with chatting with the user, while fixing their grammar mistakes.
The fixes will be given while maintaining a conversation.
"""


res = palm.chat(
    context=CONTEXT,
    messages=[{'author': '0', 'content': f"Start."}]
)
res.messages[1] = {'author': '1', 'content': "What would you like to talk about today?"}

