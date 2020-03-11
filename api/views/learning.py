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
from statistics import mean 

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
        errors = errors.values()

        #get the corrections
        corrections = FieldCorrection.objects.all()
        corrections = corrections.values()

        formatted_corrections = []
        formatted_errors = []

        for error in errors:
            formatted_errors.append(dict(error))

        for correct in corrections:
            formatted_corrections.append(dict(correct))

        for error in formatted_errors:
            for correct in formatted_corrections:
                if correct["error_id"] == error["id"]:
                    error["correction_applied"] = correct
                


        return JsonResponse(status=200, data={
            "errors": formatted_errors
        })

class SuggestCorrectionsForTrade(APIView):
    def get(self, request, trade):
        #Does this trade even have any errors?
        errors = ErroneousTradeAttribute.objects.filter(trade_id=trade)
        errors = errors.values()

        formatted_errors = []
        for error in errors:
            formatted_errors.append(dict(error))

        #print(formatted_errors)
        
        #No errors for this trade, not point suggesting
        if len(formatted_errors) == 0:
            return JsonResponse(status=200, data={
                "suggestion": [],
                "message": "No errors to suggest corrections for"
            })

        #Get the actual trade info
        trade = Trade.objects.filter(id=trade)[0]
        trade = TradeSerializer(trade).data

        #print(trade)

        #Get the similar trades
        erroneous = DeletedTrade.objects.all().values('trade_id')
        deleted = ErroneousTradeAttribute.objects.all().values('trade_id')

        data = None
        if trade["product"] == 1:
            trades = Trade.objects.filter(buying_party=trade["buying_party"], selling_party=trade["selling_party"], product_id=trade["product"]).order_by('-date')
            dataFirst = trades.exclude(id__in = erroneous)
            data = dataFirst.exclude(id__in = deleted)[0:150]
        else:
            trades = Trade.objects.filter(buying_party=trade["buying_party"], product_id=trade["product"]).order_by('-date')
            dataFirst = trades.exclude(id__in = erroneous)
            data = dataFirst.exclude(id__in = deleted)[0 : 150]

        
        trades_s = TradeSerializer(data, many=True)
        listed_data = []
        for trade in trades_s.data:
            listed_data.append(dict(trade))

        if len(listed_data) < 6:
            return JsonResponse(status=200, data={
                "suggestion": [],
                "message": "Not enough information to base predictions one"
            })

        for idx, trade in enumerate(listed_data):
            #print(trade, end="\n\n")
            #Need to convert all of the strike prices and underlying prices into USD
            underlying_currency = trade["underlying_currency"]
            underlying_price = trade["underlying_price"]
            strike_price = trade["strike_price"]
            
            current_value_of_underlying = convertCurrencyAtDate("USD", underlying_currency, underlying_price, datetime.today().strftime('%Y-%m-%d'))
            current_value_of_strike = convertCurrencyAtDate("USD", underlying_currency, strike_price, datetime.today().strftime('%Y-%m-%d'))

            trade["underlying_current_usd"] = current_value_of_underlying
            trade["strike_current_usd"] = current_value_of_strike
            listed_data[idx] = trade

        
        #Log all similar quantities
        quantities = []
        underlyings = []
        strikes = []

        for trade in listed_data:
            quantities.append(trade["quantity"])
            underlyings.append(trade["underlying_current_usd"])
            strikes.append(trade["strike_current_usd"])


        mean_quantity = round(mean(quantities), 0)
        mean_underlying = round(mean(underlyings), 2)
        mean_strikes = round(mean(strikes), 2)

        print("Mean quantity: " + str(mean_quantity))
        print("Mean underlying: " + str(mean_underlying))
        print("Mean strikes: " + str(mean_strikes))


        return JsonResponse(status=200, data={
            "suggestion": "Yes",
            "message": "Here are the suggested values",
            "quantity": mean_quantity,
            "underlying": mean_underlying,
            "strike": mean_strikes
        }, safe=False)

class SystemCorrection(APIView):
    def post(self, request):
        errorid = request.data["errorID"]
        tradeid = request.data["tradeID"]
        fieldtype = request.data["field_type"]
        correction_value = request.data["value"]

        #Get the error being referenced
        errorfound = ErroneousTradeAttribute.objects.filter(id=errorid)[0]

        #Get the trade
        tradefound = Trade.objects.filter(id=tradeid)[0]
        trade_s = TradeSerializer(tradefound, many=False)
        trade_data = trade_s.data

        #Check if any corrections are already applied, remove these
        removedcorrections = FieldCorrection.objects.filter(error_id=errorid).delete()

        #Apply the new correction
        new_correction = None
        if fieldtype == "QT":
            new_correction = FieldCorrection(
                error = errorfound,
                date=datetime.now(),
                old_value = trade_data["quantity"],
                new_value = correction_value,
                change_type = "SYTM"
            )
        if fieldtype == "UP":
            new_correction = FieldCorrection(
                error = errorfound,
                date=datetime.now(),
                old_value = trade_data["underlying_price"],
                new_value = correction_value,
                change_type = "SYTM"
            )

        if fieldtype == "SP":
            new_correction = FieldCorrection(
                error = errorfound,
                date=datetime.now(),
                old_value = trade_data["strike_price"],
                new_value = correction_value,
                change_type = "SYTM"
            )

        new_correction.save()

        if fieldtype == "QT":
            tradefound.quantity = correction_value
        if fieldtype == "SP":
            tradefound.strike_price = correction_value
        if fieldtype == "UP":
            tradefound.underlying_price = correction_value

        tradefound.save()

        return JsonResponse(status=200, data={
           "working": "wow"
        }, safe=False)

class SuggestCorrectionsForTrade(APIView):
    def get(self, request, trade):
        #Does this trade even have any errors?
        errors = ErroneousTradeAttribute.objects.filter(trade_id=trade)
        errors = errors.values()

        formatted_errors = []
        for error in errors:
            formatted_errors.append(dict(error))

        #print(formatted_errors)
        
        #No errors for this trade, not point suggesting
        if len(formatted_errors) == 0:
            return JsonResponse(status=200, data={
                "suggestion": [],
                "message": "No errors to suggest corrections for"
            })

        #Get the actual trade info
        trade = Trade.objects.filter(id=trade)[0]
        trade = TradeSerializer(trade).data

        #print(trade)

        #Get the similar trades
        erroneous = DeletedTrade.objects.all().values('trade_id')
        deleted = ErroneousTradeAttribute.objects.all().values('trade_id')

        data = None
        if trade["product"] == 1:
            trades = Trade.objects.filter(buying_party=trade["buying_party"], selling_party=trade["selling_party"], product_id=trade["product"]).order_by('-date')
            dataFirst = trades.exclude(id__in = erroneous)
            data = dataFirst.exclude(id__in = deleted)[0:150]
        else:
            trades = Trade.objects.filter(buying_party=trade["buying_party"], product_id=trade["product"]).order_by('-date')
            dataFirst = trades.exclude(id__in = erroneous)
            data = dataFirst.exclude(id__in = deleted)[0 : 150]

        
        trades_s = TradeSerializer(data, many=True)
        listed_data = []
        for trade in trades_s.data:
            listed_data.append(dict(trade))

        if len(listed_data) < 6:
            return JsonResponse(status=200, data={
                "suggestion": [],
                "message": "Not enough information to base predictions one"
            })

        for idx, trade in enumerate(listed_data):
            #print(trade, end="\n\n")
            #Need to convert all of the strike prices and underlying prices into USD
            underlying_currency = trade["underlying_currency"]
            underlying_price = trade["underlying_price"]
            strike_price = trade["strike_price"]
            
            current_value_of_underlying = convertCurrencyAtDate("USD", underlying_currency, underlying_price, datetime.today().strftime('%Y-%m-%d'))
            current_value_of_strike = convertCurrencyAtDate("USD", underlying_currency, strike_price, datetime.today().strftime('%Y-%m-%d'))

            trade["underlying_current_usd"] = current_value_of_underlying
            trade["strike_current_usd"] = current_value_of_strike
            listed_data[idx] = trade

        
        #Log all similar quantities
        quantities = []
        underlyings = []
        strikes = []

        for trade in listed_data:
            quantities.append(trade["quantity"])
            underlyings.append(trade["underlying_current_usd"])
            strikes.append(trade["strike_current_usd"])


        mean_quantity = round(mean(quantities), 0)
        mean_underlying = round(mean(underlyings), 2)
        mean_strikes = round(mean(strikes), 2)

        print("Mean quantity: " + str(mean_quantity))
        print("Mean underlying: " + str(mean_underlying))
        print("Mean strikes: " + str(mean_strikes))


        return JsonResponse(status=200, data={
            "suggestion": "Yes",
            "message": "Here are the suggested values",
            "quantity": mean_quantity,
            "underlying": mean_underlying,
            "strike": mean_strikes
        }, safe=False)

class SystemCorrection(APIView):
    def post(self, request):
        errorid = request.data["errorID"]
        tradeid = request.data["tradeID"]
        fieldtype = request.data["field_type"]
        correction_value = request.data["value"]

        #Get the error being referenced
        errorfound = ErroneousTradeAttribute.objects.filter(id=errorid)[0]

        #Get the trade
        tradefound = Trade.objects.filter(id=tradeid)[0]
        trade_s = TradeSerializer(tradefound, many=False)
        trade_data = trade_s.data

        #Check if any corrections are already applied, remove these
        removedcorrections = FieldCorrection.objects.filter(error_id=errorid).delete()

        #Apply the new correction
        new_correction = None
        if fieldtype == "QT":
            new_correction = FieldCorrection(
                error = errorfound,
                date=datetime.now(),
                old_value = trade_data["quantity"],
                new_value = correction_value,
                change_type = "SYTM"
            )
        if fieldtype == "UP":
            new_correction = FieldCorrection(
                error = errorfound,
                date=datetime.now(),
                old_value = trade_data["underlying_price"],
                new_value = correction_value,
                change_type = "SYTM"
            )

        if fieldtype == "SP":
            new_correction = FieldCorrection(
                error = errorfound,
                date=datetime.now(),
                old_value = trade_data["strike_price"],
                new_value = correction_value,
                change_type = "SYTM"
            )

        new_correction.save()

        return JsonResponse(status=200, data={
           "working": "wow"
        }, safe=False)


        
