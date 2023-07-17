import requests
import finnhub
from flask import Flask, render_template, request, redirect, url_for
from pyfiglet import Figlet
import re

app = Flask(__name__)

def get_stock_price(symbol):
    api_key = 'ciqmtm9r01qjff7crg10ciqmtm9r01qjff7crg1g'  # Replace with your Finnhub API key
    url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}'

    try:
        response = requests.get(url)
        data = response.json()
        print(data)
        stock_data = data
        stock_price = stock_data['c']
        change = round(float(stock_data['d']), 2)
        changePercent = round(float(stock_data['dp']), 2)
        high = round(float(stock_data['h']), 2)
        low = round(float(stock_data['l']), 2)
        return stock_price, change, changePercent, high, low
    except (requests.RequestException, KeyError) as e:
        print(f"Error retrieving stock price: {e}")

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
        font = Figlet(font='colossal')
        ascii_price = font.renderText(str(price))

        return render_template('stock_price.html', ascii_price=ascii_price, stock_symbol=symbol, change=change, changePercent=changePercent, high=high, low=low)
    else:
        return 'Error retrieving stock price'

if __name__ == '__main__':
    app.run()
