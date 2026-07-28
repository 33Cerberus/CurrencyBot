from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from api import get_exchange_rate, get_exchange_rates, CURRENCY_CODES
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def main_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="USD", callback_data="currency_840"),
            InlineKeyboardButton(text="EUR", callback_data="currency_978"),
        ],
        [
            InlineKeyboardButton(text="PLN", callback_data="currency_985"),
            InlineKeyboardButton(text="GBP", callback_data="currency_826"),
        ],
    ])

def back_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Back", callback_data="back")]
    ])

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Select currency", reply_markup=main_menu_keyboard())

@dp.callback_query(F.data.startswith("currency_"))
async def show_rate(callback: CallbackQuery):
    await callback.answer()
    currency_code = int(callback.data.split("_")[1])
    await callback.message.edit_text(f"Double checking {CURRENCY_CODES[currency_code]}...")
    data = await get_exchange_rates()
    if data is None:
        await callback.message.edit_text("Select currency", reply_markup=main_menu_keyboard())
        return

    rate = get_exchange_rate(data, currency_code)
    if rate is None:
        await callback.message.edit_text("Select currency", reply_markup=main_menu_keyboard())
        return

    if "rateCross" in rate:
        message = f"{CURRENCY_CODES[currency_code]} -> UAH Cross: {rate.get('rateCross')}"
    else:
        message = f"{CURRENCY_CODES[currency_code]} -> UAH Buy: {rate.get('rateBuy')} Sell: {rate.get('rateSell')}"

    await callback.message.edit_text(message, reply_markup=back_keyboard())

@dp.callback_query(F.data == "back")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.edit_text("Select currency", reply_markup=main_menu_keyboard())
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())