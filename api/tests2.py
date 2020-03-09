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

from dotenv import load_dotenv
load_dotenv()

class IntegrationTests(TestCase):
    def setUp(self):
        """Create the connection to the database"""
        self.client = Client()
        self.__connection = mariadb.connect(user = os.getenv('DB_USER'),
                                            password = os.getenv('DB_PASS'),
                                            database = os.getenv('DB_NAME'),
                                            host = os.getenv('DB_HOST'),
                                            port = os.getenv('DB_PORT'),
                                            auth_plugin = 'mysql_native_password')
        self.BASE_URL = "http://localhost:8000/"
        self.url = lambda x : self.BASE_URL + x

    def create_trade(self, vals):
        """Create a new trade.

        Args:
            vals ([str]): Values of the new trade
        
        Returns:
            bool: If the trade was successfully created
            (int, {key : value}) : attributes of the created trade
        """
        # Create a new trade
        create_url = self.url("api/trade/create/")
        tags = ['selling_party', 'buying_party', 'product' , 'quantity',
                'maturity_date', 'underlying_currency', 'notional_currency', 
                'strike_price', 'underlying_price']
        args = dict(zip(tags, vals))
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = requests.request("POST", create_url, headers=headers, data=args)

        # Ensure trade creation was successful
        if data.status_code != 200:
             return False, None
        
        json = data.json()

        # Ensure a trade id was returned
        trade_id = json.get('trade_id', None)
        print(data.content.decode('utf-8'))
        if trade_id is None:
            return False, None

        return True, (trade_id, json['data'][0])

    def retrieve_trade(self, trade_id):
        """Returns a trade given a trade ID.
        Args:
            trade_id (int): Values of the new trade
        
        Returns:
            bool: If the trade with the given ID is returned
        """
         # Request the trade using the trade id
        get_url = self.url(f"api/trade/id={trade_id}")
        saved_trade = requests.get(get_url)
        
        # Ensure the request was successful 
        if saved_trade.status_code != 200:
            return False
        
        # Check the response
        data = saved_trade.json()
        if len(data) < 1:
            return False
        
        saved_trade_json = data[0]
        exists = saved_trade_json.get('id', None)
        if exists != None:
            return saved_trade_json
        
        return False

    def verify_trade(self, trade_id, args):
        """Compares a trade to an existing one.

        Args:
            trade_id (int): Values of the new trade
            args ({key: value}): Trade attributes
        
        Returns:
            bool: If the trade matches that expected values
        """

        # Check the values match those inputted
        saved_trade_json = self.retrieve_trade(trade_id)

        for i in args.keys():
            returned = saved_trade_json.get(i, None)
            if returned is None or args[i] != returned:
                return False
        
        return True
    
    def edit_trade(self, args):
        """Edit an exising trade.

        Args:
            args ({key : value}): Arguments for post request
        
        Returns:
            int: ID of the created trade
            {key: value} : attributes and values of trade
        """
        # Edit a new trade
        edit_url = self.url("api/trade/edit/")
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = requests.request("POST", edit_url, headers=headers, data=args)

        # Ensure trade creation was successful
        if data.status_code != 200:
             return False
        
        # Ensure trade returned matches that of the data entered
        json = data.json()
        for i in [x for x in args.keys() if x not in ['trade_id']]:
            returned = json["trade"][0].get(i, None)
            if returned is None or args[i] != returned:
                return False

        return True

    def delete_trade(self, trade_id):
        """Deletes a trade with the gives trade ID.

        Args:
            trade_id (int): ID of the trade.
        
        Returns:
            bool: If the trade is successfully deleted

        Raises:
            AssertionError: If the trade wasn't successfully deleted
        """
        # Request the trade using the trade id
        delete_url = self.url(f"api/trade/delete/")
        args = {'trade_id' : trade_id}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = requests.request("POST", delete_url, headers=headers, data=args)

        # Ensure trade creation was successful
        return data.status_code == 200

    def generate_report(self, year, month, day):
        """Deletes a trade with the gives trade ID.

        Args:
            trade_id (int): ID of the trade.
        
        Returns:
            bool: If the trade is successfully deleted

        Raises:
            AssertionError: If the trade wasn't successfully deleted
        """
        # Request the report using the date
        report_url = self.url(f"api/report/year={year}&month={month}&day={day}")
        data = requests.get(report_url)

        # Ensure report was successfully returned
        if data.status_code != 200:
            return False, None
        else: 
            return True, data.json()

    def number_of_trades(self):
        """Returns the total number of trades

        Returns:
            int: Number of trades
        """
        num_of_trades_url = self.url("api/trade/total/")
        num_of_trades = requests.get(num_of_trades_url).json()
        return num_of_trades['total_trades']

    def create_valid_trade(self):
        """Creates a valid trade within the system

        Returns:
            int: ID of the created trade
            {key: value} : attributes and values of trade
        """
        valid_maturity = datetime.now() + timedelta(days=365)
        maturity = valid_maturity.strftime("%Y-%m-%d")
        valid = ['1', '17', '9', '16', maturity, 'AUD', 'GBP',
                 '51', '17.21']
        return self.create_trade(valid)
    
    def create_invalid_trade(self):
        """Creates a valid trade within the system

        Returns:
            int: ID of the created trade
            {key: value} : attributes and values of trade
        """
        invalid_maturity = datetime.now() - timedelta(days=365)
        maturity = invalid_maturity.strftime("%Y-%m-%d")
        invalid = ['1', '17', '9', '16', maturity, 'AUD', 'GBP',
                   '51', '17.21']
        return self.create_trade(invalid)

    def test_trade_creation(self):
        """Tests trades are successfully created.

        Raises:
            AssertionError: If a specific test fails
        """
        # Valid Trade
        success, data = self.create_valid_trade()
        # Ensure the trade was successfully created
        assert success, \
            "Trade was not successfully created"
        
        trade_id, args = data

        # Ensure the trade stored matches the arguments given
        assert self.verify_trade(trade_id, args), \
            "Created trade doesn't exist"
    
        # Invalid Trade - Unit tests have already verfied invalid inputs are 
        # rejected, therefore, it is sufficient to use one invalid input to 
        # determine whether invalid trades are returned by the system

        # Get the number of trades 
        before = self.number_of_trades()

        # Ensure an invalid trade can't be created
        success, data = self.create_invalid_trade()

        # Ensure the trade was successfully created
        assert not success, \
            "Trade was not created successfully"

        # Ensure thee number of trades has remained constant
        after = self.number_of_trades()
        assert before == after, \
            "Trade was added"

    def test_trade_deletion(self):
        """Tests the systems ability to delete a valid trade stored.
        
        Raises:
            AssertionError: If a specific test fails
        """

        # Create new trade
        success, data = self.create_valid_trade()
        
        # Ensure the trade was successfully created
        assert success, \
            "Trade was not successfully created"

        trade_id, _ = data

        # Ensure the new trade exists
        assert self.retrieve_trade(trade_id), \
            "Trade not successfully created"

        # Delete the trade
        assert self.delete_trade(trade_id), \
            "Trade not successfully deleted"

        # Ensure the trade doesn't exist
        assert not self.retrieve_trade(trade_id), \
            "Trade still exists"
        
        # Attempt to delete the trade again
        assert not self.delete_trade(trade_id), \
            "Deleted trade was deleted"
    
    def test_trade_edit(self):
        """Tests the systems ability to edit a valid trade stored.
        
        Raises:
            AssertionError: If a specific test fails
        """
       # Create new trade
        success, data = self.create_valid_trade()
        
        # Ensure the trade was successfully created
        assert success, \
            "Trade was not successfully created"

        trade_id, _ = data
        
        # Valid edit
        valid_edit = self.edit_trade({"trade_id" : trade_id, 
                                      "quantity" : 100})
        assert valid_edit, \
            "Edit was not successfully made"

        # Invalid edit - similarly, this functionality has already been tested 
        # in unit testing, therefore, it is sufficient to  use one invalid input  
        # to determine whether invalid edits are returned by the system

        # Invalid edit
        invalid_maturity = datetime.now() - timedelta(days=365)
        maturity = invalid_maturity.strftime("%Y-%m-%d")
        invalid_edit = self.edit_trade({"trade_id" : trade_id, 
                                        "maturity_date" : maturity})
        assert not invalid_edit, \
            "Invalid edit was successfully made"

        # Edit a deleted trade
        success, data = self.create_valid_trade()
        trade_id, _ = data

        self.delete_trade(trade_id)

        valid_edit = self.edit_trade({"trade_id" : trade_id, 
                                      "quantity" : 100})
        assert not valid_edit, \
            "Edit occured on deleted trade"

    def test_trade_reports(self):
        """Tests whether reports are returned successfully

        Raises:
            AssertionError: If a specific test fails
        """
        # Create new trade
        _, (trade_id, _) = self.create_valid_trade()
        # trade_id, _ = data

        # _, data = self.create_valid_trade()
        # trade_id, _ = data

        # _, data = self.create_valid_trade()
        # trade_id, _ = data

        # _, data = self.create_valid_trade()
        # trade_id, _ = data



    def tearDown(self):
        self.__connection.close()












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

    #     #Test 10 random rows in response if they are in the database
    #     for i in range(10):
    #         rand = random.randint(0, responseLength-1)
    #         currency = response.json()[rand]["currency"]
    #         isInDatabase = self.isCurrencyInDatabase(self.__connection, currency)
    #         self.assertEqual(isInDatabase, True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(responseLength, len(list))

    # def test_currency_all_currency_prices(self):
    #     #Test if the amount of data in response is equal to what is in the database
    #     response = requests.get("http://localhost:8000/api/currency/?page_size=100000000")
    #     responseLength = len(response.json())
    #     list = self.getListOfCurrencyPrices(self.__connection)

    #     #Test 10 random rows in response if they are in the database
    #     for i in range(10):
    #         rand = random.randint(0, responseLength-1)
    #         currency = response.json()[rand]["currency"]
    #         value = response.json()[rand]["value"]
    #         date = response.json()[rand]["date"]
    #         isInDatabase = self.isCurrencyPriceInDatabase(self.__connection, currency, value, date)
    #         self.assertEqual(isInDatabase, True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(responseLength, len(list))

    # def test_currency_by_currency(self):
    #     response = requests.get("http://localhost:8000/api/currency/currency=GBP/")
    #     responseLength = len(response.json())
    #     list = self.getCurrencyPricesByCurrency(self.__connection, "GBP")

    #     #Test 10 random rows in response if they are in the database
    #     for i in range(10):
    #         rand = random.randint(0, responseLength-1)
    #         currency = response.json()[rand]["currency"]
    #         value = response.json()[rand]["value"]
    #         date = response.json()[rand]["date"]
    #         isInDatabase = self.isCurrencyPriceInDatabase(self.__connection, currency, value, date)
    #         self.assertEqual(isInDatabase, True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(responseLength, len(list))

    # def test_currency_by_year(self):
    #     response = requests.get("http://localhost:8000/api/currency/currency=GBP&year=2018/")
    #     responseLength = len(response.json())
    #     list = self.getCurrencyPricesByYear(self.__connection, "GBP", 2018)

    #     #Test 10 random rows in response if they are in the database
    #     for i in range(10):
    #         rand = random.randint(0, responseLength-1)
    #         currency = response.json()[rand]["currency"]
    #         value = response.json()[rand]["value"]
    #         date = response.json()[rand]["date"]
    #         isInDatabase = self.isCurrencyPriceInDatabase(self.__connection, currency, value, date)
    #         self.assertEqual(isInDatabase, True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(responseLength, len(list))

    # def test_currency_by_month(self):
    #     response = requests.get("http://localhost:8000/api/currency/currency=GBP&year=2018&month=12/")
    #     responseLength = len(response.json())
    #     list = self.getCurrencyPricesByMonth(self.__connection, "GBP", 2018, 12)

    #     #Test 10 random rows in response if they are in the database
    #     for i in range(10):
    #         rand = random.randint(0, responseLength-1)
    #         currency = response.json()[rand]["currency"]
    #         value = response.json()[rand]["value"]
    #         date = response.json()[rand]["date"]
    #         isInDatabase = self.isCurrencyPriceInDatabase(self.__connection, currency, value, date)
    #         self.assertEqual(isInDatabase, True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(responseLength, len(list))

    # def test_currency_by_day(self):
    #     response = requests.get("http://localhost:8000/api/currency/currency=GBP&year=2018&month=12&day=12/")
    #     responseLength = len(response.json())
    #     list = self.getCurrencyPricesByDay(self.__connection, "GBP", 2018, 12, 12)

    #     #Test 10 random rows in response if they are in the database
    #     for i in range(10):
    #         rand = random.randint(0, responseLength-1)
    #         currency = response.json()[rand]["currency"]
    #         value = response.json()[rand]["value"]
    #         date = response.json()[rand]["date"]
    #         isInDatabase = self.isCurrencyPriceInDatabase(self.__connection, currency, value, date)
    #         self.assertEqual(isInDatabase, True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(responseLength, len(list))

    # def getListOfCurrencies(self, conn):
    #     cursor = conn.cursor()
    #     query = "SELECT * FROM currency"
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     return result

    # def isCurrencyInDatabase(self, conn, currency):
    #     cursor = conn.cursor()
    #     query = "SELECT * FROM currency WHERE currency= \""+currency+"\""
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     if len(result) > 0:
    #         return True
    #     return False

    # def getListOfCurrencyPrices(self, conn):
    #     cursor = conn.cursor()
    #     query = "SELECT * FROM currency_price"
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     return result

    # def isCurrencyPriceInDatabase(self, conn, currency, value, date):
    #     cursor = conn.cursor()
    #     query = "SELECT * FROM currency_price WHERE currency_id=\""+currency+"\" AND value="+str(value)+"AND date= \""+date+"\""
    #     #print(query)
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     if len(result) > 0:
    #         return True
    #     return False

    # def getCurrencyPricesByCurrency(self, conn, currency):
    #     cursor = conn.cursor()
    #     query = "SELECT * FROM currency_price WHERE currency_id=\""+currency+"\""
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     return result

    # def getCurrencyPricesByYear(self, conn, currency, year):
    #     cursor = conn.cursor()
    #     query = "SELECT * FROM currency_price WHERE currency_id=\""+currency+"\" AND YEAR(date)="+str(2018)
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     return result

    # def getCurrencyPricesByMonth(self, conn, currency, year, month):
    #     cursor = conn.cursor()
    #     query = "SELECT * FROM currency_price WHERE currency_id=\""+currency+"\" AND YEAR(date)="+str(2018)+" AND MONTH(date)="+str(12)
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     return result

    # def getCurrencyPricesByDay(self, conn, currency, year, month, day):
    #     cursor = conn.cursor()
    #     query = "SELECT * FROM currency_price WHERE currency_id=\""+currency+"\" AND YEAR(date)="+str(2018)+" AND MONTH(date)="+str(12)+" AND DAY(date)="+str(12)
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     return result

    # #Testing the company endpoints

    # def test_company_list_of_companies(self):
    #     #Test if the amount of data in response is equal to what is in the database
    #     response = requests.get("http://localhost:8000/api/company/list/?page_size=100000000")
    #     responseLength = len(response.json())
    #     list = self.getListOfCompanies(self.__connection)

    #     #Test 10 random rows in response if they are in the database
    #     for i in range(10):
    #         rand = random.randint(0, responseLength-1)
    #         id = response.json()[rand]["id"]
    #         name = response.json()[rand]["name"]
    #         isInDatabase = self.isCompanyInDatabase(self.__connection, id, name)
    #         self.assertEqual(isInDatabase, True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(responseLength, len(list))

    # def test_company_by_id(self):
    #     #Get the row of data for the company with ID ESPL27
    #     #API data
    #     # response = self.client.get(reverse("company_all"))
    #     # print(response.content)

    #     response = requests.get("http://localhost:8000/api/company/id=178")
    #     #print(response.content) #chek against this
    #     self.assertEqual(response.status_code, 200) #checking the status code
    #     self.assertEqual(response.content, b'[{"id":178,"name":"The Worst Generation"}]')

    #     #Database Data
    #     #Request data from the database here to compare against known quantities/values.

    #     #Assert against manual check from the data file
    #     #Assert that the data matches whats expected from the test data.

    # #The status code is still 200 but alma is not a companyID
    # def test_fake_company_by_id(self):
    #     #Test errorcodes in case of incorrect data
    #     response = requests.get("http://localhost:8000/api/company/id=fakedata")
    #     if not response.json():
    #         isEmpty = True
    #     else:
    #         isEmpty = False
    #     self.assertEqual(isEmpty, True)

    # def test_company_by_name(self):
    #     # TODO
    #     response = requests.get("http://localhost:8000/api/company/name=Cyberbiotics/")
    #     #print(response.content)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.content, b'[{"id":19,"name":"Cyberbiotics"}]')

    # def getListOfCompanies(self, conn):
    #     cursor = conn.cursor()
    #     query = "SELECT id, name FROM company"
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     return result

    # def isCompanyInDatabase(self, conn, id, name):
    #     cursor = conn.cursor()
    #     query = "SELECT * FROM company WHERE id=\""+str(id)+"\" AND name=\""+name+"\""
    #     #print(query)
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     if len(result) > 0:
    #         return True
    #     return False

    # #Testing product endpoints

    # def test_product_list_of_products(self):
    #     #Test if the amount of data in response is equal to what is in the database
    #     response = requests.get("http://localhost:8000/api/product/list/?page_size=100000000")
    #     responseLength = len(response.json())
    #     list = self.getListOfProducts(self.__connection)

    #     #print(response.json())
    #     #Test 10 random rows in response if they are in the database
    #     for i in range(10):
    #         rand = random.randint(0, responseLength-1)
    #         id = response.json()[rand]["id"]
    #         name = response.json()[rand]["name"]
    #         isInDatabase = self.isProductInDatabase(self.__connection, id, name)
    #         self.assertEqual(isInDatabase, True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(responseLength, len(list))

    # def test_product_by_id(self):
    #     # TODO
    #     response = requests.get("http://localhost:8000/api/product/id=1/")
    #     #print(response.content)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.content, b'[{"id":1,"name":"Stocks"}]')

    # def test_product_by_name(self):
    #     # TODO
    #     response = requests.get("http://localhost:8000/api/product/name=Stocks/")
    #     #print(response.content)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.content, b'[{"id":1,"name":"Stocks"}]')


    # def test_product_by_soldby(self):
    #     response = requests.get("http://localhost:8000/api/product/soldby/id=61/")
    #     responseLength = len(response.json())
    #     inDatabase = self.getProductsByCompany(self.__connection, "61") #QLMY86

    #     for i in range(10):
    #         rand = random.randint(0, responseLength-1)
    #         product_id = response.json()[rand]["product_id"]
    #         company_id = response.json()[rand]["company_id"]
    #         isInDatabase = self.isSoldByInDatabase(self.__connection, product_id, company_id)
    #         self.assertEqual(isInDatabase, True)

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



    # def test_trade_recent(self):
    #     #Test if the amount of data in response is equal to what is in the database
    #     response = requests.get("http://localhost:8000/api/trade/recent")
    #                             # http://localhost:8000/api/trade/recent
    #     #print(response)

    #     responseLength = len(response.json())
    #     #print(response)
    #     list = self.getRecentTrades(self.__connection)
    #     #print("hola")
    #     #print(list)

    #     # #Test 10 random rows in response if they are in the database
    #     # for i in range(10):
    #     #     rand = random.randint(0, responseLength-1)
    #     #     company = response.json()[rand]["company"]
    #     #     product = response.json()[rand]["product"]
    #     #     isInDatabase = self.isSellerInDatabase(self.__connection, company, product)
    #     #     self.assertEqual(isInDatabase, True)

    #     self.assertEqual(response.status_code, 200)
    #     #self.assertEqual(responseLength, len(list))

    # # def getRecentTrades(self, conn):
    # #     cursor = conn.cursor()
    # #     query = "SELECT * FROM VIEW TradeRecentList"
    # #     cursor.execute(query)
    # #     result = cursor.fetchall()
    # #     return result
    # #
    # #     path('trade/recent', views.TradeRecentList.as_view(), name="recent_trades")
    # #
    # #     path('trade/create', views.CreateDerivativeTrade.as_view(), name="create_trade"),
    # # path('trade/delete', views.DeleteDerivativeTrade.as_view(), name="delete_trade"),
    # # path('trade/edit', views.EditDerivativeTrade.as_view(), name="edit_trade"),

    # def test_x(self):
    #     url = "http://localhost:8000/api/trade/create"
    #     payload = 'selling_party=3&buying_party=17&product=9&quantity=160&maturity_date=2022-12-14&underlying_currency=AUD&notional_currency=GBP&strike_price=51&underlying_price=17.21'
    #     headers = {
    #       'Content-Type': 'application/x-www-form-urlencoded'
    #     }
    #     response = requests.request("POST", url, headers=headers, data = payload)
    #     print(response.status_code)
    #     print("hola")
    #     #rjson = response.json()
    #     # print(response.json())
    #     # print("second")
    #     #print(response.text.encode('utf8'))




    # #"do requests that are fake, check if the error number is what I expect"
