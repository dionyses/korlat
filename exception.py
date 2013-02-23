class AutomationException(Exception):
    def __init__(self, *args, **kwargs):
        super(AutomationException, self).__init__(*args, **kwargs)


class UnknownStrategy(AutomationException):
    pass


class CheckError(AssertionError):
    pass


class CheckEqualError(CheckError):
    def __init__(self, expected, actual, extra=""):
        self.expected = expected
        self.actual = actual
        self.extra = extra

        if len(self.extra) > 0 and not self.extra.endswith(" "):
            self.extra += " "

    def __str__(self):
        return "%sexpected <%s> - got <%s>" % (self.extra, str(self.expected), str(self.actual))


class CheckAtLeastError(CheckError):
    def __init__(self, minimum, actual, extra=""):
        self.minimum = minimum
        self.actual = actual
        self.extra = extra

        if len(self.extra) > 0 and not self.extra.endswith(" "):
            self.extra += " "

    def __str__(self):
        return "%sexpected at least <%s> - got <%s>" % (self.extra, str(self.minimum), str(self.actual))


class CheckAtMostError(CheckError):
    def __init__(self, maximum, actual, extra=""):
        self.maximum = maximum
        self.actual = actual
        self.extra = extra

        if len(self.extra) > 0 and not self.extra.endswith(" "):
            self.extra += " "

    def __str__(self):
        return "%sexpected at most <%s> - got <%s>" % (self.extra, str(self.maximum), str(self.actual))

