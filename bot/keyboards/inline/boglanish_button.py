from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
check = InlineKeyboardMarkup(row_width=2)

check.insert(InlineKeyboardButton(text="✅Ha", callback_data='ha'))
check.insert(InlineKeyboardButton(text="❌Yo'q", callback_data='Yoq'))

get_premium_keyboard = InlineKeyboardMarkup(row_width=1)
get_premium_keyboard.add(InlineKeyboardButton(text="PREMIUM UCHUN SAFRLASH✅", callback_data='get_premium'))
