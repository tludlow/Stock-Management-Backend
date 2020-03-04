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
buyingCompany = 32 # buying company
sellingCompany = 61
boughtProduct = 183 # product bought
percentage = 20 # leeway percentage to be used to see if the predicted value is in range

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


product = list(data["product"])
strike = list(data["strike_price"])
underlying = list(data["underlying_price"])
notional = list(data["notional_amount"])
quantity = list(data["quantity"])
buy = list(data["buying_party"])
sell = list(data["selling_party"])
mature = list(data["maturity_date"])
date = list(data["date"])

print(sell)

predict = "quantity"  # element to be predicted

# separate the data into 2 parts
X = list(zip(product, sell))  # data to be analysed to make predictions
y = list(zip(quantity, strike, underlying))  # data to be predicted

totalTrades = round(len(y)*0.9)-1
K = totalTrades // 10
if K == 0:
    K = 1

userQuantity = [300]
userSelling = [712]
userProduct = [382]
userStrike = [2875.28]
userUnderlying = [126.71]

nonUserValues = list(zip(userProduct, userSelling))
userInput = list(zip(userQuantity, userStrike, userUnderlying))


def trainData(n, p, b):

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
        print("weeeehoooooo")
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

def testData():

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

def main():
    if totalTrades <= 5:
        print("!!! WARNING: not enough trades for accurate predictions !!!")
        print("Number of trades:", totalTrades)
        print("")
    trainData(1, boughtProduct, buyingCompany)
    # if not os.path.isfile("tradeModel_{0}_{1}.pickle".format(boughtProduct, buyingCompany)):
    #     trainData(100, boughtProduct, buyingCompany, X, y)
    testData()
    
    debug = True

    if debug:
        # plot the graph
        compare = "underlying_price"  # value to be compared against predicted data
        style.use("ggplot")
        pyplot.scatter(data[compare], data[predict])
        pyplot.xlabel(predict)  # plot the predicted value on the x
        pyplot.ylabel(compare)  # plot the compared value on the y
        pyplot.show()

if __name__ == "__main__":
    main()