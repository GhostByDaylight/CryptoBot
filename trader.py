
from coinbase_advanced_trader import coinbase_client
from coinbase_advanced_trader.coinbase_client import Side
import json

# Set your API key and secret
API_KEY = "Public"
API_SECRET = "Secret"

# Set the credentials
coinbase_client.set_credentials(API_KEY, API_SECRET)

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


amount_to_buy = 0.001
currency = "USD"
coinToBuy = "BTC"

# You can specify a price for a limit order, or leave it as None for a market order
price = 10000

result = coinbase_client.listProducts()
with open('output.json', 'w') as f:
    json.dump(result, f, indent=4)
#response = sell_coin("BTC", 0.00000032, currency, price)
#print("Sell order response: ", response)

#response = buy_coin(coinToBuy, amount_to_buy, currency, price)
#print("Buy order response:", response)