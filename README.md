# Jss Wealthtech - AI Trading System
## ॥ जय श्री सांवरीया सेठ ि॥

### Quick Start
1. Run Install.bat (first time only)
2. Copy `config/config.example.json` to `config/config.json` and fill your credentials
3. Run Start.bat
4. Complete first Telegram OTP login (if Telegram 2FA is enabled, provide password in config or popup; session will be reused)

> Install script now uses `requirements.txt` to keep dependency versions compatible.
> Dashboard now shows Telegram group read status as `TG Read X/Y`.

### Kotak Credentials
- Preferred: set values in `config/config.json` under `kotak_neo`
- Optional: use environment variables as fallback:
  - `KOTAK_ACCESS_TOKEN`
  - `KOTAK_CLIENT_CODE`
  - `KOTAK_MOBILE`
  - `KOTAK_MPIN`
  - `KOTAK_TOTP_SECRET`

### Features
- Kotak Neo Live Connection
- 8 Symbols Live Rates
- Option Chain Analysis
- Multi-Strategy Trading
- Paper Mode Only
- Telegram Alerts
- Excel Reports

### Capital
- Initial capital is controlled by `trading.initial_capital` in `config/config.json`.
- UI no longer forces it to ₹1000 if you set your own value.

### Background Mode (No Desktop UI)
- Run `Start_Hidden.bat` to start engine in background via `pythonw`.
- It should appear in Task Manager (`pythonw.exe`) without a visible CMD window.
- To monitor backend live logs, run `View_Backend_Logs.bat`.
- To check running status + last logs quickly, run `Backend_Status.bat`.

### Telegram Trade Alerts
- Entry and Exit trade messages are sent through configured Telegram bot (`telegram_alerts.bot_token` + `my_chat_id/chat_id`).
- On successful bot connection, a startup confirmation message is also sent.

### Images Required
Put these images in images/ folder:
- ganesh.png (TOP CENTER)
- swastik.png (LEFT)
- shubh.png (RIGHT)
- om.png, laxmi_kuber.png, bell.png, kalash.png
- mor_pankh.png, golden_fish.png, hanging_deepak.png
- shyam_baba.png, yantra.png
- ai_robot.jpg, ai_robot_analyst.png
- market_bull.png, market_bear.png
