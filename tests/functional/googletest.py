from os import environ
import sys
sys.path.append("/home/dionyses/projects/shelobpy/")

from selenium import webdriver

from abstraction.element import Element
from abstraction.container import Container
from core.webapp import WebApp
from core.appurl import AppUrl
from core import strategy
from google import Google

chromedriver = "/home/dionyses/Downloads/drivers/chromedriver"
environ["webdriver.chrome.driver"] = chromedriver


w = WebApp(webdriver.Chrome(chromedriver), AppUrl("www.google.com"))
c = Google(w)

w.go_to()
import time
time.sleep(10)
print "start!"
c.get("search_box").wait_until_exists() \
    .send_keys("asdf")
c.get("id_template") \
    .set_content(["gbqfq"]) \
    .send_keys("1")

c.get("search_box").send_keys("qqq")
c.get("id_template").click() \
    .send_keys("bob")

w.driver.quit()
