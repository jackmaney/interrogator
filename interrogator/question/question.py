from ..io import get_input


class Question(object):

    def __init__(self, name, context, prompt=None, default=None,
                 choices=None, follow_ups=None,
                 pre_hook=None, post_hook=None, path=None,
                 is_follow_up=False):

        self.name = name
        self.context = context
        self.default = default
        self.path = path
        self.is_follow_up = is_follow_up

        self.choices = choices
        if choices is None:
            self.choices = []

        self.follow_ups = follow_ups
        if follow_ups is None:
            self.follow_ups = {}

        self.pre_hook = None
        self.post_hook = None

        self.answer = None

        if prompt:
            self.prompt = prompt
        else:
            self.prompt = self._get_prompt()

        if not self.prompt.endswith(" "):
            self.prompt += " "

    def _get_prompt(self):
        prompt = self.name.title()

        if self.choices:
            prompt += "\n"
            prompt += "[{}] ".format(",".join(self.choices))

        if self.default:
            prompt += "(default: {})".format(self.default)

        prompt += ": "

        return prompt

    def ask(self):

        if hasattr(self.pre_hook, "__call__"):
            self.pre_hook(self)

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

        if self.answer not in self.follow_ups:
            self.context.update_answers(self)

        if hasattr(self.post_hook, "__call__"):
            self.post_hook(self)
