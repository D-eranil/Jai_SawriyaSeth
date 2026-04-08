# Jss Wealthtech - AI Trading System
## ॥ जय श्री सांवरीया सेठ ि॥

### Quick Start
1. Run Install.bat (first time only)
2. Copy `config/config.example.json` to `config/config.json` and fill your credentials
3. Run Start.bat
4. Complete first Telegram OTP login (if Telegram 2FA is enabled, provide password in config or popup; session will be reused)

> Install script now uses `requirements.txt` to keep dependency versions compatible.

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
