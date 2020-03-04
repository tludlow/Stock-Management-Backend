---
title: API Reference

language_tabs: # must be one of https://git.io/vQNgJ
  - shell

toc_footers:
  - <a href='https://github.com/lord/slate'>Documentation Powered by Slate</a>

includes:
  - errors

search: true
---
# Introduction

Group 23's API documentation for their [CS261](https://www.warwick.ac.uk/cs261) group project.

# Currency

## List Of Currencies

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

## All Currency Prices

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

## Latest Conversion

```shell
curl "https://group23.dcs.warwick.ac.uk/api/currency/conversion/latest/from=GBP&to=USD/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "date:": "2019-12-31", 
    "from": "GBP",
    "to": "USD", 
    "conversion": 11.36
  }
]
```

This endpoint retrieves the latest conversion from one currency to another.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/currency/conversion/latest/from=<FROM_CURRENCY>&to=<TO_CURRENCY>/`

### URL Parameters

Parameter | Description
--------- | -----------
FROM_CURRENCY | Currency ID of the currency to convert from
TO_CURRENCY | Currency ID of the currency to convert to


# Company

## List Of Companies

```shell
curl "https://group23.dcs.warwick.ac.uk/api/company/list/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": 1,
    "name": "Blue Sun Corporation"
  },
  ...,
  {
    "id": 202,
    "name": "Passione"
  }
]
```

This endpoint retrieves all companies.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/company/list/`

## By ID

```shell
curl "https://group23.dcs.warwick.ac.uk/api/company/id=1/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": 1,
    "name": "Blue Sun Corporation"
  }
]
```

This endpoint retrieves the company with the given id.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/company/id=<ID>/`

### URL Parameters

Parameter | Description
--------- | -----------
ID | ID of the company to retrieve

## By Name

```shell
curl "https://group23.dcs.warwick.ac.uk/api/company/name=Blue%20Sun%20Corporation/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": 1,
    "name": "Blue Sun Corporation"
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
This endpoint is paginated to aid in speeding up the requests. The default page size is 25.
You may specify the page you would like to request with the URL:
`GET api/product/list?page_number=x`

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/product/list/`

## By ID

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

This endpoint retrieves a product by it's name.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/product/name=<NAME>/`

Parameter | Description
--------- | -----------
NAME | Name of the product to retrieve

## Sold By

```shell
curl "https://group23.dcs.warwick.ac.uk/api/product/soldby/company_id=102/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id":305, 
    "product_id":305,
    "company_id":102,
    "name":"Elven Boots"
  },
  {
    "id":307,
    "product_id":307,
    "company_id":102,
    "name":"Mystic Keys"
  }
]
```

This endpoint retrieves a list of all products sold by the given company.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/product/soldby/company_id=<COMPANY_ID>/`

Parameter | Description
--------- | -----------
COMPANY_ID | ID of the company 


# Seller

## List of Sellers

```shell
curl "https://group23.dcs.warwick.ac.uk/api/seller/list/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "product": 2,
    "company": 1
  },
  ...
  {
    "product": 606,
    "company": 202
  }
]
```

This endpoint retrieves a list of all product seller pairs.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/seller/list/`

## By Company

```shell
curl "https://group23.dcs.warwick.ac.uk/api/seller/company=1/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "product": 2,
    "company": 1
  },
  ...
  {
    "product": 4,
    "company": 1
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

```shell
curl "https://group23.dcs.warwick.ac.uk/api/seller/product=1/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "product": 2,
    "company": 1
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
```shell
curl "https://group23.dcs.warwick.ac.uk/api/stock/list/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "company": 1, 
    "date": "2019-01-01", 
    "value": 1.48
  },
  ...
  {
    "company": 202, 
    "date": "2019-12-31", 
    "value": 289.62
  }
]
```

This endpoint retrieves a list of all stock prices.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/stock/list/`

<aside class="warning">This will return a huge amount of data; be wary with usage!</aside>

## By Company

```shell
curl "https://group23.dcs.warwick.ac.uk/api/stock/company=133/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "company": 133, 
    "date": "2019-01-01", 
    "value": 797.0
  }
  ...
  {
    "company": 133, 
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

```shell
curl "https://group23.dcs.warwick.ac.uk/api/stock/company=133&year=2019/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "company": 133, 
    "date": "2019-01-01", 
    "value": 797.0
  }
  ...
  {
    "company": 133, 
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

```shell
curl "https://group23.dcs.warwick.ac.uk/api/stock/company=133&year=2019&month=01/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "company": 133, 
    "date": "2019-01-01", 
    "value": 797.0
  }
  ...
  {
    "company": 133, 
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

```shell
curl "https://group23.dcs.warwick.ac.uk/api/stock/company=133&year=2019&month=01&day=01/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "company": 133, 
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

## Create Trade
```shell
curl -d 'selling_party=26&buying_party=160&product=58&quantity=100&maturity_date=2020-04-03&underlying_currency=USD&notional_currency=USD&strike_price=6.0&underlying_price=2.0' -X POST "https://group23.dcs.warwick.ac.uk/api/trade/create/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "trade_id": 2360717, 
    "data": {
        "selling_party": 26, 
        "buying_party": 160, 
        "product": "58",
        "quantity": "100", 
        "maturity_date": "2020-04-03", 
        "underlying_currency": "USD",
        "notional_currency": "USD", 
        "strike_price": "6.0",
        "underlying_price": "2.0"
    }, 
    "notional_amount": 100.0
  }
]
```

This endpoint allows for the creation of a new trade.

Parameter | Description
--------- | -----------
SELLING_PARTY | Company ID of seller
BUYING_PARTY | Company ID of buyer
PRODUCT | Product ID
QUANTITY | Quantity of trade
MATURITY_DATE | Maturity date of trade
UNDERLYING_CURRENCY | ID of underlying currency
NOTIONAL_CURRENCY | ID of notional currency
STRIKE_PRICE | Strike price of trade
UNDERLYING_PRICE | Underlying price of trade


### HTTP Request

`POST https://group23.dcs.warwick.ac.uk/api/trade/create/`

## Edit Trade
```shell
curl -d 'trade_id=2360717&product=57&underlying_price=3' -X POST "https://group23.dcs.warwick.ac.uk/api/trade/edit/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "changes": {
        "old_product": 58, 
        "new_product": 57, 
        "old_underlying_price": 2.0, 
        "new_underlying_price": 3.0
    }, 
    "trade": [
        {
            "id": "2360717", 
            "date": "2020-03-03T19:59:30.224397Z", 
            "notional_amount": 100.0, 
            "quantity": 100, 
            "maturity_date": "2020-04-03", 
            "underlying_price": 3.0, 
            "strike_price": 6.0, 
            "product": 57, 
            "buying_party": 160, 
            "selling_party": 26, 
            "notional_currency": "USD", 
            "underlying_currency": "USD"
        }
    ]
  }
]
```

This endpoint allows for a trade to be edited within a 3 day window where the maturity date hasn't been reached.

The TRADE_ID and at least one other attribute must be provided.

Parameter | Description
--------- | -----------
TRADE_ID | ID of the trade to edit
SELLING_PARTY | Company ID of seller
BUYING_PARTY | Company ID of buyer
PRODUCT | Product ID
QUANTITY | Quantity of trade
MATURITY_DATE | Maturity date of trade
UNDERLYING_CURRENCY | ID of underlying currency
NOTIONAL_CURRENCY | ID of notional currency
STRIKE_PRICE | Strike price of trade
UNDERLYING_PRICE | Underlying price of trade


### HTTP Request

`POST https://group23.dcs.warwick.ac.uk/api/trade/edit/`

## Delete Trade 
```shell
curl -d 'trade_id=2360717' -X POST "https://group23.dcs.warwick.ac.uk/api/trade/delete/"
```
```json
[
  {
    "success": "Trade has been deleted."
  }
]
```

This endpoint allows for a trade to be deleted within a 3 day window where the maturity date hasn't been reached.

Parameter | Description
--------- | -----------
TRADE_ID | ID of the trade to edit

### HTTP Request

`POST https://group23.dcs.warwick.ac.uk/api/trade/delete/`

## All Trades
```shell
curl "https://group23.dcs.warwick.ac.uk/api/trade/list/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": 1,
    "date": "2019-01-01T00:00:00Z",
    "notional_amount": 369300.0,
    "quantity": 2000,
    "maturity_date": "2022-12-18",
    "underlying_price": 1289.6,
    "strike_price": 186.12,
    "product": 1,
    "buying_party": 22,
    "selling_party": 174,
    "notional_currency": "USD",
    "underlying_currency": "GHS"
  },
  ...
  {
    "id": 2360716,
    "date": "2019-12-31T11:59:00Z",
    "notional_amount": 4396800.0,
    "quantity": 80000,
    "maturity_date": "2024-05-16",
    "underlying_price": 54.96,
    "strike_price": 50.24,
    "product": 1,
    "buying_party": 8,
    "selling_party": 178,
    "notional_currency": "USD",
    "underlying_currency": "USD"
  }
]
```

This endpoint retrieves a list of all trades.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/trade/list/`

<aside class="warning">This will return a huge amount of data; be wary with usage!</aside>

## Recent
```shell
curl "https://group23.dcs.warwick.ac.uk/api/trade/recent/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": 2360720,
    "date": "2020-03-03T18:37:03.859802Z",
    "product_id": 57,
    "buying_party_id": 160,
    "selling_party_id": 26,
    "notional_amount": 100.0,
    "notional_currency_id": "USD",
    "quantity": 100,
    "maturity_date": "2020-04-03",
    "underlying_price": 3.0,
    "underlying_currency_id": "USD",
    "strike_price": 6.0,
    "buying_company": "FOX",
    "selling_company": "Atlas Corp.",
    "product": "Cell Cells"
  },
  {
      "id": 289262,
      "date": "2019-12-31T11:59:00Z",
      "product_id": 1,
      "buying_party_id": 71,
      "selling_party_id": 145,
      "notional_amount": 5355.0,
      "notional_currency_id": "USD",
      "quantity": 500,
      "maturity_date": "2021-12-06",
      "underlying_price": 10.71,
      "underlying_currency_id": "USD",
      "strike_price": 9.36,
      "buying_company": "Gekko and Co.",
      "selling_company": "Okama",
      "product": "Stocks"
  },
  ...
}
]
```
This endpoint retrieves a list of all trades descending order by date.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/trade/id=<ID>/`

## Recent Trades By Company For Product
```shell
curl "https://group23.dcs.warwick.ac.uk/api/trade/product=1&buyer=1/"
```
> The above command returns JSON structured like this:
```json
[
  {
    "id": 289225,
    "date": "2019-12-31T11:48:00Z",
    "notional_amount": 160920.0,
    "quantity": 9000,
    "maturity_date": "2024-09-12",
    "underlying_price": 191.58,
    "strike_price": 15.21,
    "product": 1,
    "buying_party": 1,
    "selling_party": 150,
    "notional_currency": "USD",
    "underlying_currency": "GMD"
  }
  ...
]
```
This endpoint retrieves all trades with a giveen product and buyer.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/trade/product=<PRODUCT>&buyer=<BUYER>/`

Parameter | Description
--------- | -----------
PRODUCT | Product in the trade
BUYER | Buyer in the trade


## By ID 
```shell
curl "https://group23.dcs.warwick.ac.uk/api/trade/id=1/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": 1,
    "date": "2019-01-01T00:00:00Z",
    "notional_amount": 369300.0,
    "quantity": 2000,
    "maturity_date": "2022-12-18",
    "underlying_price": 1289.6,
    "strike_price": 186.12,
    "product": 1,
    "buying_party": 22,
    "selling_party": 174,
    "notional_currency": "USD",
    "underlying_currency": "GHS"
  }
]
```

This endpoint retrieves the trade with the given ID.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/trade/id=<ID>/`

Parameter | Description
--------- | -----------
ID | iD of the trade to be returned

## By Buyer

```shell
curl "https://group23.dcs.warwick.ac.uk/api/trade/buyer=22/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": 1,
    "date": "2019-01-01T00:00:00Z",
    "notional_amount": 369300.0,
    "quantity": 2000,
    "maturity_date": "2022-12-18",
    "underlying_price": 1289.6,
    "strike_price": 186.12,
    "product": 1,
    "buying_party": 22,
    "selling_party": 174,
    "notional_currency": "USD",
    "underlying_currency": "GHS"
  },
  ...
  {
    "id": 2360627,
    "date": "2019-12-31T11:58:00Z",
    "notional_amount": 8995.0,
    "quantity": 500,
    "maturity_date": "2021-01-19",
    "underlying_price": 17.99,
    "strike_price": 17.6,
    "product": 1,
    "buying_party": 22,
    "selling_party": 24,
    "notional_currency": "USD",
    "underlying_currency": "USD"
  }
]
```

This endpoint retrieves all trades for the given buyer .

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/trade/buyer=<BUYER>/`

Parameter | Description
--------- | -----------
BUYER | Buyer in the trade

## By Seller
```shell
curl "https://group23.dcs.warwick.ac.uk/api/trade/seller=24/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": 67,
    "date": "2019-01-01T02:50:00Z",
    "notional_amount": 16243.02,
    "quantity": 500,
    "maturity_date": "2023-11-11",
    "underlying_price": 93.19,
    "strike_price": 28.46,
    "product": 73,
    "buying_party": 75,
    "selling_party": 24,
    "notional_currency": "BND",
    "underlying_currency": "USD"
  },
  ...
  {
    "id": 2360627,
    "date": "2019-12-31T11:58:00Z",
    "notional_amount": 8995.0,
    "quantity": 500,
    "maturity_date": "2021-01-19",
    "underlying_price": 17.99,
    "strike_price": 17.6,
    "product": 1,
    "buying_party": 22,
    "selling_party": 24,
    "notional_currency": "USD",
    "underlying_currency": "USD"
  }
]
```

This endpoint retrieves all trades for the given seller .

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/trade/seller=<SELLER>/`

Parameter | Description
--------- | -----------
SELLER | Seller in the trade

## By Year 
```shell
curl "https://group23.dcs.warwick.ac.uk/api/trade/year=2019/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": 1,
    "date": "2019-01-01T00:00:00Z",
    "notional_amount": 369300.0,
    "quantity": 2000,
    "maturity_date": "2022-12-18",
    "underlying_price": 1289.6,
    "strike_price": 186.12,
    "product": 1,
    "buying_party": 22,
    "selling_party": 174,
    "notional_currency": "USD",
    "underlying_currency": "GHS"
  },
  ...
  {
    "id": 2360716,
    "date": "2019-12-31T11:59:00Z",
    "notional_amount": 4396800.0,
    "quantity": 80000,
    "maturity_date": "2024-05-16",
    "underlying_price": 54.96,
    "strike_price": 50.24,
    "product": 1,
    "buying_party": 8,
    "selling_party": 179,
    "notional_currency": "USD",
    "underlying_currency": "USD"
  }
]
```

This endpoint retrieves a list of all trades in a given year.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/trade/year=<YEAR>/`

Parameter | Description
--------- | -----------
YEAR | Year of data to be returned

## By Month 

```shell
curl "https://group23.dcs.warwick.ac.uk/api/trade/year=2019&month=01/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": 1,
    "date": "2019-01-01T00:00:00Z",
    "notional_amount": 369300.0,
    "quantity": 2000,
    "maturity_date": "2022-12-18",
    "underlying_price": 1289.6,
    "strike_price": 186.12,
    "product": 1,
    "buying_party": 22,
    "selling_party": 174,
    "notional_currency": "USD",
    "underlying_currency": "GHS"
  },
  ...
  {
    "id": 1967264,
    "date": "2019-01-31T11:59:00Z",
    "notional_amount": 502400.0,
    "quantity": 80000,
    "maturity_date": "2020-03-26",
    "underlying_price": 51.04,
    "strike_price": 5.75,
    "product": 1,
    "buying_party": 86,
    "selling_party": 58,
    "notional_currency": "USD",
    "underlying_currency": "BZD"
  }
]
```

This endpoint retrieves all trades for the given year and month.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/trade/year=<YEAR>&month=<MONTH>/`

Parameter | Description
--------- | -----------
YEAR | Year of data to be returned
MONTH | Month of data to be returned

## By Day
```shell
curl "https://group23.dcs.warwick.ac.uk/api/trade/year=2019&month=01&day=01/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": 1,
    "date": "2019-01-01T00:00:00Z",
    "notional_amount": 369300.0,
    "quantity": 2000,
    "maturity_date": "2022-12-18",
    "underlying_price": 1289.6,
    "strike_price": 186.12,
    "product": 1,
    "buying_party": 22,
    "selling_party": 174,
    "notional_currency": "USD",
    "underlying_currency": "GHS"
  },
  ...
  {
    "id": 646771,
    "date": "2019-01-01T11:59:00Z",
    "notional_amount": 54290.0,
    "quantity": 400,
    "maturity_date": "2021-08-01",
    "underlying_price": 135.74,
    "strike_price": 151.79,
    "product": 1,
    "buying_party": 84,
    "selling_party": 38,
    "notional_currency": "USD",
    "underlying_currency": "USD"
  }
]
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
```shell
curl "https://group23.dcs.warwick.ac.uk/api/trade/maturity_year=2024/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": 646001,
    "date": "2019-01-01T00:51:00Z",
    "notional_amount": 19976400.0,
    "quantity": 90000,
    "maturity_date": "2024-01-01",
    "underlying_price": 2761.52,
    "strike_price": 248.17,
    "product": 427,
    "buying_party": 190,
    "selling_party": 143,
    "notional_currency": "USD",
    "underlying_currency": "PAB"
  },
  ...
  {
    "id": 2330714,
    "date": "2019-12-30T11:54:00Z",
    "notional_amount": 3770500.0,
    "quantity": 50000,
    "maturity_date": "2024-12-31",
    "underlying_price": 75.41,
    "strike_price": 59.87,
    "product": 1,
    "buying_party": 164,
    "selling_party": 180,
    "notional_currency": "USD",
    "underlying_currency": "USD"
  }
]
```

This endpoint retrieves a list of all trades with the given maturity year.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/trade/maturity_year=<MATURITY_YEAR>/`

Parameter | Description
--------- | -----------
MATURITY_YEAR | Maturity year of data to be returned

## By Maturity Month 

```shell
curl "https://group23.dcs.warwick.ac.uk/api/trade/maturity_year=2024&maturity_month=01/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": 646001,
    "date": "2019-01-01T00:51:00Z",
    "notional_amount": 19976400.0,
    "quantity": 90000,
    "maturity_date": "2024-01-01",
    "underlying_price": 2761.52,
    "strike_price": 248.17,
    "product": 427,
    "buying_party": 190,
    "selling_party": 143,
    "notional_currency": "USD",
    "underlying_currency": "PAB"
  },
  ...
  {
    "id": 2360019,
    "date": "2019-12-31T04:39:00Z",
    "notional_amount": 474500.0,
    "quantity": 50000,
    "maturity_date": "2024-01-31",
    "underlying_price": 9.49,
    "strike_price": 10.65,
    "product": 1,
    "buying_party": 138,
    "selling_party": 13,
    "notional_currency": "USD",
    "underlying_currency": "USD"
  }
]
```

This endpoint retrieves a list of all trades with the given maturity month.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/trade/maturity_year=<MATURITY_YEAR>&maturity_month=<MATURITY_MONTH>/`

Parameter | Description
--------- | -----------
MATURITY_YEAR | Maturity year of data to be returned
MATURITY_MONTH | Maturity month of data to be returned

## By Maturity Day
```shell
curl "https://group23.dcs.warwick.ac.uk/api/trade/maturity_year=2024&maturity_month=01&maturity_day=01/"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": 646001,
    "date": "2019-01-01T00:51:00Z",
    "notional_amount": 19976400.0,
    "quantity": 90000,
    "maturity_date": "2024-01-01",
    "underlying_price": 2761.52,
    "strike_price": 248.17,
    "product": 427,
    "buying_party": 190,
    "selling_party": 143,
    "notional_currency": "USD",
    "underlying_currency": "PAB"
  },
  ...
  {
    "id": 2320014,
    "date": "2019-12-31T06:51:00Z",
    "notional_amount": 14310.0,
    "quantity": 3000,
    "maturity_date": "2024-01-01",
    "underlying_price": 4.77,
    "strike_price": 4.15,
    "product": 1,
    "buying_party": 143,
    "selling_party": 65,
    "notional_currency": "USD",
    "underlying_currency": "USD"
  }
]
```

This endpoint retrieves a list of all trades with the given maturity day.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/trade/maturity_year=<MATURITY_YEAR>&maturity_month=<MATURITY_MONTH>&maturity_day=<MATURITY_DAY>/`

Parameter | Description
--------- | -----------
MATURITY_YEAR | Maturity year of data to be returned
MATURITY_MONTH | Maturity month of data to be returned
MATURITY_DAY | Maturity day of data to be returned

# Report
## Get Report
```shell
curl "https://group23.dcs.warwick.ac.uk/api/report/year=2018&month=01&day=01/"
```

> The above command returns JSON structured like this:

```json
{
    "date_of_report": "2020-03-04T00:00:00Z",
    "created": "2020-03-05T00:00:00Z",
    "num_of_new_trades": 1,
    "created_trades": [
        {
            "id": 2360718, 
            "date": "2020-03-03T19:59:30.224397Z", 
            "notional_amount": 100.0, 
            "quantity": 100, 
            "maturity_date": "2020-04-03", 
            "underlying_price": 3.0, 
            "strike_price": 6.0, 
            "product": 57, 
            "buying_party": 160, 
            "selling_party": 26, 
            "notional_currency": "USD", 
            "underlying_currency": "USD"
        }
    ],
    "num_of_edited_trades": 1,
    "edited_trades": [
        {
            "trade": {
                "id": 2130102, 
                "date": "2020-02-01T14:51:11.215319Z", 
                "notional_amount": 31.0, 
                "quantity": 230, 
                "maturity_date": "2021-12-01", 
                "underlying_price": 1.0, 
                "strike_price": 2.0, 
                "product": "Stocks", 
                "buying_party": "New York Inquirer", 
                "selling_party": "International Data Corporation", 
                "notional_currency": "USD", 
                "underlying_currency": "USD"
            },
            "num_of_edits": 2,
            "edits": [
                {
                    "id": 1,
                    "attribute_edited": "product",
                    "edit_date": "2020-03-03T20:00:03Z",
                    "old_value": "Rings of Teleportation", 
                    "new_value": "Stocks", 
                },
                {
                    "id": 2,
                    "attribute_edited": "underlying_price",
                    "edit_date": "2020-03-03T22:42:20Z",
                    "old_value": "420",
                    "new_value": "1"
                }
            ]
        }
    ],
    "num_of_deleted_trades": 1,
    "deleted_trades": [
        {
            "id": 2360715, 
            "date": "2020-03-03T21:01:11.394367Z", 
            "notional_amount": 89.0, 
            "quantity": 100000, 
            "maturity_date": "2022-11-01", 
            "underlying_price": 10.0, 
            "strike_price": 60.0, 
            "product": "Stocks", 
            "buying_party": "Tokra Electronics", 
            "selling_party": "Wario Ware Inc.", 
            "notional_currency": "USD", 
            "underlying_currency": "USD"
            "delete_id": 1,
            "deleted_at": "2020-03-01T23:19:51Z"
        }
    ]
}
```

This endpoint retrieves a report for the given date.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/report/year=<YEAR>&month=<MONTH>&day=<DAY>/`

Parameter | Description
--------- | -----------
YEAR | Year of report to be returned
MONTH | Month of report to be returned
DAY | Day of report to be returned

## Available by Year
 ```shell
 curl "https://group23.dcs.warwick.ac.uk/api/report/available/"
 ```

 > The above command returns JSON structured like this:

 ```json
[
  {
    "year": "2020"
  },
  ...
  {
    "year": "2010"
  }
]
```
This endpoint retrieves the years that reports are available for.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/report/available/`

## Available by Month
 ```shell
 curl "https://group23.dcs.warwick.ac.uk/api/report/available/year=2019/"
 ```

 > The above command returns JSON structured like this:

 ```json
[
  {
    "year": "2019",
    "month": "12"
  },
  ...
  {
    "year": "2019",
    "month": "1"
  }
]
```
This endpoint retrieves the months that reports are available for given a year.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/report/available/year=<YEAR>/`

Parameter | Description
--------- | -----------
YEAR | Year of report

## Available by Day
 ```shell
 curl "https://group23.dcs.warwick.ac.uk/api/report/available/year=2019&month=1/"
 ```

 > The above command returns JSON structured like this:

 ```json
[
  {
    "year": "2019",
    "month": "1",
    "day": "31"
  },
  ...
  {
    "year": "2019",
    "month": "1",
    "day": "1"
  }
]
```
This endpoint retrieves the days that reports are available for given a year and month.

### HTTP Request

`GET https://group23.dcs.warwick.ac.uk/api/report/available/year=<YEAR>&month=<MONTH>/`

Parameter | Description
--------- | -----------
YEAR | Year of report
MONTH | Month of report

