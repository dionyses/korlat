from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait

from container import Container
from core.strategy import xpath_of, ID, XPATH
from exception import NonExistentElement, UnknownStrategy


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

    def set_link(self, link):
        """Set this element's link

        Used when clicking on an element results in a container becoming displayed.
        The resultant container is defined via link.

        :param link: the :class:`Container` this element links to.
        :type link: :class:`Container`
        :returns: this Element.
        """
        assert isinstance(container, Container)
        self.link = container
        return self

    def set_link(self, key, container):
        """Set this element's link for the key

        Used when clicking on an element results in one of many containers becoming displayed.
        The resultant container is defined via key-link mapping.

        :param key: the key to map this link under.
        :type key: str
        :param link: the :class:`Container` this element links to.
        :type link: :class:`Container`
        :returns: this Element.
        """
        assert isinstance(key, str)
        assert isinstance(container, Container)
        self.links[key] = container
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

    def get_web_element(self):
        """Find the WebElement represented by this Element on the page.

        :returns: the selenium :class:`WebElement` found on the page.
        :raises: :class:`NonExistentElement`
        :raises: :class:`UnknownStrategy`
        """
        if self.web_app.wait_delegate is not None:
            self.web_app.wait_delegate.wait()

        try:
            if self.parent is not None or self.strategy == XPATH:
                return self.web_app.driver.find_element_by_xpath(self.get_identifier())
            elif self.strategy == ID:
                return self.web_app.driver.find_element_by_id(self.get_identifier())
        except NoSuchElementException:
            raise NonExistentElement(str(self))

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
            NonExistentElement
        ]
        wait = WebDriverWait(self.web_app.driver, wait_in_seconds, .25, ignoring)

        if exists:
            wait.until(self._exists_for_wait)
        else:
            wait.until_not(self._exists_for_wait)

        return self

    def wait_until_exists(self, wait_in_seconds=None):
        """Wait until this Element exists on the page.

        :param wait_in_seconds: the number of seconds to wait.  if unspecified then the :class:`WebApp` default is used.
        :type wait_in_seconds: int
        :returns: this Element.
        """
        return self._wait_until_exists_or_not(True, wait_in_seconds)

    def wait_until_not_exists(self, wait_in_seconds=None):
        """Wait until this Element no longer exists on the page.

        :param wait_in_seconds: the number of seconds to wait.  if unspecified then the :class:`WebApp` default is used.
        :type wait_in_seconds: int
        :returns: this Element.
        """
        return self._wait_until_exists_or_not(False, wait_in_seconds)

    def _exists_for_wait(self, *args, **kwargs):
        """Wrapper for exists() which takes args, kwargs and does nothing with them

        :returns: this Element.
        """
        return self.exists()

    # methods which return bool

    def exists(self):
        """Check if this Element exists on the page.

        :returns: True if it exists, False otherwise.
        """
        try:
            self.get_web_element()
            return True
        except NonExistentElement:
            return False

    def is_displayed(self):
        """Check if this Element is displayed (visible.)

        .. note::
            if this Element does not exist, then False is still returned.

        :returns: True if it is displayed, False otherwise.
        """
        try:
            return self.get_web_element().is_displayed()
        except NonExistentElement:
            return False

    def is_enabled(self):
        """Check if this Element is enabled.

        .. note::
            if this Element does not exist, a NonExistentElement exception is raised.

        :returns: True if it is enabled, False otherwise.
        """
        return self.get_web_element().is_enabled()

    def is_selected(self):
        """Check if this Element is selected.

        .. note::
            if this Element does not exist, a NonExistentElement exception is raised.

        :returns: True if it is selected, False otherwise.
        """
        return self.get_web_element().is_selected()

    # methods which return something (not Element)

    def get_location(self):
        """Get the location of this Element.

        :returns: a dict of {str: int} containing the keys 'x' and 'y'
        """
       return self.get_web_element().location

    def get_size(self):
        """Get the size of this Element.

        :returns: a dict of {str: int} containing the keys 'width' and 'height'
        """
        return self.get_web_element().size

    def get_text(self):
        """Get the html text of this Element.

        :returns: the text of this Element.
        """
        return self.get_web_element().text

    def get_tag_name(self):
        """Get the tag name of this Element.

        :returns: the tag name of this Element.
        """
        return self.get_web_element().tag_name

    def get_attribute(self, name):
        """Get the value of attribute for this Element.

        :param name: the name to find the value for.
        :type name: str
        :returns: the value of the found attribute.  if the attribute does not exist None is returned.
        """
        return self.get_web_element().get_attribute(name)

    def get_css_value(self, prop):
        """Get the value of the css property for this Element.

        :param prop: the property to find the value for.
        :type prop: str
        :returns: the value of the found property.  if the property does not exist None is returned.
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
        """
        self.get_web_element().send_keys(keys)
        return self

    def click(self):
        """Click on this Element.

        :returns: this Element.
        """
        self.get_web_element().click()
        return self

    def clear(self):
        """Clear this Element.

        :returns: this Element.
        """
        self.get_web_element().clear()
        return self

    def submit(self):
        """Submit this Element.

        :returns: this Element.
        """
        self.get_web_element().submit()
        return self

