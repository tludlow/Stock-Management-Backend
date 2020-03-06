import requests
import datetime
import random
import os
import json
import dateutil.parser

class TradeManipulation:

    def get(self, loc):
        return requests.get(self.BASE_URL+loc).json()

    def post(self, loc, args):
        return requests.post(self.BASE_URL+loc, data=args).json()

    def edit_trade(self, id, date, field, value):
        return self.post("trade/edit/", {'trade_id' : id, field : value, 'edit_date' : date})

    def delete_trade(self, id, date):
        return self.post("trade/delete/", {'trade_id' : id, 'delete_date' : date})

    def start(self):
        for trade in self.trades:
            id = trade['id']     
            
            print("Trade ID:", id)
            
            date = dateutil.parser.isoparse((trade['date']))
            maturity_date = dateutil.parser.isoparse((trade['maturity_date']))   
            edit_count = 0
           
            # 1/20 trades will be edited
            while (random.randint(1,2) == 1 and edit_count < len(self.attributes)):
                days_later = random.randint(0, 3)
                edit_date = date + datetime.timedelta(days=days_later)
                attribute = random.randint(1, len(self.attributes))
                attribute_tag = self.attributes[attribute]

                if attribute == 1:
                    product = random.randint(0, len(self.products))
                    print(self.product)
                    value = self.product[product]['id']
                
                elif attribute in [2, 3]:
                    company = random.randint(0, len(self.companies))
                    val = self.companies[company]['id']

                elif attribute in [4, 5, 7, 8, 9]:
                    # Altered by -20% to 20%
                    val = trade[attribute_tag] * random.randint(80, 120) * 0.01
                
                elif attribute == 6:
                    days_later = random.randint(1, 10000)
                    val = maturity_date + datetime.timedelta(days=days_later)
                
                self.edit_trade(id, edit_date, attribute_tag, val)
                print("Setting", attribute_tag, "to", val)
                edit_count += 1
            if edit_count == 0:
                print("No Edits")
            else:
                print("Finished editing")
            # 1/500 trades will be deleted
            delete = random.randint(1,500) == 1
            if delete:
                if maturity_date > edit_date:
                    self.delete_trade(id, edit_date)

    def get_trades(self):
        if os.path.exists("trades.json"):
            with open("trades.json") as json_file:
                data = json_file.read()
                data = data.replace("'",'"')
                return json.loads(data)
        else:
            trades = self.get("trade/recent/")
            with open("trades.json", "w") as json_file:
                json_file.write(str(trades))
                return trades

    def __init__(self, BASE_URL):
        self.BASE_URL = BASE_URL
        self.attributes =  {1 : 'product', 2 : 'buying_party', 
                            3 : 'selling_party', 4: 'notional_currency',
                            5 : 'quantity', 6 : 'maturity_date',
                            7 : 'underlying_price', 8 : 'underlying_currency',
                            9 : 'strike_price'}
        self.trades = self.get_trades()
        self.products = self.get("product/list/")
        self.companies = self.get("company/list/")

if __name__ == '__main__':
    BASE_URL = "https://group23.warwick.ac.uk/api/"
    BASE_URL_LOCAL = "http://localhost:8000/api/"
    x = TradeManipulation(BASE_URL_LOCAL)
    x.start()







    
