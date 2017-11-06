from flask import Flask, redirect, url_for, request, render_template, session
app = Flask(__name__)
from prediction import calculate
from get_stock_details import *
value = None
stock = None

@app.route('/candle')
def candle():
    foo = value_calculation(value[1])
    get_current_stock = get_current_stock_value()
    val = get_stock_name()
    return render_template('predict_candle.html', data = value[0][0], accuracy=foo, no_of_day = value[2],
                           date=get_current_stock[0], open=get_current_stock[1], high=get_current_stock[2],
                           low=get_current_stock[3], close=get_current_stock[4], volume=get_current_stock[5],
                           stock_name=val)

@app.route('/hologram')
def hologram():
    foo = value_calculation(value[1])
    get_current_stock = get_current_stock_value()
    val = get_stock_name()
    return render_template('hologram.html',data = value[0][0], accuracy=foo, no_of_day = value[2],
                           date=get_current_stock[0], open=get_current_stock[1], high=get_current_stock[2],
                           low=get_current_stock[3], close=get_current_stock[4], volume=get_current_stock[5],
                           stock_name=val)

@app.route('/success/')
def success():
    foo = value_calculation(value[1])
    print(foo)
    get_current_stock = get_current_stock_value()
    val = get_stock_name()
    #print(len(get_current_stock))
    #print(get_current_stock)
    return render_template('predict.html', data = value[0][0], accuracy=foo, no_of_day = value[2],
                           date=get_current_stock[0], open=get_current_stock[1], high=get_current_stock[2],
                           low=get_current_stock[3], close=get_current_stock[4], volume=get_current_stock[5],
                           stock_name=val)

@app.route('/')
def indexPage():
    return render_template('index.html')

@app.route('/get_one_year')
def get_one_year_data():
    foo = value_calculation(value[1])
    return render_template('one_year_data.html', data = value[0][0], accuracy=foo, no_of_day = value[2])


@app.route('/search',methods = ['POST', 'GET'])
def year_data():
    global value
    if request.method == 'POST':
      stock = request.form['stock']
      session['stock'] = stock
      start_date = request.form['start-date']
      end_date = request.form['end-date']
      df = calculate(stock, start_date, end_date)
      value = df
      return redirect(url_for('success'))
    else:
      stock = request.args.get('stock')
      return redirect(url_for('success',name = stock))

@app.route('/get_yearly_data',methods = ['POST', 'GET'])
def start():
    global value
    global stock
    if request.method == 'POST':
      stock = request.form['stock']
      session['stock'] = stock
      start_date = request.form['start-date']
      end_date = request.form['end-date']
      df = calculate(stock, start_date, end_date)
      value = df
      return redirect(url_for('success'))
    else:
      stock = request.args.get('stock')
      return redirect(url_for('success',name = stock))

# USED FOR VISUALISATION
@app.route('/visualize')
def visualize_data():
    return render_template('visualization.html')

if __name__ == '__main__':
    app.secret_key = 'this is my world and i can do anything for this!'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run('127.0.0.1', 3000, debug=True)