import yaml
import os
import re
import six


from ..exception import ConfigurationError

from ..question import Question
from ..context import Context

_dotted_path_regex = re.compile("^((?:\w+\.)*\w+):((?:\w+\.)*\w+)$")

# http://stackoverflow.com/a/7227326/554546
# TODO: Make this more DRY


def _question_constructor(loader, node):
    fields = loader.construct_mapping(node, deep=True)

    return Question(**fields)

yaml.add_constructor("!Question", _question_constructor)


def _context_constructor(loader, node):
    fields = loader.construct_mapping(node, deep=True)

    return Context(**fields)

yaml.add_constructor("!Context", _context_constructor)


def load(config_file="interrogator.yaml"):
    if not os.path.exists(config_file):
        raise ConfigurationError(
            "Config file not found: {}".format(config_file))
    elif not os.path.isfile(config_file):
        raise ConfigurationError(
            "Config file is not a file: {}".format(config_file))

    with open(config_file) as f:

        config_text = f.read()

    return yaml.load(config_text)
