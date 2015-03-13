import sys

sys.path = [".."] + sys.path

from interrogator.config import load
from interrogator.context import Context

config = load(config_file="interrogator_basic.yaml")
context = Context(config)

print "Flattened questions:"

for q in context._flattened_questions:
    print q.name + ", " + q.path

print ""
print "---"
print ""

context.ask_questions()
print context.answers
