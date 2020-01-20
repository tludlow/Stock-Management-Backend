from flask import Flask
app = Flask(__name__)

#To enable the app debugging mode
app.debug = True

#Importing routes from the directory '/routes'
from routes.create_trade import create_trade
from routes.get_trade import get_trade
from routes.delete_trade import delete_trade

app.register_blueprint(create_trade)
app.register_blueprint(get_trade)
app.register_blueprint(delete_trade)

#Start the flask app automatically upon running this file.
if __name__ == '__main__':
    app.run()