# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 11:41:35 2017

@author: darry
"""

from Utils import GetStockPERReport, GetStockEPSGrowthReport, GetLast4QuaterEPS, GetStockIdNameDict, IsFloat
from Price import GetPrice

class PriceEarningsRatio:
    def __init__(self, sid, year, max_price, min_price, avg_price, eps, max_per, min_per, avg_per):
        self.id = sid
        self.year = year
        self.max_price = max_price
        self.min_price = min_price
        self.avg_price = avg_price
        self.eps = eps
        self.max_per = max_per
        self.min_per = min_per
        self.avg_per = avg_per
    
    def show(self):
        print(self.id, self.year, self.max_price, self.min_price, self.avg_price, self.eps, self.max_per, self.min_per, self.avg_per)
        
    def dump(self):
        return self.id, self.year, self.max_price, self.min_price, self.avg_price, self.eps, self.max_per, self.min_per, self.avg_per
        
class EPSGrowthRate:
    def __init__(self, sid, year, eps, eps_growth, eps_growth_rate, avg_price, avg_per):
        self.id = sid
        self.year = year
        self.eps = eps
        self.eps_growth = eps_growth
        self.eps_growth_rate = eps_growth_rate
        self.avg_price = avg_price
        self.avg_per = avg_per
        
    def show(self):
        print(self.id, self.year, self.eps, self.eps_growth, self.eps_growth_rate, self.avg_price, self.avg_per)
        
    def dump(self):
        return self.id, self.year, self.eps, self.eps_growth, self.eps_growth_rate, self.avg_price, self.avg_per

class EPSQuater:
    def __init__(self, year, quater, sid, eps):
        self.year = year
        self.quater = quater
        self.id = sid
        self.eps = eps
        
    def show(self):
        print(self.year, self.quater, self.id, self.eps)
        
    def dump(self):
        self.year, self.quater, self.id, self.eps
        
class StockReport:
    def __init__(self, stock_id):
        self.stock_id = stock_id
        self.per_list = []
        self.eps_list = []
        self.eps_quater_list = []
        self.name_dict = GetStockIdNameDict()
        
        self.avg_max_price = None
        self.avg_min_price = None
        self.avg_price = None
        self.avg_eps = None
        self.avg_max_per = None
        self.avg_min_per = None
        self.avg_per = None
        self.avg_eps_growth = None
        self.avg_eps_growth_rate = None
        self.sum_eps = None
        
        # 穩定型
        self.ref_low_price_s = None
        self.ref_avg_price_s = None
        self.ref_high_price_s = None
        
        # 成長型
        self.ref_eps_g_1 = None
        self.ref_eps_g_2 = None
        self.ref_eps_g = None
        self.prev_three_eps = None
        self.ref_low_price_g = None
        self.ref_avg_price_g = None
        self.ref_high_price_g = None
        self.ref_per_g = None
        
        # 現價
        self.now_price = None
        
    def collectPERReportData(self):
        price_query = GetStockPERReport(self.stock_id)
        
        if len(price_query) == 0:
            print('無年度EPS資料')
            return False

        for row in price_query:
            self.per_list.append(PriceEarningsRatio(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
            
        # last line of data (average)
        max_price_list = []
        min_price_list = []
        avg_price_list = []
        eps_list = []  # order by year
        max_per_list = []
        min_per_list = []
        avg_per_list = []
        for per in self.per_list:
            if IsFloat(per.max_price):
                max_price_list.append(float(per.max_price))
            if IsFloat(per.min_price):
                min_price_list.append(float(per.min_price))
            if IsFloat(per.avg_price):
                avg_price_list.append(float(per.avg_price))
            if IsFloat(per.eps):
                eps_list.append(float(per.eps))
            if IsFloat(per.max_per):
                max_per_list.append(float(per.max_per))
            if IsFloat(per.min_per):
                min_per_list.append(float(per.min_per))
            if IsFloat(per.avg_per):
                avg_per_list.append(float(per.avg_per))
                
        self.avg_max_price = sum(max_price_list) / len(max_price_list)
        self.avg_min_price = sum(min_price_list) / len(min_price_list)
        self.avg_price = sum(avg_price_list) / len(avg_price_list)
        self.avg_eps = sum(eps_list) / len(eps_list)
        self.avg_max_per = sum(max_per_list) / len(max_per_list)
        self.avg_min_per = sum(min_per_list) / len(min_per_list)
        self.avg_per = sum(avg_per_list) / len(avg_per_list)
        
        return True
            
    def collectLast4EPSReportData(self):
        eps_quater_query = GetLast4QuaterEPS(self.stock_id)
        
        if len(eps_quater_query) != 4:
            print('無EPS前四季資料')
            return False
        
        for row in eps_quater_query:
            self.eps_quater_list.append(EPSQuater(row[0], row[1], row[2], row[3]))
            
        self.sum_eps = sum([ float(e.eps) for e in self.eps_quater_list ])
        
        return True
            
    def collectEPSGrowthReportData(self):
        eps_query = GetStockEPSGrowthReport(self.stock_id)
        
        if len(eps_query) < 2:
            print('年度EPS資料筆數不足')
            return False
        
        prev_eps = None
        eps_growth = 'x'
        eps_growth_rate = 'x'
        for row in eps_query:
            if prev_eps:
                eps_growth = round(float(row[2]) - float(prev_eps), 2)
                eps_growth_rate = round(eps_growth / float(prev_eps), 2)
            else:
                eps_growth = 'x'
                eps_growth_rate = 'x'
            
            self.eps_list.append(EPSGrowthRate(row[0], row[1], row[2], str(eps_growth), str(eps_growth_rate), row[3], row[4]))
            prev_eps = row[2]
        
        # last line of data (average)
        eps_growth_list = []
        eps_growth_rate_list = []
        for e in self.eps_list:
            if IsFloat(e.eps_growth):
                eps_growth_list.append(float(e.eps_growth))
            if IsFloat(e.eps_growth_rate):
                eps_growth_rate_list.append(float(e.eps_growth_rate))
        
        self.avg_eps_growth = sum(eps_growth_list) / len(eps_growth_list)
        self.avg_eps_growth_rate = sum(eps_growth_rate_list) / len(eps_growth_rate_list)
        
        return True
    
    def calcEstimatePriceData(self):
        # 穩定型
        self.ref_low_price_s = self.avg_min_per * self.sum_eps
        self.ref_avg_price_s = self.avg_per * self.sum_eps
        self.ref_high_price_s = self.avg_max_per * self.sum_eps
        
        # 成長型
        self.ref_eps_g_1 = float(self.eps_list[-1].eps) * (1 + self.avg_eps_growth_rate)
        self.prev_three_eps = float(self.eps_quater_list[3].eps) + float(self.eps_quater_list[2].eps) + float(self.eps_quater_list[1].eps)
        self.ref_eps_g_2 = self.prev_three_eps / 3 * 4
        
        self.ref_eps_g = min(self.ref_eps_g_1, self.ref_eps_g_2)
        self.ref_low_price_g = self.avg_min_per * self.ref_eps_g
        self.ref_avg_price_g = self.avg_per * self.ref_eps_g
        self.ref_high_price_g = self.avg_max_per * self.ref_eps_g
        
        # 現價
        self.now_price = GetPrice(self.stock_id)
        
        if not IsFloat(self.now_price):
            print('查無股價資料')
            return False
        
        self.ref_per_g = self.now_price / self.ref_eps_g
        
        return True
        
    def getEstimatePrice(self):
        self.collectPERReportData()
        self.collectLast4EPSReportData()
        self.collectEPSGrowthReportData()
        self.calcEstimatePriceData()
        
        return min(self.ref_avg_price_s, self.ref_avg_price_g)
            
    def PERReport(self):
        if not self.collectPERReportData():
            return False
        
        print('\n{0:>6}({1})歷年本益比'.format(self.name_dict[self.stock_id], self.stock_id))
        print('{0:>8}{1:>6}{2:>6}{3:>6}{4:>8}{5:>9}{6:>6}{7:>6}'.format('年度', '最高股價', '最低股價', '平均股價', 'EPS', '最高(本益比)', '最低', '平均'))
        for p in self.per_list:
            print('{0:>10}{1:>10}{2:>10}{3:>10}{4:>8}{5:>14.2f}{6:>8.2f}{7:>8.2f}'.format(p.year, p.max_price, p.min_price, p.avg_price, p.eps, p.max_per, p.min_per, p.avg_per))
            
        # last line of report (average)
        print('{0:>10}{1:>10.2f}{2:>10.2f}{3:>10.2f}{4:>8.2f}{5:>14.2f}{6:>8.2f}{7:>8.2f}\n\n'.format('avg', self.avg_max_price, self.avg_min_price, self.avg_price, self.avg_eps, self.avg_max_per, self.avg_min_per, self.avg_per))
        
        return True
        
    def last4QuaterEPSReport(self):
        if not self.collectLast4EPSReportData():
            return False
        
        print('{0:>6}({1})預估EPS'.format(self.name_dict[self.stock_id], self.stock_id))
        print('{0:>8}Q{1}    {2}Q{3}    {4}Q{5}    {6}Q{7}    合計'.format(self.eps_quater_list[3].year, self.eps_quater_list[3].quater, self.eps_quater_list[2].year, self.eps_quater_list[2].quater, self.eps_quater_list[1].year, self.eps_quater_list[1].quater, self.eps_quater_list[0].year, self.eps_quater_list[0].quater))
        print('{0:>10}    {1:>5}    {2:>5}    {3:>5}    {4:.2f}\n\n'.format(self.eps_quater_list[3].eps, self.eps_quater_list[2].eps, self.eps_quater_list[1].eps, self.eps_quater_list[0].eps, self.sum_eps))

        return True

    def EPSGrowthReport(self):
        if not self.collectEPSGrowthReportData():
            return False
        
        print('{0:>6}({1})EPS成長率'.format(self.name_dict[self.stock_id], self.stock_id))
        print('{0:>8}{1:>8}{2:>8}{3:>8}{4:>8}{5:>8}'.format('年度', 'EPS', 'EPS成長', 'EPS成長率', '年均價', '本益比'))
        for e in self.eps_list:
            print('{0:>10}{1:>8}{2:>10}{3:>11}{4:>11}{5:>11.2f}'.format(e.year, e.eps, e.eps_growth, e.eps_growth_rate, e.avg_price, e.avg_per))
            
        # last line of report (average)
        print('{0:>10}{1:>8.2f}{2:>10.2f}{3:>11.2f}{4:>11.2f}{5:>11.2f}\n\n'.format('avg', self.avg_eps, self.avg_eps_growth, self.avg_eps_growth_rate, self.avg_price, self.avg_per))
        
        return True
    
    def estimatePriceReport(self):
        if not self.calcEstimatePriceData():
            return False
        
        print('穩定型：\n')
        print('便宜價 = {0:>6.2f} x {1:>6.2f} = {2:>6.2f}'.format(self.avg_min_per, self.sum_eps, self.ref_low_price_s))
        print('持有價 = {0:>6.2f} x {1:>6.2f} = {2:>6.2f}'.format(self.avg_per, self.sum_eps, self.ref_avg_price_s))
        print('昂貴價 = {0:>6.2f} x {1:>6.2f} = {2:>6.2f}\n'.format(self.avg_max_per, self.sum_eps, self.ref_high_price_s))
        
        print('成長型(eps取低值)：')
        print('1. {0} x ( 1 + {1:>6.2f} ) = {2:>6.2f}'.format(self.eps_list[-1].eps, self.avg_eps_growth_rate, self.ref_eps_g_1))
        print('2. 由上一年度前三季預測 {0:>6.2f} / 3 * 4 = {1:>6.2f}\n'.format(self.prev_three_eps, self.ref_eps_g_2))
        
        print('預估本益比 = {0:>6.2f}(股價) / {1:>6.2f} = {2:>6.2f}'.format(self.now_price, self.ref_eps_g, self.ref_per_g))
        
        #print('便宜價 = {0:>6.2f} x {1:>6.2f} = {2:>6.2f}'.format(self.avg_min_per, self.ref_eps_g, self.ref_low_price_g))
        #print('持有價 = {0:>6.2f} x {1:>6.2f} = {2:>6.2f}'.format(self.avg_per, self.ref_eps_g, self.ref_avg_price_g))
        #print('昂貴價 = {0:>6.2f} x {1:>6.2f} = {2:>6.2f}'.format(self.avg_max_per, self.ref_eps_g, self.ref_high_price_g))
        
        return True

def ShowLowPriceStocks():
    name_dict = GetStockIdNameDict()
    
    for sid in name_dict:
        try:
            #print('loading %s' % sid)
            now_price = GetPrice(sid)
            
            if IsFloat(now_price):
                report = StockReport(sid)
                est_price = report.getEstimatePrice()
                
                if now_price <= est_price:
                    print('%s%s, 現價：%.2f 可持有價：%.2f' % (sid, name_dict[sid], now_price, est_price))
        
        except Exception as ex:
            print(sid, ex, type(ex))
            
    print('done!')

def QuerySingleStockReport():
    while True:
        print('\n--------------------------------------------------------------------------------\n')
        stock_id = input('輸入股票代號：')
        report = StockReport(stock_id)
        
        if stock_id in report.name_dict:
        #if True:
            if not report.PERReport():
                continue
            
            if not report.last4QuaterEPSReport():
                continue
            
            if not report.EPSGrowthReport():
                continue
            
            if not report.estimatePriceReport():
                continue
        else:
            print('\n無此股票代號資料(%s)\n' % stock_id)
            continue

#ShowLowPriceStocks()
QuerySingleStockReport()