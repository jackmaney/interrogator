import commentjson
import os
import re
import six
from importlib import import_module

from ..exception import ConfigurationError
from .validator import validate

_dotted_path_regex = re.compile("^((?:\w+\.)*\w+):((?:\w+\.)*\w+)$")


def _get_functions(option):

    if isinstance(option, six.string_types):
        m = _dotted_path_regex.match(option)
        if m:
            module, fcn_name = m.groups()
            mod = import_module(module)
            fcn = getattr(mod, fcn_name, None)

            if fcn is not None and hasattr(fcn, '__call__'):
                return fcn

    if isinstance(option, (list, tuple)):
        return [_get_functions(x) for x in option]
    if isinstance(option, dict):
        return {x: _get_functions(option[x]) for x in option}

    return option


def load(config_file="interrogator.json"):
    if not os.path.exists(config_file):
        raise ConfigurationError(
            "Config file not found: {}".format(config_file))
    elif not os.path.isfile(config_file):
        raise ConfigurationError(
            "Config file is not a file: {}".format(config_file))

    with open(config_file) as f:

        options = commentjson.load(f)

        for key, option in options.items():
            options[key] = _get_functions(option)

        validate(options)

    return options
