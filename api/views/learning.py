from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django import forms
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from api.serializers import *
from ..models import *
from ..serializers import *
from datetime import datetime, timedelta, timezone, date
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

# import warnings filter
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)
le = preprocessing.LabelEncoder()  # used to encode/convert dataproduct = le.fit_transform(list(userQuantity))



#+- value we allow for it to be considered correct
percentage = 20

def scanTradeForErrors(trade):
    #Going to need to pass the information below to the AI to scan for the errors.
    #Strike Price
    #Quantity
    #Underlying Price

    trade_s = TradeSerializer(trade)
    trade_data = trade_s.data

    print(trade_data)
    
    boughtProduct = trade_data["product"]
    buyingCompany = trade_data["buying_party"]
    sellingCompany = trade_data["selling_party"]

    #Get the data to compare against
    getBuyerProduct = requests.get(
            "http://localhost:8000/api/trade/product={0}&buyer={1}&seller={2}/".format(boughtProduct, buyingCompany, sellingCompany))

    data = pd.read_json(StringIO(getBuyerProduct.text))  # convert the trade data into text to be analysed

    # parse the data
    data = data[["buying_party", "selling_party", "maturity_date", "date",
                "product", "strike_price", "underlying_price", "notional_amount", "quantity"]]


    product = list(data["product"])
    strike = list(data["strike_price"])
    underlying = list(data["underlying_price"])
    notional = list(data["notional_amount"])
    quantity = list(data["quantity"])
    buy = list(data["buying_party"])
    sell = list(data["selling_party"])
    mature = list(data["maturity_date"])
    date = list(data["date"])

    predict = "quantity"  # element to be predicted

    # separate the data into 2 parts
    X = list(zip(product, sell))  # data to be analysed to make predictions
    y = list(zip(quantity, strike, underlying))  # data to be predicted

    totalTrades = round(len(y)*0.9)-2
    K = totalTrades // 10
    if K == 0:
        K = 1

    #Cant predict confidently when there are minimal trades
    if totalTrades < 6:
        print("Not running the AI, dont have enough confidence")
        return -1

    userQuantity = [trade_data["quantity"]]
    userSelling = [trade_data["selling_party"]]
    userProduct = [trade_data["product"]]
    userStrike = [trade_data["strike_price"]]
    userUnderlying = [trade_data["underlying_price"]]

    nonUserValues = list(zip(userProduct, userSelling))
    userInput = list(zip(userQuantity, userStrike, userUnderlying))

    #We need to run the AI on the quantity
    trainData(1, boughtProduct, buyingCompany, totalTrades, K, X, y)
    testData(predict, buyingCompany, boughtProduct, totalTrades, K, userInput, nonUserValues, X, y)

    #Make it run for strike price

    #Make it run for underlying_price

    debug = True
    if debug:
#         # plot the graph
        compare = "underlying_price"  # value to be compared against predicted data
        style.use("ggplot")
        pyplot.scatter(data[compare], data[predict])
        pyplot.xlabel(predict)  # plot the predicted value on the x
        pyplot.ylabel(compare)  # plot the compared value on the y
        pyplot.show()

    #Run the AI on strike price

    #Run the AI on underlying_price
























############################################
# ACTUAL MACHINE LEARNING / AI CODE BELOW
############################################
def trainData(n, p, b, totalTrades, K, X, y):

    x_train = y_train = 0 # initialise model values
    best = 0  # the best test data set to be used in the future

    # divide the data into test data and practice data and loop over 100 times until best data set is found
    for _ in range(n):
        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.1)  # split data
        modelTest = KNeighborsRegressor(n_neighbors=K) # use K-Neighbours Regression model for K neighbours

        modelTest.fit(x_train, y_train)  # fit the model

        if totalTrades <= 19:
            with open("tradeModel_{0}_{1}.pickle".format(b,p), "wb") as f:
                pickle.dump(modelTest, f)  # save the test data set
            break
        acc = modelTest.score(x_test, y_test)  # accuracy of predictions

        # if accuracy is higher than best recorded accuracy
        if acc > best:
            best = acc  # new accuracy is best accuracy
            with open("tradeModel_{0}_{1}.pickle".format(b,p), "wb") as f:
                pickle.dump(modelTest, f)  # save the test data set

    modelTrade = KNeighborsRegressor(n_neighbors=totalTrades) # use K-Neighbours Regression model for totalTrades neighbours
    modelTrade.fit(x_train, y_train)  # fit the model
    trades = modelTrade.kneighbors(n_neighbors=totalTrades)  # get the distance of each trade in the KNN model
    tradeDistance = 0  # initiate variable to store total distances of all trades

    # loop over all trades and add their distance into tradeDistance
    for u in range(totalTrades):
        for v in range(len(trades)):
            tradeDistance += trades[0][u][v]

    average = tradeDistance / totalTrades  # get the average distance of all trades
    with open("tradeDistance_{0}_{1}.pickle".format(b,p), "wb") as f:
        pickle.dump(average, f)  # save the average distance for that model

def testData(predicting, buyingCompany, boughtProduct, totalTrades, K, userInput, nonUserValues, X, y):

    model = pickle.load(open("tradeModel_{0}_{1}.pickle".format(buyingCompany, boughtProduct), "rb"))  # load in latest saved model
    tradeDistanceAverage = pickle.load(open("tradeDistance_{0}_{1}.pickle".format(buyingCompany, boughtProduct), "rb"))  # load in saved average trade distances

    model.fit(X, y)  # fit the model using X as training data and y as target values
    predictions = model.predict(nonUserValues)
    print("nonUserValues:", nonUserValues[0])
    print("userInput:", userInput[0][0])
    print("prediction:", predictions[0][0])
    print("")

    neighbours = model.kneighbors(n_neighbors=K)  # get the distance of each neighbour analyzed in the KNN model
    neighbourDistance = 0  # initialize total neighbour distances
    # loop over all neighbours and add their distance into neighbourDistance
    for i in range(K):
        for j in range(len(neighbours) - 1):
            neighbourDistance += neighbours[0][i][j]

    neighbourDistanceAverage = neighbourDistance / K  # get the average distance of all neighbours

    compareDifference = tradeDistanceAverage * (percentage / 100)  # get the range percentage of the trade average
    print("neighbourDistanceAverage:", neighbourDistanceAverage)
    print("tradeDistanceAverage:", tradeDistanceAverage)
    print ("compareDifference: +-", compareDifference)

    # if the neighbours average is greater than the trade average+percentage or less then trade average-percentage (i.e. out of range)
    if neighbourDistanceAverage > tradeDistanceAverage + compareDifference or neighbourDistanceAverage < tradeDistanceAverage - compareDifference:
        print("Out of bounds")  # do something

# def main():
#     if totalTrades <= 5:
#         print("!!! WARNING: not enough trades for accurate predictions !!!")
#         print("Number of trades:", totalTrades)
#         print("")
#     trainData(1, boughtProduct, buyingCompany)
#     # if not os.path.isfile("tradeModel_{0}_{1}.pickle".format(boughtProduct, buyingCompany)):
#     #     trainData(100, boughtProduct, buyingCompany, X, y)
#     testData()
    
#     debug = True

#     if debug:
#         # plot the graph
#         compare = "underlying_price"  # value to be compared against predicted data
#         style.use("ggplot")
#         pyplot.scatter(data[compare], data[predict])
#         pyplot.xlabel(predict)  # plot the predicted value on the x
#         pyplot.ylabel(compare)  # plot the compared value on the y
#         pyplot.show()

# if __name__ == "__main__":
#     main()