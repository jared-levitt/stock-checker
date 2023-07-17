import requests
import finnhub
from flask import Flask, render_template, request, redirect, url_for, session
from pyfiglet import Figlet
import re
from flask_socketio import SocketIO
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app)
scheduler = BackgroundScheduler(daemon=True)
finnhub_client = finnhub.Client(api_key="your-finnhub-api-key")

def get_stock_price(symbol):
    try:
        res = finnhub_client.quote(symbol)
        stock_price = res['c']
        change = round(float(res['d']), 2)
        changePercent = round(float(res['dp']), 2)
        high = round(float(res['h']), 2)
        low = round(float(res['l']), 2)
        return stock_price, change, changePercent, high, low
    except (requests.RequestException, KeyError) as e:
        print(f"Error retrieving stock price: {e}")

def emit_stock_update(stock_symbol):
    price, change, changePercent, high, low = get_stock_price(stock_symbol)
    update_data = {
        'symbol': stock_symbol,
        'price': price,
        'change': change,
        'changePercent': changePercent,
        'high': high,
        'low': low
    }
    socketio.emit('stock_update', update_data, broadcast=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock_symbol = request.form['symbol']
        session['stock_symbol'] = stock_symbol
        return redirect(url_for('stock_price'))
    else:
        return render_template('index.html')

@app.route('/stock-price')
def stock_price():
    stock_symbol = session.get('stock_symbol')
    if not stock_symbol:
        return redirect(url_for('index'))

    price, change, changePercent, high, low = get_stock_price(stock_symbol)

    if price:
        cleaned_price = re.sub('[^0-9.]', '', price)
        cleaned_price = cleaned_price[:-2]

        spaced_price = ' '.join(cleaned_price)

        font = Figlet(font='colossal')
        ascii_price = font.renderText(spaced_price)

        return render_template('stock_price.html', ascii_price=ascii_price, stock_symbol=stock_symbol, change=change, changePercent=changePercent, high=high, low=low)
    else:
        return 'Error retrieving stock price'

if __name__ == '__main__':
    scheduler.start()
    socketio.run(app)
