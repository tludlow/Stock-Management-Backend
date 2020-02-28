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
from django.core.paginator import Paginator
import random, string
from django.core.paginator import Paginator

#You will need to create new models and a migration for the editedtrade table
#and deletedtrades table.

#Endpoint to create new edited trade

#Endpoint to create new deleted trade

#Get all trades edited in the last day, will need the old and new details

#Get all trades deleted in the last day

#Get all trades created in the last day
class AvailableReportsYearList(APIView):
    def get(self, request):
        data = Trade.objects.raw("""
            SELECT DISTINCT 1 as id, YEAR(date) as year
            FROM trade
            ORDER BY year DESC""")
        s = AvailableReportsYearSerializer(data, many=True)
        return Response(s.data)

class AvailableReportsMonthList(APIView):
    def get(self, request, year):
        data = Trade.objects.raw("""
        SELECT DISTINCT 1 as id, YEAR(date) as year, MONTH(date) as month
        FROM trade WHERE YEAR(date)=%s
        ORDER BY month DESC""", [year])
        s = AvailableReportsMonthSerializer(data, many=True)
        return Response(s.data)

class AvailableReportsDayList(APIView):
    def get(self, request, year, month):
        data = Trade.objects.raw("""
        SELECT DISTINCT 1 as id, YEAR(date) as year, MONTH(date) as month,
        DAY(date) as day
        FROM trade WHERE YEAR(date)=%s AND MONTH(date)=%s AND date < CURDATE()
        ORDER BY day DESC""", [year, month])
        s = AvailableReportsDaySerializer(data, many=True)
        return Response(s.data)

class Report(APIView):
    def get(self, request, year, month, day):
        if datetime.datetime.today() > datetime.datetime(year, month, day):
            lower = datetime.datetime(year, month, day, 0, 0, 0, 0)
            upper = datetime.datetime(year, month, day, 23, 59, 59, 9999)
            data = Trade.objects.filter(date__range=[lower, upper]).order_by('date')
            page_number = self.request.query_params.get("page_number", 1)
            page_size = self.request.query_params.get("page_size", 25)
            paginator = Paginator(data, page_size)
            s = ReportSerializer(paginator.page(page_number), many=True)
            if len(s.data) > 0:
                return Response(s.data)
        return JsonResponse(status=400, 
                data={"error": "No report available for the given date."})
