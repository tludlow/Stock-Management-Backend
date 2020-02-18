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

class TradeRecentList(APIView):
    def get(self, request):
        data = Trade.objects.all().order_by('-date')

        #Pagination 
        page_number = self.request.query_params.get("page_number", 1)
        page_size = self.request.query_params.get("page_size", 12)
        paginator = Paginator(data, page_size)
        
        s = TradeSerializer(paginator.page(page_number), many=True)
        return Response(s.data)