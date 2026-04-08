"""
Run JSS Wealthtech engine without opening the desktop dashboard.
Useful for background execution (Task Manager process only).
"""
import json
import os
import time
from datetime import datetime
from zoneinfo import ZoneInfo

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "data", "logs")
LOG_FILE = os.path.join(LOG_DIR, "headless.log")
PID_FILE = os.path.join(LOG_DIR, "headless.pid")


def load_config():
    cfg_path = os.path.join(BASE_DIR, "config", "config.json")
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    cfg.setdefault("trading", {})
    cfg["trading"].setdefault("paper_mode", True)
    cfg["trading"].setdefault("initial_capital", 1000)
    return cfg


def log(msg):
    os.makedirs(LOG_DIR, exist_ok=True)
    ts = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass
    print(line, flush=True)


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
    cfg.setdefault("telegram", {})
    cfg["telegram"].setdefault("session_name", "jss_console_session_headless")
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(PID_FILE, "w", encoding="utf-8") as f:
        f.write(str(os.getpid()))
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
    last_poll_seen = {"val": ""}

    def on_update(status):
        poll = str(status.get("tg_last_poll") or "")
        if not poll or poll == last_poll_seen["val"]:
            return
        last_poll_seen["val"] = poll
        last_rows = status.get("tg_last_messages", {}) or {}
        if not last_rows:
            log(f"TG poll {poll}: no group messages")
            return
        for grp, row in last_rows.items():
            txt = (row.get("text", "") or "").strip().replace("\n", " ")
            if len(txt) > 100:
                txt = txt[:100] + "..."
            log(f"TG poll {poll} | {grp} | {row.get('date', '-')}: {txt or 'NO_MESSAGE'}")

    engine.on_update = on_update
    engine.start()
    log(f"Engine running in {'PAPER' if cfg.get('trading', {}).get('paper_mode', True) else 'LIVE'} mode")

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        log("Stopping...")
        engine.stop()
    finally:
        try:
            if os.path.exists(PID_FILE):
                os.remove(PID_FILE)
        except Exception:
            pass


if __name__ == "__main__":
    main()
