import os, csv, datetime
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
import re
class Importer:
    
    def __start(self, path, ids, funcs, auto_pk=False, counter=1):
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            data, seen = [], []
            for row in csv_reader:
                new = {}
                for id, item, func in zip(ids, row, funcs):
                    val = func(item)
                    if val != 'null':
                        new[id] = val
                if new not in seen and len(new) > 0:
                    if auto_pk:
                        new['id'] = counter
                        counter += 1
                    data.append(new)
        if auto_pk:
            return data, counter
        return data
        
    def __find(self, json, field, target, val):
        return [obj for obj in json if obj[field]==val][0][target]
    
    def __productID(self, name):
        return self.__find(self.__productJSON, 'name', 'id', name)
        
    def __date(self, date):
        lst = [int(x) for x in re.split("[' ','/', ':']", date)]
        if len(lst) > 3:
            return datetime.datetime(lst[2], lst[1], lst[0], lst[3], lst[4])
        else:
            return datetime.datetime(lst[2], lst[1], lst[0])
            
    def __traverse(self, directory, func):
        base = '../data/'+directory
        ignore = ['.DS_Store', '2010', '2011', '2012', '2013', '2014', '2015', 
                    '2016', '2017', '2018']
        lst = lambda path : [x for x in os.listdir(path) if x not in ignore]
        
        counter = 1
        for year in lst(base):
            for month in lst(base+year):
                for day in lst(base+year+'/'+month):
                    print(base+year+'/'+month+'/'+day)
                    counter = func(base+year+'/'+month+'/'+day, counter)
    
    def __noOp(self, val):
        return val

    def __insert(self, coll, data):
        try:
            coll.insert_many(data)
        except BulkWriteError as bwe:
            print(bwe.details)
            exit()

    def __product(self):
        ids = ['name']
        funcs = [self.__noOp]
        data, _ = self.__start('../data/productSellers.csv', ids, funcs, 
                                auto_pk=True)
        return data

    def product(self):
        coll = self.__db["data"]["product"]
        self.__insert(coll, self.__productJSON)
    
    def seller(self):
        coll = self.__db["data"]["product_seller"]
        ids = ['product_id', 'company_id']

        funcs = [self.__productID, self.__noOp]

        data, _ = self.__start('../data/productSellers.csv', ids, funcs, 
                                auto_pk=True)
        self.__insert(coll, data)
    
    def company(self):
        coll = self.__db["data"]["company"]
        ids = ['name', 'id']
        
        funcs = [self.__noOp, self.__noOp]
        
        data = self.__start('../data/companyCodes.csv', ids, funcs)
        self.__insert(coll, data)
    
    def currency(self):
        coll = self.__db["data"]["currency"]
        ids = ['currency']
        
        funcs = [self.__noOp]
        
        data = self.__start('../data/currencies.csv', ids, funcs)
        self.__insert(coll, data)

    def __currency(self, dir, counter):
        coll = self.__db["data"]["currency_price"]
        ids = ['date', 'currency_id', 'value']
        
        funcs = [self.__date, self.__noOp, self.__noOp]
        
        data, counter = self.__start(dir, ids, funcs, counter=counter, 
                                    auto_pk=True)
        self.__insert(coll, data)

        return counter
        
    def currency_value(self):
        self.__traverse('currencyValues/', self.__currency)
    
    def __trade(self, dir, funcs):
        coll = self.__db["data"]["trade"]
        ids = ['date', 'id', 'product_id', 'buying_party_id', 
                'selling_party_id', 'notional_amount', 'notional_currency_id', 
                'quantity', 'maturity_date', 'underlying_price', 
                'underlying_currency_id', 'strike_price']
        
        funcs = [self.__date, self.__noOp, self.__productID, self.__noOp, 
                self.__noOp, self.__noOp, self.__noOp, self.__noOp, 
                self.__date, self.__noOp, self.__noOp, self.__noOp]
        
        data = self.__start(dir, ids, funcs)
        self.__insert(coll, data)
        
    def trade(self):
        self.__traverse('derivativeTrades/', self.__trade)

    def __stock_price(self, dir, counter):
        coll = self.__db["data"]["stock_price"]
        ids = ['date', 'company_id', 'value']
        
        funcs = [self.__date, self.__noOp, self.__noOp]
        
        data, counter = self.__start(dir, ids, funcs, counter=counter, 
                                    auto_pk=True)
        self.__insert(coll, data)

        return counter

    def stock_price(self):
        self.__traverse('stockPrices/', self.__stock_price)
    
    def __product_price(self, dir, counter):
        coll = self.__db["data"]["product_price"]
        ids = ['date', 'product_id', 'value']
        
        funcs = [self.__date, self.__productID, self.__noOp]
        
        data, counter = self.__start(dir, ids, funcs, counter=counter, 
                                    auto_pk=True)
        self.__insert(coll, data)

        return counter

    def product_price(self):
        self.__traverse('productPrices/', self.__product_price)
    
    def __init__(self):
        self.__db = MongoClient("mongodb+srv://root:root" +
                                "@cs261-qeru3.azure.mongodb.net/data")
        self.__productJSON = self.__product()
        
if __name__ == '__main__':
    im = Importer()
    im.product()
    im.company()
    im.seller()
    im.currency()
    im.currency_value()
    im.trade()
    im.stock_price()
    im.product_price()