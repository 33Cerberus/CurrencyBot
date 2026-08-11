import httpx
import asyncio
from databases.data_history import save_data, get_last_data_record
from datetime import datetime, timezone, timedelta
from currencies import currency_full_name
import json

CACHE_TTL = timedelta(minutes=3)

async def get_exchange_rates():
    max_retries = 5
    attempts = 0

    last_data_record = get_last_data_record()
    if last_data_record is not None:
        current_time = datetime.now(timezone.utc)
        last_time = datetime.fromisoformat(last_data_record["timestamp"])
        if (current_time - last_time) < CACHE_TTL:
            return json.loads(last_data_record["data"])

    async with httpx.AsyncClient() as client:
        while attempts < max_retries:
            response = await client.get("https://api.monobank.ua/bank/currency")
            data = response.json()
            if "errCode" in data:
                print(data["errText"])
                attempts += 1
                await asyncio.sleep(10)
                continue
            break
        else:
            print("Failed to get exchange data")
            return None

    save_data(json.dumps(data))
    return data

def get_exchange_rate(data, currency_code, base_code=980):
    for rate in data:
        if rate.get("currencyCodeA") == currency_code and rate.get("currencyCodeB") == base_code:
            return rate
    print("Failed to get exchange rate")
    return None

def get_available_currencies(data, base_code=980):
    currencies = []
    for rate in data:
        if rate.get("currencyCodeB") == base_code and currency_full_name(rate.get("currencyCodeA")) is not None:
            currencies.append(rate.get("currencyCodeA"))

    return currencies