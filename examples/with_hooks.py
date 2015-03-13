from datetime import datetime


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

if __name__ == "__main__":
    import sys
    sys.path = ['..'] + sys.path

    from interrogator.config import load
    from interrogator.context import Context

    context = load(config_file="interrogator_with_hooks.yaml")

    context.ask_questions()

    print context.answers
