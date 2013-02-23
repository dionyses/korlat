from mock import Mock
from time import sleep
import unittest

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from abstraction.container import Container
from abstraction.element import Element
from common.checkbox import Checkbox
from core.strategy import ID, XPATH
from core.webapp import WebApp


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.d = webdriver.Firefox()
        self.w = WebApp(self.d, "file:///home/dionyses/projects/korlat/tests/guineapig.html")
        self.w.go_to()

    @classmethod
    def tearDownClass(self):
        self.d.quit()

    def test_checkbox(self):
        c = Checkbox(self.w, ID, "checkbox-input-1")
        c.check_appearance()
        c.check_behaviour()


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(Tests)
    return suite

