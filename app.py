import requests
import finnhub
from flask import Flask, render_template, request, redirect, url_for, session
from pyfiglet import Figlet
import re
from apscheduler.schedulers.background import BackgroundScheduler
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ciqmtm9r01qjff7crg10ciqmtm9r01qjff7crg1g'
socketio = SocketIO(app)
scheduler = BackgroundScheduler()
scheduler.start()

def get_stock_price(symbol):
    finnhub_client = finnhub.Client(api_key="your_api_key")
    res = finnhub_client.quote(symbol)
    if res['c']:
        stock_price = res['c']
        change = round(float(res['d']), 2)
        changePercent = round(float(res['dp']), 2)
        high = round(float(res['h']), 2)
        low = round(float(res['l']), 2)
        return stock_price, change, changePercent, high, low
    else:
        return None, None, None, None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock_symbol = request.form['symbol']
        session['stock_symbol'] = stock_symbol  # Store symbol in session
        return redirect(url_for('stock_price', symbol=stock_symbol))
    else:
        return render_template('index.html')

@app.route('/stock-price/<symbol>')
def stock_price(symbol):
    price, change, changePercent, high, low = get_stock_price(symbol)

    if price:
        cleaned_price = re.sub('[^0-9.]', '', price)
        cleaned_price = cleaned_price[:-2]
        
        spaced_price = ' '.join(cleaned_price)
        
        font = Figlet(font='colossal')
        ascii_price = font.renderText(spaced_price)

        return render_template('stock_price.html', ascii_price=ascii_price, stock_symbol=symbol, change=change, changePercent=changePercent, high=high, low=low)
    else:
        return 'Error retrieving stock price'

@socketio.on('connect')
def handle_connect():
    print('Connected to server')

@socketio.on('disconnect')
def handle_disconnect():
    print('Disconnected from server')

@scheduler.scheduled_job('interval', seconds=5)
def emit_stock_update():
    stock_symbol = session.get('stock_symbol')
    if stock_symbol:
        price, change, changePercent, high, low = get_stock_price(stock_symbol)

        if price:
            data = {
                'symbol': stock_symbol,
                'price': price,
                'change': change,
                'changePercent': changePercent,
                'high': high,
                'low': low
            }
            emit('stock_update', data, broadcast=True)
        else:
            emit('stock_update_error')

if __name__ == '__main__':
    socketio.run(app)
