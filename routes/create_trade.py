from flask import Blueprint, request

create_trade = Blueprint("create_trade", __name__)

@create_trade.route('/trade', methods=['POST'])
def deleteTrade():
    print(request.form)
    return {"currency": request.form['currency']}
    