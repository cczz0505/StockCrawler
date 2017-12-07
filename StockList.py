# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 15:42:29 2017

@author: darry
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import time
from Utils import InsertStockListTable

def stockListByDate(yy, mm, dd):
    text_date = "%s%s%s" % (yy, mm, dd)
    ROOT_URL = "http://www.tse.com.tw/exchangeReport/BWIBBU_d?response=html&date=%s&selectType=ALL" % text_date
    
    driver = webdriver.PhantomJS(executable_path='.\phantomjs.exe')
    driver.get(ROOT_URL)
    
    time.sleep(5)
    
    
    # fetch table data
    soup = BeautifulSoup(driver.page_source, 'lxml')
    
    tbody = soup.find('tbody')
    trs = tbody.find_all('tr')
    
    rows = []
    for tr in trs:
        tds = tr.find_all('td')
        rows.append([tds[0].text.strip(), tds[1].text.strip(), 1])        
    
    InsertStockListTable(rows)
    
    driver.close()

def stockListOTCByDate(yy, mm, dd):
    text_date = "%s/%s/%s" % (yy, mm, dd)
    ROOT_URL = "http://www.tpex.org.tw/web/stock/aftertrading/peratio_analysis/pera_print.php?l=zh-tw&d=%s&c=&s=0,asc,0" % text_date
    
    driver = webdriver.PhantomJS(executable_path='.\phantomjs.exe')
    driver.get(ROOT_URL)
    
    time.sleep(5)
    
    
    # fetch table data
    soup = BeautifulSoup(driver.page_source, 'lxml')
    
    tbody = soup.find('tbody')
    trs = tbody.find_all('tr')
    
    rows = []
    for tr in trs:
        tds = tr.find_all('td')
        rows.append([tds[0].text, tds[1].text, 0])        
    
    InsertStockListTable(rows)
    
    driver.close()

#stockListByDate(2017, 11, 30)  
#stockListOTCByDate(106, 11, 30)
