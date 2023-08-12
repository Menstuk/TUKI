from langchain import PromptTemplate, LLMChain
from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import pathlib
import time

start = time.time()

template = """You are an experienced English teacher.
You receive a sentence written by a student and grade it for its grammar as either CORRECT or INCORRECT.
Your response should include the grade, and a brief explanation for giving it.
## Student's sentence:
{sentence}

##Grade and explanation:
"""


prompt = PromptTemplate(
    template=template,
    input_variables=["sentence"],
)

local_path = pathlib.Path(
    f"E:\gpt4all\models\\ggml-gpt4all-j-v1.3-groovy.bin"
).as_posix()

# Callbacks support token-wise streaming
# Verbose is required to pass to the callback manager
callbacks = [StreamingStdOutCallbackHandler()]

llm = GPT4All(model=local_path, callbacks=callbacks, verbose=False)

llm_chain = LLMChain(prompt=prompt, llm=llm)

sentence = "she looks at sky yesterday while brushed her hair"

llm_chain.run(sentence)

print(f"\nRuntime: {time.time()-start}")