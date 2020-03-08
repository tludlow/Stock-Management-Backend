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
from random import randint
from .learning import *
from django.db import connection

def raw_dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class CreateDerivativeTrade(APIView):
    def getCompany(self, cid):
        company = Company.objects.filter(id=cid)
        company_serialized = CompanySerializer(company, many=True)
        return company_serialized.data

    def convertCurrency(self, underlying, notional, amount):
        #Most recent value of the underlying currency
        underlying = CurrencyPrice.objects.filter(currency_id=underlying).order_by("-date")[0]
        underlying_s = CurrencyPriceSerializer(underlying, many=False)

        #Most recent value of the notional currency
        notional = CurrencyPrice.objects.filter(currency_id=notional).order_by("-date")[0]
        notional_s = CurrencyPriceSerializer(notional, many=False)

        #Conversion rate, what does 1 underlying_value get you in notional_value
        underlying_value = underlying_s.data["value"]
        notional_value = notional_s.data["value"]

        #The conversion goes through the base currency of dollars.
        converted_rate = round(notional_value / underlying_value, 2)

        #Overall value represented (value * quantity)
        return converted_rate * int(amount)


    def post(self, request):
        trade_data = request.data
        #if product id = 1, then its a stock, will be purchasing stocks of the selling company

        #Check that the request has all the data required for a trade.
        requiredFields = ["selling_party", "buying_party", "product", "quantity",
            "maturity_date", "underlying_currency", "notional_currency", "strike_price", "underlying_price"]

        for field in requiredFields:
            if field not in trade_data.keys():
                return JsonResponse(status=400, data={"error": "Missing the field '" + field + "' in the form."})


        if int(trade_data["quantity"]) <= 0:
            return JsonResponse(status=400, 
                data={"error": "You cannot create a trade with a negative, or zero quantity"})
        
        if float(trade_data["strike_price"]) <= 0.00:
            return JsonResponse(status=400, data={"error": "A trade's strike price cannot be negative or zero."})

        if float(trade_data["underlying_price"]) <= 0.00:
            return JsonResponse(status=400, data={"error": "A trade's underlying price cannot be negative or zero."})

        if int(trade_data["product"]) == -1:
            #Trading stocks for the seller here... Need to update the ID as frontend uses -1 and in db its 1
            trade_data["product"] = 1

        #Check that the discrete values of the trade exist.
        #Buying party
        buying_company_data = self.getCompany(trade_data["buying_party"])
        if len(buying_company_data) == 0:
            return JsonResponse(status=400, data={"error": "The buying party does not exist."})

        #Selling party
        selling_company_data = self.getCompany(trade_data["selling_party"])
        if len(selling_company_data) == 0:
            return JsonResponse(status=400, data={"error": "The selling party does not exist."})

        #Generate a random trade ID 16 characters long. 8 letters followed by 8 numbers
        letters = ''.join(random.choice(string.ascii_letters).upper() for x in range(8))
        nums = ''.join(["{}".format(randint(0, 9)) for num in range(0, 8)])
        trade_id = letters+nums

        #Compute the notional amount, this is the underlying_price converted to the notional_price
        #which you then multiply by the quantity of the trade.
        notional_amount = round(self.convertCurrency(trade_data["underlying_currency"], trade_data["notional_currency"], trade_data["quantity"]), 2)

        #Get the product being traded
        product_instance = Product.objects.filter(id=trade_data["product"])[0]
        
        #Get the companies represented
        buying_instance = Company.objects.filter(id=trade_data["buying_party"])[0]
        selling_instance = Company.objects.filter(id=trade_data["selling_party"])[0]

        #Get the currencies being represented
        notional_instance = Currency.objects.filter(currency=trade_data["notional_currency"])[0]
        underlying_instance = Currency.objects.filter(currency=trade_data["underlying_currency"])[0]

        if trade_data.get('demo', None) != None:
            date_of_trade = trade_data['date']
        else:
            date_of_trade = datetime.now()
        #Create the trade
        new_trade = Trade(
            date=date_of_trade,
            product=product_instance,
            buying_party=buying_instance,
            selling_party=selling_instance,
            notional_amount=notional_amount,
            notional_currency=notional_instance,
            quantity=trade_data["quantity"],
            maturity_date=trade_data["maturity_date"],
            underlying_price=trade_data["underlying_price"],
            underlying_currency=underlying_instance,
            strike_price=trade_data["strike_price"]
        )

        new_trade.save()
        trade_id = new_trade.id

        # scanTradeForErrors(new_trade) - causing errors
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT 
                T.id, T.date, T.notional_amount, T.quantity, 
                T.maturity_date, T.underlying_price, T.strike_price, 
                P.name as product, T.product_id, T.buying_party_id, 
                BP.name as buying_party, 
                T.selling_party_id, SP.name as selling_party, 
                T.underlying_currency_id as underlying_currency, 
                T.notional_currency_id as notional_currency 
            FROM trade T 
            INNER JOIN 
                (SELECT * FROM product) P 
            ON P.id = T.product_id
            INNER JOIN 
                (SELECT * FROM company) BP
            ON BP.id = T.buying_party_id
            INNER JOIN
                (SELECT * FROM company) SP
            ON SP.id = T.selling_party_id
            LEFT JOIN
                (SELECT trade_id_id FROM deleted_trade) DT
            ON DT.trade_id_id = T.id
            WHERE 
                T.id=%s AND DT.trade_id_id IS NULL
            ORDER BY T.date DESC
            """, [trade_id])
            data = raw_dictfetchall(cursor)
        s = JoinedTradeSerializer(data, many=True)

        return JsonResponse(status=200, data={"trade_id": new_trade.id, "data": s.data, "notional_amount": notional_amount})