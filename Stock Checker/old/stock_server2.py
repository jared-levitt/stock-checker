import requests
from art import *
from flask import Flask, render_template
import re

app = Flask(__name__)

def get_stock_price(symbol):
    api_key = 'T0R7REUTTRQP4F4V'  # Replace with your Alpha Vantage API key
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'

    try:
        response = requests.get(url)
        data = response.json()
        stock_price = data['Global Quote']['05. price']
        print(f"Stock Price: {stock_price}")
        return stock_price
    except (requests.RequestException, KeyError) as e:
        print(f"Error retrieving stock price: {e}")

@app.route('/stock-price')
def stock_price():
    stock_symbol = 'AAPL'  # Replace with the stock symbol you want to check
    price = get_stock_price(stock_symbol)

    if price:
        # Remove non-digit characters from the price
        cleaned_price = re.sub('[^0-9.]', '', price)

        # Generate ASCII art representation of the cleaned price
        ascii_price = text2art(cleaned_price)

        return render_template('stock_price.html', ascii_price=ascii_price)
    else:
        return 'Error retrieving stock price'

if __name__ == '__main__':
    app.run()
