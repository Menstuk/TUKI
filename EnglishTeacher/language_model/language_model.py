import requests
from bardapi import Bard
import queue

class LanguageModel:
    def __init__(self):
        self.token = "Zwh8KgwxEwmke1uuJoNv1SwqoQqo8cvZFVxGB8hzN2t7_RIVioZftsMg8ACWoVTLQrrHtw."
        self.session = requests.Session()
        self.session.headers = {
            "Host": "bard.google.com",
            "X-Same-Domain": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.4472.114 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "https://bard.google.com",
            "Referer": "https://bard.google.com/",
        }

        self.session.cookies.set("__Secure-1PSID", self.token)
        self.session.cookies.set("__Secure-1PSIDCC", "APoG2W_E0YuGekX777Mq38TNpU6IZ7ptw7wV5Qg7sBmn_VJ_9ehZ9GF1YyE9adyo5odiJcb-ow")
        self.session.cookies.set("__Secure-1PSIDTS", "sidts-CjIBSAxbGbH51-HDLiXFRgbM-u-EEB6u9-qUHxBajb9wYGOQPIhiAunHQlmm7J5rtC9INhAA")
        self.model = Bard(token=self.token, session=self.session, timeout=30)

    def get_response(self, bard_queue, bard_reply_queue, terminate_queue):
        while terminate_queue.empty():
            try:
                prompt = bard_queue.get(block=True, timeout=1)
                answer = self.model.get_answer(prompt)["content"]
                bard_reply_queue.put(answer)
            except queue.Empty:
                pass

    def get_rephrase_response(self, bard_queue, bard_reply_queue, terminate_queue):
        while terminate_queue.empty():
            try:
                prompt = "I will provide you a sentence in this prompt, your task is to rephrase it \
                    in two ways with only one option for each way: causal and formal. The format is: \
                    Casual: (insert here the casual rephrase text) Formal: (insert here the formal rephrase text). \
                    Please don't add any additional text to your answer, only one casual and one formal \
                    alternatives. The sentence you need to rephrase is: "
                prompt += bard_queue.get(block=True, timeout=1)
                answer = self.model.get_answer(prompt)["content"]
                bard_reply_queue.put(answer)
            except queue.Empty:
                pass

    def init_teacher(self):
        starting_prompt = "In the next prompts you will have a casual conversation. You will answer in a short manner, " \
                          "no more than one sentences per answer. Please follow this instructions for the entire session until it ends."
        # starting_prompt = "In the next prompts you will have a conversation with a student to practice \
        # his speaking abilities. Adjust your answers to his English level based on his prompts. Make sure \
        # your answers are short and  make it feel more like a phone call conversation. I need you to answer \
        # in a short manner. No more than two sentences per answer. \
        # Please follow this instructions for the entire session until it ends. "

        resp = self.get_response(starting_prompt)

if __name__ == '__main__':
    lm = LanguageModel()