import os
import time
import re
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
from datetime import datetime
from pyfiglet import Figlet

import finnhub

finnhub_client = finnhub.Client(api_key="ciqqfbhr01qjff7ctobgciqqfbhr01qjff7ctoc0")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

socketio = SocketIO(app)

cache = {}
update_interval = 15  # Update interval in seconds

def get_stock_price(symbol):
    # Check if data exists in the cache and if it is still valid
    if symbol in cache and time.time() - cache[symbol]['last_updated'] <= update_interval:
        return cache[symbol]['data']

    # Fetch new data from the API
    try:
        data = finnhub_client.quote(symbol)
        stock_price = data['c']
        change = round(float(data['d']), 2)
        changePercent = round(float(data['dp']), 2)
        high = round(float(data['h']), 2)
        low = round(float(data['l']), 2)
        
        formatted_price = re.sub('[^0-9.]', '', str(stock_price))
        spaced_price = ' '.join(formatted_price)

        font = Figlet(font='colossal')
        ascii_price = font.renderText(spaced_price)

        # Update cache with new data and last update time
        cache[symbol] = {
            'data': (ascii_price, change, changePercent, high, low),
            'last_updated': time.time()
        }

        return cache[symbol]['data']
    except Exception as e:
        print(f"Error retrieving stock price: {e}")
        return None, None, None, None, None

def emit_stock_update():
    stock_price, change, changePercent, high, low = get_stock_price(stock_symbol)
    last_updated = time.strftime("%d/%m/%Y %H:%M")

    if stock_price is not None:
        formatted_price = re.sub('[^0-9.]', '', str(stock_price))
        spaced_price = ' '.join(formatted_price)

        font = Figlet(font='colossal')
        ascii_price = font.renderText(spaced_price)

        socketio.emit('stock_update', {
            'ascii_price': ascii_price,
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
    stock_price, change, changePercent, high, low = get_stock_price(symbol)
    return render_template('stock_price.html', stock_symbol=symbol, current_time=current_time, ascii_price=ascii_price, change=change, changePercent=changePercent, high=high, low=low)

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
