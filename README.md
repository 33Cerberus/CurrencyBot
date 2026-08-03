# CurrencyBot

A simple Telegram bot that shows real-time currency exchange rates against UAH, using data from the Monobank public API. Built with inline keyboards for a clean, spam-free chat experience.

## Features

- Inline keyboard menu — select a currency (USD, EUR, PLN, GBP) with a single tap
- Real-time exchange rates (buy/sell or cross rate) fetched from Monobank's public API
- Rate history — every checked rate is saved per user, with a `/history` view of the last 5 checks per currency
- Automatic retry logic if the API is temporarily unavailable
- Clean UX — messages are edited in place instead of sending new ones

## Tech Stack

- Python 3.11+
- [aiogram 3.x](https://docs.aiogram.dev/) — async Telegram Bot framework
- [httpx](https://www.python-httpx.org/) — async HTTP client
- SQLite — local storage for rate history
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
├── bot.py          # Telegram bot logic and handlers
├── api.py          # Monobank API client and rate-lookup logic
├── db.py           # SQLite storage: init, save, and fetch rate history
├── keyboards.py     # Inline keyboard builders (main menu, history menu, back button)
├── .env.example    # Template for environment variables
├── .gitignore
└── requirements.txt
```

## How It Works

1. User sends `/start` → bot shows an inline keyboard with currency options
2. User taps a currency → bot fetches live rates from Monobank's API, edits the message to show the rate, and saves the result to the database
3. User can tap "History" from the main menu → select a currency → see the last 5 checked rates for that currency
4. Tapping "Back" returns to the previous menu

## Roadmap

- [x] Store rate history in SQLite for statistics
- [ ] Currency rate subscriptions with periodic updates
- [ ] Rate change charts

## License

MIT

---

*This README was created with the help of Claude AI.*
