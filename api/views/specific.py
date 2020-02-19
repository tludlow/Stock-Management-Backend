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