from time import sleep
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from abstraction.element import Element
from abstraction.container import Container
from core.strategy import ID, XPATH
from core.webapp import WebApp, MAIN_WINDOW
from exception import NonExistentElement


class GP2(Container):
    def _build_elements(self):
        self.put(Element(self, ID, "guineapig2", "guineapig2").set_required(True))


class GP3(Container):
    def _build_elements(self):
        self.put(Element(self, ID, "guineapig3", "guineapig3").set_required(True))


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.d = webdriver.Firefox()
        self.w = WebApp(self.d, "file:///home/dionyses/projects/korlat/tests/guineapig.html")

        self.gp2s = Element(self.w, ID, "gp2s", "gp2s_label") \
                        .set_link(GP2(self.w))
        self.gp2n = Element(self.w, ID, "gp2n", "gp2n_label") \
                        .set_link(GP2(self.w))
        self.gp3s = Element(self.w, ID, "gp3s", "gp3s_label") \
                        .set_link(GP3(self.w))
        self.gp3n = Element(self.w, ID, "gp3n") \
                        .set_link(GP3(self.w), "key")

    @classmethod
    def tearDownClass(self):
        self.d.quit()

    def setUp(self):
        self.w.go_to()
        # every go_to should wipe any extra windows
        self.assertTrue(1, len(self.w.get_windows()))

    def test_go_to_link_key_error(self):
        with self.assertRaises(KeyError):
            self.gp2s.go_to_link("no_keys")

        with self.assertRaises(KeyError):
            self.gp3n.go_to_link("incorrect_key")

        with self.assertRaises(KeyError):
            self.gp2s.go_to_link("Key")

    def test_go_to_link(self):
        # open gp2 in the same window
        for e in self.gp2s.go_to_link().get_elements(required=True):
            # make sure you land at gp2
            self.assertTrue(e.is_displayed())

        # there should be one windows
        self.assertEquals(1, len(self.w.get_windows()))
        # we shouldn't see the link which brought us here
        self.assertFalse(self.gp2s.exists())
        # go back
        self.w.driver.back()

        # open gp3 in a new window
        for e in self.gp3n.go_to_link("key").get_elements(required=True):
            # make sure you land at gp3
            self.assertTrue(e.is_displayed())

        # there should be two windows
        self.assertEquals(2, len(self.w.get_windows()))
        # we shouldn't see the link which brought us here
        self.assertFalse(self.gp2s.exists())

    def test_window_labels(self):
        ### opening no new window should leave the get_windows unaltered
        handles = self.w.get_windows()
        self.gp2s.go_to_link()
        self.assertEquals(handles, self.w.get_windows())

        ### opening a new window from a labelled element should use the label
        self.w.driver.back()
        self.gp2n.go_to_link()
        self.assertNotEqual(handles, self.w.get_windows())
        # get_windows should still contain the previous key
        self.assertTrue(handles[0] in self.w.get_windows())
        # get_windows should also contain a key equal of the element's label which brought it there
        self.assertTrue(self.gp2n.label in self.w.get_windows())

        ### opening a new window from an unlabelled element should use the next_window_key
        handles = self.w.get_windows()
        self.w.use_window(MAIN_WINDOW)
        next_key = self.w.next_window_key()
        self.gp3n.go_to_link("key")
        self.assertNotEqual(handles, self.w.get_windows())
        # get_windows should still contain the previous keys
        self.assertTrue(handles[0] in self.w.get_windows())
        self.assertTrue(handles[1] in self.w.get_windows())
        # get_windows should also contain a key equal which is next_window_key
        self.assertTrue(next_key in self.w.get_windows())

        ### opening a pre-existing label/key should not alter the get_windows()
        handles = self.w.get_windows()
        self.w.use_window(MAIN_WINDOW)
        self.gp2s.go_to_link()
        self.assertEquals(handles, self.w.get_windows())

    def test_switching_windows(self):
        self.gp2n.go_to_link()
        self.w.use_window(MAIN_WINDOW)
        n_k_1 = self.w.next_window_key()
        self.gp3n.go_to_link("key") # should be next key 1
        self.assertTrue(n_k_1 in self.w.get_windows())
        self.w.use_window(MAIN_WINDOW)
        n_k_2 = self.w.next_window_key()
        self.gp3n.go_to_link("key") # should be next key 2
        self.assertTrue(n_k_1 in self.w.get_windows())
        self.assertTrue(n_k_2 in self.w.get_windows())
        self.assertEquals(4, len(self.w.get_windows()))

        for k in self.w.get_windows():
            self.w.use_window(k)

            if k == MAIN_WINDOW:
                self.assertTrue(self.gp2s.exists())
                self.assertFalse(self.gp2n.link.get_elements(required=True)[0].exists())
                self.assertFalse(self.gp3n.links["key"].get_elements(required=True)[0].exists())
            elif k == self.gp2n.label:
                self.assertFalse(self.gp2s.exists())
                self.assertTrue(self.gp2n.link.get_elements(required=True)[0].exists())
                self.assertFalse(self.gp3n.links["key"].get_elements(required=True)[0].exists())
            else:
                self.assertFalse(self.gp2s.exists())
                self.assertFalse(self.gp2n.link.get_elements(required=True)[0].exists())
                self.assertTrue(self.gp3n.links["key"].get_elements(required=True)[0].exists())

    def test_dead_windows(self):
        self.gp2n.go_to_link()
        self.w.use_window(MAIN_WINDOW)
        self.gp2n.go_to_link()
        self.assertEquals(2, len(self.w.get_windows()))
        self.assertEquals(3, len(self.w.driver.window_handles))

        self.w.go_to()
        self.assertEquals(1, len(self.w.get_windows()))
        self.assertEquals(1, len(self.w.driver.window_handles))
        self.assertTrue(MAIN_WINDOW in self.w.get_windows())


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(Tests)
    return suite

