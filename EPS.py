# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 16:16:47 2017

@author: darry

"""

import urllib.request
from bs4 import BeautifulSoup
import re
from Utils import GetStockIdNameList, InsertEPSTable, InsertEPSQuaterTable

def GetEPS(stock_id, year):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}
    eps_url = 'https://tw.stock.yahoo.com/d/s/company_%s.html' % stock_id
    search_text = '%s年' % year
    
    try:
        req = urllib.request.Request(eps_url, headers=headers)
        response = urllib.request.urlopen(req)
        html = response.read().decode('big5')
        response.close()
    
        soup = BeautifulSoup(html, 'html.parser')
        td_list = soup.find_all('td')
        
    
    
        for td in td_list:
            if td.text == search_text:
                r = re.search('[0-9]+\.[0-9]+', td.find_next().text)
                eps = r.group()
                print(year, stock_id, eps)
                return eps
            
    except Exception as ex:
        print(stock_id, year, ex, type(ex))
        response.close()
        return "EXCEPTION"
        
    return "NO_DATA"

def GetEPSInQuater(stock_id):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}
    eps_url = 'https://tw.stock.yahoo.com/d/s/company_%s.html' % stock_id
    search_pattern = "[0-9]+第[0-9]+季"
    eps_list = []
    
    try:
        req = urllib.request.Request(eps_url, headers=headers)
        response = urllib.request.urlopen(req)
        html = response.read().decode('big5')
        response.close()
    
        soup = BeautifulSoup(html, 'html.parser')
        td_list = soup.find_all('td')
        
    
    
        for td in td_list:
            search_result = re.match(search_pattern, td.text)
            if search_result:
                year = search_result.group()[:3]
                season = search_result.group()[4:5]
                r = re.search('[0-9]+\.[0-9]+', td.find_next().text)
                eps = r.group()
                print(year, season, stock_id, eps)
                eps_list.append((year, season, stock_id, eps))

            
    except Exception as ex:
        print(stock_id, ex, type(ex))
        response.close()
        
    return eps_list

def GetAllEPSByQuater():
    stock_list = GetStockIdNameList()
    data_list = []
    
    for stock in stock_list:
        stock_id = stock[0]
        eps_list = GetEPSInQuater(stock_id)
        data_list.extend(eps_list)
    
    return data_list

def GetAllEPSByYear(year):
    stock_list = GetStockIdNameList()
    data_list = []
    
    for stock in stock_list:
        stock_id = stock[0]
        stock_name = stock[1]
        eps = GetEPS(stock_id, year)
        data_list.append((year, stock_id, stock_name, eps))
    
    return data_list
        

# EPSQuater table
data_q = GetAllEPSByQuater()
InsertEPSQuaterTable(data_q)
# EPS table
data_y = GetAllEPSByYear('105') # 102 ~ 105
InsertEPSTable(data_y)