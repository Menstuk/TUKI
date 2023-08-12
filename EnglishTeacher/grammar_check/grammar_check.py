import language_tool_python
import queue

class GrammarChecker:
    def __init__(self):
        self.model = language_tool_python.LanguageTool('en-US')

    def grammar_response(self, grammar_queue, grammar_reply, terminate_queue):
        while terminate_queue.empty():
            try:
                prompt = grammar_queue.get(block=True, timeout=1)
                matches = self.model.check(prompt)
                num_mistakes = len(matches)
                correct_grammar = self.model.correct(prompt)
                print(correct_grammar)
                grammar_reply.put([num_mistakes, correct_grammar])
            except queue.Empty:
                pass