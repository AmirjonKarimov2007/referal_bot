from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import json
check = InlineKeyboardMarkup(row_width=2)
check.insert(InlineKeyboardButton(text="✅Ha", callback_data='ha'))
check.insert(InlineKeyboardButton(text="❌Yo'q", callback_data='Yoq'))

get_premium_keyboard = InlineKeyboardMarkup(row_width=1)
get_premium_keyboard.insert(InlineKeyboardButton(text='PREMIUM UCHUN SARFLASH✅',callback_data="select_premium_package"))

def premium_keyboard(balance):
    # Tariflarga mos emoji tayyorlash
    emoji_map = {
        "1_oy": "🏅",
        "3_oy": "⚡",
        "6_oy": "🔥",
        "12_oy": "💎"
    }
    
    premiums = InlineKeyboardMarkup(row_width=1)
    with open('data.json', 'r') as file:
        data = json.load(file)
    premium_prices = data['premium_prices']
    
    for k, v in premium_prices.items():
        v = int(v)
        if balance >= v: 
            emoji = emoji_map.get(k, "💎")  
            premiums.insert(
                InlineKeyboardButton(
                    text=f"{emoji} {k.replace('_', ' ')} - {v} so'm",  
                    callback_data=f"take_premium:{k}"
                )
            )
    return premiums