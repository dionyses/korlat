class AutomationException(Exception):
    def __init__(self, *args, **kwargs):
        super(AutomationException, self).__init__(*args, **kwargs)


class NonExistentElement(AutomationException):
    pass


class UnknownStrategy(AutomationException):
    pass

class UsageError(AutomationException):
    pass

