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
from datetime import datetime, timedelta, timezone, date

class DeleteDerivativeTrade(APIView):
    def post(self, request):
        trade_data = request.data
        requiredFields = ["trade_id"]
        for field in requiredFields:
            if field not in trade_data.keys():
                return JsonResponse(status=400, data={"error": "Missing the field '" + field + "' in the form."})

        #Get the trade, if it exists
        found_trade = Trade.objects.filter(id=trade_data["trade_id"])

        #No trade has been found with this ID
        if len(found_trade) == 0:
            return JsonResponse(status=400, data={"error": "No trade with id: " + trade_data["trade_id"] +
                " has been found in the database"})

        # Ensure that the trade has not already been deleted
        deleted_already = DeletedTrade.objects.filter(trade_id=trade_data["trade_id"])
        if len(deleted_already) > 0:
            return JsonResponse(status=400, data={"error": "Trade with id: " + trade_data["trade_id"] +
                " has already been deleted."})

        deleted_already = DeletedTrade.objects.filter(trade_id=trade_data["trade_id"])
        trade_serialized = list(found_trade.values())
        
        #Check if the trade was created within the last 3 days or hasnt matured.
        trade_created_at = trade_serialized[0]["date"]
        now = datetime.now(timezone.utc)
        date_delta = now - trade_created_at
        
        if date_delta.days > 3:
            return JsonResponse(status=400, data={"error": "Trades can only be deleted within 3 days of creation"})

        #Check if the trade has matured
        trade_maturity = trade_serialized[0]["maturity_date"]
        
        #Need to convert the date to a datetime for comparison.
        if datetime(trade_maturity.year, trade_maturity.month, trade_maturity.day, tzinfo=timezone.utc) < now :
            return JsonResponse(status=400, data={"error": "Trades can only be deleted before they mature"})

        trade = trade_serialized[0]

        #Create a new entry into the deleted trades table before we delete from trades
        new_deleted_trade = DeletedTrade(
            trade_id=found_trade[0],
            deleted_at=now,
        )
        new_deleted_trade.save()

        #Delete all erroneous data and corrections referncing this trade
        errors = ErroneousTradeAttribute.objects.filter(trade_id=trade_data["trade_id"])
        errors.delete()

        return JsonResponse(status=200, data={"success": "Trade has been deleted."})