from time import sleep
from urlparse import urlparse

from waitdelegate import WaitDelegate


DEFAULT_WAIT_IN_SECONDS = 10
"""The default wait time to wait for an element.  10 seconds.
"""
MAIN_WINDOW = "main_window"
"""The key locating the primary window.
"""


class WebApp(object):
    """WebApp is the core entry point of korlat, acting to identify your web application and to manage top level controls.

    On creation, the WebApp will have a single window identified by MAIN_WINDOW.

    :param driver: the selenium.WebDriver instace.
    :type driver: :class:`WebDriver`
    :param url: the URL of the web application.  this should be the absolute point of entry into the web application.
    :type url: str parsable as a URL

    Usage clarification:
        1. Access documented instance variables simply through direct dot syntax.
        2. Never set documented instance variables directly; use setters.
        3. Don't get/set private (_var) instance variables (these are left un-documented.)

    :var driver: the :class:`WebDriver` instance.
    :var url: the URL of the web application.
    :var wait_delegate: the :class:`WaitDelegate` for this WebApp.
    :var default_wait: the default time to wait, in seconds.
    """
    def __init__(self, driver, url):
        super(WebApp, self).__init__()
        # assuming the url must start with either
        #   http
        #   https
        #   file
        assert len(urlparse(url).scheme) > 3
        self.driver = driver
        self.url = url
        self.wait_delegate = None
        self.default_wait = DEFAULT_WAIT_IN_SECONDS

        # No implicit wait as waiting is controlled at the element
        # level via "wait_until_*"
        self.driver.implicitly_wait(0)
        assert len(self.driver.window_handles) == 1
        self._windows = {MAIN_WINDOW: self.driver.window_handles[0]}
        self._current_window = None

    def _destroy_windows(self):
        while len(self.driver.window_handles) > 1:
            self.driver.switch_to_window(self.driver.window_handles[-1])
            self.driver.close()

        self._windows = {}
        self.put_window(MAIN_WINDOW, self.driver.window_handles[0])

    def go_to(self):
        """Go to this WebApp.

        :result: the WebDriver navigates to the defined WebApp.url, and any existing windows attached to this WebDriver are closed.
        :returns: this WebApp.
        """
        self._destroy_windows()
        self.use_window(MAIN_WINDOW)

        pre_handles = set(self.driver.window_handles)
        self.driver.get(str(self.url))
        post_handles = set(self.driver.window_handles)
        assert len(pre_handles) == len(post_handles)
        return self

    def put_window(self, key, handle):
        """Add the window by reference key.

        :param key: the key reference to locate the window handle by.
        :type key: str
        :param handle: the selenium handle associated with the window.
        :result: the window handle is added to this WebApp's map of windows.  if there already exists a handle mapped by key then it is replaced.
        :returns: this WebApp.
        """
        self._windows[key] = handle
        return self

    def use_window(self, key):
        """Switch to the window by reference key.

        :param key: the key reference specifying which window to use.
        :type key: str
        :result: the window mapped by key is set to be the context the WebDriver should operate in.  in other words, after use_window(), the Elements in other windows will always return False to exists().
        :returns: this WebApp.
        """
        self.driver.switch_to_window(self._windows[key])
        self._current_window = key
        return self

    def get_windows(self):
        """Get the list of windows for this WebApp.

        :returns: the list of keys which map to windows defined on this WebApp.
        """
        return self._windows.keys()

    def next_window_key(self):
        """Generate a key which can be used with put_window() and will not overwrite an existing key->handle mapping.

        >>> web_app.next_window_key()
        1
        >>> web_app.next_window_key()
        1
        >>> web_app.put_window(web_app.next_window_key(), some_handle)
        >>> web_app.next_window_key()
        2

        :returns: a str which is unique among the already defined keys (get_windows()).
        """
        current_keys = self.get_windows()
        n = 1

        while str(n) in current_keys:
            n += 1

        return str(n)

    def set_wait_delegate(self, new_delegate):
        """Set the WaitDelegate for this WebApp.

        :param new_delegate: the new WaitDelegate to set for this WebApp.
        :type new_delegate: :class:`WaitDelegate`
        :returns: this WebApp.
        """
        assert isinstance(new_delegate, WaitDelegate)
        self.wait_delegate = new_delegate

    def set_default_wait(self, wait_in_seconds):
        """Set the default wait (in seconds) for this WebApp.

        :param wait_in_seconds: the default wait in seconds to set.
        :type wait_in_seconds: int
        :returns: this WebApp.
        """
        assert wait_in_seconds >= 0
        self.default_wait = wait_in_seconds

