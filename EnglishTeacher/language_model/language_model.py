import os
import google.generativeai as palm
import queue

EXAMPLE_RESPONSE = """Of course! My favorite movies are:

The Dark Knight
The Shawshank Redemption
The Godfather Part II
Pulp Fiction
Forrest Gump
And many more!

Notice that the correct phrasing should be "What are your favorite movies?".
"""


class LanguageModel:
    def __init__(self):
        self.api_key = os.getenv("PALM_API_KEY")
        palm.configure(api_key=self.api_key)
        self.context = """
            You an English teacher who is tasked with chatting with the user, while fixing their grammar mistakes.
            The fixes will be given while maintaining a conversation.
            Do not contain any signs such as |,-,* in your responses.
            Punctuation is allowed, and even appreciated.
            """
        self.examples = [(
            "what u favorite movies.", EXAMPLE_RESPONSE)]
        self.palm = None

    def get_chat_response(self, palm_queue, palm_reply_queue, terminate_queue):
        while terminate_queue.empty():
            try:
                if self.palm is None:
                    res = palm.chat(
                        context=self.context,
                        messages=[{'author': '0', 'content': f"Start."}],
                        examples=self.examples
                    )
                    res.messages[1] = {'author': '1', 'content': "Hello! Feel free to ask or say anything."}
                    self.palm = res
                prompt = palm_queue.get(block=True, timeout=1)
                self.palm = self.palm.reply(prompt)
                answer = self.palm.last
                palm_reply_queue.put(answer)
            except queue.Empty:
                pass

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

