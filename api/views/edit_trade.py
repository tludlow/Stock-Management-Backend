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
from random import randint
from datetime import datetime, timedelta, timezone, date

class EditDerivativeTrade(APIView):
    
    def update(self, updated, original, obj):
        tags = {'date' : 'DT', 'product' : 'PR', 'buying_party' : 'BP',
                'selling_party' : 'SP', 'notional_amount' : 'NA', 
                'notional_currency' : 'NC', 'quantity' : 'QT',
                'maturity_date' : 'MD', 'underlying_price' : 'UP',
                'underlying_currency' : 'UC', 'strike_price' : 'ST'
        }

        trade = Trade.objects.filter(id=original["id"])
        trade.update(     
            date=updated["date"], 
            product=updated["product"], 
            buying_party=updated["buying_party"], 
            selling_party=updated["selling_party"], 
            notional_amount=updated["notional_amount"], 
            notional_currency=updated["notional_currency"], 
            quantity=updated["quantity"], 
            maturity_date=updated["maturity_date"], 
            underlying_price=updated["underlying_price"], 
            underlying_currency=updated["underlying_currency"], 
            strike_price=updated["strike_price"])
        
        new = TradeSerializer(trade[0], many=False).data

        return_info = {}
        for item in updated.keys():
            if new[item] != original[item]:
                update_made = True
                new_edit = EditedTrade(
                    trade_id=obj,
                    edit_date=datetime.now(),
                    attribute_edited=tags[item],
                    old_value=str(original[item]),
                    new_value=str(new[item])
                )
                new_edit.save()
                return_info["old_"+item] = original[item]
                return_info["new_"+item] = new[item]
        return return_info

    def post(self, request):
        trade_data = request.data
        edits = []
        allowed_fields = ["trade_id", "date", "product", "buying_party", 
                    "selling_party", "notional_amount", "notional_currency", 
                    "quantity",  "maturity_date", "underlying_price", 
                    "underlying_currency", "strike_price"]
        #Makes sure we have all the data we should in the request
        if "trade_id" not in trade_data.keys():
            return JsonResponse(status=400, data={"error": "No trade id provided."})
        elif len(trade_data.keys()) <= 2:
            return JsonResponse(status=400, data={"error": "Too many or too few attributes provided."})
        else:
            for param in trade_data.keys():
                if param not in allowed_fields:
                    return JsonResponse(status=400, data={"error": "Field '" + param + "' is not permitted."})
                elif param!="trade_id":
                    edits.append(param)

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
        print("trade mat: ", datetime(trade_maturity.year, trade_maturity.month, trade_maturity.day))
        print("now: ", now)
        if datetime(trade_maturity.year, trade_maturity.month, trade_maturity.day) < now:
            return JsonResponse(status=400, data={"error": "Trades can only be edited before they mature"})

        #Check that the trade was created within the last 3 days
        trade_created_at = datetime.strptime(trade_obj_s.data["date"], '%Y-%m-%dT%H:%M:%SZ').date()
        date_delta = now - datetime(trade_created_at.year, trade_created_at.month, trade_created_at.day)
        if date_delta.days > 3:
            return JsonResponse(status=400, data={"error": "Trades can only be edited within 3 days of creation"})

        #Compare the provided trade details with those known in the database to see if they have been edited

        updated = {}
        for i in allowed_fields[1:]:
            updated[i] = trade_data.get(i, trade_obj_s.data[i])
        
        return_info = self.update(updated, trade_obj_s.data, trade_obj)
        if len(return_info) < 2:
            return JsonResponse(status=200, data={"message": "No need to edit, all fields the same"})
        else:
            return_trade = Trade.objects.filter(id=trade_data["trade_id"])
            return_s = TradeSerializer(return_trade, many=True)
            return JsonResponse(status=200, data={"changes": return_info, "trade": return_s.data})