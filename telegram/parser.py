"""Signal Parser"""
import re

class SignalParser:
    def __init__(self):
        symbols_group = r'(NIFTY|BANKNIFTY|FINNIFTY|MIDCPNIFTY|SENSEX|BANKEX|CRUDEOIL|NATURALGAS)'
        self.buy_patterns = [
            r'BUY\s+(CE|PE|FUT)',
            rf'BUY\s+{symbols_group}',
            r'LONG\s+(\w+)',
            r'🎯\s*BUY',
            r'🟢\s*BUY',
            r'⚡\s*BUY',
            r'GO\s+LONG',
            r'SCALP\s+BUY',
        ]
        self.sell_patterns = [
            r'SELL\s+(CE|PE|FUT)',
            rf'SELL\s+{symbols_group}',
            r'SHORT\s+(\w+)',
            r'🔴\s*SELL',
            r'⚡\s*SELL',
            r'GO\s+SHORT',
            r'EXIT\s*:',
        ]

    def parse(self, text):
        if not text:
            return None
        
        text = text.upper()
        symbol = self._extract_symbol(text)
        strike = self._extract_strike(text)
        option_type = 'CE' if 'CE' in text else ('PE' if 'PE' in text else None)
        
        for pattern in self.buy_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return {
                    'direction': 'BUY',
                    'symbol': symbol,
                    'strike': strike,
                    'option_type': option_type,
                    'raw': text[:100]
                }
        
        for pattern in self.sell_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return {
                    'direction': 'SELL',
                    'symbol': symbol,
                    'strike': strike,
                    'option_type': option_type,
                    'raw': text[:100]
                }
        
        return None

    def _extract_symbol(self, text):
        symbols = ['MIDCPNIFTY', 'BANKNIFTY', 'FINNIFTY', 'NATURALGAS', 'CRUDEOIL', 'SENSEX', 'BANKEX', 'NIFTY']
        for sym in symbols:
            if re.search(rf'\b{sym}\b', text):
                return sym
        return None

    def _extract_strike(self, text):
        match = re.search(r'(\d{4,6})\s*(CE|PE)', text)
        if match:
            return int(match.group(1))
        return None
