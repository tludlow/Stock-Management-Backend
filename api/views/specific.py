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

        data = Trade.objects.all().order_by('-date')[(page_number-1)*page_size : page_number*page_size]
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

            #print(str(idx) + ":  " + str(trade), end="\n\n")

        #Modified the structure of a trade, will need to use a custom serializer.
        return Response(trade_data)

class RecentTradesByCompanyForProduct(APIView):
    def get(self, request, buyer, product):
        #Get pagination data before the request so that it saves memory and is quicker to query.
        page_number = int(self.request.query_params.get("page_number", 1))
        page_size = int(self.request.query_params.get("page_size", 150))

        data = Trade.objects.filter(buying_party=buyer, product_id=product).order_by('-date')[(page_number-1)*page_size : page_number*page_size]
        
        s = TradeSerializer(data, many=True)
        return Response(s.data)

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


