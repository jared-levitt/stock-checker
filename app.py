import os
import time
import re
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
from datetime import datetime

import finnhub

finnhub_client = finnhub.Client(api_key="ciqmtm9r01qjff7crg10ciqmtm9r01qjff7crg1g")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

socketio = SocketIO(app)

stock_symbol = None

def get_stock_price(symbol):
    try:
        data = finnhub_client.quote(symbol)
        print(data)
        stock_price = data['c']
        change = round(float(data['d']), 2)
        changePercent = round(float(data['dp']), 2)
        high = round(float(data['h']), 2)
        low = round(float(data['l']), 2)
        return stock_price, change, changePercent, high, low
    except Exception as e:
        print(f"Error retrieving stock price: {e}")
        return None, None, None, None, None

def emit_stock_update():
    global stock_symbol

    stock_price, change, changePercent, high, low = get_stock_price(stock_symbol)
    last_updated = time.strftime("%d/%m/%Y %H:%M")

    socketio.emit('stock_update', {
        'price': stock_price,
        'change': change,
        'changePercent': changePercent,
        'high': high,
        'low': low,
        'lastUpdated': last_updated
    }, broadcast=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    global stock_symbol

    if request.method == 'POST':
        stock_symbol = request.form['symbol']
        return redirect(url_for('stock_price', symbol=stock_symbol))
    else:
        return render_template('index.html')

@app.route('/stock-price/<symbol>')
def stock_price(symbol):
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
    return render_template('stock_price.html', stock_symbol=symbol, current_time=current_time)

@socketio.on('connect')
def handle_connect():
    print('Connected to server')

@socketio.on('disconnect')
def handle_disconnect():
    print('Disconnected from server')

if __name__ == '__main__':
    from apscheduler.schedulers.background import BackgroundScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(emit_stock_update, 'interval', seconds=5)
    scheduler.start()
    socketio.run(app)
