"""
Context
=======

The ``Context`` object consists of a list of questions, a method to ask the set of questions, and the recorded answers from all questions and applicable follow-up questions.

``Context`` objects are loaded from a configuration file.

The Configuration File
----------------------

The questions are generated from a YAML config file and parsed by :mod:`PyYAML`. At the top-most level, the config file needs to correspond to key-value pairs, with the ``questions`` consuming most of the configuration. The ``!Question`` tag allows `a PyYAML constructor <http://pyyaml.org/wiki/PyYAMLDocumentation#Constructorsrepresentersresolvers>`_ to automagically build :py:mod:`Question`\ s out of the existing YAML configuration file.


YAML Map Keys For Questions:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``name``: The only required attribute. This is used as a unique identifier for the given question, so you should make it something meaningful and brief for what you want to ask.

- ``prompt``: Use this attribute to customize the text that the user sees when the question is asked.

- ``default``: The chosen answer if no input is entered (ie the user hits the enter key upon the ``prompt``).

- ``choices``: A list that limits the possible answers a user can give (essentially an ``enum``). This is a list of things, each of which is one of the following types:

  - A string (which, if chosen, is just passed along as an answer), or

  - A key whose value is another question. This denotes a follow-up question. For example, the following question has two follow-ups, one asking teenagers to get off one's lawn, and the other asking about retirement readiness.

Example
~~~~~~~

    ::


            !Context
            questions:
                -
                    !Question
                    name: age_bucket
                    prompt: Which of the following describes your age?
                    choices:
                        - "13-19":
                            !Question
                            name: yawn
                            prompt: Would you please get off my lawn?!
                            choices: ["yes", "no"]
                            default: no
                        - "20-25"
                        - "26-55"
                        - "56+":
                            !Question
                            name: aarp
                            prompt: >
                                    In an sentence, what does
                                    financial security look like to you?




"""


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

    def __init__(self, questions=None):
        self.questions = questions

        if questions is None:
            raise ValueError

        for question in self.questions:
            self._clean_up_question(question)

        self.answers = {}

    @classmethod
    def from_yaml_string(cls, yaml_string):
        fields = yaml.loads(StringIO(yaml_string))
        return cls(**fields)

    @classmethod
    def from_yaml_file(cls, yaml_file="interrogator.yaml"):
        with open(yaml_file) as f:
            fields = yaml.load(f)

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

        for q in self.questions:
            q.ask()

    def update_answers(self, question):

        dpath.util.new(self.answers, question.path, question.answer)
