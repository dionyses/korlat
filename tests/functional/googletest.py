from os import environ
import sys
sys.path.append("/home/dionyses/projects/shelobpy/")

from selenium import webdriver

from abstraction.element import Element
from abstraction.container import Container
from core.webapp import WebApp
from core import strategy
from google import Google

chromedriver = "/home/dionyses/Downloads/drivers/chromedriver"
environ["webdriver.chrome.driver"] = chromedriver


w = WebApp(webdriver.Chrome(chromedriver), "http://www.google.com")
c = Google(w)

w.go_to()
print "if you want, go back now!"
import time
time.sleep(2)
print "start!"
print c.get("search_box").wait_until_exists() \
    .send_keys("asdf") \
    .get_location()
print c.get("search_box").get_size()
print c.get("search_box").get_tag_name()
c.get("id_template") \
    .set_content(["gbqfq"]) \
    .send_keys("1")

c.get("search_box").send_keys("qqq")
c.get("id_template").click() \
    .send_keys("bob")

w.driver.quit()
