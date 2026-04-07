class IndicatorCalculator:
    def __init__(self, prices):
        self.prices = prices

    def calculate_rsi(self, period=14):
        gains = [0] * len(self.prices)
        losses = [0] * len(self.prices)

        for i in range(1, len(self.prices)):
            difference = self.prices[i] - self.prices[i - 1]
            if difference > 0:
                gains[i] = difference
            else:
                losses[i] = -difference

        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        return 100 - (100 / (1 + rs))

    def calculate_ema(self, period=20):
        if len(self.prices) < period:
            return None
        k = 2 / (period + 1)
        ema = [sum(self.prices[:period]) / period]
        for price in self.prices[period:]:
            ema.append((price * k) + (ema[-1] * (1 - k)))
        return ema[-1]

class TradeSignal:
    def __init__(self, prices):
        self.indicator_calculator = IndicatorCalculator(prices)

    def generate_trade_signals(self):
        rsi = self.indicator_calculator.calculate_rsi()
        ema = self.indicator_calculator.calculate_ema()

        signals = []

        # Example conditions for CALL and PUT
        if rsi < 30 and ema is not None:
            signals.append("CALL")
        elif rsi > 70 and ema is not None:
            signals.append("PUT")

        return signals

    def analyze_candle_patterns(self, candle_data):
        # Logic for candle pattern analysis would go here
        pass

# Example usage:
# prices = [100, 102, 101, 103, 102, 104, 105, 103, 102, 101]
# trade_signal_generator = TradeSignal(prices)
# signals = trade_signal_generator.generate_trade_signals()
# print(signals)  # Output: ['CALL'] or ['PUT'] based on conditions