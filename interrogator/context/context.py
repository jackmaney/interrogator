from ..config.loader import load as load_config
from ..question import Question

import dpath
import six


class Context(object):

    def __init__(self, config):
        self.config = config

        self._flattened_questions = []
        self.questions = self._load_questions()

        self.answers = {}

    def _load_question(self, question, base_path=None):
        name = question.get("name")
        prompt = question.get("prompt")
        default = question.get("default")
        pre_hook = question.get("pre_hook")
        post_hook = question.get("post_hook")

        path = name
        if base_path:
            path = "{}/{}".format(base_path, name)

        choices = []
        follow_ups = {}

        for choice in question.get("choices", []):
            if isinstance(choice, dict):
                key = choice.keys()[0]
                choices.append(key)
                follow_ups[key] = self._load_question(
                    choice[key], base_path=path)

                self._flattened_questions.append(follow_ups[key])
            else:
                choices.append(choice)

        q = Question(name, self, prompt=prompt, default=default,
                     choices=choices, follow_ups=follow_ups,
                     pre_hook=pre_hook, post_hook=post_hook, path=path)

        if q.name not in self._flattened_questions:
            self._flattened_questions.append(q)

        return q

    def _load_questions(self):

        return [self._load_question(q) for q in self.config.get("questions")]

    def ask_questions(self):

        for q in self.questions:
            q.ask()

    def update_answers(self, question):

        dpath.util.new(self.answers, question.path, question.answer)
