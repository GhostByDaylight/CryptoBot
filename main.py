from datetime import * 
import numpy as np
import time
import pandas as pd
import requests
import json
import tkinter as tk
import matplotlib.pyplot as plt
import mplfinance as mpf
from coinbase.wallet.client import Client
from coinbase_advanced_trader import coinbase_client
from coinbase_advanced_trader.coinbase_client import Side

key = <Coinbase Public Key>
secret = <Coinbase Private key>


with open("coinbase_cloud_api_key.json") as file:
    data = json.load(file)
pubKey = json.dumps(data["publicKey"], ensure_ascii=False)
priKey = json.dumps(data["privateKey"], ensure_ascii=False)
client = Client(pubKey, priKey)
coinbase_client.set_credentials(key, secret)
price_data = {}




def get_current_price(symbol):
    url = f"https://api.coinbase.com/v2/prices/{symbol}-USD/spot"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        price = data["data"]["amount"]
        return float(price)
    else:
        print(
            f"Failed to retrieve price for {symbol}. Status code: {response.status_code}"
        )
        return None


def get_payment_methods():
    pms = client.get_payment_methods()
    print(pms)
    pass

def calculate_price_changes(prices):
    temp = [prices[i + 1] - prices[i] for i in range(len(prices) - 1)]
    return temp

def get_price_history_over_period(symbol, period='week'):
    url = f"https://api.coinbase.com/v2/prices/{symbol}-USD/historic?period={period}"
    response = requests.get(url)
    if response.status_code == 200:
        
        history = response.json()
        #print(history['data']['prices'])
        x_values = [entry["time"] for entry in reversed(history['data']['prices'])]
        
        y_values = [float(entry["price"]) for entry in history['data']['prices']]
        

        
        # Convert timestamp strings to datetime objects
        x_values = [datetime.fromisoformat(x[:-1]) for x in x_values]  # Remove the trailing 'Z' from the timestamp
        
        # Combine data into a pandas DataFrame
        candlestick_data = pd.DataFrame({
            'Date': x_values,
            'Open': y_values,
            'High': y_values,
            'Low': y_values,
            'Close': y_values
        })

        
        
        # Set the 'Date' column as the index
        candlestick_data.set_index('Date', inplace=True)
        
        # Create the candlestick graph
        #mpf.plot(candlestick_data, type='candle', style='charles', title=f'{symbol}-USD Candlestick Graph', ylabel='Price', mav=7)
        return x_values, y_values
    else:
            print("Query Failed")
    pass

def get_average_gain_loss(delta):
    gains = [i if i > 0 else 0 for i in delta]
    losses = [-i if i < 0 else 0 for i in delta]

    avg_gain = sum(gains) / len(gains)
    avg_loss = sum(losses) / len(losses)

    return avg_gain, avg_loss

def generate_signals(rsi_value):
    if rsi_value < 30:
        return "BUY"
    elif rsi_value > 70:
        return "SELL"
    else:
        return None


def buy_coin(symbol, amount, currency="USD", price=None):
    product_id = f"{symbol}-{currency}"

    if price:
        order_type = "limit_limit_gtc"
        order_configuration = {
            order_type: {
                "base_size": str(amount),
                "limit_price": str(price)
            }
        }
    else:
        order_type = "market_market_ioc"
        order_configuration = {
            order_type: {
                "quote_size": str(amount),
            }
        }

    client_order_id = coinbase_client.generate_client_order_id()
    side = Side.BUY.name

    response = coinbase_client.createOrder(
        client_order_id=client_order_id,
        product_id=product_id,
        side=side,
        order_configuration=order_configuration
    )

    return response


def sell_coin(symbol, amount, currency="USD", price=None):
    product_id = f"{symbol}-{currency}"

    if price:
        order_type = "limit_limit_gtc"
        order_configuration = {
            order_type: {
                "base_size": str(amount),
                "limit_price": str(price)
            }
        }
    else:
        order_type = "market_market_ioc"
        order_configuration = {
            order_type: {
                "quote_size": str(amount),
            }
        }

    client_order_id = coinbase_client.generate_client_order_id()
    side = Side.SELL.name

    response = coinbase_client.createOrder(
        client_order_id=client_order_id,
        product_id=product_id,
        side=side,
        order_configuration=order_configuration
    )

    return response


def trading_algorithm():
    # print("This is the trading_algorithm function")
    #Using the RSI (Relative Strength Index) stradegy
    arr = ["USDT", "ETH", "ATOM", "ADA"]

    for item in arr:
        data = get_current_price(item)
        if data is not None:
            if item not in price_data:
                price_data[item] = []
            price_data[item].append(data)
            print(f"The current price of {item} is ${data}")
        dates, prices = get_price_history_over_period(item, 'hour')
        #Calculate price changes
       
        deltas = calculate_price_changes(prices)
        #print(deltas)
        gain, loss = get_average_gain_loss(deltas)
        # Calculate RS
        if loss > 0:
            rs = gain / loss
        else:
            rs = float('inf')  # Avoid division by zero

        # Calculate RSI
        rsi = 100 - (100 / (1 + rs))
        
        print(f"Gain: {gain}")
        print(f"Loss: {loss}")
        print(f"RS: {rs}")
        print(f"RSI: {rsi}")
        

        signal = generate_signals(rsi)
        if signal == "BUY":
            print("Buy")
            response = buy_coin(item, 0.001, "USD", None)
            print(response)
        elif signal == "SELL":
            print("Sell")
            response = sell_coin(item, 0.001, "USD", None)
            print(response)
        else:
            print("Do Nothing")
        print("\n")




while True:
    trading_algorithm()
    time.sleep(5)

