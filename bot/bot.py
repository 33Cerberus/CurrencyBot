from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from api import get_exchange_rate, get_exchange_rates, get_available_currencies
from dotenv import load_dotenv
from databases.data_history import init_db as init_data_history
from databases.rate_history import init_db as init_rate_history, save_rate, get_last_rates
from databases.subscriptions import init_db as init_subscriptions, add_subscription, remove_subscription, has_subscription, get_all_subscriptions
from keyboards import main_menu_keyboard, back_keyboard, history_menu_keyboard, show_rate_keyboard
from datetime import datetime
import asyncio
from currencies import currency_name
import os
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
UPDATE_INTERVAL = 300
AVAILABLE_CURRENCIES = []

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    answer = await message.answer("Loading currencies...")
    await show_main_menu(answer)

@dp.callback_query(F.data.startswith("open_"))
async def open_menu (callback: CallbackQuery):
    menu = callback.data.split("_")[1]
    match menu:
        case "main":
            await show_main_menu(callback.message)
        case "history":
            await show_history_menu(callback.message)
    await callback.answer()

@dp.callback_query(F.data.startswith("currency_"))
async def show_rate(callback: CallbackQuery):
    currency_code = int(callback.data.split("_")[1])
    message = callback.message
    user_id = callback.from_user.id
    await callback.answer()

    await message.edit_text(f"Double checking {currency_name(currency_code)}...")

    data = await get_exchange_rates()
    if data is None:
        await show_main_menu(message)
        return

    rate = get_exchange_rate(data, currency_code)
    if rate is None:
        await show_main_menu(message)
        return

    message_text = format_and_save_rate(rate, currency_code)
    await message.edit_text(message_text, reply_markup=show_rate_keyboard(currency_code, has_subscription(user_id, currency_code)))

@dp.callback_query(F.data.startswith("subscribe_"))
async def subscribe(callback: CallbackQuery):
    currency_code = int(callback.data.split("_")[1])
    subscribed = has_subscription(callback.from_user.id, currency_code)
    if not subscribed:
        add_subscription(callback.from_user.id, currency_code)

    await callback.message.edit_text(callback.message.text, reply_markup=show_rate_keyboard(currency_code, True))
    await callback.answer()

@dp.callback_query(F.data.startswith("unsubscribe_"))
async def unsubscribe(callback: CallbackQuery):
    currency_code = int(callback.data.split("_")[1])
    subscribed = has_subscription(callback.from_user.id, currency_code)
    if subscribed:
        remove_subscription(callback.from_user.id, currency_code)

    await callback.message.edit_text(callback.message.text, reply_markup=show_rate_keyboard(currency_code, False))
    await callback.answer()

@dp.callback_query(F.data.startswith("history_"))
async def show_history(callback: CallbackQuery):
    await callback.answer()
    currency_code = int(callback.data.split("_")[1])
    await callback.message.edit_text(f"Double checking {currency_name(currency_code)}...")

    history = get_last_rates(currency_code, 5)
    if len(history) == 0:
        await callback.message.edit_text(f"No history on {currency_name(currency_code)}", reply_markup=back_keyboard("history"))
        return

    message = f"{currency_name(currency_code)} -> UAH history"
    for rate in history:
        date_time = datetime.fromisoformat(rate['timestamp']).strftime("%d.%m.%Y %H:%M")
        if rate['rate_cross'] is None:
            message += f"\n{date_time} Buy: {rate['rate_buy']} Sell: {rate['rate_sell']}"
        else:
            message += f"\n{date_time} Cross: {rate['rate_cross']}"

    await callback.message.edit_text(message, reply_markup=back_keyboard("history"))

@dp.callback_query(F.data.startswith("page_"))
async def change_page(callback: CallbackQuery):
    _, menu_prefix, page = callback.data.split("_")
    match menu_prefix:
        case "currency":
            await show_main_menu(callback.message, int(page))
        case "history":
            await show_history_menu(callback.message, int(page))
    await callback.answer()

@dp.callback_query(F.data == "noop")
async def noop(callback: CallbackQuery):
    await callback.answer()

async def show_main_menu(message: Message, page=0):
    currencies = AVAILABLE_CURRENCIES or await load_currencies()
    if not currencies:
        await message.edit_text("Currency list is unavailable, try again later")
        return
    await message.edit_text(
        "Select currency to check its rate",
        reply_markup=main_menu_keyboard(currencies, page),
    )


async def show_history_menu(message: Message, page=0):
    currencies = AVAILABLE_CURRENCIES or await load_currencies()
    if not currencies:
        await message.edit_text("Currency list is unavailable, try again later")
        return
    await message.edit_text(
        "Select currency to check its history",
        reply_markup=history_menu_keyboard(currencies, page),
    )

async def rate_updater():
    while True:
        try:
            await asyncio.sleep(UPDATE_INTERVAL)
            data = await get_exchange_rates()
            if data is None:
                continue
            for row in get_all_subscriptions():
                try:
                    await send_update(row["user_id"], row["currency_code"], data)
                except Exception as error:
                    print(f"Failed to notify {row['user_id']}: {error}")
        except Exception as error:
            print(f"Rate updater cycle failed: {error}")

async def send_update(user_id, currency_code, data):
    message = await bot.send_message(chat_id=user_id,text=f"Double checking {currency_name(currency_code)}...")

    rate = get_exchange_rate(data, currency_code)
    if rate is None:
        await message.edit_text(f"No data on {currency_name(currency_code)}")
        return

    message_text = format_and_save_rate(rate, currency_code)
    await message.edit_text(message_text)

def format_and_save_rate(rate, currency_code):
    last_rates = get_last_rates(currency_code, 1)
    if "rateCross" in rate:
        message_text = f"{currency_name(currency_code)} -> UAH Cross: {rate.get('rateCross')}"
        if not last_rates or rate.get('rateCross') != last_rates[0]['rate_cross']:
            save_rate(currency_code, None, None, rate.get('rateCross'))
    else:
        message_text = f"{currency_name(currency_code)} -> UAH Buy: {rate.get('rateBuy')} Sell: {rate.get('rateSell')}"
        if not last_rates or rate.get('rateBuy') != last_rates[0]['rate_buy'] or rate.get('rateSell') != last_rates[0]['rate_sell']:
            save_rate(currency_code, rate.get('rateBuy'), rate.get('rateSell'), None)

    return message_text

async def load_currencies():
    global AVAILABLE_CURRENCIES
    data = await get_exchange_rates()
    if data is not None:
        AVAILABLE_CURRENCIES = get_available_currencies(data)
    return AVAILABLE_CURRENCIES

async def main():
    init_data_history()
    init_rate_history()
    init_subscriptions()
    await load_currencies()
    task = asyncio.create_task(rate_updater())
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass