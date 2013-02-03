from functools import wraps

from selenium.common.exceptions import WebDriverException

from exception import AutomationException


def rethrow_webdriverexception(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except WebDriverException as e:
            raise AutomationException(e)
    return wrapper

