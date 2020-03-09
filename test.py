import requests
url="http://localhost:8000/api/trade/edit/"
args = {"trade_id" : 1, "maturity_date" : '2020-12-12', "quantity" : 1, "strike_price" : 1, "underlying_price" : 1}
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
data = requests.request("POST", url, headers=headers, data=args)

url="http://localhost:8000/api/trade/edit/"
args = {"trade_id" : 1, "maturity_date" : '2020-12-12', "quantity" : 1, "strike_price" : 1, "underlying_price" : 1}
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
data = requests.request("POST", url, headers=headers, data=args)
print(data.content.decode('utf-8'))