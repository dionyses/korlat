class AutomationException(Exception):
    def __init__(self, *args, **kwargs):
        super(AutomationException, self).__init__(*args, **kwargs)


class UnknownStrategy(AutomationException):
    pass

