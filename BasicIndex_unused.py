# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 09:44:18 2017

@author: darry
"""

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
from Utils import InsertBasicIndexTable

class TSEParser:
    def __init__(self, html):
        pass

def singleStock():
    # open web page
    ROOT_URL = "http://www.tse.com.tw/zh/page/trading/exchange/STOCK_DAY.html"
    
    driver = webdriver.PhantomJS(executable_path='.\phantomjs.exe')
    driver.get(ROOT_URL)
    
    time.sleep(2)
    
    # send search request
    element_search = driver.find_element_by_name('stockNo')
    button_search = driver.find_element_by_link_text('查詢')
    
    element_search.send_keys('2412')
    button_search.click()
    
    time.sleep(2)
    
    # fetch table data
    soup = BeautifulSoup(driver.page_source, 'lxml')
    
    table = soup.find(attrs={'class' : 'dataTables_wrapper'})
    thead = table.find('thead')
    
    cols = thead.find_all('th')
    col_names = [ c.text.strip() for c in cols ]
    print(col_names)
    
    tbody = table.find('tbody')
    rows = tbody.find_all('tr')
    
    for r in rows:
        data = r.find_all('td')
        data = [ d.text.strip() for d in data ]
        print(data)

def basicIndexByDate(yy=None, mm=None, dd=None):
    ROOT_URL = "http://www.tse.com.tw/zh/page/trading/exchange/BWIBBU_d.html"
    
    driver = webdriver.PhantomJS(executable_path='.\phantomjs.exe')
    driver.get(ROOT_URL)
    
    time.sleep(5)
    
    # select date to search
    select_yy = Select(driver.find_element_by_xpath("//select[@name='yy']"))
    select_mm = Select(driver.find_element_by_xpath("//select[@name='mm']"))
    select_dd = Select(driver.find_element_by_xpath("//select[@name='dd']"))
    
    if yy:
        select_yy.select_by_value(str(yy))
    if mm:
        select_mm.select_by_value(str(mm))
    if dd:
        select_dd.select_by_value(str(dd))
    
    if yy or mm or dd:
        element_search = driver.find_element_by_xpath("//a[@class='button search']")
        element_search.click()
        
    text_yy = select_yy.all_selected_options[0].get_attribute('value')
    text_mm = select_mm.all_selected_options[0].get_attribute('value')
    text_dd = select_dd.all_selected_options[0].get_attribute('value')
    text_date = "%s/%s/%s" % (text_yy, text_mm, text_dd)
    
    # select table length by select object
    element_select = Select(driver.find_element_by_xpath("//select[@name='report-table_length']"))
    element_select.select_by_value('-1')
    
    # fetch table data
    soup = BeautifulSoup(driver.page_source, 'lxml')
    
    table = soup.find(attrs={'id' : 'report-table'})
    tbody = table.find('tbody')
    rows = tbody.find_all('tr')
    
    InsertBasicIndexTable(rows, text_date)
    
    driver.close()

basicIndexByDate(2017, 11, 22)
    
    
    