from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *

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
        fields = ('date', 'value', 'currency')

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

class ReportSerializer(serializers.ModelSerializer):

    edits = serializers.SerializerMethodField()
    deleted = serializers.SerializerMethodField()
    class Meta:
        model = Trade
        fields = ('id', 'date', 'notional_amount', 'quantity', 
                  'maturity_date', 'underlying_price', 'strike_price', 
                  'product', 'buying_party', 'selling_party', 
                  'notional_currency', 'underlying_currency', 'edits', 
                  'deleted')

    def get_edits(self, parent):
        return EditedTradeSerializer(many=True, instance=parent.edited_trade.all()).data
    
    def get_deleted(self, parent):
        return DeletedTradeSerializer(many=True, instance=parent.deleted_trade.all()).data
class AvailableReportsYearSerializer(serializers.Serializer):
    year = serializers.CharField(max_length=4)

class AvailableReportsMonthSerializer(serializers.Serializer):
    year = serializers.CharField(max_length=4)
    month = serializers.CharField(max_length=2)

class AvailableReportsDaySerializer(serializers.Serializer):
    year = serializers.CharField(max_length=4)
    month = serializers.CharField(max_length=2)
    day = serializers.CharField(max_length=2)
