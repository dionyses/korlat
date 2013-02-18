from element import Element


class Widget(Element):
    """Widget acts to model the behaviour on a collection of Elements which all share a common ancestor.

    A basic example of what you may use a Widget for is a search area.  These are often comprised of a
    textbox + button.  You could create a SearchWidget which defines custom the custom method
    use_search(text) and overrides exists() and is_displayed() to verify both textbox and button exist
    and are displayed.
    """
    def __init__(self, container_or_web_app, strategy, identifier, label=None):
        super(Widget, self).__init__(container_or_web_app, strategy, identifier, label)

    def exists():
        """Same as Element.exists()

        .. note::
            must be overridden
        """
        raise NotImplementedError()

    def is_displayed():
        """Same as Element.is_displayed()

        .. note::
            must be overridden
        """
        raise NotImplementedError()

class CheckableWidget(Widget):
    """CheckableWidget can be used to add common checks (assertions) to Widgets.

    This class acts similarily to CheckableElement, except in the same way that Widget encapsulates
    a collection of Elements, CheckableWidget encapsulates the appearance and behaviour of a collection
    of Elements.
    """
    def __init__(self, container_or_web_app, strategy, identifier, label=None):
        super(Widget, self).__init__(container_or_web_app, strategy, identifier, label)

    def check_appearance(self):
        """Override to assert this Widget is layed out correctly.

        :result: this Widget is inspected in regards to its appearance.
        :returns: this CheckableWidget.
        :raises: :class:`CheckError`
        """
        raise NotImplementedError()

    def check_behaviour(self):
        """Override to assert this Widget can be used and interacted with correctly.

        :result: this Widget is inspected in regards to its behaviour.
        :returns: this CheckableWidget.
        :raises: :class:`CheckError`
        """
        raise NotImplementedError()

