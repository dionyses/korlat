from abstraction.element import Element
from abstraction.container import Container
from core.strategy import ID, XPATH


class GoogleLanding(Container):
    def __init__(self, *args, **kwargs):
        super(GoogleLanding, self).__init__(*args, **kwargs)

    def build_elements(self):
        self.put(Element(self, ID, "gbqfq", "search_box")) \
            .put(Element(self, XPATH, "//*[@id='%s']", "id_template")) \
            .put(Element(self, ID, "gbqf", "root"))

        self.get("search_box").set_parent(self.get("root"))
        self.get("id_template").set_parent(self.get("root"))
