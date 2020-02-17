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

# Create your tests here.

#Example company codes, based on the data provided in the data folder.
#ESPL27 = The Worst Generation  |   QXFF29 = Okama    | ZFHD93 = Brawndo
class CompanyAPITest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.client = Client()

        #Make this use the environment variables of your computer to connect to the database for testing.
        self.__connection = mariadb.connect(user= os.environ.get('DB_USER'), 
                                        password= os.environ.get('DB_PASSWORD'),
                                        database= os.environ.get('DB_NAME'), 
                                        host= os.environ.get("DB_HOST"),
                                        port= OS.environ.get("DB_PORT"),
                                        auth_plugin='mysql_native_password')

    def tearDown(self):
        self.__connection.close()

    def test_company_by_id(self):
        #Get the row of data for the company with ID ESPL27
        #API data
        # response = self.client.get(reverse("company_all"))
        # print(response.content)

        response = requests.get("http://localhost:8000/api/company/id=ESPL27")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'[{"id":"ESPL27","name":"The Worst Generation"}]')

        #Database Data
        #Request data from the database here to compare against known quantities/values.

        #Assert against manual check from the data file
        #Assert that the data matches whats expected from the test data.

    def test_company_by_name(self):
        # TODO
        self.assertEqual(1,)
