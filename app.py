import requests
import finnhub
from flask import Flask, render_template, request, redirect, url_for
from pyfiglet import Figlet
import re

app = Flask(__name__)
finnhub_client = finnhub.Client(api_key="ciqmtm9r01qjff7crg10ciqmtm9r01qjff7crg1g")

def get_stock_price(symbol):
    try:
        response = finnhub_client.quote(symbol)
        stock_price = response['c']
        change = round(float(response['d']), 2)
        changePercent = round(float(response['dp']), 2)
        high = round(float(response['h']), 2)
        low = round(float(response['l']), 2)
        return stock_price, change, changePercent, high, low
    except Exception as e:
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
