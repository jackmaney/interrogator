import sys

sys.path = [".."] + sys.path

from interrogator.config import load
from interrogator.context import Context

context = load(config_file="interrogator_basic.yaml")

context.ask_questions()
print context.answers
