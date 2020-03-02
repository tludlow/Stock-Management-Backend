import requests
from io import StringIO
import pandas as pd
import os
import sklearn
import numpy
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor
import pickle
import matplotlib.pyplot as pyplot
from matplotlib import style
from warnings import simplefilter

# ignore all future warnings
simplefilter(action='ignore', category=Warning)

le = preprocessing.LabelEncoder()  # used to encode/convert dataproduct = le.fit_transform(list(userQuantity))


debug=False

buyingCompany = "SUOX82" # buying company
boughtProduct = 331 # product bought
percentage = 15 # leeway percentage to be used to see if the predicted value is in range

userQuantity = [32000]
userSelling = [712]
userProduct = [382]
userStrike = [128.71]
userUnderlying = [135.32]


getBuyerProduct = requests.get(
        "http://localhost:8000/api/trade/product={0}&buyer={1}&seller={2}/".format(boughtProduct, buyingCompany, "ESPL27"))

data = pd.read_json(StringIO(getBuyerProduct.text))  # convert the trade data into text to be analysed

data = data[["buying_party",
                 "selling_party",
                 "maturity_date",
                 "date",
                 "product",
                 "strike_price",
                 "underlying_price",
                 "notional_amount",
                 "quantity"]]

# convert data to numerical values so comparative evaluations can be performed on them
product = list(data["product"])
strike = list(data["strike_price"])
underlying = list(data["underlying_price"])
notional = le.fit_transform(list(data["notional_amount"]))
quantity = list(data["quantity"])
buy = le.fit_transform(list(data["buying_party"]))
sell = le.fit_transform(list(data["selling_party"]))
mature = le.fit_transform(list(data["maturity_date"]))
date = le.fit_transform(list(data["date"]))

print(product)
print(strike)
print(underlying)
print(quantity)


predict = "quantity"  # element to be predicted

# separate the data into 2 parts
X = list(zip(product, strike, underlying))  # data to be analysed to make predictions
y = list(zip(quantity))  # data to be predicted (quantity, strike, underlying)

totalTrades = round(len(y)*0.9)-1
K = totalTrades // 3

if debug:
    # plot the graph
    compare = "underlying_price"  # value to be compared against predicted data
    style.use("ggplot")
    pyplot.scatter(data[compare], data[predict])
    pyplot.xlabel(predict)  # plot the predicted value on the x
    pyplot.ylabel(compare)  # plot the compared value on the y
    pyplot.show()


nonUserValues = list(zip(userProduct))
userInput = list(zip(userQuantity, userStrike, userUnderlying))


def trainData(n, p, b, i, o):

    x_train = y_train = 0 # initialise model values
    best = 0  # the best test data set to be used in the future

    # divide the data into test data and practice data and loop over 100 times until best data set is found
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(i, o, test_size=0.1)  # split data
    print("!!! TRADES COUNT: " + str(totalTrades) + "   K: " + str(K))
    modelTest = KNeighborsRegressor(n_neighbors=K) # use K-Neighbours Regression model for K neighbours
    print("!!! TRADES COUNT: " + str(totalTrades) + "   K: " + str(K))
    modelTest.fit(x_train, y_train)  # fit the model
    print("1")
    print(x_train)
    print(y_train)
    print("===")
    print(x_test)
    print(y_test)
    print("2")

    print("3")
    modelTrade = KNeighborsRegressor(n_neighbors=totalTrades) # use K-Neighbours Regression model for totalTrades neighbours
    print("4")
    modelTrade.fit(x_train, y_train)  # fit the model
    print("5")
    trades = modelTrade.kneighbors(n_neighbors=totalTrades)  # get the distance of each trade in the KNN model
    print("6")
    tradeDistance = 0  # initiate variable to store total distances of all trades

    # loop over all trades and add their distance into tradeDistance
    for u in range(totalTrades):
        for v in range(len(trades)):
            tradeDistance += trades[0][u][v]

    average = tradeDistance / totalTrades  # get the average distance of all trades
    with open("tradeDistance_{0}_{1}.pickle".format(b,p), "wb") as f:
        pickle.dump(average, f)  # save the average distance for that model

    return modelTest

def testData(i, o):

    model = trainData(1, boughtProduct, buyingCompany, X, y)
    tradeDistanceAverage = pickle.load(open("tradeDistance_{0}_{1}.pickle".format(buyingCompany, boughtProduct), "rb"))  # load in saved average trade distances

    model.fit(i, o)  # fit the model using X as training data and y as target values
    # accuracy = model.score(nonUserValues, userInput) * 100
    predictions = model.predict(nonUserValues)
    print("prediction:", predictions[0])
    print("nonUserValues: ", nonUserValues)
    print("userInput: ", userInput)
    print("")

    # print("Accuracy: %f%%" % accuracy)
    print(K)
    neighbours = model.kneighbors(n_neighbors=K)  # get the distance of each neighbour analyzed in the KNN model
    neighbourDistance = 0  # initialize total neighbour distances
    print(K)

    # loop over all neighbours and add their distance into neighbourDistance
    for i in range(K):
        for j in range(len(neighbours)):
            neighbourDistance += neighbours[0][i][j]

    neighbourDistanceAverage = neighbourDistance / K  # get the average distance of all neighbours

    comparePercentage = tradeDistanceAverage * (percentage / 100)  # get the range percentage of the trade average
    print("neighbourDistanceAverage: ", neighbourDistanceAverage)
    print("tradeDistanceAverage: ", tradeDistanceAverage)

    # if the neighbours average is greater than the trade average+percentage or less then trade average-percentage (i.e. out of range)
    if neighbourDistanceAverage > tradeDistanceAverage + comparePercentage or neighbourDistanceAverage < tradeDistanceAverage - comparePercentage:
        print("Out of bounds")  # do something

testData(X, y)