from mock import Mock
import unittest

import selenium

from abstraction.container import Container
from abstraction.element import Element
from core.strategy import ID
from core.webapp import WebApp


class SimpleElement(Element):
    pass


class EmptyContainer(Container):
    def _build_elements(self):
        pass


class SimpleContainer(Container):
    def _build_elements(self):
        self.put(Element(self, ID, "id_1", "id_1")) \
            .put(Element(self, ID, "id_2", "id_2").set_required(True)) \
            .put(Element(self, ID, "id_3", "id_3").set_required(False)) \
            .put(SimpleElement(self, ID, "id_4", "id_4"))


class NoRequiredContainer(Container):
    def _build_elements(self):
        self.put(Element(self, ID, "id_1", "id_1")) \
            .put(Element(self, ID, "id_2", "id_2").set_required(False))


class Tests(unittest.TestCase):
    def setUp(self):
        self.mock_driver = Mock()
        self.mock_driver.__class__ = selenium.webdriver.remote.webdriver.WebDriver
        self.mock_driver.window_handles = ["a"]
        self.web_app = WebApp(self.mock_driver, "http://coolsite.com")

    def test_unimplemented_build_elements(self):
        with self.assertRaises(NotImplementedError):
            bad_container = Container(self.mock_driver)

    def test_put_and_get(self):
        c = EmptyContainer(self.web_app)
        self.assertEquals(0, len(c._elements)) # some glass-box testing

        e1 = Element(c, ID, "yadda", "yadda")
        c.put(e1)
        self.assertEquals(1, len(c._elements)) # some glass-box testing
        # we explicitly check for the same object in memory
        self.assertTrue(e1 is c.get("yadda"))

    def test_get_elements(self):
        c = SimpleContainer(self.web_app)
        l = c.get_elements()
        self.assertEquals(4, len(l))
        self.assertTrue(c.get("id_1") in l)
        self.assertTrue(c.get("id_2") in l)
        self.assertTrue(c.get("id_3") in l)
        self.assertTrue(c.get("id_4") in l)

        l = c.get_elements(required=True)
        self.assertEquals(1, len(l))
        self.assertTrue(c.get("id_2") in l)

        l = c.get_elements(required=False)
        self.assertEquals(3, len(l))
        self.assertTrue(c.get("id_1") in l)
        self.assertTrue(c.get("id_3") in l)
        self.assertTrue(c.get("id_4") in l)

        l = c.get_elements(clss=SimpleElement)
        self.assertEquals(1, len(l))
        self.assertTrue(c.get("id_4") in l)

        l = c.get_elements(clss=Element)
        self.assertEquals(4, len(l))
        self.assertTrue(c.get("id_1") in l)
        self.assertTrue(c.get("id_2") in l)
        self.assertTrue(c.get("id_3") in l)
        self.assertTrue(c.get("id_4") in l)

        l = c.get_elements(clss=SimpleElement, required=True)
        self.assertEquals(0, len(l))

        l = c.get_elements(clss=SimpleElement, required=False)
        self.assertEquals(1, len(l))
        self.assertTrue(c.get("id_4") in l)

    def test_wait_until_no_required(self):
        c = NoRequiredContainer(self.web_app)

        with self.assertRaises(AssertionError):
            c.wait_until_visible()


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)

