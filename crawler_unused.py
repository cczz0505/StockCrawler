# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 15:10:42 2017

@author: darry
"""

from selenium import webdriver
from bs4 import BeautifulSoup

ROOT_URL = "https://tw.yahoo.com/"

driver = webdriver.PhantomJS(executable_path='.\phantomjs.exe')
driver.get(ROOT_URL)

soup = BeautifulSoup(driver.page_source, 'lxml')

for tag in soup.find_all('a'):
    if 'href' in tag.attrs:
        print(tag.attrs['href'])