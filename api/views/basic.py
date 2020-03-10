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
from django.core.paginator import Paginator
import random, string
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db import connection

def raw_dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

@method_decorator(cache_page(20), name='dispatch')
class CompanyList(APIView):
    def get(self, request):
        data = Company.objects.all()
        s = CompanySerializer(data, many=True)
        return Response(s.data)

class CompanyByIDList(APIView):
    def get(self, request, id):
        data = Company.objects.filter(id=id)
        s = CompanySerializer(data, many=True)
        return Response(s.data)
    
class CompanyByNameList(APIView):
    def get(self, request, name):
        data = Company.objects.filter(name=name)
        s = CompanySerializer(data, many=True)
        return Response(s.data)
    
@method_decorator(cache_page(20), name='dispatch')
class ProductList(APIView):
    def get(self, request):
        data = Product.objects.all()

        #Pagination
        # page_number = self.request.query_params.get("page_number", 1)
        # page_size = self.request.query_params.get("page_size", 25)
        # paginator = Paginator(data, page_size)
        # s = ProductSerializer(paginator.page(page_number), many=True)

        s = ProductSerializer(data, many=True)
        return Response(s.data)

class ProductByIDList(APIView):

    def get(self, request, id):
        data = Product.objects.filter(id=id)
        s = ProductSerializer(data, many=True)
        return Response(s.data)

class ProductByNameList(APIView):
    def get(self, request, name):
        data = Product.objects.filter(name=name)
        s = ProductSerializer(data, many=True)
        return Response(s.data)

class SellerList(APIView):
    def get(self, request):
        data = ProductSeller.objects.all()
        s = ProductSellerSerializer(data, many=True)
        return Response(s.data)

class SellerListByProduct(APIView):
    def get(self, request, product):
        data = ProductSeller.objects.filter(id=product)
        s = ProductSellerSerializer(data, many=True)
        return Response(s.data)

class SellerListByCompany(APIView):
    def get(self, request, company):
        data = ProductSeller.objects.filter(company=company)
        s = ProductSellerSerializer(data, many=True)
        return Response(s.data)

@method_decorator(cache_page(20), name='dispatch')
class AllCurrenciesList(APIView):
    def get(self, request):
        data = Currency.objects.all()
        s = CurrencySerializer(data, many=True)
        return Response(s.data)

class CurrencyPriceList(APIView):
    def get(self, request):
        data = CurrencyPrice.objects.all().order_by('date')
        s = CurrencyPriceSerializer(data, many=True)
        return Response(s.data)

class StockPriceList(APIView):
    def get(self, request):
        data = StockPrice.objects.all().order_by('date')
        s = StockPriceSerializer(data, many=True)
        return Response(s.data)

class CurrencyList(APIView):
    def get(self, request, currency):
        data = CurrencyPrice.objects.filter(currency=currency).order_by('date')
        s = CurrencyPriceSerializer(data, many=True)
        return Response(s.data)

class CurrencyYearList(APIView):
    def get(self, request, currency, year):
        data = CurrencyPrice.objects.filter(currency=currency, date__year=year).order_by('date')
        s = CurrencyPriceSerializer(data, many=True)
        return Response(s.data)

class CurrencyMonthList(APIView):
    def get(self, request, currency, year, month):
        lower = datetime.date(year, month, 1)
        days = monthrange(year, month)
        upper = lower + datetime.timedelta(days=days[1]-1)
        data = CurrencyPrice.objects.filter(currency=currency, date__range=[lower, upper]).order_by('date')
        s = CurrencyPriceSerializer(data, many=True)
        return Response(s.data)

class CurrencyDayList(APIView):
    def get(self, request, currency, year, month, day):
        date = datetime.date(year, month, day)
        data = CurrencyPrice.objects.filter(currency=currency, date=date).order_by('date')
        s = CurrencyPriceSerializer(data, many=True)
        return Response(s.data)

class StockList(APIView):
    def get(self, request, company):
        data = StockPrice.objects.filter(company=company).order_by('date')
        s = StockPriceSerializer(data, many=True)
        return Response(s.data)

class StockYearList(APIView):
    def get(self, request, company, year):
        data = StockPrice.objects.filter(company=company, date__year=year).order_by('date')
        s = StockPriceSerializer(data, many=True)
        return Response(s.data)

class StockMonthList(APIView):
    def get(self, request, company, year, month):
        lower = datetime.date(year, month, 1)
        days = monthrange(year, month)
        upper = lower + datetime.timedelta(days=days[1]-1)
        data = StockPrice.objects.filter(company=company, date__range=[lower, upper]).order_by('date')
        s = StockPriceSerializer(data, many=True)
        return Response(s.data)

class StockDayList(APIView):
    def get(self, request, company, year, month, day):
        date = datetime.date(year, month, day)
        data = StockPrice.objects.filter(company=company, date=date).order_by('date')
        s = StockPriceSerializer(data, many=True)
        return Response(s.data)

class TradeList(APIView):
    def get(self, request):
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
                DT.trade_id_id IS NULL
            ORDER BY T.date DESC
            """)
            data = raw_dictfetchall(cursor)
        s = JoinedTradeSerializer(data, many=True)
        return Response(s.data)
class TradeIDList(APIView):

    def get(self, request, id):
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
            """, [id])
            data = raw_dictfetchall(cursor)
        s = JoinedTradeSerializer(data, many=True)
        return Response(s.data)
class TradeYearList(APIView):
    def get(self, request, year):
        lower = datetime.datetime(year, 1, 1, 0, 0, 0, 0)
        upper = datetime.datetime(year, 12, 31, 23, 59, 59, 9999)
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
                DT.trade_id_id IS NULL and T.date>=%s and T.date<=%s 
            ORDER BY T.date DESC
            """, [lower, upper])
            data = raw_dictfetchall(cursor)
        s = JoinedTradeSerializer(data, many=True)
        return Response(s.data)
class TradeMonthList(APIView):
    def get(self, request, year, month):
        days = calendar.monthrange(year, month)[1]
        lower = datetime.datetime(year, month, 1, 0, 0, 0, 0)
        upper = datetime.datetime(year, month, days, 23, 59, 59, 9999)
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
                DT.trade_id_id IS NULL and T.date>=%s and T.date<=%s 
            ORDER BY T.date DESC
            """, [lower, upper])
            data = raw_dictfetchall(cursor)
        s = JoinedTradeSerializer(data, many=True)
        return Response(s.data)

class TradeDayList(APIView):
    def get(self, request, year, month, day):
        lower = datetime.datetime(year, month, day, 0, 0, 0, 0)
        upper = datetime.datetime(year, month, day, 23, 59, 59, 9999)
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
                DT.trade_id_id IS NULL and T.date>=%s and T.date<=%s 
            ORDER BY T.date DESC
            """, [lower, upper])
            data = raw_dictfetchall(cursor)
        s = JoinedTradeSerializer(data, many=True)
        return Response(s.data)

class TradeMaturityYearList(APIView):
    def get(self, request, year):
        lower = datetime.datetime(year, 1, 1, 0, 0, 0, 0)
        upper = datetime.datetime(year, 12, 31, 23, 59, 59, 9999)
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
                DT.trade_id_id IS NULL and T.maturity_date>=%s and T.maturity_date<=%s 
            ORDER BY T.date DESC
            """, [lower, upper])
            data = raw_dictfetchall(cursor)
        s = JoinedTradeSerializer(data, many=True)
        return Response(s.data)
class TradeMaturityMonthList(APIView):
    def get(self, request, year, month):
        days = calendar.monthrange(year, month)[1]
        lower = datetime.datetime(year, month, 1, 0, 0, 0, 0)
        upper = datetime.datetime(year, month, days, 23, 59, 59, 9999)
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
                DT.trade_id_id IS NULL and T.maturity_date>=%s and T.maturity_date<=%s 
            ORDER BY T.date DESC
            """, [lower, upper])
            data = raw_dictfetchall(cursor)
        s = JoinedTradeSerializer(data, many=True)
        return Response(s.data)

class TradeMaturityDayList(APIView):
    def get(self, request, year, month, day):
        lower = datetime.datetime(year, month, day, 0, 0, 0, 0)
        upper = datetime.datetime(year, month, day, 23, 59, 59, 9999)
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
                DT.trade_id_id IS NULL and T.maturity_date>=%s and T.maturity_date<=%s 
            ORDER BY T.date DESC
            """, [lower, upper])
            data = raw_dictfetchall(cursor)
        s = JoinedTradeSerializer(data, many=True)
        return Response(s.data)

class TradeBuyerList(APIView):
    def get(self, request, buyer):
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
                BP.name=%s AND DT.trade_id_id IS NULL
            ORDER BY T.date DESC
            """, [buyer])
            data = raw_dictfetchall(cursor)
        s = JoinedTradeSerializer(data, many=True)
        return Response(s.data)

class TradeSellerList(APIView):
    def get(self, request, seller):
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
                SP.name=%s AND DT.trade_id_id IS NULL
            ORDER BY T.date DESC
            """, [buyer])
            data = raw_dictfetchall(cursor)
        s = JoinedTradeSerializer(data, many=True)
        return Response(s.data)

class TradeBuyerSellerList(APIView):
    def get(self, request, buyer, seller):
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
                SP.name=%s AND BP.name=%s AND DT.trade_id_id IS NULL
            ORDER BY T.date DESC
            """, [buyer])
            data = raw_dictfetchall(cursor)
        s = JoinedTradeSerializer(data, many=True)
        return Response(s.data)

