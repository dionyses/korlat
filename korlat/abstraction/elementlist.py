from time import sleep

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait

from korlat.container import Container
from korlat.core.strategy import xpath_of, ID, XPATH
from korlat.core.webapp import WebApp
from korlat.exception import UnknownStrategy, CheckError


class ElementLists(object):
    """ElementList is the basic atomic handle to a list of objects

    :param container_or_web_app: either the abstraction :class:`Container` which holds these elements or the application :class:`WebApp`.
    :type container_or_web_app: :class:`Container` or :class:`WebApp`
    :param strategy: the lookup strategy used to locate these elements.
    :type strategy: :py:const:`strategy`
    :param identifier: the identifier used to locate these elements.  this parameter may be templated using python templating.
    :type identifier: str
    :param label: the label (name) of these elements.
    :type label: str

    >>> # build a templated element list
    >>> es = ElementList(my_web_app, strategy.TAG, "%s")
    >>> es.set_content("input").get_identifier()
    input

    >>> # build an element list in a container
    >>> e = ElementList(my_container, strategy.XPATH, "//div[contains(@class, 'test')]", "TEST")
    >>> my_container.get("TEST").

    Usage clarficiation:
        1. Access documented instace variables simply through direct dot syntax.
        2. Never set documeneted instance variables directly; use setters.
        3. Don't get/set private (_var) instance variables (these are left un-documented.)

    :var web_app: the :class:`WebApp` this Element belongs to.
    :var label: the label of this element (used in reference to :class:`Container`.)
    :var strategy: the strategy used to locate this element.
    :var required: whether this element is required to be displayed in its :class:`Container`.  can be None.
    :var parent: the parent element to this element.  can be None.
    :var link: the :class:`Container` this element links to.  can be None.
    :var links: the map of :class:`Container` s this element links to.
    :var content: the filler content used to populate the identifier (when applicable.)
    """
    def __init__(self, container_or_web_app, strategy, identifier, label=None):
        super(ElementList, self).__init__()
        assert isinstance(container_or_web_app, Container) or isinstance(container_or_web_app, WebApp)

        if isinstance(container_or_web_app, Container):
            self.web_app = container_or_web_app.web_app
        else:
            self.web_app = container_or_web_app

        self.strategy = strategy
        self._identifier = identifier
        self.label = label

        self.required = False
        self.parent = None
        self.link = None
        self.links = {}
        self.content = []

    def set_parent(self, parent_element):
        """Set this element's parent

        An element with a parent will be located based off of the parent's identifier + this element's identifier.
        Element's do not need to share the same strategy to be used with this mechanism.

        >>> # parented element location
        >>> p = Element(my_web_app, strategy.ID, "login-form")
        >>> e = Element(my_web_app, strategy.XPATH, "/input[@type='text']").set_parent(p)
        >>> e.get_identifier()
        //*[@id='login-form']/input[@type='text']

        :param parent_element: the parent to this element.
        :type parent_element: :class:`Element`
        :returns: this Element.
        """
        assert isinstance(parent_element, Element)
        self.parent = parent_element
        return self

    def set_content(self, contents):
        """Set the content used to fill this element's templated identifier

        >>> e = Element(my_web_app, strategy.ID, "button_%s")
        >>> e.set_content("login").get_identifier()
        button_login

        >>> e = Element(my_web_app, strategy.ID, "button_%s_%d")
        >>> e.set_content(["login", 5]).get_identifier()
        button_login_5

        :param contents: the content or list of contents to fill with.
        :type contents: list or object
        :returns: this Element.
        """
        if isinstance(contents, list):
            self.content = contents
        else:
            self.content = [contents]

        return self

    def get_web_elements(self):
        """Find the WebElement represented by this Element on the page.

        :returns: the selenium :class:`WebElement` found on the page.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        :raises: :class:`UnknownStrategy`
        """
        if self.web_app.wait_delegate is not None:
            self.web_app.wait_delegate.wait()

        if self.parent is not None or self.strategy == XPATH:
            return self.web_app.driver.find_elements_by_xpath(self.get_identifier())
        elif self.strategy == ID:
            return self.web_app.driver.find_elements_by_id(self.get_identifier())

        raise UnknownStrategy(self.strategy)

    def get_identifier(self):
        """Get the identifier for this Element.

        :returns: the identifier used to locate this Element.
        """
        if self.parent is not None:
            return xpath_of(self.parent.strategy, self.parent.get_identifier()) + xpath_of(self.strategy, self._identifier, self.content)
        else:
            return self._identifier % tuple(self.content)

    def make_ith_identifier(self, i):
        return xpath_of(self.get_identifier())

    def __str__(self):
        # TODO: fill with other usefull properties
        return "Identifier: %s\n" % self.get_identifier()

    def _wait_until_exists_or_not(self, exists, wait_in_seconds=None):
        """Wait until this Element exists or not.

        :returns: this Element.
        """
        if wait_in_seconds is None:
            wait_in_seconds = self.web_app.default_wait

        assert wait_in_seconds > 0
        ignoring = [
            StaleElementReferenceException,
            NoSuchElementException
        ]
        wait = WebDriverWait(self.web_app.driver, wait_in_seconds, .25, ignoring)

        if exists:
            wait.until(self._exists_for_wait)
        else:
            wait.until_not(self._exists_for_wait)

        return self

    def _wait_until_displayed_or_not(self, displayed, wait_in_seconds=None):
        """Wait until this Element is displayed or not.

        :returns: this Element.
        """
        if wait_in_seconds is None:
            wait_in_seconds = self.web_app.default_wait

        assert wait_in_seconds > 0
        ignoring = [
            StaleElementReferenceException,
            NoSuchElementException
        ]
        wait = WebDriverWait(self.web_app.driver, wait_in_seconds, .25, ignoring)

        if displayed:
            wait.until(self._is_displayed_for_wait)
        else:
            wait.until_not(self._is_displayed_for_wait)

        return self

    def wait_until_exists(self, wait_in_seconds=None):
        """Wait until this Element exists on the page.

        :param wait_in_seconds: the number of seconds to wait.  if unspecified then the :class:`WebApp` default is used.
        :type wait_in_seconds: int
        :returns: True if it **does** exist after the wait, False otherwise.
        """
        try:
            self._wait_until_exists_or_not(True, wait_in_seconds)
        except TimeoutException:
            pass
        finally:
            return self.exists()

    def wait_until_not_exists(self, wait_in_seconds=None):
        """Wait until this Element no longer exists on the page.

        :param wait_in_seconds: the number of seconds to wait.  if unspecified then the :class:`WebApp` default is used.
        :type wait_in_seconds: int
        :returns: True if it **does not** exist after the wait, False otherwise.
        """
        try:
            self._wait_until_exists_or_not(False, wait_in_seconds)
        except TimeoutException:
            pass
        finally:
            return not self.exists()

    def wait_until_displayed(self, wait_in_seconds=None):
        """Wait until this Element is displayed (visible) on the page.

        :param wait_in_seconds: the number of seconds to wait.  if unspecified then the :class:`WebApp` default is used.
        :type wait_in_seconds: int
        :returns: True if it **is** displayed after the wait, False otherwise.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        try:
            self._wait_until_displayed_or_not(True, wait_in_seconds)
        except TimeoutException:
            pass
        finally:
            return self.is_displayed()

    def wait_until_not_displayed(self, wait_in_seconds=None):
        """Wait until this Element is no longer displayed (visible) on the page.

        :param wait_in_seconds: the number of seconds to wait.  if unspecified then the :class:`WebApp` default is used.
        :type wait_in_seconds: int
        :returns: True if it **is not** displayed after the wait, False otherwise.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        try:
            self._wait_until_displayed_or_not(False, wait_in_seconds)
        except TimeoutException:
            pass
        finally:
            return not self.is_displayed()

    def _exists_for_wait(self, *args, **kwargs):
        """Wrapper for exists() which takes args, kwargs and does nothing with them.

        :returns: True if it exists, False otherwise.
        """
        return self.exists()

    def _is_displayed_for_wait(self, *args, **kwargs):
        """Wrapper for is_displayed() which takes args, kwargs and does nothing with them.

        :returns: True if it is displayed, False otherwise.
        """
        return self.is_displayed()

    # methods which return bool

    def count(self):
        """Check if this Element exists on the page.

        :returns: True if it exists, False otherwise.
        """
        return len(self.get_web_elements())

    def displayed_list(self):
        """Check if this Element is displayed (visible.)

        :returns: True if it is displayed, False otherwise.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        return [e.is_displayed() for e in self.get_web_elements()]

    def enabled_list(self):
        """Check if this Element is enabled.

        :returns: True if it is enabled, False otherwise.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        return [e.is_enabled() for e in self.get_web_elements()]

    def selected_list(self):
        """Check if this Element is selected.

        :returns: True if it is selected, False otherwise.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        return [e.is_selected() for e in self.get_web_elements()]

    # methods which return something (other than Element)

    def location_list(self):
        """Get the location of this Element.

        :returns: a dict of {str: int} containing the keys 'x' and 'y'
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        return [e.location for e in self.get_web_elements()]

    def size_list(self):
        """Get the size of this Element.

        :returns: a dict of {str: int} containing the keys 'width' and 'height'
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        return [e.size for e in self.get_web_elements()]

    def text_list(self):
        """Get the html text of this Element.

        :returns: the (trimmed) text of this Element.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        return [e.text for e in self.get_web_elements()]

    def tag_name_list(self):
        """Get the tag name of this Element.

        :returns: the tag name of this Element.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        return [e.tag_name for e in self.get_web_elements()]

    def attribute_list(self, name):
        """Get the value of attribute for this Element.

        :param name: the name to find the value for.
        :type name: str
        :returns: the value of the found attribute.  if the attribute does not exist None is returned.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        return [e.get_attribute(name) for e in self.get_web_elements()]

    def value_list(self):
        """Get the value for this Element.

        :returns: the value of this Element.  if there is no value None is returned.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        return [e.get_attribute("value") for e in self.get_web_element()]

    def css_value_list(self, prop):
        """Get the value of the css property for this Element.

        :param prop: the property to find the value for.
        :type prop: str
        :returns: the value of the found property.  if the property does not exist None is returned.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        return [e.value_of_css_property(prop) for e in self.get_web_elements()]

