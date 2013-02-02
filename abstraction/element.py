from selenium.common.exceptions import NoSuchElementException

from container import Container
from core.strategy import xpath_of, ID, XPATH
from exception.nonexistentelement import NonExistentElement
from exception.unknownstrategy import UnknownStrategy


class Element(object):
    """Element is the basic atomic handle to an object

    :param container_or_web_app: Either the abstraction :class:`container` which holds this element or the application :class:`web_app`.
    :type container_or_web_app: :class:`container` or :class:`web_app`
    :param strategy: The lookup strategy used to locate this element.
    :type strategy: :py:const:`strategy`

    :var label: the label of this element (used in reference to :class:`container`.)
    :var strategy: the strategy
    :var link: TODO
    :var links: TODO
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

        A required element is one that you expect to be displayed in the containing :class:`container`.

        :param is_required: whether this element is required or not
        :type is_required: bool

        """
        assert isinstance(is_required, bool)
        self.required = is_required
        return self

    def set_parent(self, parent_element):
        assert isinstance(parent_element, Element)
        self.parent = parent_element
        return self.parent

    def set_content(self, contents):
        if isinstance(contents, list):
            self.content = contents
        else:
            self.content = [contents]

        return self

    def get_web_element(self):
        if self.web_app.wait_delegate is not None:
            self.web_app.wait_delegate.wait()

        try:
            if self.parent is not None or self.strategy == XPATH:
                return self.web_app.driver.find_element_by_xpath(self.get_identifier())
            elif self.strategy == ID:
                return self.web_app.driver.find_element_by_id(self.get_identifier())
        except NoSuchElementException:
            raise NonExistentElement(self.get_identifier())

        raise UnknownStrategy(self.strategy)

    def get_identifier(self):
        if self.parent is not None:
            return xpath_of(self.parent.strategy, self.parent.get_identifier()) + xpath_of(self.strategy, self._identifier, self.content)
        else:
            return self._identifier % tuple(self.content)

    def type(self, keys):
        self.get_web_element().send_keys(keys)
        return self

    def click(self):
        self.get_web_element().click()
        return self

