from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django import forms
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from api.serializers import *
from ..models import *
from ..serializers import *
import datetime
from calendar import monthrange
from django.core.paginator import Paginator
import random, string
from rest_framework.pagination import PageNumberPagination
from django.db import connection
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
import calendar

#You will need to create new models and a migration for the editedtrade table
#and deletedtrades table.

#Endpoint to create new edited trade

#Endpoint to create new deleted trade

#Get all trades edited in the last day, will need the old and new details

#Get all trades deleted in the last day

#Get all trades created in the last day

# https://docs.djangoproject.com/en/3.0/topics/db/sql/#performing-raw-queries
def raw_dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
    
class AvailableReportsYearList(APIView):
    def get(self, request):
        BASE_YEAR = 2010
        CURRENT_YEAR = datetime.datetime.now().year
        sql = ""

        for i in reversed(range(BASE_YEAR, CURRENT_YEAR+1)):
            lower = datetime.datetime(i, 1, 1, 0, 0, 0, 0)
            upper = datetime.datetime(i, 12, 31, 23, 59, 59, 9999)
            if i != CURRENT_YEAR:
                sql += " UNION "
            sql += f"""
            (SELECT 
                YEAR(date) as year 
            FROM trade
            WHERE 
                date>='{lower}' AND date<='{upper}'
            LIMIT 1)
            UNION
            (SELECT 
                YEAR(edit_date) as year 
            FROM edited_trade
            WHERE 
                edit_date>='{lower}' AND edit_date<='{upper}'
            LIMIT 1)
            UNION
            (SELECT 
                YEAR(deleted_at) as year 
            FROM deleted_trade
            WHERE 
                deleted_at>='{lower}' AND deleted_at<='{upper}'
            LIMIT 1)"""
        with connection.cursor() as cursor:
            cursor.execute(sql)
            data = raw_dictfetchall(cursor)
        return Response(data)

class AvailableReportsMonthList(APIView):
    def get(self, request, year):
        sql = ""
        FIRST_MONTH = 1
        LAST_MONTH = 12
        for i in reversed(range(FIRST_MONTH, LAST_MONTH+1)):
            days = calendar.monthrange(year, i)[1]
            lower = datetime.datetime(year, i, 1, 0, 0, 0, 0)
            upper = datetime.datetime(year, i, days, 23, 59, 59, 9999)
            if i != LAST_MONTH:
                sql += " UNION "
            sql += f"""
            (SELECT 
                MONTH(date) as month, 
                YEAR(date) as year 
            FROM trade
            WHERE 
                date>='{lower}' AND date<='{upper}'
            LIMIT 1)
            UNION
            (SELECT 
                MONTH(edit_date) as month, 
                YEAR(edit_date) as year 
            FROM edited_trade
            WHERE 
                edit_date>='{lower}' AND edit_date<='{upper}'
            LIMIT 1)
            UNION
            (SELECT 
                MONTH(deleted_at) as month, 
                YEAR(deleted_at) as year 
            FROM deleted_trade
            WHERE 
                deleted_at>='{lower}' AND deleted_at<='{upper}'
            LIMIT 1)"""
        with connection.cursor() as cursor:
            cursor.execute(sql)
            data = raw_dictfetchall(cursor)
        return Response(data)

class AvailableReportsDayList(APIView):
    def get(self, request, year, month):
        sql = ""
        FIRST_DAY = 1
        LAST_DAY = calendar.monthrange(year, month)[1]
        for i in reversed(range(FIRST_DAY, LAST_DAY+1)):
            lower = datetime.datetime(year, month, i, 0, 0, 0, 0)
            upper = datetime.datetime(year, month, i, 23, 59, 59, 9999)
            if i != LAST_DAY:
                sql += " UNION "
            sql += f"""
            (SELECT 
                DAY(date) as day, MONTH(date) as month, 
                YEAR(date) as year 
            FROM trade
            WHERE 
                date>='{lower}' AND date<='{upper}'
            LIMIT 1)
            UNION
            (SELECT 
                DAY(edit_date) as day, MONTH(edit_date) as month, 
                YEAR(edit_date) as year 
            FROM edited_trade
            WHERE 
                edit_date>='{lower}' AND edit_date<='{upper}'
            LIMIT 1)
            UNION
            (SELECT 
                DAY(deleted_at) as day, MONTH(deleted_at) as month, 
                YEAR(deleted_at) as year 
            FROM deleted_trade
            WHERE 
                deleted_at>='{lower}' AND deleted_at<='{upper}'
            LIMIT 1)"""
        sql += ""
        with connection.cursor() as cursor:
            cursor.execute(sql)
            data = raw_dictfetchall(cursor)
        return Response(data)

class Combine(object):
    def __len__(self):
        return len(self.created_trades) + len(self.edited_trades)

    def __init__(self, created, edited, deleted, date):
        self.created_trades = created
        self.num_of_new_trades = len(created)
        self.edited_trades = edited
        self.num_of_edited_trades = len(edited)
        self.deleted_trades = deleted
        self.num_of_deleted_trades = len(deleted)
        self.date_of_report = datetime.datetime(*date)
        self.created = datetime.datetime(*date) + timedelta(days=1)


def revert_dictfetchall(cursor, lower, upper):
    columns = [col[0] for col in cursor.description]
    vals = []
    for row in cursor.fetchall():
        trade = dict(zip(columns, row))
        with connection.cursor() as cursor2:
            cursor2.execute("""
            SELECT * FROM edited_trade WHERE trade_id_id=%s and edit_date>%s
            ORDER BY edit_date ASC
            """, [trade['id'], upper])
            post_edits = raw_dictfetchall(cursor2)

        revert = []
        for i in [EditedTrade(**x) for x in post_edits]:
            edit = i.get_attribute_edited_display()
            if edit not in revert:
                revert.append(edit)
                trade[edit] = i.old_value
        vals.append(trade)
    return vals
        


def fetch_edits(cursor, lower, upper):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    vals = []
    for row in cursor.fetchall():
        trade = dict(zip(columns, row))
        with connection.cursor() as cursor2:
            cursor2.execute("""
            SELECT * FROM edited_trade WHERE trade_id_id=%s and edit_date>%s
            ORDER BY edit_date ASC
            """, [trade['id'], upper])
            post_edits = raw_dictfetchall(cursor2)
        
        revert = []
        for i in [EditedTrade(**x) for x in post_edits]:
            edit = i.get_attribute_edited_display()
            if edit not in revert:
                revert.append(edit)
                trade[edit] = i.old_value
                

        with connection.cursor() as cursor3:
            cursor3.execute("""
            SELECT * FROM edited_trade WHERE trade_id_id=%s AND 
            edit_date>=%s AND edit_date<=%s
            """, [trade['id'], lower, upper])
            edits = raw_dictfetchall(cursor3)

        new = {'trade' : trade, 'num_of_edits' : len(edits), 'edits' : edits}
        vals.append(new)

    return vals

def report_data(year, month, day):
    lower = datetime.datetime(year, month, day, 0, 0, 0, 0)
    upper = datetime.datetime(year, month, day, 23, 59, 59, 9999)
    with connection.cursor() as cursor:
        # Get the new trades
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
            (SELECT trade_id_id FROM deleted_trade WHERE deleted_at < %s) DT
        ON DT.trade_id_id = T.id
        WHERE 
            DT.trade_id_id IS NULL and T.date>=%s and T.date<=%s 
        ORDER BY T.date DESC
        """, [upper, lower, upper])
        trades = revert_dictfetchall(cursor, lower, upper)
        
        # Get the edits
        cursor.execute("""
        SELECT 
            T.id, T.date, T.notional_amount, T.quantity, 
            T.maturity_date, T.underlying_price, T.strike_price, 
            P.name as product, T.product_id, T.buying_party_id, 
            BP.name as buying_party, 
            T.selling_party_id, SP.name as selling_party, 
            T.underlying_currency_id as underlying_currency, 
            T.notional_currency_id as notional_currency, ET.edit_date 
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
        INNER JOIN 
            (SELECT 
                trade_id_id, edit_date 
            FROM edited_trade 
            WHERE 
                edit_date>=%s and edit_date<=%s) ET
        ON ET.trade_id_id = T.id
        LEFT JOIN
            (SELECT trade_id_id FROM deleted_trade WHERE deleted_at < %s) DT
        ON DT.trade_id_id = T.id
        WHERE 
            DT.trade_id_id IS NULL
        GROUP BY 
            T.id, T.date, T.notional_amount, T.quantity, 
            T.maturity_date, 
            T.underlying_price, T.strike_price, product, buying_party, 
            selling_party, underlying_currency, notional_currency,
            ET.edit_date
        ORDER BY ET.edit_date DESC
        """, [lower, upper, upper])
        edits = fetch_edits(cursor, lower, upper)

        # Get the deletions
        cursor.execute("""
        SELECT 
            T.id, T.date, T.notional_amount, T.quantity, 
            T.maturity_date, T.underlying_price, T.strike_price, 
            P.name as product, T.product_id, T.buying_party_id, 
            BP.name as buying_party, 
            T.selling_party_id, SP.name as selling_party, 
            T.underlying_currency_id as underlying_currency, 
            T.notional_currency_id as notional_currency,
            DT.id as delete_id, DT.deleted_at 
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
        INNER JOIN
            (SELECT * FROM deleted_trade WHERE deleted_at>=%s
            and deleted_at<=%s) DT
        ON DT.trade_id_id = T.id
        ORDER BY DT.deleted_at DESC
        """, [lower, upper])
        deleted = revert_dictfetchall(cursor, lower, upper)
        date = (year, month, day)
        combined = Combine(trades, edits, deleted, date)
        s = ReportSerializer(combined, many=False)
        return s.data
class Report(APIView, PageNumberPagination):

    def get(self, request, year, month, day):
        if datetime.datetime.today() >= datetime.datetime(year, month, day):
            s = report_data(year, month, day)
            return Response(s)

            if len(s) > 0:
                return Response(s)
        
        return JsonResponse(status=400, 
                data={"error": "No report available for the given date."})

class SearchReport(APIView, PageNumberPagination):

    def get(self, request, year, month, day, search_term):
        s = report_data(year, month, day)
        new = {}
        new['date_of_report'] = s['date_of_report']
        new['created'] = s['created']
        new['num_of_new_trades'] = s['num_of_new_trades']
        created_trades = []
        for i in s["created_trades"]:
            for j in i.values():
                if search_term.lower() in str(j).lower():
                    created_trades.append(i)
                    break
        new['created_trades'] = created_trades
        
        edited_trades = []
        for i in s["edited_trades"]:
            for j in i["trade"] + i["edits"]:
                for k in j.values():
                    if search_term.lower() in str(k).lower():
                        edited_trades.append(i)
                        break
        new['edited_trades'] = edited_trades

        deleted_trades = []
        for i in s["deleted_trades"]:
            for j in i.values():
                if search_term.lower() in str(j).lower():
                    deleted_trades.append(i)
                    break
        new['deleted_trades'] = deleted_trades

        return Response(new)