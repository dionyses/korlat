from os import environ

from selenium import webdriver

from abstraction.element import Element
from abstraction.container import Container
from core.webapp import WebApp
from core.appurl import AppUrl
from core import strategy
from googlelanding import GoogleLanding

chromedriver = "/home/dionyses/Downloads/drivers/chromedriver"
environ["webdriver.chrome.driver"] = chromedriver


w = WebApp(webdriver.Chrome(chromedriver), AppUrl("www.google.com"))
c = GoogleLanding(w)

w.go_to()
c.get("search_box").type("asdf")
c.get("id_template") \
    .set_content(["gbqfq"]) \
    .type("1")

c.get("search_box").type("qqq")
c.get("id_template").click() \
    .type("bob")

