from datetime import datetime
from datetime import datetime, timedelta
from data.config import ADMINS
from filters.users import IsUser
from filters.admins import IsSuperAdmin
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.menu import *
from loader import dp, db,bot
from keyboards.inline.boglanish_button import get_premium_keyboard,premium_keyboard

MANUAL = "<b>❓Botda qanday qilib pul ishlayman?</b>\n" \
         "— Botga do'stlaringizni taklif qiling va har bir yangi taklif qilgan do'stlaringiz uchun pullik mukofotlarga ega bo'ling.\n\n" \
         "<b>❓Pulni qanday qilib olish mumkin?</b>\n" \
         "— Botda ishlagan pullaringizni telefon raqamingizga chiqarib olishingiz mumkin. (HUMANS raqamlariga to'lab berilmaydi!)\n\n" \
         "<b>👥 Referal qachon aktiv xolatga o'tadi?</b>\n" \
         "— Siz chaqirgan do'stingiz bizning homiylar kanaliga a'zo bo'lganidan so'ng sizning referalingiz hisoblanadi va sizning balansingizga pul tushadi!\n\n" \
         "<i>✅ To'lovlar soni cheklanmagan, xohlaganingizcha shartlar bajaring va pul ishlang!</i>"

TARIX = "<b>Botimiz haqiqatdan ham to'lab beradi. ✅</b>\n\n<i>Quyidagi kanal orqali to'lovlar tarixini kuzatib borishingiz mumkin👇</i>\nhttps://t.me/+Q6TsT4YXvXplZDUy"
@dp.message_handler(text="💳 Mening Hisobim")
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    id_send = await db.select_user(user_id=user_id)
    if id_send:
        balance = id_send[0]['balance']
        number = id_send[0]['number']
        referred_count = await db.count_referred_users(user_id)
        await message.answer(text=f"<b>💰Hisobingiz: <code>{balance}</code> so'm</b>\n"
                 f"<b>👥Taklif qilgan do'stlaringiz: <code>{referred_count}</code> odam</b>\n"
                 f"<b>📱Hisob raqamingiz: <code>+{number}</code></b>\n",
            reply_markup=get_premium_keyboard,
            parse_mode=types.ParseMode.HTML
        )
    else:
        await message.reply("Foydalanuvchi ma'lumotlari topilmadi.", reply_markup=kb.main())


@dp.callback_query_handler(text='select_premium_package')
async def get_premium_func(call: types.CallbackQuery):
    user_id = call.from_user.id
    with open('data.json', 'r') as file:
        data = json.load(file)
    max_balance = data['premium_prices']['1_oy']
    profile = await db.select_user(user_id=user_id)
    if profile and max_balance:
        user_balance = profile[0]['balance']
        user_balance = int(user_balance)
        max_balance = int(max_balance)
        if user_balance < max_balance:
            await bot.answer_callback_query(call.id, text=f"Premiumga sarflash uchun hisobingizda kamida {max_balance} so'm bo'lishi kerak!", show_alert=True)
        elif user_balance>=max_balance:
            await call.message.edit_text(text='Premium Tarifingizni Tanlang!',reply_markup=premium_keyboard(user_balance))
        
from main import generate_unique_promo_code
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
@dp.callback_query_handler(IsUser(),text_contains="take_premium:")
async def takepremium(call:types.CallbackQuery):
    await call.answer(cache_time=1)
    pr = call.data.rsplit(":")[1]
    with open('data.json','r') as file:
        data = json.load(file)
    check = InlineKeyboardMarkup(row_width=1)
    if data['premium_prices'][pr]:
        premium_price = data['premium_prices'][pr]
        premium_price = int(premium_price)
        profile = await db.select_user(user_id=int(call.from_user.id))
        if profile:
            if profile[0]['balance'] >= premium_price:
                check.add(InlineKeyboardButton(text="✅Tasdiqlayman",callback_data=f"checked_premium:{pr}"))
                check.add(InlineKeyboardButton(text="⬅️Orqaga",callback_data=f"select_premium_package"))
                await call.message.edit_text(text='<b>Premium Olishni Tasdiqlaysizmi?</b>',reply_markup=check)


@dp.callback_query_handler(IsUser(),text_contains="checked_premium")
async def checked_premium(call: types.CallbackQuery):
    pr = call.data.rsplit(":")[1]
    with open('data.json','r') as file:
        data = json.load(file)
    user_id=int(call.from_user.id)
    profile = await db.select_user(user_id=user_id)
    if data['premium_prices'][pr]:
        premium_price = data['premium_prices'][pr]
        premium_price = int(premium_price)
        if profile:
            if profile[0]['balance'] >= premium_price:
                    try:
                        promocode = generate_unique_promo_code()
                        summa = int(profile[0]['balance']-int(premium_price))
                        await db.update_balances(user_id=user_id,sum=summa)
                        end_date = datetime.now() + timedelta(days=15)
                        formatted_end_date = end_date.strftime('%Y-%m-%d %H:%M')
                        await db.add_promocode(promo_code=promocode,package=pr,status="Activate",created_at=datetime.now(),user_id=user_id)
                        user_balance = await db.select_user(user_id=user_id)
                        balance = user_balance[0]['balance']
                        request = InlineKeyboardMarkup(row_width=1)
                        request.add(InlineKeyboardButton(text='📲Adminga habar berish',switch_inline_query=f"{promocode}"))
                        await bot.answer_callback_query(call.id,text=f"Sizga {pr.replace('_', ' ')}lik Premium uchun Promo kod berildi✅.\n\n🖇PROMO CODE:  {promocode}\n\n👝BALANCE:{balance}",show_alert=True)
                        await call.message.edit_text(f"<b>🎉Tabriklayman sizga <b>{pr.replace('_', ' ')}</b>ik premium uchun promo kod berildi✅.\nPromo kod⏬⏬⏬\n<code>{promocode}</code>\n\nNarxi:{str(premium_price)}so'm\nYaroqlilik muddati {formatted_end_date}\n\nPromo kodni adminga yuborish orqali premiumni qo'lga kiritishingiz mumkin.\n\nAdmin: 🙎‍♂️@hkimvv\n\nE'tibor bering bu habarni o'chirib yubormang</b>",reply_markup=request)
                        support = InlineKeyboardMarkup(row_width=1)
                        support.add(InlineKeyboardButton(text='📲Bog\'lanish',url=f"tg://user?id={call.from_user.id}"))
                        support.add(InlineKeyboardButton(text='✅Tekshirish',callback_data=f"promo_code_check:{call.from_user.id}:{promocode}"))
                        for admin in ADMINS:
                            pin_message = await bot.send_message(chat_id=admin,text=f"Assalom Aleykum Admin ,siz uchun yangi Premium bor.\n\n<b>🔰Foydalanuvchi Haqida Malumotlar\n\n📛Ism familiya: {call.from_user.first_name}\n🌐Username: @{call.from_user.username}\n🆔Id: {call.from_user.id}\n📞Telefon Raqam: +{profile[0]['number']}\n🔡Promo Code: <code>{promocode}</code></b>",reply_markup=support)
                            await bot.pin_chat_message(chat_id=admin, message_id=pin_message.message_id)
                    except Exception as e:
                            await bot.send_message(chat_id=ADMINS[0],text=f'xatolik yuz berdi"{e}')



import pytz
def check_date(profile, state="*"):
    current_date = datetime.now()
    end_date = profile[0]['end_date']

    if end_date:
        tashkent = pytz.timezone('Asia/Tashkent')
        current_date_time = current_date.astimezone(tashkent)
        current_date = current_date_time.strftime('%Y-%m-%d %H:%M:%S')
        end_date_time_tashkent = end_date.astimezone(tashkent)
        end_date = end_date_time_tashkent.strftime('%Y-%m-%d %H:%M:%S')
        if current_date > end_date:
            return False
        else:
            return True
    else:
        return True


@dp.callback_query_handler(IsSuperAdmin(),text_contains="promo_code_check:")
async def promo_check(call: types.CallbackQuery):
    check_promo = call.data.rsplit(":")
    user_id = check_promo[1]
    promo_code = check_promo[2]
    profile = await db.select_promocode(promo_code=promo_code)
    if profile:
        end_date =check_date(profile=profile)
        profile_user_id = profile[0]['user_id']
        profile_user_id = int(profile_user_id)
        text = f"🟣Status: {profile[0]['status']}\n"
        text += f"♻️Premium: {profile[0]['package']}\n"
        text += f"🔡Promo Code: {profile[0]['promo_code']}\n"
        if end_date==True and profile_user_id==int(user_id):
            await bot.answer_callback_query(call.id,text=f"{text}",show_alert=True)
        else:
            await bot.answer_callback_query(call.id,text=f"🕔Promo Kod Vaqti O'tib Ketgan",show_alert=True)
    else:
        await bot.answer_callback_query(call.id,text=f"❌Promo Kod Yaroqsiz",show_alert=True)
        






            






















@dp.message_handler(text="TOP foydalanuvchilar")
async def top_active_users(message: types.Message):
    top_users = await db.get_top_users()  # DB-dan top 10 foydalanuvchilarni olamiz

    if top_users:
        response = "<b>Botimizning eng faol foydalanuvchilari:</b>\n\n"
        for i, user in enumerate(top_users, 1):
            name = user['name']
            balance = f"{user['balance']:,}".replace(",", " ")  # Balansni chiroyli formatlash
            response += f"<b>{i}) {name}</b>  — <code>{balance}</code> so'm\n"
    else:
        response = "🛑 Hozircha faol foydalanuvchilar mavjud emas."

    await message.reply(response, parse_mode=types.ParseMode.HTML)



@dp.message_handler(text='💸 Premium Narxlari')
async def premiumprices(message: types.Message):
    with open('data.json', 'r') as file:
        data = json.load(file)
    
    if data['premium_price']['message_id'] and data['premium_price']['from_chat_id']:
        message_id = data['premium_price']['message_id']
        fchat_id = data['premium_price']['from_chat_id']
        await bot.copy_message(chat_id=message.from_user.id,from_chat_id=fchat_id,message_id=message_id)

@dp.message_handler(text="Qo'llanma 📄")
async def bot_start(message: types.Message):
    with open('data.json', 'r') as file:
        data = json.load(file) 
    
    if data['get_qollanma']['message_id'] and data['get_qollanma']['from_chat_id']:
        message_id = data['get_qollanma']['message_id']
        chat_id = data['get_qollanma']['from_chat_id']
        await bot.copy_message(chat_id=message.from_user.id,from_chat_id=chat_id,message_id=message_id,reply_markup=kb.manual())
@dp.message_handler(text="To'lovlar tarixi 🧾")
async def bot_start(message: types.Message):
    await message.reply(text=TARIX, disable_web_page_preview=True)
import json

@dp.message_handler(text="👨‍💻 Administrator")
async def admin(message:types.Message):
    with open('data.json', 'r') as file:
        data = json.load(file) 
    if data['administator']['message_id'] and data['administator']['from_chat_id']:
        message_id = data['administator']['message_id']
        chat_id = data['administator']['from_chat_id']
        await bot.copy_message(chat_id=message.from_user.id,from_chat_id=chat_id,message_id=message_id,reply_markup=kb.manual())

@dp.message_handler(text="🌟 Stars olish")
async def admin(message:types.Message):
    with open('data.json', 'r') as file:
        data = json.load(file) 
    if data['get_stars']['message_id'] and data['get_stars']['from_chat_id']:
        message_id = data['get_stars']['message_id']
        chat_id = data['get_stars']['from_chat_id']
        await bot.copy_message(chat_id=message.from_user.id,from_chat_id=chat_id,message_id=message_id)
