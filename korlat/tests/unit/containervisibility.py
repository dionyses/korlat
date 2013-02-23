import unittest

from selenium import webdriver

from abstraction.container import Container
from abstraction.element import Element
from core.strategy import ID
from core.webapp import WebApp

from tests import GUINEA_PIG


class SimpleContainerA(Container):
    def _build_elements(self):
        self.put(Element(self, ID, "hidden-label", "hidden-label").set_required(True)) \
            .put(Element(self, ID, "yadda", "yadda").set_required(False))


class SimpleContainerB(Container):
    def _build_elements(self):
        self.put(Element(self, ID, "new-label", "new-label").set_required(True)) \
            .put(Element(self, ID, "yadda", "yadda").set_required(False))


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.d = webdriver.Firefox()
        self.w = WebApp(self.d, GUINEA_PIG)
        self.w.go_to()

    @classmethod
    def tearDownClass(self):
        self.d.quit()

    def test_wait_visible(self):
        cA = SimpleContainerA(self.w)
        Element(self.w, ID, "timing-displayed-button").click()
        self.assertFalse(cA.wait_until_visible(2))
        self.assertTrue(cA.wait_until_visible(2))
        self.assertFalse(cA.wait_until_not_visible(2))
        self.assertTrue(cA.wait_until_not_visible(2))

        # also test wait_visible when element isn't in DOM
        cB = SimpleContainerB(self.w)
        Element(self.w, ID, "timing-exists-button").click()
        self.assertFalse(cB.wait_until_visible(2))
        self.assertTrue(cB.wait_until_visible(2))
        self.assertFalse(cB.wait_until_not_visible(2))
        self.assertTrue(cB.wait_until_not_visible(2))


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(Tests)
    return suite

