from appurl import AppUrl
from waitdelegate import WaitDelegate


DEFAULT_WAIT_IN_SECONDS = 10


class WebApp(object):
    def __init__(self, driver, app_url):
        super(WebApp, self).__init__()
        self.driver = driver
        self.app_url = app_url

        self.wait_delegate = None
        self.default_wait = DEFAULT_WAIT_IN_SECONDS

    def go_to(self):
        self.driver.get(self.app_url.get_url())

    def wait_delegate(self, new_delegate=None):
        if new_delegate is None:
            return self.wait_delegate
        else:
            assert isinstance(new_delegate, WaitDelegate)
            self.wait_delegate = new_delegate

    def default_wait(self, wait_in_seconds=None):
        if waitInSeconds is None:
            return self.default_wait
        else:
            assert wait_in_seconds >= 0
            self.default_wait = wait_in_seconds

