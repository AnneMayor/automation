"""Automation Exception Module"""

class UnknownTypeException(BaseException):
    """Initialize class UnknownTypeException"""

    def __init__(self, message):
        self.message = message
