from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from api import get_exchange_rate, get_exchange_rates, CURRENCY_CODES
from dotenv import load_dotenv
from db import init_db, save_rate, get_last_rates
from keyboards import main_menu_keyboard, back_keyboard, history_menu_keyboard
from datetime import datetime
import asyncio
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

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
    await callback.answer()
    currency_code = int(callback.data.split("_")[1])
    await callback.message.edit_text(f"Double checking {CURRENCY_CODES[currency_code]}...")

    data = await get_exchange_rates()
    if data is None:
        await show_main_menu(callback.message)
        return

    rate = get_exchange_rate(data, currency_code)
    if rate is None:
        await show_main_menu(callback.message)
        return

    if "rateCross" in rate:
        message = f"{CURRENCY_CODES[currency_code]} -> UAH Cross: {rate.get('rateCross')}"
        save_rate(callback.from_user.id, currency_code, -1, -1, rate.get('rateCross'))
    else:
        message = f"{CURRENCY_CODES[currency_code]} -> UAH Buy: {rate.get('rateBuy')} Sell: {rate.get('rateSell')}"
        save_rate(callback.from_user.id, currency_code, rate.get('rateBuy'), rate.get('rateSell'), -1)

    await callback.message.edit_text(message, reply_markup=back_keyboard("main"))

@dp.callback_query(F.data.startswith("history_"))
async def show_history(callback: CallbackQuery):
    await callback.answer()
    currency_code = int(callback.data.split("_")[1])
    await callback.message.edit_text(f"Double checking {CURRENCY_CODES[currency_code]}...")

    history = get_last_rates(callback.from_user.id, currency_code, 5)
    if len(history) == 0:
        await callback.message.edit_text(f"No history on {CURRENCY_CODES[currency_code]}", reply_markup=back_keyboard("history"))
        return

    message = f"{CURRENCY_CODES[currency_code]} -> UAH history"
    for rate in history:
        date_time = datetime.fromisoformat(rate['timestamp']).strftime("%d.%m.%Y %H:%M")
        if rate['rate_cross'] == -1:
            message += f"\n{date_time} Buy: {rate['rate_buy']} Sell: {rate['rate_sell']}"
        else:
            message += f"\n{date_time} Cross: {rate['rate_cross']}"

    await callback.message.edit_text(message, reply_markup=back_keyboard("history"))

async def show_main_menu(message: Message):
    await message.edit_text("Select currency tp check it's rate", reply_markup=main_menu_keyboard())

async def show_history_menu(message: Message):
    await message.edit_text("Select currency to check it's history", reply_markup=history_menu_keyboard())

async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass