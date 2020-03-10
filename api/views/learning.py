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
from datetime import datetime, timedelta, timezone, date
import requests
from io import StringIO
import os
from django.db import connection
import numpy as np

# +- value we allow for it to be considered correct
percentage = 20

def raw_dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def convertCurrencyAtDate(underlying, notional, amount, date):
    with connection.cursor() as cursor:
            cursor.execute("""
            SELECT VALUE 
            FROM currency_price 
            WHERE currency_id=%s 
            ORDER BY DATE DESC
            LIMIT 1
            """, [notional])
            notional_data = raw_dictfetchall(cursor)

    #The conversion goes through the base currency of dollars.
    converted_rate = 1 / notional_data[0]["VALUE"]

    # #Overall value represented (value * quantity)
    return round(converted_rate * amount, 2)

#CODE FROM HERE: https://gist.github.com/vishalkuo/f4aec300cf6252ed28d3
def removeOutliers(x, outlierConstant):
    a = np.array(x)
    upper_quartile = np.percentile(a, 75)
    lower_quartile = np.percentile(a, 25)
    IQR = (upper_quartile - lower_quartile) * outlierConstant
    quartileSet = (lower_quartile - IQR, upper_quartile + IQR)
    
    result = a[np.where((a >= quartileSet[0]) & (a <= quartileSet[1]))]
    
    return result.tolist()

def scanTradeForErrors(trade, tid):
    # Going to need to pass the information below to the AI to scan for the errors.
    # Strike Price
    # Quantity
    # Underlying Price

    trade_data = trade
    print(trade_data)

    boughtProduct = trade_data["product"]
    buyingCompany = trade_data["buying_party"]
    sellingCompany = trade_data["selling_party"]

    # Get the data to compare against
    # getBuyerProduct = requests.get(
    #     "http://localhost:8000/api/trade/product={0}&buyer={1}&seller={2}/".format(boughtProduct, buyingCompany,
    #                                                                                sellingCompany))

    erroneous = DeletedTrade.objects.all().values('trade_id')
    deleted = ErroneousTradeAttribute.objects.all().values('trade_id')

    data = None
    if trade_data["product"] == "1":
        trades = Trade.objects.filter(buying_party=trade_data["buying_party"], selling_party=trade_data["selling_party"], product_id=trade_data["product"]).exclude(id=tid).order_by('-date')
        dataFirst = trades.exclude(id__in = erroneous)
        data = dataFirst.exclude(id__in = deleted)[0:150]
    else:
        trades = Trade.objects.filter(buying_party=trade_data["buying_party"], product_id=trade_data["product"]).exclude(id=tid).order_by('-date')
        dataFirst = trades.exclude(id__in = erroneous)
        data = dataFirst.exclude(id__in = deleted)[0 : 150]

    trades_s = TradeSerializer(data, many=True)
    listed_data = []
    for trade in trades_s.data:
        listed_data.append(dict(trade))

    if len(listed_data) < 8:
        #Not enough data to perform realistic comparisons...
        return -1

    #Need to add a new field to all of the trades which have the same underlying and strike price as the new trade
    new_trade_underlying = trade_data["underlying_currency"]
    print("LENGTH IS: " + str(len(listed_data)))
    for idx, trade in enumerate(listed_data):
        #Converted underlying
        converted_underlying = convertCurrencyAtDate(new_trade_underlying, trade["underlying_currency"], trade["underlying_price"], datetime.today().strftime('%Y-%m-%d'))
        print("[UNDERLYING] " + str(new_trade_underlying) + " to " + str(trade["underlying_currency"]) + " is: " + str(converted_underlying) + " from " + str(trade["underlying_price"]))

        #Converted strike
        converted_strike = convertCurrencyAtDate(new_trade_underlying, trade["underlying_currency"], trade["strike_price"], datetime.today().strftime('%Y-%m-%d'))

        trade["current_underlying"] = converted_underlying
        trade["current_strike"] = converted_strike
        listed_data[idx] = trade

        print(trade, end="\n\n")
        
    quantities = []
    underlying = []
    strike = []

    for trade in listed_data:
        quantities.append(trade["quantity"])
        underlying.append(trade["current_underlying"])
        strike.append(trade["current_strike"])

    quantities = sorted(quantities)
    underlying = sorted(underlying)
    strike = sorted(strike)

    print("Quantity")
    print(quantities)
    print("\n\n")

    print("Underlying")
    print(underlying)
    print("\n\n")

    print("Strike")
    print(strike)
    print("\n\n")

    #Get our new trade
    trade_new = Trade.objects.filter(id=tid)[0]
    print(trade_data)

    if trade_data["quantity"] > quantities[-1] or trade_data["quantity"] < quantities[0]:
        new_error_field = ErroneousTradeAttribute(
                trade_id=trade_new,
                erroneous_attribute="QT",
                erroneous_value=str(trade_data["quantity"]),
                date=datetime.now()
            )
        new_error_field.save()

    if trade_data["underlying_price"] > underlying[-1] or trade_data["underlying_price"] < underlying[0]:
        new_error_field = ErroneousTradeAttribute(
                trade_id=trade_new,
                erroneous_attribute="UP",
                erroneous_value=str(trade_data["underlying_price"]),
                date=datetime.now()
            )
        new_error_field.save()

    if trade_data["strike_price"] > strike[-1] or trade_data["strike_price"] < strike[0]:
        new_error_field = ErroneousTradeAttribute(
                trade_id=trade_new,
                erroneous_attribute="ST",
                erroneous_value=str(trade_data["strike_price"]),
                date=datetime.now()
            )
        new_error_field.save()

    
class RecommendedRange(APIView):
    def get(self, request, currency, product, buyer, seller):


        # Get the data to compare against
        # getBuyerProduct = requests.get(
        #     "http://localhost:8000/api/trade/product={0}&buyer={1}&seller={2}/".format(boughtProduct, buyingCompany,
        #                                                                                sellingCompany))

        erroneous = DeletedTrade.objects.all().values('trade_id')
        deleted = ErroneousTradeAttribute.objects.all().values('trade_id')

        data = None
        if product == "1":
            trades = Trade.objects.filter(buying_party=buyer, selling_party=seller, product_id=product).order_by('-date')
            dataFirst = trades.exclude(id__in = erroneous)
            data = dataFirst.exclude(id__in = deleted)[0:150]
        else:
            trades = Trade.objects.filter(buying_party=buyer, product_id=product).order_by('-date')
            dataFirst = trades.exclude(id__in = erroneous)
            data = dataFirst.exclude(id__in = deleted)[0 : 150]

        trades_s = TradeSerializer(data, many=True)
        listed_data = []
        for trade in trades_s.data:
            listed_data.append(dict(trade))

        for idx, trade in enumerate(listed_data):
            print(trade, end="\n\n")
            #Need to convert all of the strike prices and underlying prices into USD
            underlying_currency = trade["underlying_currency"]
            underlying_price = trade["underlying_price"]
            strike_price = trade["strike_price"]
            
            current_value_of_underlying = convertCurrencyAtDate("USD", underlying_currency, underlying_price, datetime.today().strftime('%Y-%m-%d'))
            current_value_of_strike = convertCurrencyAtDate("USD", underlying_currency, strike_price, datetime.today().strftime('%Y-%m-%d'))

            trade["underlying_current_usd"] = current_value_of_underlying
            trade["strike_current_usd"] = current_value_of_strike
            listed_data[idx] = trade
            

        quantities = []
        usd_underlyings = []
        usd_strikes = []

        for trade in listed_data:
            quantities.append(trade["quantity"])
            usd_underlyings.append(trade["underlying_current_usd"])
            usd_strikes.append(trade["strike_current_usd"])

        print("Quantities:")
        quantities = sorted(quantities)
        print("\n")

        print("Underlying:")
        usd_underlyings = sorted(usd_underlyings)
        print("\n")

        print("Strike:")
        usd_strikes = sorted(usd_strikes)
        print("\n")

        print(quantities)

        #Convert the currencies back to the underlying from usd
        min_underlying_revert = convertCurrencyAtDate(underlying_currency, "USD", usd_underlyings[0], datetime.today().strftime('%Y-%m-%d'))
        max_underlying_revert = convertCurrencyAtDate(underlying_currency, "USD", usd_underlyings[-1], datetime.today().strftime('%Y-%m-%d'))
        min_strike_revert = convertCurrencyAtDate(underlying_currency, "USD", usd_strikes[0], datetime.today().strftime('%Y-%m-%d'))
        max_strike_revert = convertCurrencyAtDate(underlying_currency, "USD", usd_strikes[-1], datetime.today().strftime('%Y-%m-%d'))


        return JsonResponse(status=200, data={
            "min_quantity": quantities[0],
            "max_quantity": quantities[-1],
            "min_underlying": min_underlying_revert,
            "max_underlying": max_underlying_revert,
            "min_strike": min_strike_revert,
            "max_strikes": max_strike_revert
        })

class CheckForErrors(APIView):
    def get(self, request, id):
        errors = ErroneousTradeAttribute.objects.filter(trade_id=id)
        errors_s = ErroneousAttributeSerializer(errors, many=True)

        return Response(errors_s.data)


        
