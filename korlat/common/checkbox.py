from korlat.common.elementbase import AestheticElement
from korlat.exception import CheckError


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

