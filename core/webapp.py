from time import sleep
from urlparse import urlparse

from waitdelegate import WaitDelegate


DEFAULT_WAIT_IN_SECONDS = 10
MAIN_WINDOW = "main_window"


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
        assert len(self.driver.window_handles) == 1
        self._windows = {MAIN_WINDOW: self.driver.window_handles[0]}
        self._current_window = None

        self.wait_delegate = None
        self.default_wait = DEFAULT_WAIT_IN_SECONDS

    def _destroy_windows(self):
        while len(self.driver.window_handles) > 1:
            self.driver.switch_to_window(self.driver.window_handles[-1])
            self.driver.close()

        self._windows = {}
        self.put_window(MAIN_WINDOW, self.driver.window_handles[0])

    def go_to(self):
        self._destroy_windows()
        self.use_window(MAIN_WINDOW)

        pre_handles = set(self.driver.window_handles)
        self.driver.get(str(self.url))
        post_handles = set(self.driver.window_handles)
        assert len(pre_handles) == len(post_handles)
        return self

    def put_window(self, key, handle):
        self._windows[key] = handle
        return self

    def use_window(self, key):
        self.driver.switch_to_window(self._windows[key])
        self._current_window = key
        return self

    def get_windows(self):
        return self._windows.keys()

    def next_window_key(self):
        current_keys = self.get_windows()
        n = 1

        while str(n) in current_keys:
            n += 1

        return str(n)

    def set_wait_delegate(self, new_delegate=None):
        assert isinstance(new_delegate, WaitDelegate)
        self.wait_delegate = new_delegate

    def set_default_wait(self, wait_in_seconds=None):
        assert wait_in_seconds >= 0
        self.default_wait = wait_in_seconds

