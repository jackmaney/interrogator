"""
The ``Context`` object consists of a list of questions, a method to ask the set of questions, and the recorded answers from all questions and applicable follow-up questions.

``Context`` objects are loaded from a configuration file.

The Configuration File
----------------------

The questions are generated from a YAML config file and parsed by :mod:`PyYAML`. At the top-most level, the config file needs to correspond to key-value pairs, with the ``questions`` consuming most of the configuration. The ``!Question`` tag allows `a PyYAML constructor <http://pyyaml.org/wiki/PyYAMLDocumentation#Constructorsrepresentersresolvers>`_ to automagically build :py:mod:`Question`\ s out of the existing YAML configuration file.


YAML Map Keys For Questions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``name``: The only required attribute. This is used as a unique identifier for the given question, so you should make it something meaningful and brief for what you want to ask.

- ``prompt``: Use this attribute to customize the text that the user sees when the question is asked.

- ``default``: The chosen answer if no input is entered (ie the user hits the enter key upon the ``prompt``).

- ``choices``: A list that limits the possible answers a user can give (essentially an ``enum``). This is a list of things, each of which is one of the following types:

  - A string (which, if chosen, is just passed along as an answer), or

  - A key whose value is another question. This denotes a follow-up question. For example, the following question has two follow-ups, one asking teenagers to get off one's lawn, and the other asking about retirement readiness.

- ``pre_hook`` / ``post_hook``: These are functions specified with `dotted notation <http://mrbob.readthedocs.org/en/latest/index.html?highlight=dotted%20notation>`_ (borrowed from `mr.bob <http://mrbob.readthedocs.org/en/latest/>`_). In particular, these strings are of the form: ``module_name:function_name``. See the second example below.


Configuration File Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~

These examples can be found in the ``examples`` folder of `the repo <https://github.com/jackmaney/interrogator>`_.

``interrogator_basic.yaml``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

    ::


            questions:
                -
                    !Question
                    name: name
                    default: Jack Maney
                -
                    !Question
                    name: color
                    prompt: What is your favorite color?
                    choices:
                        - red
                        - green
                        - black:
                            !Question
                            name: black
                            prompt: Why is that?
                        - blue:
                            !Question
                            name: blue
                            prompt: Neat! me, too! Wanna get coffee?
                            choices: ["yes", "no"]
                            default: "yes"
                -
                    !Question
                    name: long-winded
                    prompt: |
                            Pardon me, dear sir!
                            Would you be interested in a monthly
                            magazine subscription?
                    choices: ["yes", "no"]
                    default: "yes"

If we build a ``Context`` from this file, and ask these questions, via

::

    from interrogator.context import Context

    context = Context.from_yaml_file(yaml_file="interrogator_basic.yaml")

    context.ask_questions()

we get the following:

* A question of ``Name? (default: Jack Maney)``

* A question of ``What is your favorite color?``

    * If the answer is ``blue``, then the user is asked out for coffee.

    * If the answer is ``black``, the user is prompted as to why (with any answer being acceptable).

    * Other acceptable choices are ``red`` or ``green``.

* A question asking you for a monthly magazine subscription (to illustrate longer prompts).

``interrogator_with_hooks.yaml``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Assuming we have a module called ``with_hooks`` that have the following functions:

::

    def pre_hook(question):

        if question.name == "lang":
            print "Now, you'll answer this the right way, won't you?..."
            print ""
        else:
            question.default = str(datetime.now())
            question.prompt += "[{}]: ".format(question.default)


    def post_hook(question):
        if question.name == "lang" and question.answer == "Python":
            print "But, of course!"
        else:
            print "Meh, fair enough."


we can use these functions as hooks in the following config file:

::

    questions:
        -
            !Question
            name: lang
            prompt: What is your favorite programming language? [Python]
            default: Python
            pre_hook: "with_hooks:pre_hook"
            post_hook: "with_hooks:post_hook"
        -
            !Question
            name: time
            prompt: OH GOD, WHAT TIME IS IT?!
            pre_hook: "with_hooks:pre_hook"


When we load this context and call the ``ask_questions`` method on it, the following happens:

* ``"Now, you'll answer this the right way, won't you?..."`` is printed, followed by a blank line.

* We're asked what our favorite programming language is, with a default of Python.

* We get the appropriate text printed out, depending on how we answered.

* We're exasperatingly asked for the current time, with a default of the current timestamp via `datetime.now()` (this demonstrates that the hooks can alter the attributes of the given question).




"""

from context import Context
