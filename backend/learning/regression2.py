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

K = 5 # number of neighbours to be compared
totalTrades = 8 # number of total trades analyzed
buyingCompany = "YLGZ72" # buying company
boughtProduct = 382 # product bought
sellingCompany = "HNLV68"
# userInput = 5 # user input to be evaluated for errors
# nonUserValues = (177, 393, 413, 161) # trade details that the user didn't input
percentage = 15 # leeway percentage to be used to see if the predicted value is in range
debug = False #whether to show graph or not

userQuantity = [300]
userSelling = [712]
userProduct = [382]
userStrike = [2875.28]
userUnderlying = [126.71]

le = preprocessing.LabelEncoder()  # used to encode/convert dataproduct = le.fit_transform(list(userQuantity))
# q = le.fit_transform(list(userQuantity))
# c = le.fit_transform(list(userSelling))
# p = le.fit_transform(list(userProduct))
# s = le.fit_transform(list(userStrike))
# u = le.fit_transform(list(userUnderlying))

# nonUserValues = list(zip(c,p,s,u))
# userInput = list(zip(q))

nonUserValues = list(zip(userProduct))
userInput = list(zip(userQuantity, userStrike, userUnderlying))

# print(nonUserValues)
# print (userInput)


# train prediction model and save best model to be used in the future
def trainData(n, p, b, i, o):

    x_train = y_train = 0 # initialise model values
    best = 0  # the best test data set to be used in the future

    # divide the data into test data and practice data and loop over 100 times until best data set is found
    for _ in range(n):
        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(i, o, test_size=0.1)  # split data
        modelTest = KNeighborsRegressor(n_neighbors=K) # use K-Neighbours Regression model for K neighbours
        modelTest.fit(x_train, y_train)  # fit the model
        acc = modelTest.score(x_test, y_test)  # accuracy of predictions

        # if accuracy is higher than best recorded accuracy
        if acc > best:
            best = acc  # new accuracy is best accuracy
            with open("tradeModel_{0}_{1}.pickle".format(b,p), "wb") as f:
                pickle.dump(modelTest, f)  # save the test data set

    modelTrade = KNeighborsRegressor(n_neighbors=totalTrades) # use K-Neighbours Regression model for totalTrades neighbours
    modelTrade.fit(x_train, y_train)  # fit the model
    trades = modelTrade.kneighbors(n_samples=100, n_neighbors=totalTrades)  # get the distance of each trade in the KNN model
    tradeDistance = 0  # initiate variable to store total distances of all trades

    # loop over all trades and add their distance into tradeDistance
    for u in range(totalTrades):
        for v in range(len(trades)):
            tradeDistance += trades[0][u][v]

    average = tradeDistance / totalTrades  # get the average distance of all trades
    with open("tradeDistance_{0}_{1}.pickle".format(b,p), "wb") as f:
        pickle.dump(average, f)  # save the average distance for that model


# Parse data and get the compare values (X) and the predicted values (y)

# get latest 150 trades of a specific product that a company bought
getBuyerProduct = requests.get(
    "http://localhost:8000/api/trade/product={0}&buyer={1}&seller={2}/".format(boughtProduct, buyingCompany, sellingCompany))

data = pd.read_json(StringIO(getBuyerProduct.text))  # convert the trade data into text to be analysed

# parse the data
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
product = le.fit_transform(list(data["product"]))
strike = le.fit_transform(list(data["strike_price"]))
underlying = le.fit_transform(list(data["underlying_price"]))
notional = le.fit_transform(list(data["notional_amount"]))
quantity = le.fit_transform(list(data["quantity"]))
buy = le.fit_transform(list(data["buying_party"]))
sell = le.fit_transform(list(data["selling_party"]))
mature = le.fit_transform(list(data["maturity_date"]))
date = le.fit_transform(list(data["date"]))

predict = "quantity"  # element to be predicted

# separate the data into 2 parts
X = list(zip(product))  # data to be analysed to make predictions
y = list(zip(quantity, strike, underlying))  # data to be predicted

# get data sets
trainData(100, boughtProduct, buyingCompany, X, y)

# if in debug mode
if debug:
    # plot the graph
    compare = "underlyingPrice"  # value to be compared against predicted data
    style.use("ggplot")
    pyplot.scatter(data[compare], data[predict])
    pyplot.xlabel(predict)  # plot the predicted value on the x
    pyplot.ylabel(compare)  # plot the compared value on the y
    pyplot.show()


model = pickle.load(open("tradeModel.pickle", "rb"))  # load in latest saved model
tradeDistanceAverage = pickle.load(open("tradeDistance.pickle", "rb"))  # load in saved average trade distances

model.fit(X, y)  # fit the model using X as training data and y as target values
# accuracy = model.score(nonUserValues, userInput) * 100
predictions = model.predict(nonUserValues)
print("prediction:", predictions[0])
print("nonUserValues: ", nonUserValues)
print("userInput: ", userInput)
print("")

# print("Accuracy: %f%%" % accuracy)

neighbours = model.kneighbors(n_neighbors=K)  # get the distance of each neighbour analyzed in the KNN model
neighbourDistance = 0  # initialize total neighbour distances

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


