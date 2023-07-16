import requests
from flask import Flask, render_template, request, redirect, url_for
from pyfiglet import Figlet
import re

app = Flask(__name__)

def get_stock_price(symbol):
    api_key = 'T0R7REUTTRQP4F4V'  # Replace with your Alpha Vantage API key
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'

    try:
        response = requests.get(url)
        data = response.json()
        print(data)
        stock_price = data['Global Quote']['05. price']
        return stock_price
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
    price = get_stock_price(symbol)

    if price:
        cleaned_price = re.sub('[^0-9.]', '', price)
        cleaned_price = cleaned_price[:-2]
        
        spaced_price = ' '.join(cleaned_price)
        
        font = Figlet(font='colossal')
        ascii_price = font.renderText(spaced_price)

        return render_template('stock_price.html', ascii_price=ascii_price, stock_symbol=symbol)
    else:
        return 'Error retrieving stock price'

if __name__ == '__main__':
    app.run()
