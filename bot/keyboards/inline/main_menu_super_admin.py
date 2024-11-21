from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
    InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main_menu")
)
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
