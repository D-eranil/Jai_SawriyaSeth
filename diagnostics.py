"""
Basic runtime diagnostics before launching desktop/headless modes.
Checks config, critical imports, and required credentials presence.
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config" / "config.json"


def _ok(msg):
    print(f"✅ {msg}")


def _warn(msg):
    print(f"⚠️ {msg}")


def _fail(msg):
    print(f"❌ {msg}")


def load_config():
    if not CONFIG_PATH.exists():
        _fail(f"Missing config file: {CONFIG_PATH}")
        _warn("Copy config/config.example.json -> config/config.json first.")
        return None
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        _fail(f"Invalid config.json: {e}")
        return None


def check_imports():
    modules = [
        "ui.desktop",
        "core.engine",
        "brokers.kotak_neo",
        "telegram.reader",
        "telegram.bot",
        "telegram.parser",
    ]
    failed = False
    for mod in modules:
        try:
            __import__(mod)
            _ok(f"Import: {mod}")
        except Exception as e:
            failed = True
            _fail(f"Import failed ({mod}): {e}")
    return not failed


def check_credentials(cfg):
    ok = True
    kotak = (cfg or {}).get("kotak_neo", {})
    env_map = {
        "access_token": "KOTAK_ACCESS_TOKEN",
        "client_code": "KOTAK_CLIENT_CODE",
        "mobile": "KOTAK_MOBILE",
        "mpin": "KOTAK_MPIN",
        "totp_secret": "KOTAK_TOTP_SECRET",
    }
    missing = []
    for k, env_key in env_map.items():
        if not str(kotak.get(k, "")).strip() and not str(os.getenv(env_key, "")).strip():
            missing.append(f"{k} / {env_key}")
    if missing:
        ok = False
        _fail("Kotak credentials missing: " + ", ".join(missing))
    else:
        _ok("Kotak credentials available (config/env)")

    tg = (cfg or {}).get("telegram", {})
    if not str(tg.get("api_id", "")).strip() or not str(tg.get("api_hash", "")).strip():
        _warn("Telegram reader API credentials missing (api_id/api_hash). Reader won't connect.")
    else:
        _ok("Telegram reader credentials present")

    alerts = (cfg or {}).get("telegram_alerts", {})
    if not str(alerts.get("bot_token", "")).strip():
        _warn("Telegram bot token missing (alerts may be disabled).")
    else:
        _ok("Telegram bot token present")

    return ok


def main():
    print("=== JSS Diagnostics ===")
    cfg = load_config()
    if cfg is None:
        sys.exit(1)

    imports_ok = check_imports()
    creds_ok = check_credentials(cfg)
    if imports_ok and creds_ok:
        print("✅ Diagnostics passed")
        sys.exit(0)

    print("❌ Diagnostics failed. Fix issues above before running Start.bat/Start_Hidden.bat")
    sys.exit(2)


if __name__ == "__main__":
    main()
