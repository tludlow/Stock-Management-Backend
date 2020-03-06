import requests
import datetime
import random
import os
import json
import dateutil.parser
import pytz
class TradeManipulation:

    def get(self, loc):
        return requests.get(self.BASE_URL+loc).json()

    def post(self, loc, args):
        args['demo'] = 'true'
        return requests.post(self.BASE_URL+loc, data=args).json()

    def edit_trade(self, id, date, field, value):
        args = {'trade_id' : id, field : value, 'edit_date' : date}
        return self.post("trade/edit/", args)

    def delete_trade(self, id, date):
        args = {'trade_id' : id, 'delete_date' : date}
        return self.post("trade/delete/", args)

    def get_trades(self, page):
        return self.get(f"trade/recent/?page_number={str(page)}")
    
    def get_trades_specific(self, year, month, day):
        return self.get(f"trade/year={year}&month={month}&day={day}/")

    def gen_company(self):
        company = random.randint(0, len(self.companies)-1)
        return self.companies[company]['id']

    def gen_currency(self):
        currency = random.randint(0, len(self.currencies)-1)
        return self.currencies[currency]['currency']

    def gen_product(self):
        product = random.randint(0, len(self.products)-1)
        return self.products[product]['id']
    
    def create(self, dates, max):
        for date in dates:
            for _ in range(random.randint(1, max)):
                buying_party = self.gen_company()
                selling_party = self.gen_company()
                product = self.gen_product()
                quantity = random.randint(1, 999999)
                underlying_currency = self.gen_currency()
                notional_currency = self.gen_currency()
                strike_price = round(random.uniform(1, 999999),2)
                underlying_price = round(random.uniform(1, 999999), 2)

                now = datetime.datetime.now()
                future = datetime.timedelta(days = random.randint(1, 9999))
                maturity_date =  now + future
                
                vals = {'date' : date,
                        'selling_party': selling_party, 
                        'buying_party' : buying_party, 
                        'product' :  product,
                        'quantity' : str(quantity),
                        'maturity_date' : maturity_date.strftime("%Y-%m-%d"),
                        'underlying_currency' : underlying_currency,
                        'notional_currency' : notional_currency,
                        'strike_price' : str(strike_price),
                        'underlying_price' : str(underlying_price)}

                new_trade = self.post("trade/create/", vals)
                print(f"[Creation] Trade with id {new_trade['trade_id']} has been created")

    def edit_manipulation(self, trade):
        utc=pytz.UTC
        id = trade['id']     
        date = dateutil.parser.isoparse((trade['date']))
        maturity_date = dateutil.parser.isoparse((trade['maturity_date'])) 
        maturity_date = maturity_date.replace(tzinfo=utc)  
        edit_count = 0
        # 1/20 trades will be edited
        while (random.randint(1,20) == 1 and edit_count < len(self.attributes)):
            # Random edit date max 3 days after
            days_later = random.randint(0, 3)
            edit_date_org = date + datetime.timedelta(days=days_later)
            edit_date_org = edit_date_org.replace(tzinfo=utc)  
            # If edit date > current date, use current date as edit date
            if edit_date_org > datetime.datetime.now().replace(tzinfo=utc):
                edit_date_org = datetime.datetime.now().replace(tzinfo=utc)  

            edit_date = edit_date_org.isoformat()
            attribute = random.randint(1, len(self.attributes))
            attribute_tag = self.attributes[attribute]

            if attribute == 1:
                val = self.gen_product()
            
            elif attribute in [2, 3]:
                val = self.gen_company()
            
            elif attribute in [4, 8]:
                attribute_tag = attribute_tag[:-3]
                val = self.gen_currency()

            elif attribute in [5]:
                # Altered by -20% to 20%
                val = int(trade[attribute_tag] * random.randint(80, 120) * 0.01)

            elif attribute in [7, 9]:
                # Altered by -20% to 20%
                rand = trade[attribute_tag] * random.randint(80, 120) * 0.01
                val = round(rand, 2)
            
            elif attribute == 6:
                days_later = random.randint(1, 10000)
                val = maturity_date + datetime.timedelta(days=days_later)
                val = val.strftime("%Y-%m-%d")
            
            
            edit = self.edit_trade(id, edit_date, attribute_tag, val)
            if edit.get('error', None) != None:
                print(f"""[Error] Trade {str(id)} wasn't edited""")
            else:
                print(f"[Trade {str(id)}] setting {attribute_tag} to {val} on {edit_date}")
            edit_count += 1
        return edit_count

    def delete_manipulation(self, trade):
        utc=pytz.UTC
        id = trade['id']     
        date = dateutil.parser.isoparse((trade['date']))
        maturity_date = dateutil.parser.isoparse((trade['maturity_date'])) 
        maturity_date = maturity_date.replace(tzinfo=utc)  

        # 1/40 trades will be deleted
        delete = random.randint(1,40) == 1
        if delete:
            # Random edit date max 3 days after
            days_later = random.randint(0, 3)
            edit_date_org = date + datetime.timedelta(days=days_later)
            edit_date_org = edit_date_org.replace(tzinfo=utc)  
            
            # If edit date > current date, use current date as edit date
            if edit_date_org > datetime.datetime.now().replace(tzinfo=utc):
                edit_date_org = datetime.datetime.now().replace(tzinfo=utc)  
            edit_date = edit_date_org.isoformat()

            if maturity_date > edit_date_org:
                delete = self.delete_trade(id, edit_date)
                if delete.get('error', None) != None:
                    print("[Error] Trade "+str(id)+" wasn't deleted")
                    return 0
                else:
                    print("[Trade "+str(id)+"] deleted on "+edit_date)
                    return 1
        return 0

    def manipulate(self, max, date=[]):
        unlimited = len(date) == 0
        manipulations = 0
        n = random.randint(1, max)
        if unlimited:
            page = 1
            while True:
                trades = self.get_trades(page)
                for trade in trades:
                    manipulations += self.edit_manipulation(trade)
                    manipulations += self.delete_manipulation(trade)
                    if manipulations >= n:
                        return
                page += 1
        else:
            for year_month_day in date:
                d = year_month_day.split('-')
                trades = self.get_trades_specific(d[0], d[1], d[2])
                manipulations = 0
                stop = False
                while manipulations < n and stop is False:
                    for trade in trades:
                        manipulations += self.edit_manipulation(trade)
                        manipulations += self.delete_manipulation(trade)
                        if manipulations >= n:
                            stop = True
                            break

    def __init__(self, BASE_URL):
        self.BASE_URL = BASE_URL
        self.attributes =  {1 : 'product', 2 : 'buying_party', 
                            3 : 'selling_party', 4: 'notional_currency_id',
                            5 : 'quantity', 6 : 'maturity_date',
                            7 : 'underlying_price', 
                            8 : 'underlying_currency_id',
                            9 : 'strike_price'}
        self.products = self.get("product/list/")
        self.companies = self.get("company/list/")
        self.currencies = self.get("currency/list/")

if __name__ == '__main__':
    BASE_URL = "https://group23.warwick.ac.uk/api/"
    BASE_URL_LOCAL = "http://localhost:8000/api/"
    x = TradeManipulation(BASE_URL_LOCAL)

    # TRADE CREATION
    # [Dates to add trades on], Max number of trades per day (random)
    x.create(['2020-03-04'], 10)

    # TRADE EDIT & DELETION
    # Max number of manipulations to carry out (edits and deletions), dates
    # (optional) that should be manipulated - if left blank uses recent
    x.manipulate(10, date=['2020-03-04'])









    
