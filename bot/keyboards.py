from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from currencies import currency_name

def main_menu_keyboard(currencies, page=0):
    keyboard = currencies_keyboard(currencies, "currency", page)
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="History", callback_data="open_history"),
    ])
    return keyboard

def history_menu_keyboard(currencies, page=0):
    keyboard = currencies_keyboard(currencies, "history", page)
    keyboard.inline_keyboard.append([back_button("main")])
    return keyboard

def total_pages(total_items, per_page=8):
    return max(1, (total_items + per_page - 1) // per_page)

def currencies_keyboard(currencies, callback_prefix, page=0, per_page=8):
    pages = total_pages(len(currencies), per_page)
    page = max(0, min(page, pages - 1))

    start = page * per_page
    chunk = currencies[start:start + per_page]

    rows = []
    for i in range(0, len(chunk), 2):
        rows.append([
            InlineKeyboardButton(
                text=currency_name(code),
                callback_data=f"{callback_prefix}_{code}",
            )
            for code in chunk[i:i + 2]
        ])

    if pages > 1:
        rows.append(navigation_row(callback_prefix, page, pages))

    return InlineKeyboardMarkup(inline_keyboard=rows)

def navigation_row(callback_prefix, page, pages):
    prev_page = (page - 1) % pages
    next_page = (page + 1) % pages
    return [
        InlineKeyboardButton(text="‹", callback_data=f"page_{callback_prefix}_{prev_page}"),
        InlineKeyboardButton(text=f"{page + 1}/{pages}", callback_data="noop"),
        InlineKeyboardButton(text="›", callback_data=f"page_{callback_prefix}_{next_page}"),
    ]

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