from bardapi import Bard
import time

start = time.time()

token = 'YAjGbfRdaqH2_VbideTcafHBuxNbWvkA3PFGNAmC2Ihz-RtqtRnLweJQxfCzgRIHUSZS-A.'
bard = Bard(token=token, timeout=30)
# prompt = "You are an experienced English teacher. \
# You receive a sentence written by a student and grade it for its grammar as either CORRECT or INCORRECT.\
# Your response should include if correct or incorrect, the grade (perfect for no mistakes, high for \
# minor mistake and low if many mistakes) is in the scale of 0-1 ,and a brief explanation for giving \
# this grade. Student's sentence: she looks at sky yesterday while brushed her hair."
resp = bard.get_answer('Hi')['content']
print(resp)

print(f"\nRuntime: {time.time()-start}")

