from flask import Blueprint, escape

get_trade = Blueprint("get_trade", __name__)

@get_trade.route('/trade/<string:trade_id>', methods=['GET'])
def getTrade(trade_id=None):
    return "You have tried to get the trade with id: %s" % escape(trade_id)