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
    path('product/soldby/company_id=<str:company>/', views.ProductsForSellers.as_view(), name="products_for_company"),
    path('seller/company=<str:company>/', views.SellerListByCompany.as_view()),
    path('seller/product=<str:product>/', views.SellerListByProduct.as_view()),
    path('currency/', views.CurrencyPriceList.as_view()),
    path('currency/list/', views.AllCurrenciesList.as_view()),
    path('currency/currency=<str:currency>&year=<int:year>/', views.CurrencyYearList.as_view()),
    path('currency/currency=<str:currency>&year=<int:year>&month=<int:month>/', views.CurrencyMonthList.as_view()),
    path('currency/currency=<str:currency>&year=<int:year>&month=<int:month>&day=<int:day>/', views.CurrencyDayList.as_view()),
    path('currency/currency=<str:currency>/', views.CurrencyList.as_view()),
    path('currency/conversion/latest/from=<str:from_currency>&to=<str:to_currency>/', views.CurrencyConversionLatest.as_view(), name="latest_currency_conversion"),
    path('currency/report/currency=<str:currency>/', views.CurrencyValuesPastMonth.as_view()),
    path('currency/report/changes', views.CurrencyChanges.as_view()),
    path('seller/list/', views.SellerList.as_view()),
    path('stock/company=<str:company>&year=<int:year>/', views.StockYearList.as_view()),
    path('stock/company=<str:company>&year=<int:year>&month=<int:month>/', views.StockMonthList.as_view()),
    path('stock/company=<str:company>&year=<int:year>&month=<int:month>&day=<int:day>/', views.StockDayList.as_view()),
    path('stock/company=<str:company>/', views.StockList.as_view()),
    path('stock/list/', views.StockPriceList.as_view()),
    path('trade/id=<str:id>/', views.TradeIDList.as_view()),
    path('trade/buyer=<str:buyer>&seller=<str:seller>/', views.TradeBuyerSellerList.as_view()),
    path('trade/buyer=<str:buyer>/', views.TradeBuyerList.as_view()),
    path('trade/seller=<str:seller>/', views.TradeSellerList.as_view()),
    path('trade/year=<int:year>/', views.TradeYearList.as_view()),
    path('trade/year=<int:year>&month=<int:month>/', views.TradeMonthList.as_view()),
    path('trade/year=<int:year>&month=<int:month>&day=<int:day>/', views.TradeDayList.as_view()),
    path('trade/maturity_year=<int:year>/', views.TradeMaturityYearList.as_view()),
    path('trade/maturity_year=<int:year>&maturity_month=<int:month>/', views.TradeMaturityMonthList.as_view()),
    path('trade/maturity_year=<int:year>&maturity_month=<int:month>&maturity_day=<int:day>/', views.TradeMaturityDayList.as_view()),
    path('trade/list/', views.TradeList.as_view()),
    path('trade/total/', views.TotalTrades.as_view()),
    path('trade/recent/', views.TradeRecentList.as_view(), name="recent_trades"),
    path('trade/product=<str:product>&buyer=<str:buyer>&seller=<str:seller>/', views.RecentTradesByCompanyForProduct.as_view(), name="recent_product_for_company"),
    path('trade/create/', views.CreateDerivativeTrade.as_view(), name="create_trade"),
    path('trade/delete/', views.DeleteDerivativeTrade.as_view(), name="delete_trade"),
    path('trade/edit/', views.EditDerivativeTrade.as_view(), name="edit_trade"),
    path('trade/filter/date_lower=<str:date_lower>&date_upper=<str:date_upper>&quantity_lower=<str:quantity_lower>&quantity_upper=<str:quantity_upper>&underlying_lower=<str:underlying_lower>&underlying_upper=<str:underlying_upper>&strike_lower=<str:strike_lower>&strike_upper=<str:strike_upper>&maturity_lower=<str:maturity_lower>&maturity_upper=<str:maturity_upper>/',views.FilterTradeList.as_view(), name="filter_trade"),
    #&&>&/', 
    
    path('report/year=<int:year>&month=<int:month>&day=<int:day>/', views.Report.as_view()),
    path('report/year=<int:year>&month=<int:month>&day=<int:day>&query=<str:search_term>/', views.SearchReport.as_view()),
    path('report/available/', views.AvailableReportsYearList.as_view()),
    path('report/available/year=<int:year>&month=<int:month>/', views.AvailableReportsDayList.as_view()),
    path('report/available/year=<int:year>/', views.AvailableReportsMonthList.as_view()),
    path('report/actions/today/', views.TotalActionsOnDay.as_view()),
    path('errorsandcorrections/', views.ErrorsAndCorrections.as_view()),
    path('errorsandcorrections/trade=<str:trade>/', views.TradeErrorAndCorrections.as_view()),
    path('correction/suggest/trade=<str:trade>/', views.SuggestCorrectionsForTrade.as_view()),
    path('correction/delete/', views.DeleteCorrection.as_view()),
    path('correction/apply', views.CreateCorrection.as_view()),
    path('correction/system', views.SystemCorrection.as_view()),
    path('error/ignore', views.ErrorIgnore.as_view()),
    path('error/check/id=<str:id>', views.CheckForErrors.as_view()),
    path('learning/recommendedrange/currency=<str:currency>&product=<str:product>&buyer=<str:buyer>&seller=<str:seller>/', views.RecommendedRange.as_view())
]
