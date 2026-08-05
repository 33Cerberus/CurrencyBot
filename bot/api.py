import httpx
import asyncio
from databases.data_history import save_data, get_last_data_record
from datetime import datetime, timezone, timedelta
import json

CURRENCY_CODES = {
    980: "UAH",
    840: "USD",
    978: "EUR",
    826: "GBP",
    985: "PLN",
}

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

def get_exchange_rate(data, currency_code):
    for rate in data:
        if rate.get("currencyCodeA") == currency_code:
            return rate
    print("Failed to get exchange rate")
    return None

async def main():
    data_task = asyncio.create_task(get_exchange_rates())

    while True:
        try:
            currencyCode = int(input("Enter currency code: "))
            if currencyCode in CURRENCY_CODES and CURRENCY_CODES[currencyCode] != "UAH":
                break
            print("Invalid currency code")
        except ValueError:
            print("Invalid currency code")

    data = await data_task
    if data is None:
        return
    rate = get_exchange_rate(data, currencyCode)
    if rate is None:
        return

    if "rateCross" in rate:
        print(CURRENCY_CODES[currencyCode], "-> UAH", '\n', "Cross:", rate.get("rateCross"))
    else:
        print(CURRENCY_CODES[currencyCode], "-> UAH", '\n', "Buy:", rate.get("rateBuy"), '\n', "Sell:", rate.get("rateSell"))

if __name__ == "__main__":
    asyncio.run(main())