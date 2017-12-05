# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 15:29:17 2017

@author: darry
"""

import sqlite3

def IsFloat(arg):
    try:
        float(arg)
        return True
    except Exception as ex:
        #print(type(ex), ex)
        return False

def GetStockPERReport(stock_id=None):
    conn = sqlite3.connect('Stock.db')
    cur = conn.cursor()
    
    if stock_id:
        cur.execute('''select p.id, p.year, p.highest_price, p.lowest_price, p.avg_price, e.eps, p.highest_price / e.eps, p.lowest_price / e.eps, p.avg_price / e.eps
                       from priceyear p, eps e
                       where p.year = e.year
                       and p.id = e.id
                       and p.id = %s
                       order by p.year
                       ''' % stock_id)
    else:
        cur.execute('''select p.id, p.year, p.highest_price, p.lowest_price, p.avg_price, e.eps, p.highest_price / e.eps, p.lowest_price / e.eps, p.avg_price / e.eps
                       from priceyear p, eps e
                       where p.year = e.year
                       and p.id = e.id
                       order by p.id, p.year
                       ''')
        
    query_result = cur.fetchall()
    
    conn.close()
    
    return query_result

def GetStockEPSGrowthReport(stock_id):
    conn = sqlite3.connect('Stock.db')
    cur = conn.cursor()
    
    cur.execute('''select e.id, e.year, e.eps, p.avg_price, p.avg_price / e.eps
                   from eps e, priceyear p
                   where e.year = p.year
                   and e.id = p.id
                   and e.id = %s
                   order by e.year
                   ''' % stock_id)
    
    query_result = cur.fetchall()
    
    conn.close()
    
    return query_result

def GetLast4QuaterEPS(stock_id):
    conn = sqlite3.connect('Stock.db')
    cur = conn.cursor()
    
    cur.execute('''select *
                   from EPSQuater
                   where id = %s
                   order by year desc, quater desc
                   limit 4
                   ''' % stock_id)
    
    query_result = cur.fetchall()
    
    conn.close()
    
    return query_result

'''
select e.year, e.eps, p.avg_price, p.avg_price / e.eps
from eps e, priceyear p
where e.year = p.year
and e.id = p.id
and e.id = "2892"
'''

def GetStockIdNameList():
    conn = sqlite3.connect('Stock.db')
    cur = conn.cursor()
    
    cur.execute("select id, name from StockList")
    query_result = cur.fetchall()
    
    conn.close()
    
    stock_id_name_list = [ (r[0], r[1]) for r in query_result ]
    
    return stock_id_name_list

def GetStockListListing():
    conn = sqlite3.connect('Stock.db')
    cur = conn.cursor()
    
    cur.execute("select id from StockList where is_listing = '1'")
    query_result = cur.fetchall()
    
    conn.close()
    
    stock_id_list = [ r[0] for r in query_result ]
    
    return stock_id_list

def GetStockListOTC():
    conn = sqlite3.connect('Stock.db')
    cur = conn.cursor()
    
    cur.execute("select id from StockList where is_listing = '0'")
    query_result = cur.fetchall()
    
    conn.close()
    
    stock_id_list = [ r[0] for r in query_result ]
    
    return stock_id_list

def GetStockIdNameDict():
    conn = sqlite3.connect('Stock.db')
    cur = conn.cursor()
    
    cur.execute("select id, name from StockList")
    query_result = cur.fetchall()
    
    conn.close()
    
    stock_id_name_dict = {}
    for r in query_result:
        stock_id_name_dict[r[0]] = r[1]
        
    return stock_id_name_dict

def InitPriceYearTable():
    conn = sqlite3.connect('Stock.db')
    
    with conn:
        conn.execute('create table PriceYear (id text, year text, trade_shares text, trade_money text, trade_count text, highest_price text, highest_date text, lowest_price text, lowest_date text, avg_price text, primary key (id, year))')
    
    conn.close()

def InsertPriceYearTable(row_list):
    conn = sqlite3.connect('Stock.db')
    cur = conn.cursor()
    
    for row_data in row_list:
        try:
            cur.execute('insert into PriceYear values (?,?,?,?,?,?,?,?,?,?)', row_data)
        except Exception as ex:
            print(row_data[0], row_data[1], ex, type(ex))
            
    conn.commit()
    conn.close()
    
def InsertPriceDayTable(row_list):
    conn = sqlite3.connect('Stock.db')
    cur = conn.cursor()
    
    for row_data in row_list:
        try:
            cur.execute('insert into PriceDay values (?, datetime(),?)', row_data)
        except Exception as ex:
            print(row_data[0], row_data[1], ex, type(ex))
            
    conn.commit()
    conn.close()
    
def InitPriceDayTable():
    conn = sqlite3.connect('Stock.db')
    
    with conn:
        conn.execute('create table PriceDay (id text, sysdate date, price text, primary key (id, sysdate))')
    
    conn.close()

def InitEPSTable():
    conn = sqlite3.connect('Stock.db')
    
    with conn:
        conn.execute('create table EPS (year text, id text, name text, eps text, primary key (year, id))')
    
    conn.close()
    
def InsertEPSTable(row_list):
    conn = sqlite3.connect('Stock.db')
    cur = conn.cursor()
    
    for row_data in row_list:
        try:
            cur.execute('insert into EPS values (?,?,?,?)', row_data)
        except Exception as ex:
            print(row_data[1], row_data[2], ex, type(ex))
            
    conn.commit()
    conn.close()
    
def InitEPSQuater():
    conn = sqlite3.connect('Stock.db')
    
    with conn:
        conn.execute('create table EPSQuater (year text, quater text,  id text, eps text, primary key (year, quater, id))')
    
    conn.close()
    
def InsertEPSQuaterTable(row_list):
    conn = sqlite3.connect('Stock.db')
    cur = conn.cursor()
    
    for row_data in row_list:
        try:
            cur.execute('insert into EPSQuater values (?,?,?,?)', row_data)
        except Exception as ex:
            print(row_data[0], row_data[1], row_data[2], ex, type(ex))
            
    conn.commit()
    conn.close()
    
def InitBasicIndexTable():
    conn = sqlite3.connect('Stock.db')
    
    with conn:
        conn.execute('create table BasicIndex (date text, id text, name text, dy real, dy_year integer, per real, pbr real, financial_year text, primary key (date, id))')
    
    conn.close()
    
def InsertBasicIndexTable(row_list, text_date):
    # insert into sqllite
    conn = sqlite3.connect('Stock.db')        
    
    for r in row_list:
        data = r.find_all('td')
        data = [ d.text.strip() for d in data ]
        data.insert(0, text_date)
        
        print('inserting ', data)
        try:
            cur = conn.cursor()
            cur.execute('insert into BasicIndex values (?,?,?,?,?,?,?,?)', data)
        except Exception as ex:
            print(ex, type(ex))
            
    conn.commit()
    conn.close()
    
def InitStockListTable():
    conn = sqlite3.connect('Stock.db')
    
    with conn:
        conn.execute('create table StockList (id text, name text, is_listing text, primary key (id, name))')
    
    conn.close()
    
    
def InsertStockListTable(rows):
    # insert into sqllite
    conn = sqlite3.connect('Stock.db')        
    
    for r in rows:
        print('inserting ', r)
        try:
            cur = conn.cursor()
            cur.execute('insert into StockList values (?,?,?)', r)
        except Exception as ex:
            print(ex, type(ex))
            
    conn.commit()
    conn.close()