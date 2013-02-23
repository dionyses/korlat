
from korlat.abstraction.element import CheckableElement
from korlat.exception import CheckError, CheckEqualError, CheckAtLeastError


class AestheticElement(CheckableElement):
    def __init__(self, container_or_web_app, strategy, identifier, label=None):
        super(AestheticElement, self).__init__(container_or_web_app, strategy, identifier, label)
        self.minimum_size = {}
        self.exact_size = {}

    def set_minimum_height(self, height):
        self.minimum_size["height"] = height

    def set_minimum_width(self, width):
        self.minimum_size["width"] = width

    def set_exact_height(self, height):
        self.exact_size["height"] = height

    def set_exact_width(self, width):
        self.exact_size["width"] = width

    def check_appearance(self):
        if not self.is_displayed():
            raise CheckError("expected to be displayed")

        if len(self.minimum_size) > 0 or len(self.exact_size) > 0:
            size = self.get_size()

            if self.minimum_size.has_key("height"):
                if self.minimum_size["height"] > size["height"]:
                    raise CheckAtLeastError(self.minimum_size["height"], size["height"], "height:")

            if self.minimum_size.has_key("width"):
                if self.minimum_size["width"] > size["width"]:
                    raise CheckAtLeastError(self.minimum_size["width"], size["width"], "width:")

            if self.exact_size.has_key("height"):
                if self.exact_size["height"] != size["height"]:
                    raise CheckEqualError(self.exact_size["height"], size["height"], "height:")

            if self.exact_size.has_key("width"):
                if self.exact_size["width"] != size["width"]:
                    raise CheckEqualError(self.exact_size["width"], size["width"], "width:")

