from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_keyboard():
    keyboard = currencies_keyboard("currency")
    keyboard.inline_keyboard.append([InlineKeyboardButton(text="History", callback_data="open_history"),])
    return keyboard

def history_menu_keyboard():
    keyboard = currencies_keyboard("history")
    keyboard.inline_keyboard.append([back_button("main"), ])
    return keyboard

def currencies_keyboard(callback_prefix):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="USD", callback_data=f"{callback_prefix}_840"),
            InlineKeyboardButton(text="EUR", callback_data=f"{callback_prefix}_978"),
        ],
        [
            InlineKeyboardButton(text="PLN", callback_data=f"{callback_prefix}_985"),
            InlineKeyboardButton(text="GBP", callback_data=f"{callback_prefix}_826"),
        ],
    ])

def back_keyboard(back_to):
    return InlineKeyboardMarkup(inline_keyboard=[
        [back_button(back_to)],
    ])

def show_rate_keyboard(currency_code, subscribed):
    return InlineKeyboardMarkup(inline_keyboard=[
        [subscribe_button(currency_code, subscribed),
        back_button("main")]
    ])

def back_button(back_to):
    return InlineKeyboardButton(text="Back", callback_data=f"open_{back_to}")

def subscribe_button(currency_code, subscribed):
    return InlineKeyboardButton(text="Unsubscribe" if subscribed else "Subscribe", callback_data=f"{"unsubscribe" if subscribed else "subscribe"}_{currency_code}")