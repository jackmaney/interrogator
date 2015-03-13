from ..question import Question

import dpath


class Context(object):

    def __init__(self, questions=None):
        self.questions = questions

        if questions is None:
            raise ValueError

        for question in self.questions:
            self._clean_up_question(question)

        self.answers = {}

    def _clean_up_question(self, question, base_path=None):

        question.context = self
        path = question.name

        if base_path:
            path = "{}/{}".format(base_path, question.name)

        question.path = path

        for choice in question.choices:
            if choice in question.follow_ups:
                follow_up = question.follow_ups.get(choice)
                self._clean_up_question(follow_up, base_path=path)

    def ask_questions(self):

        for q in self.questions:
            q.ask()

    def update_answers(self, question):

        dpath.util.new(self.answers, question.path, question.answer)
