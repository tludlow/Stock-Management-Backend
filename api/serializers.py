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
    class Meta:
        model = EditedTrade
        fields = ('id', 'attribute_edited', 'edit_date', 'old_value', 'new_value')
class DeletedTradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeletedTrade
        fields = ('id', 'deleted_at')

class DeletedTradesSerializer(serializers.Serializer):
    trade = serializers.SerializerMethodField()
    deletion = serializers.SerializerMethodField()
    
    def get_trade(self, parent):
        return TradeSerializer(parent, many=False).data
    
    def get_deletion(self, parent):
        print(parent.deleted_trade.all())
        return DeletedTradeSerializer(many=True, instance=parent.deleted_trade.all()).data

class EditedTradesSerializer(serializers.Serializer):
    trade = serializers.SerializerMethodField()
    num_of_edits = serializers.SerializerMethodField()
    edits = serializers.SerializerMethodField()

    def get_trade(self, parent):
        trade = TradeSerializer(parent, many=False).data
        self.edits = self.find_edits(parent)
        seen_revert = []
        seen_today = []
        year, month, day = self.context.get("date")

        utc=pytz.UTC
        date = datetime.datetime(year, month, day).replace(tzinfo=utc)
        for i in self.edits:
            edit = i["attribute_edited"]
            edit_date = dateutil.parser.isoparse(i['edit_date']).replace(tzinfo=utc)
            if edit_date > date:
                if edit not in seen_revert:
                    seen_revert.append(edit)
                    trade[edit] = i["old_value"]
            if edit_date == date:
                if edit not in seen_today:
                    seen_today.append(edit)
                    trade[edit] = i["new_value"]
        return trade

    def find_edits(self, parent):
        year, month, day = self.context.get("date")
        d = datetime.datetime.now()
        n_year, n_month, n_day = d.year, d.month, d.day
        lower = datetime.datetime(year, month, day, 0, 0, 0, 0)
        upper = datetime.datetime(n_year, n_month, n_day, 23, 59, 59, 9999)
        return EditedTradeSerializer(many=True, instance=parent.edited_trade.filter(edit_date__range=[lower, upper]).order_by('edit_date')).data

    def get_num_of_edits(self, parent):
        year, month, day = self.context.get("date")
        lower = datetime.datetime(year, month, day, 0, 0, 0, 0)
        upper = datetime.datetime(year, month, day, 23, 59, 59, 9999)
        self.edits = EditedTradeSerializer(many=True, instance=parent.edited_trade.filter(edit_date__range=[lower, upper]).order_by('-edit_date')).data
        return len(self.edits)
        
    def get_edits(self, parent):
        return self.edits 
        
class ReportSerializer(serializers.Serializer):
    created = serializers.DateTimeField()
    num_of_new_trades = serializers.IntegerField()
    created_trades = serializers.SerializerMethodField()
    num_of_edited_trades = serializers.IntegerField()
    edited_trades = serializers.SerializerMethodField()
    num_of_deleted_trades = serializers.IntegerField()
    deleted_trades = serializers.SerializerMethodField()

    def get_created_trades(self, parent):
        return TradeSerializer(parent.created_trades, many=True).data#["created_trades"]
    
    def get_edited_trades(self, parent):
        year, month, day = parent.date
        return EditedTradesSerializer(parent.edited_trades, context={'date':(year, month, day)}, many=True).data#parent.edited_trades#["edited_trades"]

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
