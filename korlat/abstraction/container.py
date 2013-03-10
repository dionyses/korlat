from selenium.common.exceptions import NoSuchElementException


class Container(object):
    """Container represents an area or collection in the application of Elements and Widgets.

    :param web_app: the application :class:`WebApp` this Container is relevant to.
    :type web_app: :class:`WebApp`

    Usage clarification:
        1. Access documented instance variables simply through direct dot syntax.
        2. Never set documented instance variables directly; use setters.
        3. Don't get/set private (_var) instance variables (these are left un-documented.)

    :var web_app: the :class:`WebApp` context this Container exists in.
    """
    def __init__(self, web_app):
        super(Container, self).__init__()
        self.web_app = web_app
        self._elements = {}
        self._build_elements()

    def _build_elements(self):
        """Populate this Container's Elements.

        .. note::
            this method must be overridden

        >>> class SimpleContainer(Container)
        >>>     def _build_elements(self):
        >>>         self.put(Element(self, ID, "test_id", "test_label"))

        """
        raise NotImplementedError()

    def put(self, element):
        """Put an Element into this Container.

        :param element: the **labelled** :class:`Element` to add.
        :type element: :class:`Element`
        :result: element is added this Container's collection of elements, under the key element.label.  if this Container already had an element keyed by the element.label, then it is replaced.
        :returns: this Container.
        """
        assert element is not None
        assert element.label is not None and len(element.label) > 0
        self._elements[element.label] = element
        return self

    def get(self, label):
        """Get the Element from this Container.

        :param label: the label to find the element by.
        :type label: str
        :returns: the :class:`Element` found to be keyed by label.  if one cannot be found, then KeyError is raised.
        """
        assert label is not None and len(label) > 0
        return self._elements[label]

    def get_elements(self, clss=None, required=None):
        """Get the (sub-)set of Elements in this Container.

        :param clss: the specific class of :class:`Element` to get.
        :type clss: a sub-class of :class:`Element`
        :param required: include only required or not required Elements
        :type required: bool
        :returns: the list of :class:`Element` in this Container which meet the specified criteria.  unspecified criteria are ignored.
        """
        l = []

        if clss is not None:
            l = [v for v in self._elements.values() if isinstance(v, clss)]
        else:
            l = [v for v in self._elements.values()]

        if required is None:
            return l
        else:
            return [v for v in l if v.required == required]

    def wait_until_visible(self, wait_in_seconds=None):
        """Wait until this Container becomes visible (displayed)

        Allow the Container to become visible.  To use, the Container must have at least
        one required Element.

        :param wait_in_seconds: the number of seconds to wait.  if unspecified, then the :class:`WebApp` default is used.
        :type wait_in_seconds: int
        :returns: True if it **is** visible after the wait, False otherwise.
        :raises: AssertionError (if there are no required Elements in this Container)

        .. note::
            this method traps NoSuchElementExceptions, returning as False
        """
        required_elements = self.get_elements(required=True)
        assert len(required_elements) > 0
        return required_elements[0].wait_until_displayed(wait_in_seconds, ignore=True)

    def wait_until_not_visible(self, wait_in_seconds=None):
        """Wait until this Container goes away (becomes in-visible)

        Allow the Container to 'go away'.  To use, the Container must have at least
        one required Element.

        :param wait_in_seconds: the number of seconds to wait.  if unspecified, then the :class:`WebApp` default is used.
        :type wait_in_seconds: int
        :returns: True if it **is not** visible after the wait, False otherwise.
        :raises: AssertionError (if there are no required Elements in this Container)

        .. note::
            this method traps NoSuchElementExceptions, returning as True
        """
        required_elements = self.get_elements(required=True)
        assert len(required_elements) > 0
        return required_elements[0].wait_until_not_displayed(wait_in_seconds, ignore=True)

    def is_visible(self):
        """Check if this Container is visible (displayed)

        To use, the Container must have at least one required Element.

        :returns: True if the container is visible, False otherwise.
        :raises: AssertionError (if there are no required Elements in this Container)

        .. note::
            this method traps NoSuchElementExceptions, returning as False
        """
        required_elements = self.get_elements(required=True)
        assert len(required_elements) > 0
        return required_elements[0].is_displayed(ignore=True)

