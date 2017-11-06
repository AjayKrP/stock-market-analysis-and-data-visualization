from flask import session
import pandas as pd


def get_stock_name():
    df = pd.read_csv('static/WIKI-datasets-codes.csv')
    val = df.loc[df['name'] == session['stock']]
    val = val['description']
    val = str(val)
    val = val.split(',')
    val = val[0]
    val = val[4:]
    return val

def get_current_stock_value():
    f = open('/home/ajay/PycharmProjects/SDL-PROJ/static/data_full.csv', 'r+')
    lines = f.readlines()
    get_current_stock = lines[-1:]
    get_current_stock = get_current_stock[0]
    get_current_stock = get_current_stock.split(',')
    return get_current_stock

def value_calculation(value):
    foo = value
    if foo < 0 and foo > -0.5:
        foo = -1 * foo
    elif value < -0.5:
        foo = -1 * foo
        foo = foo - int(foo)
    elif value > 1 and value < 2:
        foo -= 1
    return foo
