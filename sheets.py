from bs4 import BeautifulSoup
from bs4.element import ResultSet
import requests
import db
import utils
from stockinfo import Info

class Sheet():
    co_id = -1
    year = -1
    season = -1

    cycs = '' # current year current season
    lycs = '' # last year current season
    lyls = '' # last year last season
    cycd = '' # current year current duration
    cyfd = '' # current year full duration
    lycd = '' # last year current duration
    lyfd = '' # last year full duration

    __url_i = 1
    __soup = ''
    __BalanceSheet = {}
    __IncomeStatement = {}
    __CashFlowStatement = {}

    def __init__(self, co_id, year, season):
        self.co_id = co_id
        self.year = year
        self.season = season
        # self.getSoup(1)
        _year = str(self.year)
        _lastyear = str(self.year - 1)
        _date = Info.season2date[self.season]
        _fromdate = Info.season2duration[self.season][0]
        _todate = Info.season2duration[self.season][1]
        self.cycs = _year + _date
        self.lycs = _lastyear + _date
        self.lyls = _lastyear + Info.season2date[4]
        self.cycd = _year + _fromdate + '-' + _year + _todate
        self.cyfd = _year + '0101' + '-' + _year + _todate
        self.lycd = _lastyear + _fromdate + '-' + _lastyear + _todate
        self.lyfd = _lastyear + '0101' + '-' + _lastyear + _todate

    def getBalanceSheet(self):
        if not self.__BalanceSheet: # empty
            self.__BalanceSheet = self.__getSheet('balancesheet')

        return self.__BalanceSheet

    def getIncomeStatement(self):
        if not self.__IncomeStatement:
            self.__IncomeStatement = self.__getSheet('incomestatement')

        return self.__IncomeStatement

    def getCashFlowStatement(self):
        if not self.__CashFlowStatement:
            self.__CashFlowStatement = self.__getSheet('cashflowstatement')

        return self.__CashFlowStatement

    def __getSheet(self, sheet_name):
        result = db.checkDBExist(self.co_id, self.year, self.season, sheet_name)
        if result == None: # not in database
            if self.__soup == '':
                while True and self.__url_i <= 3: # try different url
                    self.__genSoup(self.__url_i)
                    if utils.checkPageExist(self.__soup) is True:
                        break
                    self.__url_i = self.__url_i + 1
            if self.__url_i <= 3:
                sheet_dict = utils.parseSheet(self.__soup, sheet_name)
                db.writetoDB(self.co_id, self.year, self.season, sheet_name, sheet_dict)
                return sheet_dict
            else: # not found in web
                return None
        result 
        return result

    def __genSoup(self, type):
        if type == 1:
            url = 'https://mops.twse.com.tw/server-java/t164sb01?step=3&SYEAR=' + str(self.year) + '&file_name=tifrs-fr1-m1-ci-cr-' + str(self.co_id) + '-' + str(self.year) + 'Q' + str(self.season) + '.html'
        elif type == 2:
            url = 'https://mops.twse.com.tw/server-java/t164sb01?step=3&SYEAR=' + str(self.year) + '&file_name=tifrs-fr1-m1-ci-ir-' + str(self.co_id) + '-' + str(self.year) + 'Q' + str(self.season) + '.html'
        elif type == 3:
            url = 'https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID='+ str(self.co_id) + '&SYEAR=' + str(self.year) + '&SSEASON=' + str(self.season) + '&REPORT_ID=C' 
        print(url)

        req = requests.get(url)
        req.encoding = req.apparent_encoding
        html = req.text
        self.__soup = BeautifulSoup(html, 'html.parser')