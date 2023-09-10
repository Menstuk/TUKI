import google.generativeai as palm
import os

API_KEY = os.getenv("PALM_API_KEY")
palm.configure(api_key=API_KEY)


CONTEXT = """You are tasked with chatting with the user in a short and friendly manner. \
You respond with an informative, yet brief response. A response can not be longer than 60 words! \
Imagine it is a phone covnersation and make your anaswers accordingly. \
Every response should intrigue the user to continue the conversation."""

prompt = "Tell me about the greek island of Crete"

start_prompt = "Answer to the text in a short manner like explained in the context. Treat it like a phone \
conversation. No more than 60 words, if more, summarize it. Text: "
final_prompt = start_prompt + prompt
res = palm.chat(
    context=CONTEXT,
    messages=final_prompt,
    top_k=3,
    temperature=0.2
)
answer = res.last
print(answer)