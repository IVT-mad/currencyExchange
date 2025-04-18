# 💱 ExchangeBot

    Telegram bot that provides real-time currency exchange rates via API and Central Bank web scraping.

# 🚀 Features

    •	Get exchange rates using currencylayer.com
    •	Scrape rates from the Central Bank of Russia
    •	Sort by rate, currency code, or currency name
    •	User-friendly interaction with inline keyboards

# 📦 Deployment (Railway)

    1.	Deploy this repository on Railway via GitHub integration
    2.	Set the required environment variable:
    BOT_TOKEN=your-telegram-bot-token
    3.	Railway will automatically detect and start the project using:
    python3 src/BotMain.py

# 🧪 Local Development

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    BOT_TOKEN=your-token python3 src/BotMain.py

# 🗂 Project Structure

    exchangeBot/
    ├── src/
    │   ├── BotMain.py         — Telegram bot core logic
    │   ├── APIRate.py         — API-based exchange rate logic
    │   └── WEBScrappa.py      — Web scraping from Central Bank
    ├── .env.example           — Example environment config
    ├── requirements.txt       — Python dependencies
    ├── Procfile               — Railway process definition
    ├── runtime.txt            — Python version specification
