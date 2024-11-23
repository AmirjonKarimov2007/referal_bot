from loader import dp, bot, db
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.deep_linking import get_start_link

@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    query_text = query.query.strip()
    user_id = query.from_user.id
    
    # Agar foydalanuvchi hech narsa yozmasa
    if query_text == '':
        link = await get_start_link(user_id)
        caption = "<b>✅ Eyyy! Sizda-chi premium bormi?!</b>\n\n"\
                  f"➡️ Shu kungacha olmagan boʻlsangiz, yaxshi qilibsiz. Endi bepulga olishingiz mumkin.\n\n"\
                  f"➡️ Shunchaki botga start bosing va berilgan havola orqali doʻstlaringizni taklif qiling. Evaziga bot sizga pul beradi. Oʻsha pullarni 1, 3, 6, 12 oylik Premium uchun ishlating!\n\n"\
                  f"Pastdagi havola orqali doʻstlaringizga ulashing:\n"\
                  f"<b>🔗 {link}</b>"
        
        input_content = types.InputTextMessageContent(caption, disable_web_page_preview=True)
        inl = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("✅ Boshlash ✅", url=f"{link}"))
        
        referal = types.InlineQueryResultArticle(
            id='01',
            thumb_url='https://img.freepik.com/premium-photo/3d-telegram-logo-icon-glow-high-quality-render_474486-37.jpg',
            title="Do'stlarga yuborish 📲",
            description="Do'stlarga yuborish uchun shu yerni bosing",
            input_message_content=input_content,
            reply_markup=inl,
        )
        
        await query.answer(results=[referal], cache_time=1)
        return

    # Agar foydalanuvchi katta harflardan iborat bo'lsa
    if query_text.isupper():
        promo_code = await db.select_promocode(promo_code=query_text)
        if promo_code and int(user_id)==int(promo_code[0]['user_id']):
            forward = InlineKeyboardMarkup(row_width=1)
            forward.insert(InlineKeyboardButton(text="Ulashish↗️", callback_data='salom'))
            promo_message = f"<b>🎉 Mening promo kodim: <code>{query_text}</code></b>\n\n" \
                            f"🚀 Bu promo kod yordamida botdagi Premium xizmatlarni bepul yoki chegirmalar bilan olishim mumkinmi?!\n\n" \

            await query.answer(
                results=[
                    types.InlineQueryResultArticle(
                        id=query_text,
                        title='Promo kodni Yuborish',
                        thumb_url='https://as2.ftcdn.net/v2/jpg/05/33/75/35/1000_F_533753588_1krxEE0SDZWl0ZKd9cUzCL6HaTRo9UxK.jpg',
                        description='Adminga yuborish uchun shu yerni bosing',
                        input_message_content=types.InputTextMessageContent(
                            message_text=f"{promo_message}"
                        ),
                    )
                ],
                cache_time=1
            )
            return
    await query.answer(results=[], cache_time=1)
