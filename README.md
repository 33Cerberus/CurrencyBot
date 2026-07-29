# CurrencyBot

A simple Telegram bot that shows real-time currency exchange rates against UAH, using data from the Monobank public API. Built with inline keyboards for a clean, spam-free chat experience.

## Features

- Inline keyboard menu — select a currency (USD, EUR, PLN, GBP) with a single tap
- Real-time exchange rates (buy/sell or cross rate) fetched from Monobank's public API
- Automatic retry logic if the API is temporarily unavailable
- Clean UX — messages are edited in place instead of sending new ones

## Tech Stack

- Python 3.11+
- [aiogram 3.x](https://docs.aiogram.dev/) — async Telegram Bot framework
- [httpx](https://www.python-httpx.org/) — async HTTP client
- python-dotenv — environment variable management

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/33Cerberus/CurrencyBot.git
   cd CurrencyBot
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate       # Windows
   source .venv/bin/activate    # macOS/Linux
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:
   ```env
   BOT_TOKEN=your_telegram_bot_token_here
   ```

   Get a token from [@BotFather](https://t.me/BotFather) on Telegram.

4. Run the bot:
   ```bash
   python bot.py
   ```

## Project Structure

```
CurrencyBot/
├── bot.py          # Telegram bot logic, handlers, keyboards
├── api.py          # Monobank API client and rate-lookup logic
├── .env.example    # Template for environment variables
├── .gitignore
└── requirements.txt
```

## How It Works

1. User sends `/start` → bot shows an inline keyboard with currency options
2. User taps a currency → bot fetches live rates from Monobank's API
3. Bot edits the message in place to show the rate, with a "Back" button
4. Tapping "Back" returns to the main menu

## Roadmap

- [ ] Store rate history in SQLite for statistics
- [ ] Currency rate subscriptions with periodic updates
- [ ] Rate change charts

## License

MIT
