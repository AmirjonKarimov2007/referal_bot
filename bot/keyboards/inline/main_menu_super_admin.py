from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
main_menu_for_super_admin = InlineKeyboardMarkup(row_width=2)

main_menu_for_super_admin.add(InlineKeyboardButton(text="➕ Kanal qo'shish", callback_data="add_channel"),
                              InlineKeyboardButton(text="➖ Kanal o'chirish", callback_data="del_channel"),
                              InlineKeyboardButton(text="➕ Admin qo'shish", callback_data="add_admin"),
                              InlineKeyboardButton(text="➖ Admin o'chirish", callback_data="del_admin"),
                              InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="settings"),
                              InlineKeyboardButton(text="👤 Adminlar", callback_data="admins"),
                              InlineKeyboardButton(text="📝 Adminlarga Xabar yuborish",callback_data="send_message_to_admins"),
                              InlineKeyboardButton(text="📝 Reklama Jo'natish", callback_data="send_advertisement"),
                              InlineKeyboardButton(text="📊 Statistika", callback_data="statistics"),
                              )
settings_menu_for_super_admin = InlineKeyboardMarkup(row_width=2)
settings_menu_for_super_admin.add(
    # InlineKeyboardButton(text='🟣Premium Olishni Sozlash',callback_data='edit_premium'),
    InlineKeyboardButton(text='💸Narxni o\'zgartirish',callback_data='edit_narx'),
    InlineKeyboardButton(text='📄Qo\'llanmani o\'zgartirish',callback_data='edit_qollanma'),
    InlineKeyboardButton(text='🧑‍💻Adminni o\'zgartirish',callback_data='edit_admin'),
    InlineKeyboardButton(text='🌟 Starsni o\'zgartirish',callback_data='edit_starts'),
    InlineKeyboardButton(text='💴Referal Narxini o\'zgartirish',callback_data='edit_ref_sum'),
    InlineKeyboardButton(text='💎Premium Narxlarini o\'zgartirish',callback_data='edit_premium_prices'),
    InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main_menu")
)

# Ref Price
edit_price_button = InlineKeyboardMarkup(row_width=2)
edit_price_button.add(InlineKeyboardButton(text="✅Oddiy", callback_data="edit_price_normal"))
edit_price_button.add(InlineKeyboardButton(text="💎Premium", callback_data="edit_price_premium"))
edit_price_button.add(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="settings"))
# Premium Price

def edit_premium_prices():
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
        emoji = emoji_map.get(k, "💎")  
        premiums.insert(
            InlineKeyboardButton(
                text=f"{emoji} {k.replace('_', ' ')} - {v} so'm", 
                callback_data=f"premium_edit:{k}"
            )
        )
    premiums.add(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="settings"))
    
    return premiums




back_settings= InlineKeyboardMarkup(row_width=2)
back_settings.add(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="settings"))
# Admin Button
main_menu_for_admin = InlineKeyboardMarkup(row_width=2)
main_menu_for_admin.add(InlineKeyboardButton(text="📊 Statistika", callback_data="stat"))

# Back buttons
back_to_main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main_menu")
        ]
    ]
)
