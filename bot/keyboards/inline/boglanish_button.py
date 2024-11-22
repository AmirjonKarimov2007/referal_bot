from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import json
check = InlineKeyboardMarkup(row_width=2)
check.insert(InlineKeyboardButton(text="✅Ha", callback_data='ha'))
check.insert(InlineKeyboardButton(text="❌Yo'q", callback_data='Yoq'))

get_premium_keyboard = InlineKeyboardMarkup(row_width=1)
get_premium_keyboard.insert(InlineKeyboardButton(text='PREMIUM UCHUN SARFLASH✅',callback_data="select_premium_package"))

def premium_keybaord():
    # Tariflarga mos emoji tayyorlash
    emoji_map = {
        "1_month": "🏅",
        "3_month": "⚡",
        "6_month": "🔥",
        "12_month": "💎"
    }
    
    premiums = InlineKeyboardMarkup(row_width=1)
    with open('data.json', 'r') as file:
        data = json.load(file)
    premium_prices = data['premium_prices']
    
    for k, v in premium_prices.items():
        # Har bir tarifga mos emoji topish
        emoji = emoji_map.get(k, "💎")  # Agar emoji topilmasa, default emoji
        premiums.insert(
            InlineKeyboardButton(
                text=f"{emoji} {k.replace('_', ' ')} - {v} so'm",  # Matnni formatlash
                callback_data=f"premium_{k}"
            )
        )
    return premiums