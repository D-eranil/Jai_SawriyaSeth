"""
Run JSS Wealthtech engine without opening the desktop dashboard.
Useful for background execution (Task Manager process only).
"""
import json
import os
import time
from datetime import datetime
from zoneinfo import ZoneInfo


def load_config():
    cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "config.json")
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    cfg.setdefault("trading", {})
    cfg["trading"].setdefault("paper_mode", True)
    cfg["trading"].setdefault("initial_capital", 1000)
    return cfg


def log(msg):
    ts = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def main():
    from brokers.kotak_neo import KotakNeo
    from core.capital import CapitalManager
    from core.engine import TradingEngine
    from core.indicators import Indicators
    from core.option_chain import OptionChain
    from core.risk import RiskManager
    from strategies import load_all_strategies
    from telegram.bot import TelegramBot
    from telegram.parser import SignalParser
    from telegram.reader import TelegramReader

    cfg = load_config()
    log("Starting headless mode...")

    kotak = KotakNeo(cfg.get("kotak_neo", {}))
    tg_reader = TelegramReader(cfg)
    tg_bot = TelegramBot(cfg)

    kotak.set_log_callback(log)
    tg_reader.set_log_callback(log)

    if not kotak.connect():
        log(f"Kotak connect failed: {kotak.status_msg}")
    else:
        log("Kotak connected")

    tg_bot.connect()
    if not tg_reader.connect():
        log(f"Telegram reader connect failed: {tg_reader.status_msg}")
    else:
        log("Telegram reader connected")

    initial_capital = float(cfg.get("trading", {}).get("initial_capital", 1000) or 1000)
    engine = TradingEngine(
        config=cfg,
        kotak=kotak,
        option_chain=OptionChain(),
        indicators=Indicators(),
        capital=CapitalManager(initial_capital=initial_capital),
        risk=RiskManager(cfg),
        telegram_bot=tg_bot,
        telegram_reader=tg_reader,
        signal_parser=SignalParser(),
        strategies=load_all_strategies(),
    )
    engine.on_log = log
    engine.start()
    log(f"Engine running in {'PAPER' if cfg.get('trading', {}).get('paper_mode', True) else 'LIVE'} mode")

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        log("Stopping...")
        engine.stop()


if __name__ == "__main__":
    main()
