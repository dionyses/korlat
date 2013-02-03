import sys


class AutomationException(Exception):
    def __init__(self, *args, **kwargs):
        super(AutomationException, self).__init__(*args, **kwargs)
        self._bottom_tb = sys.exc_info()[2].tb_next

    def __str__(self):
        out = "%s\n" % super(AutomationException, self).__str__()
        t = self._bottom_tb

        while t is not None:
            out += "  File \"%s\", line %d, in %s\n" % (t.tb_frame.f_code.co_filename,
                                                        t.tb_lineno,
                                                        t.tb_frame.f_code.co_name)
            t = t.tb_next

        return out


class NonExistentElement(AutomationException):
    pass


class UnknownStrategy(AutomationException):
    pass

