from ..io import get_input
from importlib import import_module

import yaml
import re

_dotted_path_regex = re.compile("^((?:\w+\.)*\w+):((?:\w+\.)*\w+)$")


def _function_from_hook_str(hook):

    if hook is None:
        return hook
    m = _dotted_path_regex.match(hook)
    if m:
        module, fcn_name = m.groups()
        mod = import_module(module)
        fcn = getattr(mod, fcn_name, None)

        if fcn is not None and hasattr(fcn, '__call__'):
            return fcn

    return hook


class Question(object):

    yaml_tag = u'!Question'

    def __init__(self, name, context=None, prompt=None, default=None,
                 choices=None, follow_ups=None,
                 pre_hook=None, post_hook=None, path=None):

        if choices is None:
            choices = []
        if follow_ups is None:
            follow_ups = {}

        self.name = name
        self.context = context
        self.default = default
        self.path = path

        self.pre_hook = _function_from_hook_str(pre_hook)
        self.post_hook = _function_from_hook_str(post_hook)

        self.answer = None

        _choices = []
        _follow_ups = {}

        for choice in choices:
            if isinstance(choice, dict):
                # TODO: Put some validation somewhere...
                key = choice.keys()[0]
                _follow_ups[key] = choice[key]
                _choices.append(key)
            else:
                _choices.append(choice)

        self.follow_ups = _follow_ups
        self.choices = _choices

        if prompt:
            self.prompt = prompt
        else:
            self.prompt = self._get_prompt()

        if not self.prompt.endswith(" "):
            self.prompt += " "

    def _get_prompt(self):
        prompt = self.name.title()

        if self.default:
            prompt += "(default: {})".format(self.default)

        prompt += ": "

        return prompt

    def ask(self):

        if hasattr(self.pre_hook, "__call__"):
            self.pre_hook.__call__(self)

        answer = get_input(self.prompt)

        if not answer and self.default:
            answer = self.default

        if self.choices:

            while True:

                if answer in self.choices:

                    self.answer = answer

                    if self.answer in self.follow_ups:
                        self.follow_ups.get(self.answer).ask()

                    break

                print "Unknown option: '{}'. Need one of: '{}'".format(
                    answer, ",".join(self.choices))

                answer = get_input(self.prompt)
        else:
            self.answer = answer

        if self.context and self.answer not in self.follow_ups:
            self.context.update_answers(self)

        if hasattr(self.post_hook, "__call__"):
            self.post_hook(self)

    def __repr__(self):
        return "<Question '{}'>".format(self.prompt)
