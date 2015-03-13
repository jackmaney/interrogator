class InterrogatorError(Exception):

    """Base class for interrogator-specific exceptions"""


class ConfigurationError(InterrogatorError):

    """Exceptions related to configuration"""


class ValidationError(InterrogatorError):

    """Exception for validation"""
