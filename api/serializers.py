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