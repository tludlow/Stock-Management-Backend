---
title: API Reference

language_tabs: # must be one of https://git.io/vQNgJ
  - python
  - shell

toc_footers:
  - <a href='https://github.com/lord/slate'>Documentation Powered by Slate</a>

includes:
  - errors

search: true
---
# Introduction

Primitive API documentation for group project.

<aside class="warning">Check usage & required credits of using slate before final submission.</aside>

# Authentication

No authentication is currently required.

# Currency

## List Of Currencies


```python
from query import API

api = API()
api.getCurrencyList()
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/currency/list/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "currency": "AEF",
  },
  {
    "currency": "AFN",
  },
  ...
]
```

This endpoint to return all supported currencies.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/currency/list/`

<aside class="warning">For the moment, queries made must be exact - both case and format (ensure backslash at end of request)</aside>

## All Currency Prices

```python
from query import API

api = API()
api.getCurrency()
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/currency/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "date": "2019-01-01",
    "value": "18.291",
    "currency": "AFN",
  },
  ...,
  {
    "date": "2019-12-31",
    "value": "4.45",
    "currency": "ZWD",
  },
]
```

This endpoint retrieves all recorded prices for all currencies (in relation to USD).

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/currency/`

<aside class="warning">This will return a huge amount of data; be wary with usage!</aside>

## By Currency

```python
from query import API

api = API()
api.getCurrency(currency='GBP')
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/currency/currency=GBP/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "date": "2019-01-01",
    "value": "12.2624",
    "currency": "GBP",
  },
  ...,
  {
    "date": "2019-12-31",
    "value": "11.3627",
    "currency": "GBP",
  }
]
```

This endpoint retrieves all recorded prices for the given currency (in relation to USD).

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/currency/currency=<CURRENCY>/`

### URL Parameters

Parameter | Description
--------- | -----------
CURRENCY | The currency to retrieve

## By Year

```python
from query import API

api = API()
api.getCurrency(currency='GBP', year='2019')
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/currency/currency=GBP&year=2019/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "date": "2019-01-01",
    "value": "12.2624",
    "currency": "GBP",
  },
  ...,
  {
    "date": "2019-12-31",
    "value": "11.3627",
    "currency": "GBP",
  }
]
```

This endpoint retrieves all recorded prices for the given currency for the given year (in relation to USD).

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/currency/currency=<CURRENCY>&year=<YEAR>/`

### URL Parameters

Parameter | Description
--------- | -----------
CURRENCY | The currency to retrieve
YEAR | Year of data to be returned

## By Month

```python
from query import API

api = API()
api.getCurrency(currency='GBP', year='2019', month='01')
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/currency/currency=GBP&year=2019&month=01/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "date": "2019-01-01",
    "value": "12.2624",
    "currency": "GBP",
  },
  ...,
  {
    "date": "2019-01-31",
    "value": "11.9242",
    "currency": "GBP",
  }
]
```

This endpoint retrieves all recorded prices for the given currency for the given year and month (in relation to USD).

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/currency/currency=<CURRENCY>&year=<YEAR>&month=<MONTH>/`

### URL Parameters

Parameter | Description
--------- | -----------
CURRENCY | The currency to retrieve
YEAR | Year of data to be returned
MONTH | Month of data to be returned

## By Day

```python
from query import API

api = API()
api.getCurrencyPrices(currency='GBP', year='2019', month='01', day='01')
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/currency/currency=GBP&year=2019&month=01&day=01/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "date": "2019-01-01",
    "value": "12.2624",
    "currency": "GBP",
  }
]
```

This endpoint retrieves all recorded prices for the given currency for the given year and month (in relation to USD).

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/currency/currency=<CURRENCY>&year=<YEAR>&month=<MONTH>&day=<DAY>/`

### URL Parameters

Parameter | Description
--------- | -----------
CURRENCY | The currency to retrieve
YEAR | Year of data to be returned
MONTH | Month of data to be returned
DAY | Day of data to be returned


# Company

## List Of Companies

```python
from query import API

api = API()
api.getCompanyList()
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/company/list/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": "AGBH66",
    "name": "Cyberbiotics"
  },
  ...,
  {
    "id": "ZXVX98",
    "name": "The Noah Family"
  }
]
```

This endpoint retrieves all companies.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/company/list/`

## By ID

```python
from query import API

api = API()
api.getCompany(id="AGBH66")
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/company/id=AGBH66/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": "AGBH66",
    "name": "Cyberbiotics"
  }
]
```

This endpoint retrieves the company with the given id.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/company/id=<ID>`

### URL Parameters

Parameter | Description
--------- | -----------
ID | ID of the company to retrieve

## By Name

```python
from query import API

api = API()
api.getCompany(name="Cyberbiotics")
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/company/name=Cyberbiotics/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": "AGBH66",
    "name": "Cyberbiotics"
  }
]
```

This endpoint retrieves the company with the given name.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/company/name=<NAME>/`

### URL Parameters

Parameter | Description
--------- | -----------
NAME | Name of the company to retrieve

<aside class="notice">
You'll need to replace a space (" ") with it's encoded equivilant ("%20").
</aside>

# Product

## List Of Products

```python
from query import API

api = API()
api.getProductList()
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/product/list/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": 1,
    "name": "Stocks"
  },
  ...,
  {
    "id": 606,
    "name": "Cancellers"
  }
]
```

This endpoint retrieves all products.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/product/list/`

## By ID

```python
from query import API

api = API()
api.getProduct(id="1")
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/product/id=1/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": 1,
    "name": "Stocks",
  }
]
```

This endpoint retrieves a product by it's ID.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/product/id=<ID>/`

Parameter | Description
--------- | -----------
ID | ID of the product to retrieve

## By Name

```python
from query import API

api = API()
api.getProduct(name="Stocks")
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/product/name=Stocks/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": 1,
    "name": "Stocks",
  }
]
```

This endpoint retrieves a product by it's namee.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/product/name=<NAME>/`

Parameter | Description
--------- | -----------
NAME | Name of the product to retrieve

# Seller

## List of Sellers

```python
from query import API

api = API()
api.getSellerList()
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/seller/list/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "product": 2,
    "company": "QETH27"
  },
  ...
  {
    "product": 606,
    "company": "DILF10"
  }
}
```

This endpoint retrieves a list of all product seller pairs.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/seller/list/`

## By Company

```python
from query import API

api = API()
api.getSeller(seller="QETH27")
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/seller/company=QETH27/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "product": 2,
    "company": "QETH27"
  },
  ...
  {
    "product": 4,
    "company": "QETH27"
  }
]
```

This endpoint retrieves all products the company sells.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/seller/company=<COMPANY>/`

Parameter | Description
--------- | -----------
COMPANY | Company ID 

## By Product

```python
from query import API

api = API()
api.getSeller(product="2")
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/seller/product=1/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "product": 2,
    "company": "QETH27"
  }
]
```

This endpoint retrieves all companies which the product is sold by.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/seller/product=<PRODUCT>/`

Parameter | Description
--------- | -----------
PRODUCT | Product ID 

# Stock

## All Stock Prices

```python
from query import API

api = API()
api.getStock()
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/stock/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "company": "QETH27", 
    "date": "2019-01-01", 
    "value": 1.48
  },
  ...
  {
    "company": "DILF10", 
    "date": "2019-12-31", 
    "value": 289.62
  }
}
```

This endpoint retrieves a list of all stock prices.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/stock/`

<aside class="warning">This will return a huge amount of data; be wary with usage!</aside>

## By Company

```python
from query import API

api = API()
api.getStock(company="NCCX02")
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/stock/company=NCCX02/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "company": "NCCX02", 
    "date": "2019-01-01", 
    "value": 797.0
  }
  ...
  {
    "company": "NCCX02", 
    "date": "2019-12-31", 
    "value": 1221.27
  }
]
```

This endpoint retrieves all stock prices for the given company.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/stock/company=<COMPANY>/`

Parameter | Description
--------- | -----------
COMPANY | Company ID

## By Year (Company)

```python
from query import API

api = API()
api.getStock(company="NCCX02", year="2019")
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/stock/company=NCCX02&year=2019/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "company": "NCCX02", 
    "date": "2019-01-01", 
    "value": 797.0
  }
  ...
  {
    "company": "NCCX02", 
    "date": "2019-12-31", 
    "value": 1221.27
  }
]
```

This endpoint retrieves all stock prices for the given company and year.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/stock/company=<COMPANY>&year=<YEAR>/`

Parameter | Description
--------- | -----------
COMPANY | Company ID
YEAR | Year of data to be returned

## By Month (Company)

```python
from query import API

api = API()
api.getStock(company="NCCX02", year="2019", month="01")
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/stock/company=NCCX02&year=2019&month=01/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "company": "NCCX02", 
    "date": "2019-01-01", 
    "value": 797.0
  }
  ...
  {
    "company": "NCCX02", 
    "date": "2019-01-31", 
    "value": 869.27
  }
]
```

This endpoint retrieves all stock prices for the given company, year and month.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/stock/company=<COMPANY>&year=<YEAR>&month=<MONTH>/`

Parameter | Description
--------- | -----------
COMPANY | Company ID
YEAR | Year of data to be returned
MONTH | Month of data to be returned

## By Day (Company)

```python
from query import API

api = API()
api.getStock(company="NCCX02", year="2019", month="01", day="01")
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/stock/company=NCCX02&year=2019&month=01&day=01/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "company": "NCCX02", 
    "date": "2019-01-01", 
    "value": 797.0
  }
]
```

This endpoint retrieves all stock prices for the given company, year, month and day.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/stock/company=<COMPANY>&year=<YEAR>&month=<MONTH>&day=<DAY>/`

Parameter | Description
--------- | -----------
COMPANY | Company ID
YEAR | Year of data to be returned
MONTH | Month of data to be returned
DAY | Day of data to be returned

# Trade

## All Trades

```python
from query import API

api = API()
api.getTrade()
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/trade/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": "PASYTZVI53631072",
    "date": "2019-01-01T00:00:00Z",
    "notional_amount": 369300.0,
    "quantity": 2000,
    "maturity_date": "2022-12-18",
    "underlying_price": 1289.6,
    "strike_price": 186.12,
    "product": 1,
    "buying_party": "FORM54",
    "selling_party": "ISWT83",
    "notional_currency": "USD",
    "underlying_currency": "GHS"
  },
  ...
  {
    "id": "ZTLGMVSN76336825",
    "date": "2019-12-31T11:59:00Z",
    "notional_amount": 4396800.0,
    "quantity": 80000,
    "maturity_date": "2024-05-16",
    "underlying_price": 54.96,
    "strike_price": 50.24,
    "product": 1,
    "buying_party": "SWGF93",
    "selling_party": "ESPL27",
    "notional_currency": "USD",
    "underlying_currency": "USD"
  }
}
```

This endpoint retrieves a list of all trades.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/trade/`

<aside class="warning">This will return a huge amount of data; be wary with usage!</aside>

## By ID 

```python
from query import API

api = API()
api.getTrade(id="PASYTZVI53631072")
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/trade/id=PASYTZVI53631072/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": "PASYTZVI53631072",
    "date": "2019-01-01T00:00:00Z",
    "notional_amount": 369300.0,
    "quantity": 2000,
    "maturity_date": "2022-12-18",
    "underlying_price": 1289.6,
    "strike_price": 186.12,
    "product": 1,
    "buying_party": "FORM54",
    "selling_party": "ISWT83",
    "notional_currency": "USD",
    "underlying_currency": "GHS"
  }
}
```

This endpoint retrieves a list of the trade with the given ID.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/trade/id=<ID>/`

Parameter | Description
--------- | -----------
ID | iD of the trade to be returned

## By Buyer

```python
from query import API

api = API()
api.getStock(buyer="FORM54")
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/trade/buyer=FORM54/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": "PASYTZVI53631072",
    "date": "2019-01-01T00:00:00Z",
    "notional_amount": 369300.0,
    "quantity": 2000,
    "maturity_date": "2022-12-18",
    "underlying_price": 1289.6,
    "strike_price": 186.12,
    "product": 1,
    "buying_party": "FORM54",
    "selling_party": "ISWT83",
    "notional_currency": "USD",
    "underlying_currency": "GHS"
  },
  ...
  {
    "id": "UDXTYEZM95287495",
    "date": "2019-12-31T11:58:00Z",
    "notional_amount": 8995.0,
    "quantity": 500,
    "maturity_date": "2021-01-19",
    "underlying_price": 17.99,
    "strike_price": 17.6,
    "product": 1,
    "buying_party": "FORM54",
    "selling_party": "WIZJ73",
    "notional_currency": "USD",
    "underlying_currency": "USD"
  }
}
```

This endpoint retrieves all trades for the given buyer .

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/trade/buyer=<BUYER>/`

Parameter | Description
--------- | -----------
BUYER | Buyer in the trade

## By Seller

```python
from query import API

api = API()
api.getStock(seller="WIZJ73")
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/trade/seller=WIZJ73/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": "RAKMTSOF05364150",
    "date": "2019-01-01T02:50:00Z",
    "notional_amount": 16243.02,
    "quantity": 500,
    "maturity_date": "2023-11-11",
    "underlying_price": 93.19,
    "strike_price": 28.46,
    "product": 73,
    "buying_party": "CVMG22",
    "selling_party": "WIZJ73",
    "notional_currency": "BND",
    "underlying_currency": "USD"
  },
  ...
  {
    "id": "UDXTYEZM95287495",
    "date": "2019-12-31T11:58:00Z",
    "notional_amount": 8995.0,
    "quantity": 500,
    "maturity_date": "2021-01-19",
    "underlying_price": 17.99,
    "strike_price": 17.6,
    "product": 1,
    "buying_party": "FORM54",
    "selling_party": "WIZJ73",
    "notional_currency": "USD",
    "underlying_currency": "USD"
  }
}
```

This endpoint retrieves all trades for the given seller .

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/trade/seller=<SELLER>/`

Parameter | Description
--------- | -----------
SELLER | Seller in the trade

## By Year 

```python
from query import API

api = API()
api.getTrade(year="2019")
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/trade/year=2019/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": "PASYTZVI53631072",
    "date": "2019-01-01T00:00:00Z",
    "notional_amount": 369300.0,
    "quantity": 2000,
    "maturity_date": "2022-12-18",
    "underlying_price": 1289.6,
    "strike_price": 186.12,
    "product": 1,
    "buying_party": "FORM54",
    "selling_party": "ISWT83",
    "notional_currency": "USD",
    "underlying_currency": "GHS"
  },
  ...
  {
    "id": "ZTLGMVSN76336825",
    "date": "2019-12-31T11:59:00Z",
    "notional_amount": 4396800.0,
    "quantity": 80000,
    "maturity_date": "2024-05-16",
    "underlying_price": 54.96,
    "strike_price": 50.24,
    "product": 1,
    "buying_party": "SWGF93",
    "selling_party": "ESPL27",
    "notional_currency": "USD",
    "underlying_currency": "USD"
  }
}
```

This endpoint retrieves a list of all trades in a given year.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/trade/year=<YEAR>/`

Parameter | Description
--------- | -----------
YEAR | Year of data to be returned

## By Month 

```python
from query import API

api = API()
api.getTrade(year="2019", month="01")
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/trade/year=2019&month=01/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": "PASYTZVI53631072",
    "date": "2019-01-01T00:00:00Z",
    "notional_amount": 369300.0,
    "quantity": 2000,
    "maturity_date": "2022-12-18",
    "underlying_price": 1289.6,
    "strike_price": 186.12,
    "product": 1,
    "buying_party": "FORM54",
    "selling_party": "ISWT83",
    "notional_currency": "USD",
    "underlying_currency": "GHS"
  },
  ...
  {
    "id": "VRAOOOSE39397903",
    "date": "2019-01-31T11:59:00Z",
    "notional_amount": 502400.0,
    "quantity": 80000,
    "maturity_date": "2020-03-26",
    "underlying_price": 51.04,
    "strike_price": 5.75,
    "product": 1,
    "buying_party": "CBOX52",
    "selling_party": "MEOQ86",
    "notional_currency": "USD",
    "underlying_currency": "BZD"
  }
}
```

This endpoint retrieves all trades for the given year and month.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/trade/year=<YEAR>&month=<MONTH>/`

Parameter | Description
--------- | -----------
YEAR | Year of data to be returned
MONTH | Month of data to be returned

## By Day

```python
from query import API

api = API()
api.getStock(year="2019", month="01", day="01")
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/trade/year=2019&month=01&day=01/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": "PASYTZVI53631072",
    "date": "2019-01-01T00:00:00Z",
    "notional_amount": 369300.0,
    "quantity": 2000,
    "maturity_date": "2022-12-18",
    "underlying_price": 1289.6,
    "strike_price": 186.12,
    "product": 1,
    "buying_party": "FORM54",
    "selling_party": "ISWT83",
    "notional_currency": "USD",
    "underlying_currency": "GHS"
  },
  ...
  {
    "id": "CQHJKYMA90014810",
    "date": "2019-01-01T11:59:00Z",
    "notional_amount": 54290.0,
    "quantity": 400,
    "maturity_date": "2021-08-01",
    "underlying_price": 135.74,
    "strike_price": 151.79,
    "product": 1,
    "buying_party": "DNIL23",
    "selling_party": "PKBF70",
    "notional_currency": "USD",
    "underlying_currency": "USD"
  }
}
```

This endpoint retrieves all trades for the given year, month and day.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/trade/year=<YEAR>&month=<MONTH>&day=<DAY>/`

Parameter | Description
--------- | -----------
YEAR | Year of data to be returned
MONTH | Month of data to be returned
DAY | Day of data to be returned

## By Maturity Year 

```python
from query import API

api = API()
api.getTrade(maturity_year="2024")
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/trade/maturity_year=2024/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": "JZXTBWMB27877603",
    "date": "2019-01-01T00:51:00Z",
    "notional_amount": 19976400.0,
    "quantity": 90000,
    "maturity_date": "2024-01-01",
    "underlying_price": 2761.52,
    "strike_price": 248.17,
    "product": 427,
    "buying_party": "HHOA99",
    "selling_party": "PQSW95",
    "notional_currency": "USD",
    "underlying_currency": "PAB"
  },
  ...
  {
    "id": "KSLSFRZA92830687",
    "date": "2019-12-30T11:54:00Z",
    "notional_amount": 3770500.0,
    "quantity": 50000,
    "maturity_date": "2024-12-31",
    "underlying_price": 75.41,
    "strike_price": 59.87,
    "product": 1,
    "buying_party": "SRYE59",
    "selling_party": "VKMV12",
    "notional_currency": "USD",
    "underlying_currency": "USD"
  }
}
```

This endpoint retrieves a list of all trades with the given maturity year.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/trade/maturity_year=<MATURITY_YEAR>/`

Parameter | Description
--------- | -----------
MATURITY_YEAR | Maturity year of data to be returned

## By Maturity Month 

```python
from query import API

api = API()
api.getTrade(maturity_year="2024", maturity_month="01")
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/trade/maturity_year=2024&maturity_month=01/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": "JZXTBWMB27877603",
    "date": "2019-01-01T00:51:00Z",
    "notional_amount": 19976400.0,
    "quantity": 90000,
    "maturity_date": "2024-01-01",
    "underlying_price": 2761.52,
    "strike_price": 248.17,
    "product": 427,
    "buying_party": "HHOA99",
    "selling_party": "PQSW95",
    "notional_currency": "USD",
    "underlying_currency": "PAB"
  },
  ...
  {
    "id": "RIIIHLYF92433894",
    "date": "2019-12-31T04:39:00Z",
    "notional_amount": 474500.0,
    "quantity": 50000,
    "maturity_date": "2024-01-31",
    "underlying_price": 9.49,
    "strike_price": 10.65,
    "product": 1,
    "buying_party": "FGQR22",
    "selling_party": "PJKH65",
    "notional_currency": "USD",
    "underlying_currency": "USD"
  }
}
```

This endpoint retrieves a list of all trades with the given maturity month.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/trade/maturity_year=<MATURITY_YEAR>&maturity_month=<MATURITY_MONTH>/`

Parameter | Description
--------- | -----------
MATURITY_YEAR | Maturity year of data to be returned
MATURITY_MONTH | Maturity month of data to be returned

## By Maturity Day

```python
from query import API

api = API()
api.getTrade(maturity_year="2024", maturity_month="01", maturity_day="01")
```

```shell
curl "https://group23.dcs.warwick.ac.uk/api/trade/maturity_year=2024&maturity_month=01&maturity_day=01/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": "JZXTBWMB27877603",
    "date": "2019-01-01T00:51:00Z",
    "notional_amount": 19976400.0,
    "quantity": 90000,
    "maturity_date": "2024-01-01",
    "underlying_price": 2761.52,
    "strike_price": 248.17,
    "product": 427,
    "buying_party": "HHOA99",
    "selling_party": "PQSW95",
    "notional_currency": "USD",
    "underlying_currency": "PAB"
  },
  ...
  {
    "id": "TBHUTJXH45919615",
    "date": "2019-12-31T06:51:00Z",
    "notional_amount": 14310.0,
    "quantity": 3000,
    "maturity_date": "2024-01-01",
    "underlying_price": 4.77,
    "strike_price": 4.15,
    "product": 1,
    "buying_party": "PQSW95",
    "selling_party": "OKYS51",
    "notional_currency": "USD",
    "underlying_currency": "USD"
  }
}
```

This endpoint retrieves a list of all trades with the given maturity day.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/trade/maturity_year=<MATURITY_YEAR>&maturity_month=<MATURITY_MONTH>&maturity_day=<MATURITY_DAY>/`

Parameter | Description
--------- | -----------
MATURITY_YEAR | Maturity year of data to be returned
MATURITY_MONTH | Maturity month of data to be returned
MATURITY_DAY | Maturity day of data to be returned
