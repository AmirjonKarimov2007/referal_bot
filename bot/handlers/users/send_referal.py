from aiogram import types


from loader import dp, bot

from aiogram.utils.deep_linking import get_start_link





@dp.message_handler(text="🌟 Premium Olish")
async def Money(message: types.Message):
    user_id =message.from_user
    link = await get_start_link(user_id.id)
    bot_get = await bot.get_me()
    await message.answer_photo(photo='https://fdn.gsmarena.com/imgroot/news/22/06/telegram-premium-ofic/-1200/gsmarena_001.jpg'
                               ,caption="<b>✅ Eyyy! Sizda-chi premium bormi?!</b>\n\n"
                                f"➡️ Shu kungacha olmagan boʻlsangiz, yaxshi qilibsiz. Endi bepulga olishingiz mumkin.\n\n"
                                f"➡️ Shunchaki botga start bosing va berilgan havola orqali doʻstlaringizni taklif qiling. Evaziga bot sizga pul beradi. Oʻsha pullarni 1, 3, 6, 12 oylik Premium uchun ishlating!\n\n"
                                f"Pastdagi havola orqali doʻstlaringizga ulashing:\n"
                                f"<b>🔗 {link}</b>",reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Ulashish ♻️", url=f"https://t.me/share/url?url={link}")))

@dp.inline_handler()
async def referals(inline_query: types.InlineQuery):
    user_id =inline_query.from_user
    link = await get_start_link(user_id.id)
    bot_get = await bot.get_me()
    text = f"<b>✅ «Axcha Pul» konkursi rasmiy boti.</b>\n\n"\
           f"🎈<a href='{user_id.url}'>{inline_query.from_user.first_name}</a> do'stingizdan unikal havola-taklifnoma.\n\n"\
           f"📣 <a href='{'https://t.me/+Q6TsT4YXvXplZDUy'}'>{'<b>«About Me : Portfolio»</b>'}</a> kanalining rasmiy botiga do'stlaringizni taklif qiling va kuniga 100.000 so'mdan ko'proq pul toping!\n\n" \
           f"<b>👇 Boshlash uchun bosing:</b>\n"\
           f"{link}"

    input_content = types.InputTextMessageContent(text,disable_web_page_preview=True)
    inl = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("✅ Boshlash ✅", url=f"{link}"))
    referal = types.InlineQueryResultArticle(
        id='01',
        thumb_url=None,
        title="Do'stlarga yuborish 📲",
        description="Do'stlarga yuborish uchun shu yerni bosing",
        input_message_content=input_content,
        reply_markup=inl,
    )
    lis = [referal]
    msg = await inline_query.answer(results=lis, cache_time=1)