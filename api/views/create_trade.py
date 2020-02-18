from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django import forms
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from api.serializers import *
from ..models import *
from ..serializers import *
import datetime
from calendar import monthrange
from datetime import datetime
from django.core.paginator import Paginator
import random, string

class CreateDerivativeTrade(APIView):
    def getCompany(self, cid):
        company = Company.objects.filter(id=cid)
        company_serialized = CompanySerializer(company, many=True)
        return company_serialized.data

    def post(self, request):
        trade_data = request.data
        #if product id = 1, then its a stock, will be purchasing stocks of the selling company
        print(trade_data)

        #Check that the request has all the data required for a trade.
        requiredFields = ["quantity", "strike_price", "buying_party", "selling_party", "underlying_price"]
        for field in requiredFields:
            if field not in trade_data.keys():
                return JsonResponse(status=400, data={"error": "Missing the field '" + field + "' in the form."})


        if int(trade_data["quantity"]) <= 0:
            return JsonResponse(status=400, 
                data={"error": "You cannot create a trade with a negative, or zero quantity"})
        
        if int(trade_data["strike_price"]) <= 0:
            return JsonResponse(status=400, data={"error": "A trade's strike price cannot be negative or zero."})

        if int(trade_data["underlying_price"]) <= 0:
            return JsonResponse(status=400, data={"error": "A trade's underlying price cannot be negative or zero."})


        #Check that the discrete values of the trade exist.
        #Buying party
        buying_company_data = self.getCompany(trade_data["buying_party"])
        if len(buying_company_data) == 0:
            return JsonResponse(status=400, data={"error": "The buying party does not exist."})

        #Selling party
        selling_company_data = self.getCompany(trade_data["selling_party"])
        if len(selling_company_data) == 0:
            return JsonResponse(status=400, data={"error": "The selling party does not exist."})

        #Currency checks, make sure the currencies provided actually exist.


        #Notional value calculation, this is underlying_price * quantity.
        #In scenarios where the underlying and notional currency differ the exchange rate will need to be used.
        do_currencies_differ = trade_data["underlying_currency"] == trade_data["notional_currency"]


        #Generate a random trade ID between 16 and 18 characters long
        trade_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16)).upper()

        #Create the trade
        new_trade = Trade(trade_id, )
        #new_trade.save()

        return JsonResponse(status=400, data={"trade_id": trade_id, "data": trade_data})