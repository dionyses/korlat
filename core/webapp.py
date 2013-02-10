from urlparse import urlparse

from waitdelegate import WaitDelegate


DEFAULT_WAIT_IN_SECONDS = 10


class WebApp(object):
    def __init__(self, driver, url):
        super(WebApp, self).__init__()
        # assuming the url must start with either
        #   http
        #   https
        #   file
        assert len(urlparse(url).scheme) > 3
        self.driver = driver
        # No implicit wait as waiting is controlled at the element
        # level via "wait_until_*"
        self.driver.implicitly_wait(0)
        self.url = url

        self.wait_delegate = None
        self.default_wait = DEFAULT_WAIT_IN_SECONDS

    def go_to(self):
        self.driver.get(str(self.url))

    def set_wait_delegate(self, new_delegate=None):
        assert isinstance(new_delegate, WaitDelegate)
        self.wait_delegate = new_delegate

    def set_default_wait(self, wait_in_seconds=None):
        assert wait_in_seconds >= 0
        self.default_wait = wait_in_seconds

