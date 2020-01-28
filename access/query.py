import requests
import json

class API:
    def __request(self, method):
        try:
            print(self.__prefix+method)
            r = requests.get(url=self.__prefix+method)
            return r.json()
        except json.decoder.JSONDecodeError:
            raise RuntimeError("Didn't reach a valid endpoint - check requested URL.")

    def __genArgs(self, dic):
        args = [x + '=' + dic[x] for x in dic.keys() if dic[x] != None]
        url_args = '&'.join(args)
        if len(url_args) > 0 :
            url_args += '/'
        return url_args
    
    def getCurrencyList(self):
        return self.__request('currency/list/')
        
    def getCurrency(self, currency=None, year=None, month=None, day=None):
        dic = {'currency' : currency, 'year' : year, 'month' : month, 'day' : day}
        url_args = self.__genArgs(dic)
        return self.__request(f'currency/{url_args}')
    
    def getCompanyList(self):
        return self.__request('company/list/')
    
    def getCompany(self, id=None, name=None):
        dic = {'id' : id, 'name' : name}
        url_args = self.__genArgs(dic)
        return self.__request(f'company/{url_args}')
    
    def getProductList(self):
        return self.__request('product/list/')
    
    def getProduct(self, id=None, name=None):
        dic = {'id' : id, 'name' : name}
        url_args = self.__genArgs(dic)
        return self.__request(f'product/{url_args}')
    
    def getSellerList(self):
        return self.__request('seller/list/')
    
    def getSeller(self, company=None, product=None):
        dic = {'company' : company, 'product' : product}
        url_args = self.__genArgs(dic)
        return self.__request(f'seller/{url_args}')
    
    def getStock(self, company=None, year=None, month=None, day=None):
        dic = {'company' : company, 'year' : year, 'month' : month, 'day' : day}
        url_args = self.__genArgs(dic)
        return self.__request(f'stock/{url_args}')
        
    def getTrade(self, id=None, buyer=None, seller=None, year=None, month=None,
                       day=None, maturity_year=None, maturity_month=None,
                       maturity_day=None):
        dic = { 'id' : id, 'buyer' : buyer, 'seller' : seller, 'year' : year, 'month' : month,
                'day' : day, 'maturity_year' : maturity_year,
                'maturity_month' : maturity_month, 'maturity_day' : maturity_day}
        url_args = self.__genArgs(dic)
        return self.__request(f'trade/{url_args}')
    
    def __init__(self):
        self.__prefix = 'http://localhost:8000/api/'
    
if __name__ == '__main__':
    x = API()
    # print(x.getCurrencyList())
    # print(x.getCurrency(currency='GBP', year='2019', month='01'))
    # print(x.getCompanyList())
    # print(x.getCompany(name='Germa 66'))
    # print(x.getProductList())
    # print(x.getProduct(id='1'))
    # print(x.getSellerList())
    # print(x.getSeller(product='2'))
    # print(x.getStock(company='NCCX02', year='2019', month='01', day='01'))
    # print(x.getTrade(maturity_year="2024", maturity_month="01", maturity_day="01"))
