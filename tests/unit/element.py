# -*- coding: utf-8 -*-
from mock import Mock
from time import sleep
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from abstraction.container import Container
from abstraction.element import Element
from core.strategy import ID, XPATH
from core.webapp import WebApp
from exception import NonExistentElement


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.d = webdriver.Firefox()
        self.w = WebApp(self.d, "file:///home/dionyses/projects/korlat/tests/guineapig.html")
        self.w.go_to()

    def setUp(self):
        self.root_div_id = Element(self.w, ID, "root")
        self.root_div_xpath = Element(self.w, XPATH, "//div[contains(@class, 'root-class')]")

        self.text_input_id = Element(self.w, ID, "text-input")

        self.button_input_id = Element(self.w, ID, "button-input")

        self.change_label_id = Element(self.w, ID, "change-label")

        self.label_xpath_a = Element(self.w, XPATH, "//label[@class='label-class']")
        self.label_xpath_b = Element(self.w, XPATH, "//label[contains(@class, 'label-class')]")
        self.label_xpath_c = Element(self.w, XPATH, "//*[@class='label-class' and not(starts-with(@id, 'bob'))]")
        self.label_relative_xpath = Element(self.w, XPATH, "/label[@class='label-class']")

        self.checkbox_input_1 = Element(self.w, ID, "checkbox-input-1")
        self.checkbox_input_2 = Element(self.w, ID, "checkbox-input-2")

        self.hidden_label_id = Element(self.w, ID, "hidden-label")

        self.non_existent_id = Element(self.w, ID, "non-existent")

        self.bad_xpath = Element(self.w, XPATH, "//input[type='button']")

    @classmethod
    def tearDownClass(self):
        self.d.quit()

    def test_base_lookup(self):
        self.assertTrue(self.root_div_id.exists())
        self.assertTrue(self.root_div_xpath.exists())

        self.assertTrue(self.text_input_id.exists())

        self.assertTrue(self.label_xpath_a.exists())
        self.assertTrue(self.label_xpath_b.exists())
        self.assertTrue(self.label_xpath_c.exists())
        self.assertFalse(self.label_relative_xpath.exists())

        self.assertFalse(self.non_existent_id.exists())

        self.assertFalse(self.bad_xpath.exists())

    def test_parent_lookup(self):
        self.text_input_id.set_parent(self.root_div_id)
        self.assertTrue(self.text_input_id.exists())
        self.text_input_id.set_parent(self.root_div_xpath)
        self.assertTrue(self.text_input_id.exists())

        self.label_xpath_a.set_parent(self.root_div_id)
        self.assertTrue(self.label_xpath_a.exists())
        self.label_xpath_a.set_parent(self.root_div_xpath)
        self.assertTrue(self.label_xpath_a.exists())

        self.label_xpath_b.set_parent(self.root_div_id)
        self.assertTrue(self.label_xpath_b.exists())
        self.label_xpath_b.set_parent(self.root_div_xpath)
        self.assertTrue(self.label_xpath_b.exists())

        self.label_xpath_c.set_parent(self.root_div_id)
        self.assertTrue(self.label_xpath_c.exists())
        self.label_xpath_c.set_parent(self.root_div_xpath)
        self.assertTrue(self.label_xpath_c.exists())

        self.label_relative_xpath.set_parent(self.root_div_id)
        self.assertTrue(self.label_relative_xpath.exists())
        self.label_relative_xpath.set_parent(self.root_div_xpath)
        self.assertTrue(self.label_relative_xpath.exists())

        self.non_existent_id.set_parent(self.root_div_id)
        self.assertFalse(self.non_existent_id.exists())
        self.non_existent_id.set_parent(self.root_div_xpath)
        self.assertFalse(self.non_existent_id.exists())

        self.bad_xpath.set_parent(self.root_div_id)
        self.assertFalse(self.bad_xpath.exists())
        self.bad_xpath.set_parent(self.root_div_xpath)
        self.assertFalse(self.bad_xpath.exists())

    def test_gets(self):
        # get_value
        self.assertEquals("button", self.button_input_id.get_value())
        # get_text
        self.assertEquals("Test Label", self.label_xpath_a.get_text())
        # get_attribute
        self.assertEquals("checkbox", self.checkbox_input_1.get_attribute("type"))
        # get_css_value
        self.assertEquals("1", self.text_input_id.get_css_value("z-index"))
        # get_tag_name
        self.assertEquals("label", self.label_xpath_a.get_tag_name())
        # get_identifier
        self.assertEquals("text-input", self.text_input_id.get_identifier())
        # get_location
        self.assertEquals({"x": 1, "y": 50}, self.text_input_id.get_location())
        # get_size
        self.assertEquals({"width": 150, "height": 25}, self.text_input_id.get_size())

    def test_states(self):
        # is_enabled
        self.assertTrue(self.checkbox_input_1.is_enabled())
        self.assertFalse(self.checkbox_input_2.is_enabled())

        # is_selected
        self.assertFalse(self.checkbox_input_1.is_selected())
        self.assertTrue(self.checkbox_input_2.is_selected())

        # is_displayed
        self.assertTrue(self.label_xpath_a.is_displayed())
        self.assertFalse(self.hidden_label_id.is_displayed())

        with self.assertRaises(NonExistentElement):
            self.label_relative_xpath.is_displayed()

        with self.assertRaisesRegexp(NonExistentElement, str(self.non_existent_id)):
            self.non_existent_id.is_displayed()

    def test_controls(self):
        # click
        self.assertEquals("0", self.change_label_id.get_text())
        self.button_input_id.click()
        self.assertEquals("1", self.change_label_id.get_text())
        self.button_input_id.click()
        self.assertEquals("2", self.change_label_id.get_text())

        # send_keys
        self.text_input_id.send_keys("test text")
        self.assertEquals("test text", self.text_input_id.get_value())
        self.text_input_id.send_keys(u"你好吗?")
        self.assertEquals(u"test text你好吗?", self.text_input_id.get_value())
        self.text_input_id.send_keys(Keys.BACK_SPACE)
        self.text_input_id.send_keys(Keys.BACK_SPACE)
        self.text_input_id.send_keys(Keys.ARROW_LEFT)
        self.text_input_id.send_keys(Keys.BACK_SPACE)
        self.assertEquals(u"test text好", self.text_input_id.get_value())

        # clear
        self.text_input_id.clear()
        self.assertEquals("", self.text_input_id.get_value())

    def test_waiting(self):
        Element(self.w, ID, "timing-button").click()
        new_label = Element(self.w, ID, "new-label")
        # test that when the element still hasn't appeared until_exists returns False
        self.assertFalse(new_label.wait_until_exists(2))
        # test that when the element finally appears until_exists returns True
        self.assertTrue(new_label.wait_until_exists(2))
        # test that when the element still hasn't dissappeared until_not_exists returns False
        self.assertFalse(new_label.wait_until_not_exists(2))
        # test that when the element finally dissappears until_not_exists returns True
        self.assertTrue(new_label.wait_until_not_exists(2))

    def test_links(self):
        mock_container_a = Mock()
        mock_container_a.__class__ = Container
        e = Element(self.w, ID, "nadda", "nadda") \
            .set_link(mock_container_a)
        self.assertTrue(mock_container_a is e.link)

        mock_container_b = Mock()
        mock_container_b.__class__ = Container
        e.set_link(mock_container_b)
        self.assertTrue(mock_container_b is e.link)

        e.set_link(mock_container_a, "a")
        self.assertTrue(mock_container_a is e.links["a"])
        self.assertTrue(mock_container_b is e.link)

        with self.assertRaises(KeyError):
            e.links["b"]


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(Tests)
    return suite

