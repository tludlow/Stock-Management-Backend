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

    def post(self, request):
        trade_data = request.data

        #Makes sure we have all the data we should in the request
        required_fields = ["trade_id", "maturity_date", "quantity", "strike_price", "underlying_price"]
        for field in required_fields:
            if field not in trade_data.keys():
                return JsonResponse(status=400, data={"error": "Missing the field '" + field + "' in the form."})


        #Get the trade being edited's database values
        trade_obj = Trade.objects.filter(id=trade_data["trade_id"])[0]
        trade_obj_s = TradeSerializer(trade_obj, many=False)

        #Check if data actually got returned
        if not trade_obj:
            return JsonResponse(status=400, data={"error": "Cannot edit the trade with id: " + 
                trade_data["trade_id"] + ". Cannot find the trade information."})
        
        #Check that the trade is not matured
        now = datetime.now()
        trade_maturity = datetime.strptime(trade_obj_s.data["maturity_date"], '%Y-%m-%d').date()

        if datetime(trade_maturity.year, trade_maturity.month, trade_maturity.day) < now:
            return JsonResponse(status=400, data={"error": "Trades can only be edited before they mature"})

        #Check that the trade was created within the last 3 days
        trade_created_at = datetime.strptime(trade_obj_s.data["date"], '%Y-%m-%dT%H:%M:%S.%fZ')
        date_delta = now - trade_created_at
        
        if date_delta.days > 3:
            return JsonResponse(status=400, data={"error": "Trades can only be edited within 3 days of creation"})


        #Compare the provided trade details with those known in the database to see if they have been edited
        #Format of tuples in edited_fields = (fieldName, newData, oldData) - will only contain changed fields
        edited_fields = list()
        editable_field = ["maturity_date", "strike_price", "underlying_price", "quantity"]

        for field in editable_field:
            if str(trade_data[field]) != str(trade_obj_s.data[field]):
                edited_fields.append((field, str(trade_data[field]), str(trade_obj_s.data[field])))
                # print("Mismatch on: " + field + ", has: " + str(trade_data[field]) + " and want: " + str(trade_obj_s.data[field]))

        #Check if we actually need to update anything
        if len(edited_fields) == 0:
            return JsonResponse(status=200, data={"message": "No need to edit, all fields the same"})

        #Update the fields in the trade row and store information about the edit
        #TODO A bit ugly but gets the job done, probably needs some good old abstraction
        returnInfo = dict()
        for field in edited_fields:
            if field[0] == "strike_price":
                Trade.objects.filter(id=trade_data["trade_id"]).update(strike_price=field[1])
                edited_strike = EditedTradeField(
                    trade_id=trade_data["trade_id"],
                    field="strike_price",
                    old_value=str(field[2]),
                    new_value=str(field[1])
                )
                edited_strike.save()
                returnInfo["old_strike_price"] = field[2]
                returnInfo["new_strike_price"] = field[1]
            elif field[0] == "maturity_date":
                Trade.objects.filter(id=trade_data["trade_id"]).update(maturity_date=field[1])
                edited_strike = EditedTradeField(
                    trade_id=trade_data["trade_id"],
                    field="maturity_date",
                    old_value=str(field[2]),
                    new_value=str(field[1])
                )
                edited_strike.save()
                returnInfo["old_maturity_date"] = field[2]
                returnInfo["new_maturity_date"] = field[1]
            elif field[0] == "underlying_price":
                Trade.objects.filter(id=trade_data["trade_id"]).update(underlying_price=field[1])
                edited_strike = EditedTradeField(
                    trade_id=trade_data["trade_id"],
                    field="underlying_price",
                    old_value=str(field[2]),
                    new_value=str(field[1])
                )
                edited_strike.save()
                returnInfo["old_underlying_price"] = field[2]
                returnInfo["new_underlying_price"] = field[1]
            elif field[0] == "quantity":
                Trade.objects.filter(id=trade_data["trade_id"]).update(quantity=field[1])
                edited_strike = EditedTradeField(
                    trade_id=trade_data["trade_id"],
                    field="quantity",
                    old_value=str(field[2]),
                    new_value=str(field[1])
                )
                edited_strike.save()
                returnInfo["old_quantity"] = field[2]
                returnInfo["new_quantity"] = field[1]


        if len(edited_fields) == 0:
            return JsonResponse(status=200, data={"changes": "No fields were modified"})
        else:
            return JsonResponse(status=200, data={"changes": returnInfo})