import httpx
import asyncio

CURRENCY_CODES = {
    980: "UAH",
    840: "USD",
    978: "EUR",
    826: "GBP",
    985: "PLN",
}

async def get_exchange_rates():
    max_retries = 5
    attempts = 0

    async with httpx.AsyncClient() as client:
        while attempts < max_retries:
            response = await client.get("https://api.monobank.ua/bank/currency")
            data = response.json()

            if "errCode" in data:
                print(data["errText"], ", trying again")
                attempts += 1
                await asyncio.sleep(10)
                continue
            break
        else:
            print("Failed to get exchange data")
            return None

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