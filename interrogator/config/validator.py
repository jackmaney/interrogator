from ..exception import ValidationError

import six

__all__ = ["validate"]


def _validate_choices(choices, question, config):

    if not isinstance(choices, list):
        raise ValidationError

    for choice in choices:
        if isinstance(choice, dict):

            if len(choice.keys()) != 1:
                msg = "Question {}: choice '{}' must have only one key".format(
                    question["name"], choice)
                raise ValidationError(msg)

            key = choice.keys()[0]

            if choice[key] in [q["name"] for q in config["questions"]]:
                msg = "Question{}: choice '{}' has an existing question as a "
                msg += "follow-up question"
                msg = msg.format(question["name"], choice)
                raise ValidationError(msg)

        elif not isinstance(choice, six.string_types):
            raise ValidationError(
                "Choice '{}' not a string or dict".format(choice))


def _validate_question(question, config):

    if not isinstance(question, dict):
        raise ValidationError

    if "name" not in question:
        raise ValidationError("Missing key: 'name'")

    if "choices" in question:
        _validate_choices(question["choices"], question, config)


def validate(config):

    if not isinstance(config, dict):
        raise ValidationError("Config: expected a dict")
    if "questions" not in config:
        raise ValidationError("No questions found")
    if not isinstance(config["questions"], list):
        raise ValidationError(
            "Expected a list, got: {}".format(config["questions"]))

    # Doing separate validation of each question first, then
    # will validate that names of the global list of
    # questions are unique.
    for question in config["questions"]:
        _validate_question(question, config)

    for i, question in enumerate(config["questions"]):
        if i in [
            j for j in range(len(config["questions"]))
            if j != i and
            config["questions"][j]["name"] == question["name"]
        ]:
            raise ValidationError(
                "Duplicate question name: {}".format(question["name"]))
