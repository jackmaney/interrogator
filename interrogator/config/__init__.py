"""
The Configuration File
======================

The questions are generated from a YAML config file and parsed by :mod:`PyYAML`. At the top-most level, the config file needs to correspond to key-value pairs, with the ``questions`` consuming most of the configuration. Two custom tags allow `PyYAML constructors <http://pyyaml.org/wiki/PyYAMLDocumentation#Constructorsrepresentersresolvers>`_ to automagically build a ``Context`` and :py:mod:`Question`\ s out of the existing YAML configuration file.

Custom Tags:
------------

- ``!Context``: This tag should be at the very top of the configuration file (anything defined above it will not be included in the global context).

- ``!Question``: Relevant sets of key-value pairs are grouped together to form questions.

YAML Map Keys For Questions:
----------------------------

- ``name``: The only required attribute. This is used as a unique identifier for the given question, so you should make it something meaningful and brief for what you want to ask.

- ``prompt``: Use this attribute to customize the text that the user sees when the question is asked.

- ``default``: The chosen answer if no input is entered (ie the user hits the enter key upon the ``prompt``).

- ``choices``: A list that limits the possible answers a user can give (essentially an ``enum``). This is a list of things, each of which is one of the following types:

  - A string (which, if chosen, is just passed along as an answer), or

  - A key whose value is another question. This denotes a follow-up question. For example, the following question has two follow-ups, one asking teenagers to get off one's lawn, and the other asking about retirement readiness.

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

from loader import load
