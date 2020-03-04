from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *
import dateutil.parser
import datetime
from datetime import timedelta, timezone, date
import pytz
# from .views.reports import Combine
class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

class ProductSellerSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductSeller
        fields = ('product', 'company')

class ProductPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductPrice
        fields = '__all__'

class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = '__all__'

class CurrencyPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = CurrencyPrice
        fields = '__all__'

class StockPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockPrice
        fields = ('company', 'date', 'value')

class TradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trade
        fields = '__all__'

class EditedTradeSerializer(serializers.ModelSerializer):

    attribute_edited = serializers.CharField(source='get_attribute_edited_display')
    # 'attribute_edited', 
    class Meta:
        model = EditedTrade
        fields = ('id', 'attribute_edited', 'edit_date', 'old_value', 'new_value')
class DeletedTradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeletedTrade
        fields = ('id', 'deleted_at')

class JoinedTradeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    date = serializers.DateTimeField()
    notional_amount = serializers.FloatField()
    quantity = serializers.IntegerField()
    maturity_date = serializers.DateField()
    underlying_price = serializers.FloatField()
    strike_price = serializers.FloatField()
    product = serializers.CharField()
    buying_party = serializers.CharField()
    selling_party = serializers.CharField()
    notional_currency = serializers.CharField()
    underlying_currency = serializers.CharField()

class DeletedTradesSerializer(JoinedTradeSerializer):
    delete_id = serializers.IntegerField()
    deleted_at = serializers.DateTimeField()

class EditedTradesSerializer(serializers.Serializer):
    trade = serializers.SerializerMethodField()
    num_of_edits = serializers.SerializerMethodField()
    edits = serializers.SerializerMethodField()

    def get_trade(self, parent):
        print(parent)
        trade = JoinedTradeSerializer(parent['trade'], many=False).data
        return trade

    def get_num_of_edits(self, parent):
        return parent['num_of_edits']
        
    def get_edits(self, parent):
        return EditedTradeSerializer([EditedTrade(**x) for x in parent['edits']], many=True).data

class ReportSerializer(serializers.Serializer):
    date_of_report = serializers.DateTimeField()
    created = serializers.DateTimeField()
    num_of_new_trades = serializers.IntegerField()
    created_trades = serializers.SerializerMethodField()
    num_of_edited_trades = serializers.IntegerField()
    edited_trades = serializers.SerializerMethodField()
    num_of_deleted_trades = serializers.IntegerField()
    deleted_trades = serializers.SerializerMethodField()

    def get_created_trades(self, parent):
        return JoinedTradeSerializer(parent.created_trades, many=True).data
    
    def get_edited_trades(self, parent):
        print(parent)
        return EditedTradesSerializer(parent.edited_trades, many=True).data

    def get_deleted_trades(self, parent):
        return DeletedTradesSerializer(parent.deleted_trades, many=True).data

class AvailableReportsYearSerializer(serializers.Serializer):
    year = serializers.CharField(max_length=4)

class AvailableReportsMonthSerializer(serializers.Serializer):
    year = serializers.CharField(max_length=4)
    month = serializers.CharField(max_length=2)

class AvailableReportsDaySerializer(serializers.Serializer):
    year = serializers.CharField(max_length=4)
    month = serializers.CharField(max_length=2)
    day = serializers.CharField(max_length=2)
