from functools import wraps

from selenium.webdriver.remote.webdriver import WebDriver

from exception import UsageError


def usage(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        raise UsageError("Do not use %s.  korlat encapsulates this detail so direct access is discouraged.  If you would like to turn this error off, see the WebApp constructor.")
    return wrapper


class UsageErrorDriver(WebDriver):
    def __init__(self, driver_parent):
        super(UsageErrorDriver, self).__init__(
            command_executor=driver_parent.command_executor,
            desired_capabilities=driver_parent.desired_capabilities,
            browser_profile=None,
            proxy=None)

    @usage
    def implicitly_wait(self, time):
        pass

