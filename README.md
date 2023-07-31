# Crypto Trading Bot

This project contains a simple automated trading bot for cryptocurrency trading on the Coinbase platform. It utilizes the Relative Strength Index (RSI) strategy to make buy or sell decisions.

## Dependencies

- `datetime`
- `numpy`
- `time`
- `pandas`
- `requests`
- `json`
- `tkinter`
- `matplotlib`
- `mplfinance`
- `coinbase.wallet.client`
- `coinbase_advanced_trader`


# Functions
### get_current_price(symbol)<br />
Fetches the current price of the given cryptocurrency symbol.

### get_payment_methods()<br />
Lists the available payment methods on your Coinbase account.

### calculate_price_changes(prices)<br />
Calculates the price changes between consecutive elements in a list of prices.

### get_price_history_over_period(symbol, period='week')<br />
Fetches the price history of the given cryptocurrency symbol over the specified period.

### get_average_gain_loss(delta)<br />
Calculates the average gain and loss from a list of price changes.

### generate_signals(rsi_value)<br />
Generates a buy or sell signal based on the RSI value.

### buy_coin(symbol, amount, currency="USD", price=None)<br />
Places a buy order for the given cryptocurrency symbol.

### sell_coin(symbol, amount, currency="USD", price=None)<br />
Places a sell order for the given cryptocurrency symbol.

### trading_algorithm()<br />
The main trading algorithm that uses the RSI strategy to make trading decisions.

## Running the Bot

To run the bot, simply execute the script. It will continuously fetch the latest prices, calculate the RSI, and make trading decisions accordingly.

```bash
python main.py
