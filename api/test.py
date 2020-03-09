from django.test import TestCase
from .models import *
from api import views
from django.test import RequestFactory, Client
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from django.urls import reverse
import requests
import mysql.connector as mariadb
import mysql.connector.errors
import os
import random
from datetime import datetime, timedelta

# Load environmental variables
from dotenv import load_dotenv
load_dotenv()

# Create your tests here.

#Example company codes, based on the data provided in the data folder.
#ESPL27 = The Worst Generation  |   QXFF29 = Okama    | ZFHD93 = Brawndo
class CompanyAPITest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.client = Client()

        #Make this use the environment variables of your computer to connect to the database for testing.
        self.__connection = mariadb.connect(user= os.getenv('DB_USER'),
                                        password= os.getenv('DB_PASS'),
                                        database= os.getenv('DB_NAME'),
                                        host= os.getenv('DB_HOST'),
                                        port= os.getenv('DB_PORT'),
                                        auth_plugin='mysql_native_password')

    def tearDown(self):
        self.__connection.close()

    #Testing currency endpoints

    # def test_currency_list_of_currencies(self):
    #     #Test if the amount of data in response is equal to what is in the database
    #     response = requests.get("http://localhost:8000/api/currency/list/?page_size=100000000")
    #     responseLength = len(response.json())
    #     list = self.getListOfCurrencies(self.__connection)
    #
    #     #Test 10 random rows in response if they are in the database
    #     for i in range(10):
    #         rand = random.randint(0, responseLength-1)
    #         currency = response.json()[rand]["currency"]
    #         isInDatabase = self.isCurrencyInDatabase(self.__connection, currency)
    #         self.assertEqual(isInDatabase, True)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(responseLength, len(list))
    #
    # def test_currency_all_currency_prices(self):
    #     #Test if the amount of data in response is equal to what is in the database
    #     response = requests.get("http://localhost:8000/api/currency/?page_size=100000000")
    #     responseLength = len(response.json())
    #     list = self.getListOfCurrencyPrices(self.__connection)
    #
    #     #Test 10 random rows in response if they are in the database
    #     for i in range(10):
    #         rand = random.randint(0, responseLength-1)
    #         currency = response.json()[rand]["currency"]
    #         value = response.json()[rand]["value"]
    #         date = response.json()[rand]["date"]
    #         isInDatabase = self.isCurrencyPriceInDatabase(self.__connection, currency, value, date)
    #         self.assertEqual(isInDatabase, True)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(responseLength, len(list))
    #
    # def test_currency_by_currency(self):
    #     response = requests.get("http://localhost:8000/api/currency/currency=GBP/")
    #     responseLength = len(response.json())
    #     list = self.getCurrencyPricesByCurrency(self.__connection, "GBP")
    #
    #     #Test 10 random rows in response if they are in the database
    #     for i in range(10):
    #         rand = random.randint(0, responseLength-1)
    #         currency = response.json()[rand]["currency"]
    #         value = response.json()[rand]["value"]
    #         date = response.json()[rand]["date"]
    #         isInDatabase = self.isCurrencyPriceInDatabase(self.__connection, currency, value, date)
    #         self.assertEqual(isInDatabase, True)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(responseLength, len(list))
    #
    # def test_currency_by_year(self):
    #     response = requests.get("http://localhost:8000/api/currency/currency=GBP&year=2018/")
    #     responseLength = len(response.json())
    #     list = self.getCurrencyPricesByYear(self.__connection, "GBP", 2018)
    #
    #     #Test 10 random rows in response if they are in the database
    #     for i in range(10):
    #         rand = random.randint(0, responseLength-1)
    #         currency = response.json()[rand]["currency"]
    #         value = response.json()[rand]["value"]
    #         date = response.json()[rand]["date"]
    #         isInDatabase = self.isCurrencyPriceInDatabase(self.__connection, currency, value, date)
    #         self.assertEqual(isInDatabase, True)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(responseLength, len(list))
    #
    # def test_currency_by_month(self):
    #     response = requests.get("http://localhost:8000/api/currency/currency=GBP&year=2018&month=12/")
    #     responseLength = len(response.json())
    #     list = self.getCurrencyPricesByMonth(self.__connection, "GBP", 2018, 12)
    #
    #     #Test 10 random rows in response if they are in the database
    #     for i in range(10):
    #         rand = random.randint(0, responseLength-1)
    #         currency = response.json()[rand]["currency"]
    #         value = response.json()[rand]["value"]
    #         date = response.json()[rand]["date"]
    #         isInDatabase = self.isCurrencyPriceInDatabase(self.__connection, currency, value, date)
    #         self.assertEqual(isInDatabase, True)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(responseLength, len(list))
    #
    # def test_currency_by_day(self):
    #     response = requests.get("http://localhost:8000/api/currency/currency=GBP&year=2018&month=12&day=12/")
    #     responseLength = len(response.json())
    #     list = self.getCurrencyPricesByDay(self.__connection, "GBP", 2018, 12, 12)
    #
    #     #Test 10 random rows in response if they are in the database
    #     for i in range(10):
    #         rand = random.randint(0, responseLength-1)
    #         currency = response.json()[rand]["currency"]
    #         value = response.json()[rand]["value"]
    #         date = response.json()[rand]["date"]
    #         isInDatabase = self.isCurrencyPriceInDatabase(self.__connection, currency, value, date)
    #         self.assertEqual(isInDatabase, True)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(responseLength, len(list))
    #
    # def getListOfCurrencies(self, conn):
    #     cursor = conn.cursor()
    #     query = "SELECT * FROM currency"
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     return result
    #
    # def isCurrencyInDatabase(self, conn, currency):
    #     cursor = conn.cursor()
    #     query = "SELECT * FROM currency WHERE currency= \""+currency+"\""
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     if len(result) > 0:
    #         return True
    #     return False
    #
    # def getListOfCurrencyPrices(self, conn):
    #     cursor = conn.cursor()
    #     query = "SELECT * FROM currency_price"
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     return result
    #
    # def isCurrencyPriceInDatabase(self, conn, currency, value, date):
    #     cursor = conn.cursor()
    #     query = "SELECT * FROM currency_price WHERE currency_id=\""+currency+"\" AND value="+str(value)+"AND date= \""+date+"\""
    #     #print(query)
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     if len(result) > 0:
    #         return True
    #     return False
    #
    # def getCurrencyPricesByCurrency(self, conn, currency):
    #     cursor = conn.cursor()
    #     query = "SELECT * FROM currency_price WHERE currency_id=\""+currency+"\""
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     return result
    #
    # def getCurrencyPricesByYear(self, conn, currency, year):
    #     cursor = conn.cursor()
    #     query = "SELECT * FROM currency_price WHERE currency_id=\""+currency+"\" AND YEAR(date)="+str(2018)
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     return result
    #
    # def getCurrencyPricesByMonth(self, conn, currency, year, month):
    #     cursor = conn.cursor()
    #     query = "SELECT * FROM currency_price WHERE currency_id=\""+currency+"\" AND YEAR(date)="+str(2018)+" AND MONTH(date)="+str(12)
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     return result
    #
    # def getCurrencyPricesByDay(self, conn, currency, year, month, day):
    #     cursor = conn.cursor()
    #     query = "SELECT * FROM currency_price WHERE currency_id=\""+currency+"\" AND YEAR(date)="+str(2018)+" AND MONTH(date)="+str(12)+" AND DAY(date)="+str(12)
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     return result
    #
    # #Testing the company endpoints
    #
    # def test_company_list_of_companies(self):
    #     #Test if the amount of data in response is equal to what is in the database
    #     response = requests.get("http://localhost:8000/api/company/list/?page_size=100000000")
    #     responseLength = len(response.json())
    #     list = self.getListOfCompanies(self.__connection)
    #
    #     #Test 10 random rows in response if they are in the database
    #     for i in range(10):
    #         rand = random.randint(0, responseLength-1)
    #         id = response.json()[rand]["id"]
    #         name = response.json()[rand]["name"]
    #         isInDatabase = self.isCompanyInDatabase(self.__connection, id, name)
    #         self.assertEqual(isInDatabase, True)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(responseLength, len(list))
    #
    # def test_company_by_id(self):
    #     #Get the row of data for the company with ID ESPL27
    #     #API data
    #     # response = self.client.get(reverse("company_all"))
    #     # print(response.content)
    #
    #     response = requests.get("http://localhost:8000/api/company/id=178")
    #     #print(response.content) #chek against this
    #     self.assertEqual(response.status_code, 200) #checking the status code
    #     self.assertEqual(response.content, b'[{"id":178,"name":"The Worst Generation"}]')
    #
    #     #Database Data
    #     #Request data from the database here to compare against known quantities/values.
    #
    #     #Assert against manual check from the data file
    #     #Assert that the data matches whats expected from the test data.
    #
    # #The status code is still 200 but alma is not a companyID
    # def test_fake_company_by_id(self):
    #     #Test errorcodes in case of incorrect data
    #     response = requests.get("http://localhost:8000/api/company/id=4444444444444444444444444")
    #     #self.assertEqual(response.status_code, 404)
    #     if not response.json():
    #         isEmpty = True
    #     else:
    #         isEmpty = False
    #     self.assertEqual(isEmpty, True)
    #
    # def test_company_by_name(self):
    #     # TODO
    #     response = requests.get("http://localhost:8000/api/company/name=Cyberbiotics/")
    #     #print(response.content)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.content, b'[{"id":19,"name":"Cyberbiotics"}]')
    #
    # def getListOfCompanies(self, conn):
    #     cursor = conn.cursor()
    #     query = "SELECT id, name FROM company"
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     return result
    #
    # def isCompanyInDatabase(self, conn, id, name):
    #     cursor = conn.cursor()
    #     query = "SELECT * FROM company WHERE id=\""+str(id)+"\" AND name=\""+name+"\""
    #     #print(query)
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     if len(result) > 0:
    #         return True
    #     return False
    #
    # #Testing product endpoints
    #
    # def test_product_list_of_products(self):
    #     #Test if the amount of data in response is equal to what is in the database
    #     response = requests.get("http://localhost:8000/api/product/list/?page_size=100000000")
    #     responseLength = len(response.json())
    #     list = self.getListOfProducts(self.__connection)
    #
    #     #print(response.json())
    #     #Test 10 random rows in response if they are in the database
    #     for i in range(10):
    #         rand = random.randint(0, responseLength-1)
    #         id = response.json()[rand]["id"]
    #         name = response.json()[rand]["name"]
    #         isInDatabase = self.isProductInDatabase(self.__connection, id, name)
    #         self.assertEqual(isInDatabase, True)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(responseLength, len(list))
    #
    # def test_product_by_id(self):
    #     # TODO
    #     response = requests.get("http://localhost:8000/api/product/id=1/")
    #     #print(response.content)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.content, b'[{"id":1,"name":"Stocks"}]')
    #
    # def test_product_by_name(self):
    #     # TODO
    #     response = requests.get("http://localhost:8000/api/product/name=Stocks/")
    #     #print(response.content)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.content, b'[{"id":1,"name":"Stocks"}]')


#IT WORKS UNTIL HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



    # def test_product_by_soldby(self):
    #     response = requests.get("http://localhost:8000/api/product/soldby/id=61/")
    #     print(response)
    #     responseLength = len(response.json())
    #     inDatabase = self.getProductsByCompany(self.__connection, "61") #QLMY86
    #
    #     for i in range(10):
    #         rand = random.randint(0, responseLength-1)
    #         product_id = response.json()[rand]["product_id"]
    #         company_id = response.json()[rand]["company_id"]
    #         isInDatabase = self.isSoldByInDatabase(self.__connection, product_id, company_id)
    #         self.assertEqual(isInDatabase, True)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(responseLength, len(inDatabase))

    # def getProductsByCompany(self, conn, id):
    #     cursor = conn.cursor()
    #     query = "SELECT * FROM product_seller WHERE company_id=\""+id+"\""
    #     #print(query)
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     return result

    # def isSoldByInDatabase(self, conn, product_id, company_id):
    #     cursor = conn.cursor()
    #     query = "SELECT * FROM product_seller WHERE company_id="+str(company_id)+" AND product_id=\""+str(product_id)+"\""
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     if len(result) > 0:
    #         return True
    #     return False

    # def getListOfProducts(self, conn):
    #     cursor = conn.cursor()
    #     query = "SELECT id, name FROM product"
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     return result

    # def isProductInDatabase(self, conn, id, name):
    #     cursor = conn.cursor()
    #     query = "SELECT * FROM product WHERE id= \" "+str(id)+" \" AND name= \""+name+"\""
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     if len(result) > 0:
    #         return True
    #     return False

    # #Testing seller endpoints

    # def test_seller_list_of_sellers(self):
    #     #Test if the amount of data in response is equal to what is in the database
    #     response = requests.get("http://localhost:8000/api/seller/list/")
    #     responseLength = len(response.json())
    #     list = self.getListOfSellers(self.__connection)

    #     #Test 10 random rows in response if they are in the database
    #     for i in range(10):
    #         rand = random.randint(0, responseLength-1)
    #         company = response.json()[rand]["company"]
    #         product = response.json()[rand]["product"]
    #         isInDatabase = self.isSellerInDatabase(self.__connection, company, product)
    #         self.assertEqual(isInDatabase, True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(responseLength, len(list))
    # #def test_listOfSellers(self):
    # #in case of lists
    # #check the size as weel
    # #
    # #check a few random rows from the API and try to find them in what I got from the database

    # def test_seller_by_company(self):

    #     response = requests.get("http://localhost:8000/api/seller/company=178/")
    #     responseLength = len(response.json())
    #     list = self.getListOfSellersByCompany(self.__connection)

    #     #Test 10 random rows in response if they are in the database
    #     for i in range(10):
    #         rand = random.randint(0, responseLength-1)
    #         company = response.json()[rand]["company"]
    #         product = response.json()[rand]["product"]
    #         isInDatabase = self.isSellerInDatabase(self.__connection, company, product)
    #         self.assertEqual(isInDatabase, True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(responseLength, len(list))

    # def test_seller_by_product(self):
    #     response = requests.get("http://localhost:8000/api/seller/product=2/")
    #     responseLength = len(response.json())
    #     list = self.getListOfSellersByProduct(self.__connection)

    #     #Test 10 random rows in response if they are in the database
    #     for i in range(10):
    #         rand = random.randint(0, responseLength-1)
    #         company = response.json()[rand]["company"]
    #         product = response.json()[rand]["product"]
    #         isInDatabase = self.isSellerInDatabase(self.__connection, company, product)
    #         self.assertEqual(isInDatabase, True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(responseLength, len(list))

    # def getListOfSellers(self, conn):
    #     cursor = conn.cursor()
    #     query = "SELECT company_id, product_id FROM product_seller"
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     return result

    # def isSellerInDatabase(self, conn, companyID, productID):
    #     cursor = conn.cursor()
    #     query = "SELECT * FROM product_seller WHERE company_id="+str(companyID)+" AND product_id= "+str(productID)
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     if len(result) > 0:
    #         return True
    #     return False

    # def getListOfSellersByCompany(self, conn):
    #     cursor = conn.cursor()
    #     query = "SELECT company_id, product_id FROM product_seller WHERE company_id='178'"
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     return result

    # def getListOfSellersByProduct(self, conn):
    #     cursor = conn.cursor()
    #     query = "SELECT company_id, product_id FROM product_seller WHERE product_id='2'"
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     return result


    # def test_report_on_day(self):
    #     # TODO: check the numbers returned
    #     response = requests.get("http://localhost:8000/api/report/year=2020&month=03&day=05")
    #     print("holll")
    #     print(response.json()["num_of_new_trades"])
    #     print(self.num_of_n_trades(self.__connection))


    #     self.assertEqual(response.status_code, 200)

    # def num_of_n_trades(self, conn):
    #     cursor = conn.cursor()
    #     query = "SELECT COUNT(id) FROM trade WHERE date = \"2020-03-05\""
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     return result



    # def test_seller_by_company(self):

    #     response = requests.get("http://localhost:8000/api/seller/company=178/")
    #     responseLength = len(response.json())
    #     list = self.getListOfSellersByCompany(self.__connection)

    #     #Test 10 random rows in response if they are in the database
    #     for i in range(10):
    #         rand = random.randint(0, responseLength-1)
    #         company = response.json()[rand]["company"]
    #         product = response.json()[rand]["product"]
    #         isInDatabase = self.isSellerInDatabase(self.__connection, company, product)
    #         self.assertEqual(isInDatabase, True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(responseLength, len(list))


    # def test_create_trade_in_database(self):
    #     url = "http://localhost:8000/api/trade/create/"
    #     payload = 'selling_party=3&buying_party=17&product=9&quantity=160&maturity_date=2022-12-14&underlying_currency=AUD&notional_currency=GBP&strike_price=51&underlying_price=88'
    #     headers = {
    #       'Content-Type': 'application/x-www-form-urlencoded'
    #     }
    #     response = requests.request("POST", url, headers=headers, data = payload)
    #     self.assertEqual(response.status_code, 200)
    #     #test if created trade is in the database

    #     self.assertEqual(True, self.createTradeInDatabase(self.__connection, 14,12,2022,3,17,9,160,"AUD","GBP",51,88))
    #     self.deleteAddedTrade(self.__connection)

    # def test_create_trade_positive_quantity(self):
    #     url = "http://localhost:8000/api/trade/create/"
    #     payload = 'selling_party=3&buying_party=17&product=9&quantity=-160&maturity_date=2022-12-14&underlying_currency=AUD&notional_currency=GBP&strike_price=51&underlying_price=17.21'
    #     headers = {
    #       'Content-Type': 'application/x-www-form-urlencoded'
    #     }
    #     response = requests.request("POST", url, headers=headers, data = payload)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(False, self.createTradeInDatabase(self.__connection, 14,12,2022,3,17,9,-160,"AUD","GBP",51,17.21))

    # def test_create_trade_notnull_quantity(self):
    #     url = "http://localhost:8000/api/trade/create/"
    #     payload = 'selling_party=3&buying_party=17&product=9&quantity=0&maturity_date=2022-12-14&underlying_currency=AUD&notional_currency=GBP&strike_price=51&underlying_price=17.21'
    #     headers = {
    #       'Content-Type': 'application/x-www-form-urlencoded'
    #     }
    #     response = requests.request("POST", url, headers=headers, data = payload)
    #     print("response content:")
    #     print(response.content)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(False, self.createTradeInDatabase(self.__connection, 14,12,2022,3,17,9,0,"AUD","GBP",51,17.21))

    # def test_create_trade_positive_strike_price(self):
    #     url = "http://localhost:8000/api/trade/create/"
    #     payload = 'selling_party=3&buying_party=17&product=9&quantity=160&maturity_date=2022-12-14&underlying_currency=AUD&notional_currency=GBP&strike_price=-51&underlying_price=17.21'
    #     headers = {
    #       'Content-Type': 'application/x-www-form-urlencoded'
    #     }
    #     response = requests.request("POST", url, headers=headers, data = payload)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(False, self.createTradeInDatabase(self.__connection, 14,12,2022,3,17,9,160,"AUD","GBP",-51,17.21))

    # def test_create_trade_notnull_strike_price(self):
    #     url = "http://localhost:8000/api/trade/create/"
    #     payload = 'selling_party=3&buying_party=17&product=9&quantity=160&maturity_date=2022-12-14&underlying_currency=AUD&notional_currency=GBP&strike_price=0&underlying_price=17.21'
    #     headers = {
    #       'Content-Type': 'application/x-www-form-urlencoded'
    #     }
    #     response = requests.request("POST", url, headers=headers, data = payload)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(False, self.createTradeInDatabase(self.__connection, 14,12,2022,3,17,9,160,"AUD","GBP",0,17.21))

    # def test_create_trade_positive_underlying_price(self):
    #     url = "http://localhost:8000/api/trade/create/"
    #     payload = 'selling_party=3&buying_party=17&product=9&quantity=160&maturity_date=2022-12-14&underlying_currency=AUD&notional_currency=GBP&strike_price=51&underlying_price=-17.21'
    #     headers = {
    #       'Content-Type': 'application/x-www-form-urlencoded'
    #     }
    #     response = requests.request("POST", url, headers=headers, data = payload)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(False, self.createTradeInDatabase(self.__connection, 14,12,2022,3,17,9,160,"AUD","GBP",51,-17.21))

    # def test_create_trade_notnull_underlying_price(self):
    #     url = "http://localhost:8000/api/trade/create/"
    #     payload = 'selling_party=3&buying_party=17&product=9&quantity=160&maturity_date=2022-12-14&underlying_currency=AUD&notional_currency=GBP&strike_price=51&underlying_price=0'
    #     headers = {
    #       'Content-Type': 'application/x-www-form-urlencoded'
    #     }
    #     response = requests.request("POST", url, headers=headers, data = payload)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(False, self.createTradeInDatabase(self.__connection, 14,12,2022,3,17,9,160,"AUD","GBP",51,0))

    # def test_delete_trade_from_database(self):
    #     tradeids = self.addTrade(self.__connection, "2020-03-07", "2022-12-14",33.6,3,17,9,160,"AUD","GBP",51,17.21)
    #     tradeid=tradeids[-1][0]
    #     print(tradeid)
    #     url = "http://localhost:8000/api/trade/delete/"
    #     payload = 'trade_id='+str(tradeid)
    #     headers = {
    #       'Content-Type': 'application/x-www-form-urlencoded'
    #     }
    #     response = requests.request("POST", url, headers=headers, data = payload)
    #     print("WOOOO")
    #     print(response.content)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(True, self.deletedTradeInDatabase(self.__connection, tradeid))
    #     self.deleteAddedDeletedTrade(self.__connection,tradeid)

    def createTradeInDatabase(self, conn, maturity_day, maturity_month, maturity_year, selling_party_id, buying_party_id, product_id, quantity, underlying_currency_id, notional_currency_id, strike_price, underlying_price):
        cursor = conn.cursor()
        query = "SELECT * FROM trade WHERE DAY(maturity_date)="+str(maturity_day)+" AND MONTH(maturity_date)="+str(maturity_month)+" AND YEAR(maturity_date)="+str(maturity_year)+" AND selling_party_id="+str(selling_party_id)+" AND buying_party_id="+str(buying_party_id)+" AND product_id="+str(product_id)+" AND quantity="+str(quantity)+" AND  underlying_currency_id=\""+underlying_currency_id+"\" AND notional_currency_id=\""+notional_currency_id+"\" AND strike_price="+str(strike_price)+" AND underlying_price="+str(underlying_price)
        # print(strike_price)
        # print(query)
        cursor.execute(query)
        result = cursor.fetchall()
        # print("result")
        # print(result)
        if not result:
            return False
        return True

    # def deletedTradeInDatabase(self, conn, tradeid):
    #     cursor = conn.cursor()
    #     query = "SELECT * FROM deleted_trade WHERE trade_id_id ="+str(tradeid)
    #     print("ALMAAA")
    #     print(query)
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     print("result")
    #     print(result)
    #     if not result:
    #         return False
    #     return True

    # def deleteAddedTrade(self, conn):
    #     cursor = conn.cursor()
    #     query = "DELETE FROM erroneous_trade_attribute WHERE trade_id_id IN (SELECT id FROM trade WHERE DAY(maturity_date)=14 AND MONTH(maturity_date)=12 AND YEAR(maturity_date)=2022 AND selling_party_id=3 AND buying_party_id=17 AND product_id=9 AND quantity=160 AND  underlying_currency_id=\"AUD\" AND notional_currency_id=\"GBP\" AND strike_price=51 AND underlying_price=88) "
    #     cursor.execute(query)
    #     self.__connection.commit()

    #     print(cursor.rowcount)
    #     cursor = conn.cursor()
    #     query = "DELETE FROM trade WHERE DAY(maturity_date)=14 AND MONTH(maturity_date)=12 AND YEAR(maturity_date)=2022 AND selling_party_id=3 AND buying_party_id=17 AND product_id=9 AND quantity=160 AND  underlying_currency_id=\"AUD\" AND notional_currency_id=\"GBP\" AND strike_price=51 AND underlying_price=88"
    #     cursor.execute(query)
    #     self.__connection.commit()
    #     #
    #     # print(cursor.rowcount)
    #     # cursor = conn.cursor()
    #     # query = "DELETE FROM trade WHERE id = "+str(tradeid)
    #     # cursor.execute(query)
    #     # self.__connection.commit()

    #     print(cursor.rowcount)


    # def deleteAddedDeletedTrade(self, conn, tradeid):
    #     cursor = conn.cursor()
    #     query = "DELETE FROM erroneous_trade_attribute WHERE trade_id_id IN (SELECT id FROM trade WHERE DAY(maturity_date)=14 AND MONTH(maturity_date)=12 AND YEAR(maturity_date)=2022 AND selling_party_id=3 AND buying_party_id=17 AND product_id=9 AND quantity=160 AND  underlying_currency_id=\"AUD\" AND notional_currency_id=\"GBP\" AND strike_price=51 AND underlying_price=17.21) "
    #     cursor.execute(query)
    #     self.__connection.commit()

    #     cursor = conn.cursor()
    #     query = "DELETE FROM deleted_trade WHERE trade_id_id="+str(tradeid)
    #     cursor.execute(query)
    #     self.__connection.commit()

    #     print(cursor.rowcount)
    #     cursor = conn.cursor()
    #     query = "DELETE FROM trade WHERE id = "+str(tradeid)
    #     cursor.execute(query)
    #     self.__connection.commit()

    #     print(cursor.rowcount)


    def addTrade(self, conn, date, maturity_date, notional_amount, selling_party_id, buying_party_id, product_id, quantity, underlying_currency_id, notional_currency_id, strike_price, underlying_price):
        cursor = conn.cursor()
        query = "INSERT INTO trade(date, maturity_date, notional_amount, selling_party_id, buying_party_id, product_id, quantity, underlying_currency_id, notional_currency_id, strike_price, underlying_price) VALUES (\""+date+"\", \""+maturity_date+"\", "+str(notional_amount)+", "+str(selling_party_id)+", "+str(buying_party_id)+", "+str(product_id)+","+str(quantity)+",\""+underlying_currency_id+"\",\""+notional_currency_id+"\", "+str(strike_price)+"," +str(underlying_price)+")"
        # print("addddddddd")
        # print(query)
        cursor.execute(query)
        self.__connection.commit()

        cursor = conn.cursor()
        query = "SELECT id FROM trade WHERE maturity_date=\""+maturity_date+"\" AND selling_party_id="+str(selling_party_id)+" AND buying_party_id="+str(buying_party_id)+" AND product_id="+str(product_id)+" AND quantity="+str(quantity)+" AND  underlying_currency_id=\""+underlying_currency_id+"\" AND notional_currency_id=\""+notional_currency_id+"\" AND strike_price="+str(strike_price)+" AND underlying_price="+str(underlying_price)
        # print("QUERY")
        # print(query)
        cursor.execute(query)
        result = cursor.fetchall()
        # print(result)
        return result



    # def test_trade_by_ID(self):
    #     response = requests.get("http://localhost:8000/api/trade/id=61")
    #     self.assertEqual(response.status_code, 200)
    #     cursor = self.__connection.cursor()
    #     query = "SELECT * FROM trade WHERE id=61"
    #     cursor.execute(query)
    #     result = cursor.fetchall()

    #     date = response.json()[0]["date"]
    #     #datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
    #     notional_amount = response.json()[0]["notional_amount"]
    #     quantity = response.json()[0]["quantity"]
    #     maturity_date = response.json()[0]["maturity_date"]
    #     underlying_price = response.json()[0]["underlying_price"]
    #     strike_price = response.json()[0]["strike_price"]
    #     product= response.json()[0]["product"]
    #     buying_party = response.json()[0]["buying_party"]
    #     selling_party = response.json()[0]["selling_party"]
    #     notional_currency = response.json()[0]["notional_currency"]
    #     underlying_currency = response.json()[0]["underlying_currency"]

    #     #self.assertEqual(result[0][1], date)
    #     self.assertEqual(result[0][2], notional_amount)
    #     self.assertEqual(result[0][3], quantity)
    #     #self.assertEqual(result[0][4], maturity_date)
    #     self.assertEqual(result[0][5], underlying_price)
    #     self.assertEqual(result[0][6], strike_price)
    #     self.assertEqual(result[0][7], buying_party)
    #     self.assertEqual(result[0][8], notional_currency)
    #     self.assertEqual(result[0][9], product)
    #     self.assertEqual(result[0][10], selling_party)
    #     self.assertEqual(result[0][11], underlying_currency)

    # def test_trade_recent(self):
    #     response = requests.get("http://localhost:8000/api/trade/recent")
    #     cursor = self.__connection.cursor()
    #     query="SELECT id FROM trade ORDER BY date DESC LIMIT 12"
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     # print("kukucs")
    #     # print(result)
    #     # print(response.json())

    #     self.assertEqual(result[0][0], response.json()[0]["id"])
    #     self.assertEqual(result[1][0], response.json()[1]["id"])
    #     self.assertEqual(result[2][0], response.json()[2]["id"])
    #     self.assertEqual(result[3][0], response.json()[3]["id"])
    #     self.assertEqual(result[4][0], response.json()[4]["id"])
    #     self.assertEqual(result[5][0], response.json()[5]["id"])
    #     self.assertEqual(result[6][0], response.json()[6]["id"])
    #     self.assertEqual(result[7][0], response.json()[7]["id"])
    #     self.assertEqual(result[8][0], response.json()[8]["id"])
    #     self.assertEqual(result[9][0], response.json()[9]["id"])
    #     self.assertEqual(result[10][0], response.json()[10]["id"])
    #     self.assertEqual(result[11][0], response.json()[11]["id"])

    # def test_trade_total(self):
    #     response = requests.get("http://localhost:8000/api/trade/total")
    #     cursor = self.__connection.cursor()
    #     query="SELECT COUNT(id) FROM trade"
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     self.assertEqual(response.json()["total_trades"],result[0][0])



    def test_edit_trade_in_database(self):
        tradeids=self.addTrade(self.__connection, "2020-03-06", "2020-10-06", 34, 3,9,25,100, "GBP", "USD", 12, 18.5)
        tradeid=tradeids[-1][0]
        url = "http://localhost:8000/api/trade/edit/"
        payload = 'trade_id='+str(tradeid)+'&quantity=28'
        headers = {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data = payload)
        # print(response.content)
        self.assertEqual(response.status_code, 200)
        #test if created trade is in the database

        self.assertEqual(True, self.createTradeInDatabase(self.__connection, 6,10,2020,3,9,25,100, "GBP", "USD", 12, 18.5))
        #self.assertEqual(True, self.editedTradeInDatabase(self.__connection, tradeid))
        x=self.editedTradeInDatabase(self.__connection, tradeid)
        # print(x)
        # self.deleteAddedEditedTrade(self.__connection, tradeid)

    def editedTradeInDatabase(self, conn, tradeid):
        print(tradeid)
        query = f"SELECT * FROM edited_trade WHERE trade_id_id = {tradeid}"
        print("Banan")
        print(query)
        self.tearDown()
        self.setUp()
        cursor = self.__connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        print("result")
        print(result)
        if not result:
            return False
        return True

    def deleteAddedEditedTrade(self, conn, tradeid):
        cursor = conn.cursor()
        query = "DELETE FROM erroneous_trade_attribute WHERE trade_id_id IN (SELECT id FROM trade WHERE DAY(maturity_date)=14 AND MONTH(maturity_date)=12 AND YEAR(maturity_date)=2022 AND selling_party_id=3 AND buying_party_id=17 AND product_id=9 AND quantity=160 AND  underlying_currency_id=\"AUD\" AND notional_currency_id=\"GBP\" AND strike_price=51 AND underlying_price=17.21) "
        cursor.execute(query)
        self.__connection.commit()

        cursor = conn.cursor()
        query = "DELETE FROM edited_trade WHERE trade_id_id="+str(tradeid)
        # print(query)
        cursor.execute(query)
        self.__connection.commit()

        # print(cursor.rowcount)
        cursor = conn.cursor()
        query = "DELETE FROM trade WHERE id = "+str(tradeid)
        cursor.execute(query)
        self.__connection.commit()

        print(cursor.rowcount)





        #     #Get the row of data for the company with ID ESPL27
        #     #API data
        #     #
        #     # print(response.content)
        #
        #     response = requests.get("http://localhost:8000/api/company/id=178")
        #     #print(response.content) #chek against this
        #     self.assertEqual(response.status_code, 200) #checking the status code
        #     self.assertEqual(response.content, b'[{"id":178,"name":"The Worst Generation"}]')


    #"do requests that are fake, check if the error number is what I expect"

