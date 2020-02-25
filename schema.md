# Schema
| `company`     | id (PK)       | name              |
| ------------- | ------------- | ----------------- |
| *type*        | integer       | char(80)          | 
| *description* | companies id  | companies name    |  
&nbsp;

| `product`     | id (PK, auto) | name              |
| ------------- | ------------- | ----------------- |
| *type*        | integer       | char(80)          |
| *description* | product id    | product name      |
&nbsp;

| `product_seller` | id (PK, auto) | company_id (FK) | product_id (FK)    |
| ---------------- | ------------- | ----------------| ------------------ |
| *type*           | integer       | Company         | Product            |
| *description*    | product id    | company selling | product being sold |
&nbsp;

| `currency`    | currency (PK)           |
| ------------- | ----------------- |
| *type*        | char(3)           | 
| *description* | currency code     | 
&nbsp;

| `currency_price`  | id (PK, auto)     | currency (FK)     | date          | value             |
| ----------------- | ----------------- | ----------------- | ------------- | ----------------- |
| *type*            | integer           | Currency          | Date          | float             |
| *description*     | price id          | currency of price | date of price | value of currency |
&nbsp;

| `stock_price` | id (PK, auto)     | company (FK)      | date              | value             |
| ------------- | ----------------- | ----------------- | ----------------- | ----------------- | 
| *type*        | integer           | Company           | Date              |  float            |
| *description* | price id          | company of price  | date of price     |  value of company |
&nbsp;

| `trades`      | id (PK)   | date          | product (FK)   | buying_party (FK) | selling_party (FK) | notional_amount   | notional_currency (FK) | quantity          | maturity_date    | underlying_price | underlying_currency (FK) | strike_price |
| ------------- | --------- | ------------- | -------------- | ----------------- | ------------------ | ----------------- | ---------------------- | ----------------- | ---------------- | ---------------- | ------------------------ | ------------ |
| *type*        | char(16)  | DateTime      | Product        | Company           | Company            | float             | Currency               | integer           | Date             | float            | Currency                 | float        | 
| *description* | trade id  | date of trade | product traded | company buying    | company selling    | notional value    | notional currency      | quantity of trade | date of maturity | underling price  | underlying currency      | strike price |
&nbsp;
