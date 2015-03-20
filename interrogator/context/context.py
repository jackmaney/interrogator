from ..question import Question
from StringIO import StringIO

import dpath
import yaml
import os

__all__ = ["Context"]


def _class_loader(cls):

    def result(loader, node):
        fields = loader.construct_mapping(node, deep=True)

        return cls(**fields)

    return result

yaml.add_constructor("!Question", _class_loader(Question))


class Context(object):

    """As this object is loaded from the configuration file, you should only really need to worry about one constructor: ``from_yaml_file``."""

    def __init__(self, questions=None):
        self.questions = questions

        if questions is None:
            raise ValueError

        for question in self.questions:
            self._clean_up_question(question)

        self.answers = {}

    @classmethod
    def from_yaml_file(cls, yaml_file="interrogator.yaml"):
        """
        Creates a ``Context`` class out of a YAML configuration file.

        :param str yaml_file: The file (with path, if necessary) to a YAML configuration file to be loaded.

        :returns: The corresponding ``Context``.
        """
        with open(yaml_file) as f:
            fields = yaml.load(f)

        return cls(**fields)

    @classmethod
    def from_yaml_string(cls, yaml_string):
        fields = yaml.loads(StringIO(yaml_string))
        return cls(**fields)

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
        """
        Ask each question in order. The questions are specified by the ``!Question`` tag in the config file, and the questions are asked in the order specified in said file.

        As each question is being asked, its answer is updated and stored in the ``answers`` attribute of the ``Context``.
        """

        for q in self.questions:
            q.ask()

    def update_answers(self, question):

        dpath.util.new(self.answers, question.path, question.answer)
