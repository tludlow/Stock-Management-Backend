from django.db import models
from django.db.models.functions import Now


class Company(models.Model):

    class Meta():
        db_table = "company"
        

    id = models.CharField(max_length=8, primary_key = True, unique=True)
    name = models.CharField(max_length=80)

class Product(models.Model):

    class Meta():
        db_table = "product"
        

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, unique=True)

class ProductSeller(models.Model):

    class Meta():
        db_table = "product_seller"
        unique_together = (('product', 'company'),)
        

    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                                        related_name="product_selling")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, 
                                        related_name="company")

class ProductPrice(models.Model):

    class Meta():
        db_table = "product_price"
        unique_together = (('date', 'product'),)
        

    id = models.AutoField(primary_key=True)
    date = models.DateField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                                        related_name="product")
    value = models.FloatField()

class Currency(models.Model):

    class Meta():
        db_table = "currency"
        

    currency = models.CharField(max_length=3, primary_key=True)

class CurrencyPrice(models.Model):

    class Meta():
        db_table = "currency_price"
        unique_together = (('currency', 'date'),)
        

    id = models.AutoField(primary_key=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    date = models.DateField()
    value = models.FloatField()

class StockPrice(models.Model):

    class Meta():
        db_table = "stock_price"
        unique_together = (('company', 'date'),)
        

    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField()
    value = models.FloatField()

class Trade(models.Model):

    class Meta():
        db_table = "trade"
        

    id = models.CharField(max_length=16, primary_key=True)
    date = models.DateTimeField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="trade_product")
    buying_party = models.ForeignKey(Company, on_delete=models.CASCADE, 
                                        related_name="buyer")
    selling_party = models.ForeignKey(Company, on_delete=models.CASCADE, 
                                        related_name="seller")
    notional_amount = models.FloatField()
    notional_currency = models.ForeignKey(Currency, on_delete=models.CASCADE,
                                        related_name="notional")
    quantity = models.IntegerField()
    maturity_date = models.DateField()
    underlying_price = models.FloatField()
    underlying_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, 
                                        related_name="underlying")
    strike_price = models.FloatField()

#Models for the report data tables
class DeletedTrade(models.Model):

    class Meta():
        db_table = "deleted_trade"

    id = models.AutoField(primary_key=True)
    trade_id = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name="deleted_trade")
    deleted_at = models.DateTimeField(auto_now=True)

class EditedTrade(models.Model):
    
    class Meta():
        db_table = "edited_trade"
    EDITABlE_FIELDS = [
        ('PR', 'product'),
        ('BP', 'buying party'),
        ('SP', 'selling party'),
        ('NC', 'notional currency'),
        ('QT', 'quantity'),
        ('MD', 'maturity date'),
        ('UP', 'underlying price'),
        ('UC', 'underlying currency'),
        ('ST', 'strike price')
    ]
    id = models.AutoField(primary_key=True)
    trade_id = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name="edited_trade")
    edit_date = models.DateTimeField()
    attribute_edited = models.CharField(max_length=2, choices=EDITABlE_FIELDS)
    old_value = models.CharField(max_length=32)
    new_value = models.CharField(max_length=32)

