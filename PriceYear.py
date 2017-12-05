# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 14:42:24 2017

@author: darry
"""

from selenium import webdriver
import time
from bs4 import BeautifulSoup
from Utils import GetStockIdNameList, InsertPriceYearTable, GetStockListListing, GetStockListOTC

class PriceFetcher():
    def __init__(self):
        self.web_driver = webdriver.PhantomJS(executable_path='.\phantomjs.exe')
        self.price_url = 'http://www.tse.com.tw/zh/page/trading/exchange/FMNPTK.html'
        self.price_otc_url = 'http://www.tpex.org.tw/web/stock/statistics/monthly/st42.php?l=zh-tw'
        self.fetched_data = []
        self.fetch_count = 0
        
        time.sleep(5)
        
    def __del__(self):
        self.web_driver.quit()
        
        
    def getPriceByStockId(self, stock_id):
        try:
            self.fetch_count += 1
            print('%s fetching %s' % (self.fetch_count, stock_id))
            self.web_driver.get(self.price_url)
        
            # send search request
            search_input = self.web_driver.find_element_by_xpath("//input[@name='stockNo']")
            search_button = self.web_driver.find_element_by_xpath("//a[@class='button search']")
            
            search_input.send_keys(stock_id)
            search_button.click()
            
            time.sleep(1)
            
            # fetch table data
            soup = BeautifulSoup(self.web_driver.page_source, 'lxml')
            tbody = soup.select_one("#report-table > tbody")
            trs = tbody.find_all('tr')
            
            data_list = []
            for tr in trs:
                tds = tr.find_all('td')
                values = [ td.text for td in tds ]
                values.insert(0, stock_id)
                data_list.append(values)
            
            return data_list
        
        except Exception as ex:
            print(ex, type(ex))
            return None
        
    def getStockPriceOTCByStockId(self, stock_id):
        try:
            self.fetch_count += 1
            print('%s fetching %s' % (self.fetch_count, stock_id))
            self.web_driver.get(self.price_otc_url)
        
            # send search request
            search_input = self.web_driver.find_element_by_xpath("//input[@name='input_stock_code']")
             
            search_input.send_keys(stock_id)
            search_input.submit()
            
            time.sleep(1)
            
            # fetch table data
            soup = BeautifulSoup(self.web_driver.page_source, 'lxml')
            table = soup.select_one("table.page-table-board")
            trs = table.find_all('tr')
            # skip first 2 lines
            trs = trs[2:]
            
            data_list = []
            for tr in trs:
                tds = tr.find_all('td')
                values = [ td.text for td in tds ]
                values.insert(0, stock_id)
                values[2] = values[2] + ',000'
                values[3] = values[3] + ',000'
                values[4] = values[4] + ',000'
                
                data_list.append(values)
            
            return data_list
        
        except Exception as ex:
            print(ex, type(ex))
            return None
            
    
    def getAllPrice(self):        
        stock_id_list = GetStockListListing()
        stock_id_otc_list = GetStockListOTC()
        data_list = []
        
        for stock_id in stock_id_list:
            price = self.getPriceByStockId(stock_id)
            
            if price:
                data_list.extend(price)
                
        for stock_id in stock_id_otc_list:
            price = self.getStockPriceOTCByStockId(stock_id)
            
            if price:
                data_list.extend(price)        
        
        return data_list
    
    def run(self):
        data = self.getAllPrice()
        InsertPriceYearTable(data)


fetcher = PriceFetcher()
fetcher.run()
del fetcher