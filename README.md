# CurrencyBot

A Telegram bot that shows real-time currency exchange rates against UAH, using data from the Monobank public API. Built with inline keyboards for a clean, spam-free chat experience.

## Features

- Inline keyboard menu — select a currency (USD, EUR, PLN, GBP) with a single tap
- Real-time exchange rates (buy/sell or cross rate) fetched from Monobank's public API
- Rate subscriptions — subscribe to a currency and receive periodic updates automatically
- Rate history — every rate change is stored, with a menu to view the last 5 recorded changes per currency
- Response caching — API responses are cached to stay within Monobank's rate limit
- Automatic retry logic if the API is temporarily unavailable
- Resilient background worker — a failed delivery to one subscriber never stops the rest
- Clean UX — messages are edited in place instead of sending new ones

## Tech Stack

- Python 3.12+
- [aiogram 3.x](https://docs.aiogram.dev/) — async Telegram Bot framework
- [httpx](https://www.python-httpx.org/) — async HTTP client
- SQLite — local storage for rate history, subscriptions, and the API cache
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
   python bot/bot.py
   ```

   The `data/` directory and all SQLite databases are created automatically on first run.

## Project Structure

```
CurrencyBot/
├── bot/
│   ├── bot.py                    # Handlers, background updater, entry point
│   ├── api.py                    # Monobank API client, caching, rate lookup
│   ├── keyboards.py              # Inline keyboard builders
│   └── databases/
│       ├── rate_history.py       # Stored rate changes
│       ├── subscriptions.py      # User subscriptions
│       └── data_history.py       # Cached raw API response
├── data/                         # SQLite databases (generated, git-ignored)
├── .env.example                  # Template for environment variables
├── .gitignore
├── LICENSE
└── requirements.txt
```

## How It Works

1. User sends `/start` → bot shows an inline keyboard with currency options
2. User taps a currency → bot fetches the current rate (from cache if it is fresh enough) and edits the message in place
3. From the rate screen the user can subscribe or unsubscribe with a single toggle button
4. A background task polls the API on a fixed interval and pushes updates to every subscriber
5. Rates are written to the history table only when the value actually changes, so the history reflects real movements rather than poll counts
6. The History menu shows the last 5 recorded changes for the selected currency

### Configuration

Two constants control the timing:

- `CACHE_TTL` in `api.py` — how long a cached API response stays valid
- `UPDATE_INTERVAL` in `bot.py` — how often subscribers receive updates

`CACHE_TTL` must stay shorter than `UPDATE_INTERVAL`, otherwise the background updater would serve stale data to subscribers.

## Roadmap

- [x] Store rate history in SQLite for statistics
- [x] Currency rate subscriptions with periodic updates
- [ ] Rate change charts

## License

MIT

---

*This README was created with the help of Claude AI.*