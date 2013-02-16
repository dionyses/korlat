import unittest

from selenium import webdriver

from core.webapp import WebApp
from exception import UsageError


class Tests(unittest.TestCase):
    def test_usage_error(self):
        d = webdriver.Firefox()
        w = WebApp(d, "http://www.google.com")

        with self.assertRaises(UsageError):
            w.driver.implicitly_wait(1)

        d.quit()


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)

