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
        _, (id_a, _) = self.create_valid_trade()
        _, (id_b, _) = self.create_valid_trade()
        _, (id_c, _) = self.create_valid_trade()
        _, (id_d, _) = self.create_valid_trade()

        # Apply some edits
        edit_a = self.edit_trade({"trade_id" : id_b, 
                                  "quantity" : 100})

        edit_b = self.edit_trade({"trade_id" : id_c, 
                                  "quantity" : 200})

        # Apply some deletions
        self.delete_trade(id_b)
        self.delete_trade(id_c)

        today = datetime.now()
        success, report = self.generate_report(today.year, today.month, today.day)

        assert success, "Report was not successfully returned"

        # Ensure all data is included in the report
        exp_new = [id_a, id_d]
        exp_edit = [id_a]
        exp_delete = [id_b, id_c]

        found = 0

        new = report['created_trades']
        edited = report['edited_trades']
        deleted = report['deleted_trades']

        for t, comp in zip([new, edited, deleted], [exp_new, exp_edit, exp_delete]):
            for i in t:
                val = i.get('id', None)
                if val is None:
                    val = i['trade']['id']
                for q in comp:
                    if q == val:
                        trade_q = self.retrieve_trade(q)
                        if trade_q:
                            for k in trade_q.keys():
                                assert trade_q[k] == i[k], "Trade not correct in report"
                        found += 1

        total = len(exp_new) + len(exp_edit) + len(exp_delete) - 1    

        assert total == found, "Not all values were included within the report"

        # Check for presence of old reports
        old_report = self.generate_report(2019, 3, 9)
        assert len(old_report) > 1, "Old reports are not successfully returned"
    
    def tearDown(self):
        self.__connection.close()
