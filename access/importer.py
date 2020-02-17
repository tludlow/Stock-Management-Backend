import os, csv, datetime
from functools import partial
from os.path import join, dirname
from dotenv import load_dotenv
import mysql.connector as mariadb
import mysql.connector.errors
import re


class Importer:
    
    def __start(self, path, stmt):
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                new_stmt = stmt
                for item in row:
                    new_stmt = partial(new_stmt, item)
                try:
                    self.__cursor.execute(new_stmt())
                except mysql.connector.errors.IntegrityError:
                    pass
        self.__connection.commit()
        
    def __start_and_save(self, path, stmt, ids):
        data = []
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            auto_id = 1
            for row in csv_reader:
                new_stmt = stmt
                new_stmt = partial(new_stmt, auto_id)
                new = {'id': auto_id}
                for item, id in zip(row, ids):
                    new_stmt = partial(new_stmt, item)
                    new[id] = item
                auto_id += 1
                data.append(new)
                try:
                    self.__cursor.execute(new_stmt())
                except mysql.connector.errors.IntegrityError:
                    pass
        self.__connection.commit()
        return data
        
    def __find(self, json, field, target, val):
        return [obj for obj in json if obj[field]==val][0][target]
    
    def __productID(self, name):
        return self.__find(self.__products, 'name', 'id', name)
        
    def __date(self, date):
        lst = [int(x) for x in re.split("[' ','/', ':']", date)]
        if len(lst) > 3:
            return datetime.datetime(lst[2], lst[1], lst[0], lst[3], lst[4])
        else:
            return datetime.datetime(lst[2], lst[1], lst[0])
            
    def __traverse(self, directory, func):
        base = '../data/'+directory
        ignore = ['.DS_Store']
        lst = lambda path : [x for x in os.listdir(path) if x not in ignore]
        
        for year in lst(base):
            for month in lst(base+year):
                for day in lst(base+year+'/'+month):
                    print(base+year+'/'+month+'/'+day)
                    counter = func(base+year+'/'+month+'/'+day)

    def product(self):
        stmt = lambda x, y : (
            f"""
            INSERT INTO group23db.product 
                (id, name) 
            VALUES 
                ("{x}", "{y}");
            """)
        self.__products = self.__start_and_save('../data/product.csv', stmt, 
                                                ['name'])
    
    def seller(self):
        stmt = lambda x, y : (
            f"""
            INSERT INTO group23db.product_seller 
                (product_id, company_id) 
            VALUES 
                ("{self.__productID(x)}", "{y}");
            """)
        self.__start('../data/productSellers.csv', stmt)
    
    def company(self):
        stmt = lambda x, y : (
            f"""
            INSERT INTO group23db.company 
                (name, id) 
            VALUES 
                ("{x}", "{y}");
            """)
        self.__start('../data/companyCodes.csv', stmt)
    
    def currency(self):
        stmt = lambda x : (
            f"""
            INSERT INTO group23db.currency 
                (currency) 
            VALUES 
                ("{x}");
            """)
        self.__start('../data/currencies.csv', stmt)

    def __currency(self, dir):
        stmt = lambda x, y, z : (
            f"""
            INSERT INTO group23db.currency_price 
                (date, currency_id, value) 
            VALUES 
                ("{self.__date(x)}", "{y}", "{z}");
            """)
        self.__start(dir, stmt)

    def currency_value(self):
        self.__traverse('currencyValues/', self.__currency)
    
    def __trade(self, dir):
        stmt = lambda x, y, z, a, b, c, d, e, f, g, h, i : (
            f"""
            INSERT INTO group23db.trade 
                (date, id, product_id, buying_party_id, selling_party_id, 
                notional_amount, notional_currency_id, quantity, 
                maturity_date, underlying_price, underlying_currency_id, 
                strike_price) 
            VALUES 
                ("{self.__date(x)}", "{y}", "{self.__productID(z)}", "{a}", 
                "{b}", "{c}", "{d}", "{e}", "{self.__date(f)}", "{g}", 
                "{h}", "{i}");
            """)
        self.__start(dir, stmt)
        
    def trade(self):
        self.__traverse('derivativeTrades/', self.__trade)

    def __stock_price(self, dir):
        stmt = lambda x, y, z : (
            f"""
            INSERT INTO group23db.stock_price 
                (date, company_id, value) 
            VALUES 
                ("{self.__date(x)}", "{y}", "{z}");
            """)
        self.__start(dir, stmt)

    def stock_price(self):
        self.__traverse('stockPrices/', self.__stock_price)
    
    def __product_price(self, dir):
        stmt = lambda x, y, z : (
            f"""
            INSERT INTO group23db.product_price 
                (date, product_id, value) 
            VALUES 
                ("{self.__date(x)}", "{self.__productID(y)}", "{z}");
            """)
        self.__start(dir, stmt)

    def product_price(self):
        self.__traverse('productPrices/', self.__product_price)
    
    def close(self):
        self.__cursor.close()
        self.__connection.close()
        
    def __init__(self):
        dotenv_path = join(dirname(__file__), '../backend/.env')
        load_dotenv(dotenv_path)
        self.__connection = mariadb.connect(user=os.environ.get('DB_USER'), 
                                            password=os.environ.get('DB_PASSWORD'),
                                            database=os.environ.get('DB_NAME'), 
                                            host=os.environ.get('DB_HOST'),
                                            auth_plugin='mysql_native_password')
        self.__cursor = self.__connection.cursor()
        
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
    im.close()
