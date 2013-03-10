from time import sleep

from selenium.common.exceptions import NoSuchElementException, \
    StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from container import Container
from korlat.core.strategy import xpath_of, ID, TAG, XPATH
from korlat.core.webapp import WebApp
from korlat.exception import UnknownStrategy, CheckError


class Element(object):
    """Element is the basic atomic handle to an object

    :param container_or_web_app: either the abstraction :class:`Container` which holds this element or the application :class:`WebApp`.
    :type container_or_web_app: :class:`Container` or :class:`WebApp`
    :param strategy: the lookup strategy used to locate this element.
    :type strategy: :py:const:`strategy`
    :param identifier: the identifier used to locate this element.  this parameter may be templated using python templating.
    :type identifier: str
    :param label: the label (name) of this element.
    :type label: str

    >>> # build a templated element
    >>> e = Element(my_web_app, strategy.ID, "button_%d")
    >>> e.set_content(5).get_identifier()
    button_5

    >>> # build an element in a container
    >>> e = Element(my_container, strategy.XPATH, "//div[contains(@class, 'test')]", "TEST")
    >>> my_container.get("TEST").click()

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
        super(Element, self).__init__()
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

    def set_required(self, is_required):
        """Set this element as required

        A required element is one that you expect to be displayed in the containing :class:`Container`.

        :param is_required: whether this element is required or not
        :type is_required: bool
        :returns: this Element.
        """
        assert isinstance(is_required, bool)
        self.required = is_required
        return self

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

    def set_link(self, container, key=None):
        """Set a link for this Element

        Used when clicking on an element results in one or many containers becoming displayed.
        The resultant Containers may be defined via key-link mapping.

        >>> e = Element(my_web_app, strategy.ID, "login-form").set_link(container_a)
        >>> e.link
        container_a
        >>> e.links
        {}
        >>> e.set_link(container_b, "b")
        >>> e.link
        container_a
        >>> e.links["b"]
        container_b

        :param link: the :class:`Container` this element links to.
        :type link: :class:`Container`
        :param key: if keyed, the key to map this link under.
        :type key: str
        :returns: this Element.
        """
        assert isinstance(container, Container)

        if key is None:
            self.link = container
        else:
            assert isinstance(key, str)
            self.links[key] = container

        return self

    def go_to_link(self, key=None):
        """Go to the link represented by this Element.

        This performs a 'click' operation on this Element.  If a new window/tab is opened
        as a result then it is tracked in the :class:`WebApp`.  In this case, if this Element
        has a label then that label is the key identifying the window.  If this Element doesn't
        have a label then a unique one is generated (see next_window_key() from :class:`WebApp`).

        :param key: if keyed, the key to retrieve this link from.
        :type key: str
        :returns: the :class:`Container` for the link
        """
        if key is None:
            assert self.link is not None
        else:
            # try to access the keyi so a KeyError is raised if it isn't there
            self.links[key]

        pre_handles = set(self.web_app.driver.window_handles)
        self.click()
        sleep(.5)
        post_handles = set(self.web_app.driver.window_handles)
        new_handles = post_handles.difference(pre_handles)

        # a new tab/window was opened
        if len(new_handles) > 0:
            name = self.label if self.label is not None else self.web_app.next_window_key()
            self.web_app.put_window(name, new_handles.pop()) \
                .use_window(name)

        return self.link if key is None else self.links[key]

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

    def get_web_element(self):
        """Find the WebElement represented by this Element on the page.

        :returns: the selenium :class:`WebElement` found on the page.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        :raises: :class:`UnknownStrategy`
        """
        if self.web_app.wait_delegate is not None:
            self.web_app.wait_delegate.wait()

        if self.parent is not None or self.strategy == XPATH:
            return self.web_app.driver.find_element_by_xpath(self.get_identifier())
        elif self.strategy == ID:
            return self.web_app.driver.find_element_by_id(self.get_identifier())
        elif self.strategy == TAG:
            return self.web_app.driver.find_element_by_tag_name(self.get_identifier())

        raise UnknownStrategy(self.strategy)

    def get_identifier(self):
        """Get the identifier for this Element.

        :returns: the identifier used to locate this Element.
        """
        if self.parent is not None:
            return xpath_of(self.parent.strategy, self.parent.get_identifier()) + xpath_of(self.strategy, self._identifier, self.content)
        else:
            return self._identifier % tuple(self.content)

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

        return not self.exists()

    def wait_until_displayed(self, wait_in_seconds=None, ignore=False):
        """Wait until this Element is displayed (visible) on the page.

        :param wait_in_seconds: the number of seconds to wait.  if unspecified then the :class:`WebApp` default is used.
        :type wait_in_seconds: int
        :param ignore: specify whether NoSuchElementExceptions should be ignored or not.  if ignored, a caught NoSuchElementException will return as False.
        :type ignore: bool
        :returns: True if it **is** displayed after the wait, False otherwise.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        try:
            self._wait_until_displayed_or_not(True, wait_in_seconds)
        except TimeoutException:
            pass

        return self.is_displayed(ignore)

    def wait_until_not_displayed(self, wait_in_seconds=None, ignore=False):
        """Wait until this Element is no longer displayed (visible) on the page.

        :param wait_in_seconds: the number of seconds to wait.  if unspecified then the :class:`WebApp` default is used.
        :type wait_in_seconds: int
        :param ignore: specify whether NoSuchElementExceptions should be ignored or not.  if ignored, a caught NoSuchElementException will return as False.
        :type ignore: bool
        :returns: True if it **is not** displayed after the wait, False otherwise.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        try:
            self._wait_until_displayed_or_not(False, wait_in_seconds)
        except TimeoutException:
            pass

        return not self.is_displayed(ignore)

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

    def exists(self):
        """Check if this Element exists on the page.

        :returns: True if it exists, False otherwise.
        """
        try:
            self.get_web_element()
            return True
        except NoSuchElementException:
            return False

    def is_displayed(self, ignore=False):
        """Check if this Element is displayed (visible.)

        :param ignore: specify whether NoSuchElementExceptions should be ignored or not.  if ignored, a caught NoSuchElementException will return as False.
        :type ignore: bool
        :returns: True if it is displayed, False otherwise.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        if ignore:
            try:
                return self.get_web_element().is_displayed()
            except NoSuchElementException:
                return False
        else:
            return self.get_web_element().is_displayed()

    def is_enabled(self):
        """Check if this Element is enabled.

        :returns: True if it is enabled, False otherwise.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        return self.get_web_element().is_enabled()

    def is_selected(self):
        """Check if this Element is selected.

        :returns: True if it is selected, False otherwise.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        return self.get_web_element().is_selected()

    # methods which return something (other than Element)

    def get_location(self):
        """Get the location of this Element.

        :returns: a dict of {str: int} containing the keys 'x' and 'y'
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        return self.get_web_element().location

    def get_size(self):
        """Get the size of this Element.

        :returns: a dict of {str: int} containing the keys 'width' and 'height'
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        return self.get_web_element().size

    def get_text(self):
        """Get the html text of this Element.

        :returns: the (trimmed) text of this Element.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        return self.get_web_element().text

    def get_tag_name(self):
        """Get the tag name of this Element.

        :returns: the tag name of this Element.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        return self.get_web_element().tag_name

    def get_attribute(self, name):
        """Get the value of attribute for this Element.

        :param name: the name to find the value for.
        :type name: str
        :returns: the value of the found attribute.  if the attribute does not exist None is returned.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        return self.get_web_element().get_attribute(name)

    def get_value(self):
        """Get the value for this Element.

        :returns: the value of this Element.  if there is no value None is returned.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        return self.get_web_element().get_attribute("value")

    def get_css_value(self, prop):
        """Get the value of the css property for this Element.

        :param prop: the property to find the value for.
        :type prop: str
        :returns: the value of the found property.  if the property does not exist None is returned.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        return self.get_web_element().value_of_css_property(prop)

    # method which return Element

    def send_keys(self, keys):
        """Send the keys to this Element.

        .. note::
            we don't use the synonym 'type' to avoid confusion with python's keyword 'type'.

        :param keys: the keys to send.
        :type keys: str
        :returns: this Element.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        self.get_web_element().send_keys(keys)
        return self

    def click(self):
        """Click on this Element.

        :returns: this Element.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        self.get_web_element().click()
        return self

    def clear(self):
        """Clear this Element.

        :returns: this Element.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        self.get_web_element().clear()
        return self

    def submit(self):
        """Submit this Element.

        :returns: this Element.
        :raises: :class:`selenium.common.exceptions.NoSuchElementException`
        """
        self.get_web_element().submit()
        return self


class CheckableElement(Element):
    """CheckableElement can be used to add common checks (assertions) to Elements.

    A common and useful unit test technique in UI testing is to check that a set of elements
    appear nicely and can be interacted with.  For example:

        1. Make sure all the labels are visible and are at least 10px by 10px.
        2. Make sure all the checkboxes can be clicked, and clicking toggles the state between checked and unchecked.

    For these situations, Checkable can be used to simplify the writing of these tests and to
    consolidate the logic and operations by element type.
    """
    def __init__(self, container_or_web_app, strategy, identifier, label=None):
        super(CheckableElement, self).__init__(container_or_web_app, strategy, identifier, label)

    def check_appearance(self):
        """Override to assert this Element is layed out correctly.

        :result: this Element is inspected in regards to its appearance.
        :returns: this CheckableElement.
        :raises: :class:`CheckError`
        """
        raise NotImplementedError()

    def check_behaviour(self):
        """Override to assert this Element can be used and interacted with correctly.

        :result: this Element is inspected in regards to its behaviour.
        :returns: this CheckableElement.
        :raises: :class:`CheckError`
        """
        raise NotImplementedError()

