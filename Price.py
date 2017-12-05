# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 14:45:35 2017

@author: darry
"""

import urllib.request
from bs4 import BeautifulSoup
from Utils import GetStockIdNameDict, IsFloat, InsertPriceDayTable

def GetPrice(stock_id):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}
    price_url = 'https://tw.stock.yahoo.com/q/q?s=%s' % stock_id
    
    try:
        req = urllib.request.Request(price_url, headers=headers)
        response = urllib.request.urlopen(req)
        html = response.read().decode('big5')
        response.close()
    
        soup = BeautifulSoup(html, 'html.parser')
        
        return float(soup.find('b').text)
            
    except Exception as ex:
        print(stock_id, ex, type(ex))
        response.close()
        return "EXCEPTION"
        
    return "NO_DATA"

def fetchPriceData():
    name_dict = GetStockIdNameDict()
    row_list = []
    
    for sid in name_dict:
        print('fetch %s' % sid)
        price = GetPrice(sid)
        
        if IsFloat(price):
            row_list.append((sid, price))
        
    InsertPriceDayTable(row_list)
    print('done!')
    
fetchPriceData()