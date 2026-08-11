# CurrencyBot

A Telegram bot that shows exchange rates from the Monobank public API. Browse over a hundred currencies against the hryvnia, subscribe to the ones you care about, and get updates pushed to you automatically.

## Features

- **Full currency list** — every currency Monobank quotes against UAH, loaded from the API rather than hardcoded, with a paginated inline keyboard
- **Live rates** — buy/sell where the bank quotes both, cross rate otherwise
- **Subscriptions** — subscribe to a currency with a single toggle button and receive periodic updates
- **Rate history** — the last recorded changes for any currency, shared across all users
- **Change-only storage** — a rate is written to history only when it actually moves, so the history reflects real movements rather than poll counts
- **Response caching** — API responses are cached in SQLite to stay well within Monobank's rate limit
- **Resilient background worker** — a failed delivery to one subscriber never stops the rest, and a failed cycle never kills the task
- **Clean UX** — messages are edited in place instead of piling up in the chat

## Tech Stack

- Python 3.12+
- [aiogram 3.x](https://docs.aiogram.dev/) — async Telegram Bot framework
- [httpx](https://www.python-httpx.org/) — async HTTP client
- SQLite — rate history, subscriptions, and the API response cache
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
│   ├── api.py                    # Monobank client, caching, rate lookup
│   ├── currencies.py             # ISO 4217 numeric code -> name mapping
│   ├── keyboards.py              # Inline keyboards and pagination
│   └── databases/
│       ├── rate_history.py       # Recorded rate changes
│       ├── subscriptions.py      # User subscriptions
│       └── data_history.py       # Cached raw API response
├── data/                         # SQLite databases (generated, git-ignored)
├── .env.example
├── .gitignore
├── LICENSE
└── requirements.txt
```

## How It Works

1. `/start` opens a paginated menu built from the currencies Monobank currently quotes against UAH
2. Tapping a currency shows its rate — served from cache when the cached response is still fresh
3. From the rate screen a single toggle button subscribes or unsubscribes
4. A background task polls the API on a fixed interval and pushes updates to every subscriber
5. Rates are appended to history only when the value changes
6. The History menu shows the last recorded changes for the selected currency

### Configuration

Two constants control the timing:

- `CACHE_TTL` in `bot/api.py` — how long a cached API response stays valid
- `UPDATE_INTERVAL` in `bot/bot.py` — how often subscribers receive updates

`CACHE_TTL` must stay shorter than `UPDATE_INTERVAL`, otherwise the background updater would serve stale data to subscribers.

### Notes

The currency list is loaded once at startup and reused for pagination. Monobank returns the most common currencies first and the rest alphabetically; the bot preserves that order rather than re-sorting.

## License

MIT

---

*This README was created with the help of Claude AI.*