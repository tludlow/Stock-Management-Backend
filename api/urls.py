from django.urls import path
from . import views
from rest_framework import routers
from django.urls import path, include

urlpatterns = [
    path('company/list/', views.CompanyList.as_view(), name="company_all"),
    path('company/id=<str:id>/', views.CompanyByIDList.as_view(), name="company_by_id"),
    path('company/name=<str:name>/', views.CompanyByNameList.as_view()),
    path('product/list/', views.ProductList.as_view()),
    path('product/id=<int:id>/', views.ProductByIDList.as_view()),
    path('product/name=<str:name>/', views.ProductByNameList.as_view()),
    path('seller/company=<str:company>/', views.SellerListByCompany.as_view()),
    path('seller/product=<str:product>/', views.SellerListByProduct.as_view()),
    path('currency/', views.CurrencyPriceList.as_view()),
    path('currency/list/', views.AllCurrenciesList.as_view()),
    path('currency/currency=<str:currency>&year=<int:year>/', views.CurrencyYearList.as_view()),
    path('currency/currency=<str:currency>&year=<int:year>&month=<int:month>/', views.CurrencyMonthList.as_view()),
    path('currency/currency=<str:currency>&year=<int:year>&month=<int:month>&day=<int:day>/', views.CurrencyDayList.as_view()),
    path('currency/currency=<str:currency>/', views.CurrencyList.as_view()),
    path('seller/list/', views.SellerList.as_view()),
    path('stock/company=<str:company>&year=<int:year>/', views.StockYearList.as_view()),
    path('stock/company=<str:company>&year=<int:year>&month=<int:month>/', views.StockMonthList.as_view()),
    path('stock/company=<str:company>&year=<int:year>&month=<int:month>&day=<int:day>/', views.StockDayList.as_view()),
    path('stock/company=<str:company>/', views.StockList.as_view()),
    path('stock/', views.StockPriceList.as_view()),
    path('trade/id=<str:id>/', views.TradeIDList.as_view()),
    path('trade/buyer=<str:buyer>&seller=<str:seller>/', views.TradeBuyerSellerList.as_view()),
    path('trade/buyer=<str:buyer>/', views.TradeBuyerList.as_view()),
    path('trade/seller=<str:seller>/', views.TradeSellerList.as_view()),
    path('trade/year=<int:year>/', views.TradeYearList.as_view()),
    path('trade/year=<int:year>&month=<int:month>/', views.TradeMonthList.as_view()),
    path('trade/year=<int:year>&month=<int:month>&day=<int:day>/', views.TradeDayList.as_view()),
    path('trade/id=<str:id>/', views.TradeIDList.as_view()),
    path('trade/maturity_year=<int:year>/', views.TradeMaturityYearList.as_view()),
    path('trade/maturity_year=<int:year>&maturity_month=<int:month>/', views.TradeMaturityMonthList.as_view()),
    path('trade/maturity_year=<int:year>&maturity_month=<int:month>&maturity_day=<int:day>/', views.TradeMaturityDayList.as_view()),
    path('trade/', views.TradeList.as_view()),
    path('trade/recent', views.TradeRecentList.as_view(), name="recent_trades"),

    path('trade/create', views.CreateDerivativeTrade.as_view(), name="create_trade"),
    path('trade/delete', views.DeleteDerivativeTrade.as_view(), name="delete_trade")
]

