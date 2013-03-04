from korlat.common.elementbase import AestheticElement
from korlat.common import unique
from korlat.exception import CheckError, CheckEqualError


class Label(AestheticElement):
    def __init__(self, container_or_web_app, strategy, identifier, label=None):
        super(Label, self).__init__(container_or_web_app, strategy, identifier, label)
        self.set_minimum_height(20)
        self.set_minimum_width(20)

    def check_behaviour(self):
        pass # nothing to check


class Link(AestheticElement):
    def __init__(self, container_or_web_app, strategy, identifier, label=None):
        super(Link, self).__init__(container_or_web_app, strategy, identifier, label)
        self.set_minimum_height(20)
        self.set_minimum_width(20)


class Button(AestheticElement):
    def __init__(self, container_or_web_app, strategy, identifier, label=None):
        super(Button, self).__init__(container_or_web_app, strategy, identifier, label)
        self.set_minimum_height(20)
        self.set_minimum_width(40)

    def check_behaviour(self):
        pass # nothing to check


class Textbox(AestheticElement):
    def __init__(self, container_or_web_app, strategy, identifier, label=None):
        super(Textbox, self).__init__(container_or_web_app, strategy, identifier, label)
        self.set_minimum_height(20)
        self.set_minimum_width(40)
        self.default = None

    def set_default_value(self, value):
        self.default = value

    def check_behaviour(self):
        if self.default is not None and self.get_value() != self.default:
            raise CheckEqualError(self.default, self.get_value(), "textbox default value:")

        i = unique.identifier()
        self.send_keys(i)

        if self.get_value() != i:
            raise CheckEqualError(i, self.get_value(), "textbox changed value:")


class Checkbox(AestheticElement):
    def __init__(self, container_or_web_app, strategy, identifier, label=None):
        super(Checkbox, self).__init__(container_or_web_app, strategy, identifier, label)
        self.set_minimum_height(14)
        self.set_minimum_width(14)

    def check(self, check_on):
        if self.is_selected() != check_on:
            self.click()

    def check_behaviour(self):
        started_on = self.is_selected()
        self.click()

        if self.is_selected() == started_on:
            raise CheckError("checkbox should %sbe selected" % ("not " if started_on else ""))

        self.click()

        if self.is_selected() != started_on:
            raise CheckError("checkbox should %sbe selected" % ("" if started_on else "not "))

