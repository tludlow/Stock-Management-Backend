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
from random import randint
import dateutil.parser
import datetime
from datetime import datetime, timedelta, timezone, date
from django.db import connection

def raw_dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
class EditDerivativeTrade(APIView):
    
    # Given dictionaries containing the updated and original attributes 
    # respectively, as well as a trade object, updates the trade, creates new  
    # EditedTrade tuples for each edited attribute and returns the differences
    def update(self, updated, original, obj, edit_date=datetime.now()):
        # Tags for the DB
        tags = {'product' : 'PR', 'buying_party' : 'BP',
                'selling_party' : 'SP', 
                'notional_currency' : 'NC', 'quantity' : 'QT',
                'maturity_date' : 'MD', 'underlying_price' : 'UP',
                'underlying_currency' : 'UC', 'strike_price' : 'ST'
        }

        # Update the trade
        trade = Trade.objects.filter(id=original["id"])
        trade.update(     
            product=updated["product"], 
            buying_party=updated["buying_party"], 
            selling_party=updated["selling_party"], 
            notional_currency=updated["notional_currency"], 
            quantity=updated["quantity"], 
            maturity_date=updated["maturity_date"], 
            underlying_price=updated["underlying_price"], 
            underlying_currency=updated["underlying_currency"], 
            strike_price=updated["strike_price"])
        
        # Serialize the updated trade
        new = TradeSerializer(trade[0], many=False).data

        # Check difference between original & updated trade
        return_info = {}
        for item in updated.keys():
            if new[item] != original[item]:
                new_edit = EditedTrade(
                    trade_id=obj,
                    edit_date=edit_date,
                    attribute_edited=tags[item],
                    old_value=str(original[item]),
                    new_value=str(new[item])
                )
                new_edit.save()
                return_info["old_"+item] = original[item]
                return_info["new_"+item] = new[item]
        return return_info

    def post(self, request):
        raw_trade_data = request.data
        print(raw_trade_data)
        trade_data = {}
        allowed_fields = ["trade_id", "quantity",  "maturity_date", 
                         "underlying_price", "strike_price"]
        extra_fields = ['id', 'date', 'notional_amount', 'quantity', 'maturity_date', 'underlying_price', 'strike_price', 'product', 'product_id', 'buying_party', 'buying_party_id', 'selling_party', 'selling_party_id', 'notional_currency', 'underlying_currency', 'trade_id']
        #Makes sure we have all the data we should in the request
        if "trade_id" not in raw_trade_data.keys():
            return JsonResponse(status=400, data={"error": "No trade id provided."})
        elif len(raw_trade_data.keys()) <= 1:
            return JsonResponse(status=400, data={"error": "Too few attributes provided."})
        else:
            for param in raw_trade_data.keys():
                print("param", param, "is in", extra_fields, "truth:", param in extra_fields)
                if param not in allowed_fields and param not in extra_fields:
                    print("param", param, "is in", extra_fields, "truth:", param in extra_fields)
                    return JsonResponse(status=400, data={"error": "Field '" + param + "' is not permitted."})
                elif param in allowed_fields:
                    print("ADDING", param)
                    trade_data[param] = raw_trade_data[param]

        #Get the trade being edited's database values
        trades = Trade.objects.filter(id=trade_data["trade_id"])
        if len(trades) == 0:
            return JsonResponse(status=400, data={"error": "No trade with id: " + trade_data["trade_id"] +
                " has been found in the database"})
       
        trade_obj = trades[0]
        trade_obj_s = TradeSerializer(trade_obj, many=False)

        # Ensure that the trade has not already been deleted
        deleted_already = DeletedTrade.objects.filter(trade_id=trade_data["trade_id"])
        if len(deleted_already) > 0:
            return JsonResponse(status=400, data={"error": "Trade with id: " + trade_data["trade_id"] +
                " has been deleted."})

        #Check that the trade is not matured
        now = datetime.now()
        trade_maturity = datetime.strptime(trade_obj_s.data["maturity_date"], '%Y-%m-%d').date()

        if datetime(trade_maturity.year, trade_maturity.month, trade_maturity.day) < now:
            return JsonResponse(status=400, data={"error": "Trades can only be edited before they mature"})

        #Check that the trade was created within the last 3 days
        trade_created_at = dateutil.parser.isoparse(trade_obj_s.data["date"])
        date_delta = now - datetime(trade_created_at.year, trade_created_at.month, trade_created_at.day)

        # if date_delta.days > 3:
        #     return JsonResponse(status=400, data={"error": "Trades can only be edited within 3 days of creation"})

        #Compare the provided trade details with those known in the database to see if they have been edited
        updated = trade_obj_s.data
        for i in [x for x in allowed_fields if x not in ['trade_id', 'product_id']]:
            print(i)
            updated[i] = trade_data.get(i, trade_obj_s.data[i])

        if datetime.strptime(updated['maturity_date'], '%Y-%m-%d').date() < now.date():
            return JsonResponse(status=400, data={"error": "Maturity date can't be set to the past"})

        return_info = self.update(updated, trade_obj_s.data, trade_obj)

        if len(return_info) < 2:
            return JsonResponse(status=200, data={"message": "No need to edit, all fields the same"})
        else:
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
                """, [trade_data["trade_id"]])
                data = raw_dictfetchall(cursor)
            s = JoinedTradeSerializer(data, many=True)
            return JsonResponse(status=200, data={"changes": return_info, "trade": s.data})
