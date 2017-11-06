import pandas as pd
from prediction import *
import quandl, math
import numpy as np
from sklearn import preprocessing,cross_validation, svm
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, VotingClassifier


def initial_setup(ticker):
    df = quandl.get("WIKI/"+str(ticker), authtoken="sD9npaAKgpHsQdwVfZ5p")
    df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume', ]]
    df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100.0
    df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0
    df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]
    return df

def predict(ticker):
    df = initial_setup(ticker)
    forecast_col = 'Adj. Close'
    df.fillna(-99999, inplace=True)
    forecast_out = int(math.ceil(0.01 * len(df)))  # no. of days to forecast
    print("no of days forecasted ", forecast_out)
    print(len(df))
    df['label'] = df[forecast_col].shift(-forecast_out)
    df.dropna(inplace=True)

    X = np.array(df.drop(['label'], 1))
    y = np.array(df['label'])
    X = preprocessing.scale(X)
    df.dropna(inplace=True)
    y = np.array(df['label'])

    clf1 = LogisticRegression(random_state=1)
    clf2 = RandomForestClassifier(random_state=1)
    clf3 = GaussianNB()
    eclf1 = VotingClassifier(estimators=[('lr', clf1), ('rf', clf2), ('gnb', clf3)], voting='hard')

    eclf1 = eclf1.fit(X, y)
    print(X)
    print('hola: ' + str(eclf1.predict(X)))

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

    #clf = svm.SVR()  ## USING SVM
    clf = LinearRegression(n_jobs = -1)
    clf.fit(X_train, y_train)
    accuracy = clf.score(X_test, y_test)
    print(accuracy)

if __name__=="__main__":
    predict('FB')


