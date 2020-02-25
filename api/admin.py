from django.contrib import admin
from .models import *

admin.site.register(Company)
admin.site.register(Product)
admin.site.register(ProductSeller)
admin.site.register(ProductPrice)
admin.site.register(Currency)
admin.site.register(CurrencyPrice)
admin.site.register(StockPrice)
admin.site.register(Trade)
