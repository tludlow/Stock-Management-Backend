from flask import Blueprint, escape

delete_trade = Blueprint("delete_trade", __name__)

@delete_trade.route('/trade/delete/<string:trade_id>', methods=['POST'])
def deleteTrade(trade_id=None):
    return "Deleting the trade: %s" % escape(trade_id)