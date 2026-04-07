import random
import time

class MockBroker:
    def __init__(self):
        self.symbols = ['AAPL', 'GOOGL', 'MSFT']
        self.current_prices = {symbol: random.uniform(100, 1000) for symbol in self.symbols}

    def get_candles(self, symbol, duration='1h', num_candles=10):
        candles = []
        for _ in range(num_candles):
            time_stamp = time.time() - random.randint(1, 3600)
            open_price = self.current_prices[symbol]
            close_price = open_price + random.uniform(-10, 10)
            high_price = max(open_price, close_price) + random.uniform(0, 5)
            low_price = min(open_price, close_price) - random.uniform(0, 5)
            candles.append({
                'timestamp': time_stamp,
                'open': open_price,
                'close': close_price,
                'high': high_price,
                'low': low_price,
                'volume': random.randint(1, 1000)
            })
        return candles

    def get_current_price(self, symbol):
        return self.current_prices[symbol] 

    def place_order(self, symbol, quantity, order_type='market'):
        if order_type == 'market':
            price = self.get_current_price(symbol)
            total_cost = price * quantity
            return {
                'symbol': symbol,
                'quantity': quantity,
                'price': price,
                'total_cost': total_cost,
                'status': 'filled'
            }
        else:
            return {'status': 'order type not supported'}

