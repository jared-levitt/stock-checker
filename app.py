import os
import requests
import finnhub
from flask import Flask, render_template, request, redirect, url_for
from pyfiglet import Figlet
import re
from flask_socketio import SocketIO, emit
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)

def get_stock_price(symbol):
    api_key = 'ciqpdm9r01qjff7css00ciqpdm9r01qjff7css0g'
    finnhub_client = finnhub.Client(api_key=api_key)
    quote = finnhub_client.quote(symbol)
    stock_price = quote['c']
    change = round(float(quote['d']), 2)
    changePercent = round(float(quote['dp']), 2)
    high = round(float(quote['h']), 2)
    low = round(float(quote['l']), 2)
    return stock_price, change, changePercent, high, low

def emit_stock_update():
    stock_symbol = request.args.get('symbol')
    price, change, changePercent, high, low = get_stock_price(stock_symbol)

    if price:
        formatted_price = re.sub('[^0-9.]', '', price)
        formatted_price = formatted_price[:-2]
        ascii_price = Figlet(font='colossal').renderText(' '.join(formatted_price))

        emit('stock_update', {
            'price': ascii_price,
            'change': change,
            'changePercent': changePercent,
            'high': high,
            'low': low
        }, broadcast=True)
        emit('time_update', {'lastUpdated': datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}, broadcast=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock_symbol = request.form['symbol']
        return redirect(url_for('stock_price', symbol=stock_symbol))
    else:
        return render_template('index.html')

@app.route('/stock-price/<symbol>')
def stock_price(symbol):
    price, change, changePercent, high, low = get_stock_price(symbol)

    if price:
        formatted_price = re.sub('[^0-9.]', '', str(price))
        spaced_price = ' '.join(formatted_price)
        
        font = Figlet(font='colossal')
        ascii_price = font.renderText(spaced_price)

        return render_template('stock_price.html', ascii_price=ascii_price, stock_symbol=symbol, change=change, changePercent=changePercent, high=high, low=low)
    else:
        return 'Error retrieving stock price'

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(emit_stock_update, 'interval', seconds=5)
    scheduler.start()
    socketio.run(app)
