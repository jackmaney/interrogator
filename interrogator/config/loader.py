import yaml
import os
import re
import six


from ..exception import ConfigurationError

from ..question import Question
from ..context import Context

_dotted_path_regex = re.compile("^((?:\w+\.)*\w+):((?:\w+\.)*\w+)$")

# http://stackoverflow.com/a/7227326/554546

def _class_loader(cls):

    def result(loader, node):
        fields = loader.construct_mapping(node, deep=True)

        return cls(**fields)

    return result

yaml.add_constructor("!Question", _class_loader(Question))
yaml.add_constructor("!Context", _class_loader(Context))


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
