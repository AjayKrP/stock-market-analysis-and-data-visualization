import quandl, math, datetime
import numpy as np
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from matplotlib import style
import time
from sklearn import svm, model_selection

import os
import threading

style.use ('ggplot')

def save_total_data(df):
    df.rename(index=str, columns={"Adj. Open": "Open", "Adj. High": "High", "Adj. Low": "Low", "Adj. Close": "Close",
                                  "Adj. Volume": "Volume"})

    df.to_csv('/home/ajay/PycharmProjects/SDL-PROJ/static/' + 'data_full.csv', sep=',', encoding='utf-8')


def calculate(stock, start_date, end_date):
    print(stock + ' from calculate')
    #df = quandl.get("GOOG/NASDAQ_GOOGL", authtoken="sD9npaAKgpHsQdwVfZ5p")
    stock = stock.upper()
    df = quandl.get("WIKI/" + stock, trim_start=start_date, trim_end=end_date, authtoken="sD9npaAKgpHsQdwVfZ5p")
    df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume', ]]
    pf = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume', ]]
    pf.rename(index=str, columns={"Adj. Open": "Open", "Adj. High": "High", "Adj. Low": "Low", "Adj. Close": "Close",
                                  "Adj. Volume": "Volume"})

    pf.to_csv('/home/ajay/PycharmProjects/SDL-PROJ/static/' + 'data_full.csv', sep=',', encoding='utf-8')

    df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100.0
    df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0
    # define a new data frame
    df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]

    forecast_col = 'Adj. Close'


    df.fillna(-99999, inplace=True)
    forecast_out = int(math.ceil(0.01 * len(df)))
    df['label'] = df[forecast_col].shift(-forecast_out)

    X = np.array(df.drop(['label'], 1))
    X = preprocessing.scale(X)
    X_lately = X[-forecast_out:]
    X = X[:-forecast_out:]
    df.dropna(inplace=True)
    y = np.array(df['label'])


    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)

    #clf = svm.SVR()
    clf = LinearRegression()
    clf.fit(X_train, y_train)
    accuracy = clf.score(X_test, y_test)
    forecast_set = clf.predict(X_lately)
    #print(forecast_set, accuracy, forecast_out)
    df['Forecast'] = np.nan

    last_date = df.iloc[-1].name

    last_unix = time.mktime(last_date.timetuple())
    one_day = 86400
    next_unix = last_unix + one_day

    for i in forecast_set:
        next_date = datetime.datetime.fromtimestamp(next_unix)
        next_unix += one_day
        df.loc[next_date] = [np.nan for _ in range(len(df.columns) - 1)] + [i]
    print(forecast_set)

    fs = df[['Adj. Close', 'Forecast']]
    fs.to_csv('/home/ajay/PycharmProjects/SDL-PROJ/static/forecast.csv', sep=',', encoding='utf-8')
    #cwd = os.getcwd()
    df['Adj. Close'].to_csv('/home/ajay/PycharmProjects/SDL-PROJ/static/temp.csv', sep=',', encoding='utf-8',
                            header={'date,close'})
    try:
        f = open("/home/ajay/PycharmProjects/SDL-PROJ/static/temp.csv", "r+")
        fi = open( "/home/ajay/PycharmProjects/SDL-PROJ/static/data.csv", 'w+')
        lines = f.readlines()
        lines = lines[:-1]
        for line in lines:
            fi.write(line)
    except FileNotFoundError:
        print("file not found")

    return (forecast_set, accuracy, forecast_out)




