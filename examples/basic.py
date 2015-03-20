import sys

sys.path = [".."] + sys.path

from interrogator.context import Context

context = Context.from_yaml_file(yaml_file="interrogator_basic.yaml")

context.ask_questions()
print context.answers
