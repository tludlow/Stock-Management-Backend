from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django import forms
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from api.serializers import *
from django.core import serializers
from ..models import *
from ..serializers import *
import datetime
from calendar import monthrange
from datetime import datetime
from django.core.paginator import Paginator
import random, string
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@method_decorator(cache_page(5), name='dispatch')
class TradeRecentList(APIView):
    def get(self, request):
        #Get pagination data before the request so that it saves memory and is quicker to query.
        page_number = int(self.request.query_params.get("page_number", 1))
        page_size = int(self.request.query_params.get("page_size", 12))

        trades = Trade.objects.all().order_by('-date')
        deleted = DeletedTrade.objects.all().values('trade_id')
        data = trades.exclude(id__in = deleted)[(page_number-1)*page_size : page_number*page_size]
        trade_data = data.values()
        
        for idx, trade in enumerate(trade_data):
            buying_party_id = trade.get("buying_party_id")
            selling_party_id = trade.get("selling_party_id")

            #Get the data for the buying and selling party
            #Needs to be done here, cannot be done in the original call recursively because its too slow.
            buying_party_company_data = Company.objects.get(id=buying_party_id)
            buying_company = CompanySerializer(buying_party_company_data)

            selling_party_company_data = Company.objects.get(id=selling_party_id)
            selling_company = CompanySerializer(selling_party_company_data)

            #Add the companies data to the trade
            trade_data[idx]["buying_company"] = buying_company.data.get("name")
            trade_data[idx]["selling_company"] = selling_company.data.get("name")

            #Take the product_id and append meaningful data about this product to the trade
            product_id = trade.get("product_id")
            product_data = Product.objects.get(id=product_id)
            product_s = ProductSerializer(product_data)

            trade_data[idx]["product"] = product_s.data.get("name")

        #Modified the structure of a trade, will need to use a custom serializer.
        return Response(trade_data)


class TotalTrades(APIView):
    def get(self, request):
        total_trades = Trade.objects.all().count()

        return JsonResponse(status=200, data={
            "total_trades": total_trades
        })

class RecentTradesByCompanyForProduct(APIView):
    def convertCurrencyAtDate(self, underlying, notional, amount, date):
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
        return converted_rate * amount

    def get(self, request, buyer, product, seller):
        #Get pagination data before the request so that it saves memory and is quicker to query.
        page_number = int(self.request.query_params.get("page_number", 1))
        page_size = int(self.request.query_params.get("page_size", 150))

        erroneous = DeletedTrade.objects.all().values('trade_id')
        deleted = ErroneousTradeAttribute.objects.all().values('trade_id')


        #If the product is stocks we need more limitations on the data returned
        data = None
        if product == "1":
            trades = Trade.objects.filter(buying_party=buyer, selling_party=seller, product_id=product).order_by('-date')
            dataFirst = trades.exclude(id__in = erroneous)
            data = dataFirst.exclude(id__in = deleted)
        else:
            trades = Trade.objects.filter(buying_party=buyer, product_id=product).order_by('-date')
            dataFirst = trades.exclude(id__in = erroneous)
            data = dataFirst.exclude(id__in = deleted)[(page_number-1)*page_size : page_number*page_size]

        listed_data = []
        for trade in list(trades):
            listed_data.append(trade.__dict__)

        trades_s = TradeSerializer(trades, many=True)
        listed_data = []
        for trade in trades_s.data:
            listed_data.append(dict(trade))

        print(listed_data)

        for idx, trade in enumerate(listed_data):
            print(type(trade))
            #Need to convert all of the strike prices and underlying prices into USD
            underlying_currency = trade["underlying_currency"]
            underlying_price = trade["underlying_price"]
            strike_price = trade["strike_price"]
            date = trade["date"]

            underlying_value_at_date_in_base = self.convertCurrencyAtDate("USD", underlying_currency, underlying_price, date)
            strike_value_at_date_in_base = self.convertCurrencyAtDate("USD", underlying_currency, strike_price, date)

            trade["usd_underlying"] = underlying_value_at_date_in_base
            trade["usd_strike"] = strike_value_at_date_in_base
            listed_data[idx] = trade
            print("UNDERLYING= " + str(underlying_value_at_date_in_base) + "  |  " + "STRIKE= " + str(strike_value_at_date_in_base))
            print(trade, end="\n\n")

        print(listed_data)
        return JsonResponse(status=200, data=listed_data, safe=False)

#Converts a currency from one type, into another at the latest exchange rate
#All must pass "through" dollars as they all derive a dollar value, where a dollar = 1
class CurrencyConversionLatest(APIView):
    def get(self, request, from_currency, to_currency):
        #Check if these currencies actually exist...
        check_from = Currency.objects.filter(currency=from_currency)
        check_to = Currency.objects.filter(currency=to_currency)

        if len(check_from) != 1:
            return JsonResponse(status=400, data={
                "error": "The currency: " + from_currency + " does not exist or has more than 1 result",
                "count": len(check_from)
                })

        if len(check_to) != 1:
            return JsonResponse(status=400, data={
                "error": "The currency: " + to_currency + " does not exist or has more than 1 result.",
                "count": len(check_to)
            })

        #Get the latest currency value of the from currency in USD
        from_data = CurrencyPrice.objects.filter(currency_id=from_currency).order_by("-date")[0]
        to_data = CurrencyPrice.objects.filter(currency_id=to_currency).order_by("-date")[0]

        # if len(from_data) != 1 or len(to_data) != 1:
        #     return JsonResponse(status=500, data={
        #         "error": "Error getting latest currency data",
        #     })
        
        s_from_data = CurrencyPriceSerializer(from_data, many=False)
        s_to_data = CurrencyPriceSerializer(to_data, many=False)

        #Need data to be in 2dp for simplicity
        usd_converted = round(s_from_data.data["value"] / s_to_data.data["value"], 2)

        return JsonResponse(status=200, data={
            "date:": s_from_data.data["date"],
            "from": from_currency,
            "to": to_currency,
            "conversion": usd_converted
        })

class ProductsForSellers(APIView):
    def get(self, id, company):
        #Check the company exists
        check_company = Company.objects.filter(id=company)

        if len(check_company) == 0:
            return JsonResponse(status=400, data={
                "error": "The company does not exist",
                "count": len(check_company)
                })
        
        #Get the products sold by this company
        products_sold = ProductSeller.objects.filter(company_id=company)
        product_data = products_sold.values()
        
        for idx, trade in enumerate(product_data):
            #Take the product_id and append meaningful data about this product to the trade
            product_id = trade.get("product_id")
            product_data_inner = Product.objects.get(id=product_id)
            product_s = ProductSerializer(product_data_inner)
            product_data[idx]["name"] = product_s.data.get("name")

        return Response(product_data)

class CurrencyValuesPastMonth(APIView):
    def get(self, request, currency):
        data = CurrencyPrice.objects.filter(currency_id=currency).order_by("-date")[:30]
        s = CurrencyPriceSerializer(data, many=True)
        return Response(s.data)

class TotalActionsOnDay(APIView):
    def get(self, request):
        now = datetime.now()
        lower = datetime(now.year, now.month, now.day, 0, 0, 0, 0)
        upper = datetime(now.year, now.month, now.day, 23, 59, 59, 9999)

        creation_count = Trade.objects.filter(date__range=[lower, upper]).count()
        edit_count = EditedTrade.objects.filter(edit_date__range=[lower, upper]).distinct().count()
        delete_count = DeletedTrade.objects.filter(deleted_at__range=[lower, upper]).count()
        erroneous_count = ErroneousTradeAttribute.objects.filter(date__range=[lower, upper]).count()
        correction_count = FieldCorrection.objects.filter(date__range=[lower, upper]).count()

        return JsonResponse(status=200, data={
            "creation_count": creation_count,
            "edit_count": edit_count,
            "delete_count": delete_count,
            "erroneous_fields": erroneous_count,
            "corrections": correction_count
        })

class CurrencyChanges(APIView):
    def get(self, request):
        currency_rows = dict()
        percentage_change = dict()
        day_one = None
        day_two = None
        day_three = None
        day_four = None
        day_five = None
        day_six = None
        day_seven = None

        for row in Trade.objects.raw("""
        SELECT id, currency_id, value, 
        (SELECT MAX(DATE) FROM currency_price) AS day_seven, 
        (DATE_SUB((SELECT MAX(DATE) FROM currency_price), INTERVAL 2 DAY)) AS day_six,
        (DATE_SUB((SELECT MAX(DATE) FROM currency_price), INTERVAL 3 DAY)) AS day_five,
        (DATE_SUB((SELECT MAX(DATE) FROM currency_price), INTERVAL 4 DAY)) AS day_four,
        (DATE_SUB((SELECT MAX(DATE) FROM currency_price), INTERVAL 5 DAY)) AS day_three,
        (DATE_SUB((SELECT MAX(DATE) FROM currency_price), INTERVAL 6 DAY)) AS day_two,
        (DATE_SUB((SELECT MAX(DATE) FROM currency_price), INTERVAL 7 DAY)) AS day_one
        FROM currency_price 
        WHERE DATE BETWEEN DATE_SUB((SELECT MAX(DATE) FROM currency_price), INTERVAL 7 DAY) AND (SELECT MAX(DATE) FROM currency_price) 
        ORDER BY currency_id, DATE DESC;
        """):
            day_one = row.day_one
            day_two = row.day_two
            day_three = row.day_three
            day_four = row.day_four
            day_five = row.day_five
            day_six = row.day_six
            day_seven = row.day_seven
            if row.currency_id not in currency_rows.keys():
                currency_rows[row.currency_id] = list()
                percentage_change[row.currency_id] = 0

            currency_rows[row.currency_id].append(row.value)

        #Calculate the change in value of the currencies compared to the start of the week and now.
        for currency in currency_rows:
            start_value = currency_rows[currency][0]
            end_value = currency_rows[currency][-1]
            change = round(end_value / start_value, 3)
            # print(str(currency) + ": " + str(currency_rows[currency]))
            # print("Start: " + str(start_value) + "   |   End: " + str(end_value))
            # print("Change: " + str(change), end="\n\n")
            percentage_change[currency] = change

        #Sort the currencies by their change, this allows us to get the largest appreciation and depreciation
        percentage_sorted = list({k: v for k, v in sorted(percentage_change.items(), key=lambda item: -item[1])})
        largest_appreciations = percentage_sorted[:3]
        largest_depreciations = percentage_sorted[-3:]
    
        appreciation_dict = list()
        depreciation_dict = list()

        #Format the data so its suitable to be returned as json.
        for index, currency in enumerate(largest_appreciations):
            appreciation_dict.append(dict())
            appreciation_dict[index]["currency"] = currency
            appreciation_dict[index]["change"] = str(percentage_change[currency]) + "%"
            appreciation_dict[index]["values"] = currency_rows[currency]
        for index, currency in enumerate(reversed(largest_depreciations)):
            depreciation_dict.append(dict())
            depreciation_dict[index]["currency"] = currency
            depreciation_dict[index]["change"] = str(round(1 - percentage_change[currency], 3)) + "%"
            depreciation_dict[index]["values"] = currency_rows[currency]

        return JsonResponse(status=200, data={
            "day_one": day_one,
            "day_two": day_two,
            "day_three": day_three,
            "day_four": day_four,
            "day_five": day_five,
            "day_six": day_six,
            "day_seven": day_seven,
            "largest_appreciations": appreciation_dict,
            "largest_depreciations": depreciation_dict})


class ErrorsAndCorrections(APIView):
    def getErrorsForTrade(self, tradeID, errors):
        returnList = []
        for error in errors:
            if error["trade_id"] == tradeID:
                returnList.append(error)
        return returnList

    def getCorrectionsForError(self, tradeID, errors, corrections):
        returnList = []
        for error in errors:
            if error["trade_id"] == tradeID:
                for correction in corrections:
                    if correction["error"] == error["id"]:
                        returnList.append(correction)
        return returnList


    def get(self, request):
        #Get all errors ordered by date
        errors = ErroneousTradeAttribute.objects.all().order_by("-date")
        corrections = FieldCorrection.objects.all()

        errors_s = ErroneousAttributeSerializer(errors, many=True)
        corrections_s = CorrectionSerializer(corrections, many=True)

        trades = []
        formatted_errors = []
        formatted_corrections = []

        for error in errors_s.data:
            formatted_errors.append(dict(error))

        for correction in corrections_s.data:
            formatted_corrections.append(dict(correction))

        for error in formatted_errors:
            if error["trade_id"] not in trades:
                trades.append(error["trade_id"])
    
        #Convert to nested trades with errors and corrections included
        finalList = []
        for trade in trades:
            errors = self.getErrorsForTrade(trade, formatted_errors)
            corrections = self.getCorrectionsForError(trade, formatted_errors, formatted_corrections)

            correction_count = 0

            for error in errors:
                foundCorrection = False
                if foundCorrection == True:
                    continue

                for correction in corrections:
                    if correction["error"] == error["id"]:
                        error["correction"] = correction
                        correction_count += 1
                        foundCorrection = True
                if foundCorrection == False:
                    error["correction"] = "null"


            finalList.append({"id": trade, "correction_count": correction_count, "errors": errors})
            
        return JsonResponse(status=200, data={"errors_and_corrections": finalList}, safe=False)

class DeleteCorrection(APIView):
    def post(self, request):
        cid = request.data["correctionID"]

        correction = FieldCorrection.objects.filter(id=cid)[0]
        correction_s = CorrectionSerializer(correction)

        #Get the trade being corrected and revert the correction
        trade = trade = Trade.objects.filter(id=request.data["tradeID"])[0]
        old_value = correction_s.data["old_value"]
        field = request.data["field_type"]

        if field == "QT":
            trade.quantity = old_value
        if field == "SP":
            trade.strike_price = old_value
        if field == "UP":
            trade.underlying_price = old_value
        trade.save()

        correction.delete()

        return JsonResponse(status=200, data={"success": "Correction has been deleted."})

class CreateCorrection(APIView):
    def post(self, request):

        print(request.data)
        #Get the error referenced in the correction
        error = ErroneousTradeAttribute.objects.filter(id=request.data["errorID"])[0]
        error_s = ErroneousAttributeSerializer(error)

        #Create new correction
        new_correction = FieldCorrection(
            error = error,
            old_value = error_s.data["erroneous_value"],
            new_value = request.data["new_value"],
            change_type = "USER",
            date = datetime.now()
        )
        new_correction.save()

        #Get the trade being corrected
        trade = Trade.objects.filter(id=request.data["tradeID"])[0]
        
        field = request.data["field_type"]
        new_value = request.data["new_value"]
        if field == "QT":
            trade.quantity = new_value
        if field == "SP":
            trade.strike_price = new_value
        if field == "UP":
            trade.underlying_price = new_value

        trade.save()

        return JsonResponse(status=200, data={"success": "Correction has been applied."})