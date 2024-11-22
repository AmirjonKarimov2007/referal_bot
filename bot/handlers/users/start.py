import logging
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery
from filters import IsUser, IsSuperAdmin, IsGuest
from filters.admins import IsAdmin
from keyboards.inline.main_menu_super_admin import main_menu_for_super_admin, main_menu_for_admin
from loader import db,dp,bot
import asyncpg
from data.config import ADMINS
logging.basicConfig(level=logging.INFO)
from keyboards.default.menu import kb
@dp.callback_query_handler(text="start")
async def bot_echo(call: CallbackQuery):
    await call.answer(cache_time=1)
    user = call.from_user
    await call.message.delete()
    try:
        await db.add_user(user_id=user.id,username=call.from_user.username, name=user.first_name)
    except asyncpg.exceptions.UniqueViolationError:
        await db.select_user(user_id=call.from_user.id)

    await bot.send_message(chat_id=user.id, text="<b>✅Botdan bemalol foydalanishingiz mumkin.</b>")

@dp.message_handler(IsAdmin(), CommandStart(), state="*")
async def bot_start_admin(message: types.Message):
    await message.answer(f"Assalom alaykum Admin, {message.from_user.full_name}!",
                         reply_markup=main_menu_for_admin)
@dp.message_handler(IsSuperAdmin(), CommandStart(), state="*")
async def bot_start_super_admin(message: types.Message):
    await message.answer(f"<b>Assalom alaykum Bosh Admin, <a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>!</b>",
                         reply_markup=main_menu_for_super_admin)

@dp.message_handler(IsGuest(), CommandStart(), state="*")
async def bot_start(message: types.Message):
    user = message.from_user
    username = message.from_user.username
    try:
        await db.add_user(user_id=message.from_user.id,username=username, name=user.first_name)
    except asyncpg.exceptions.UniqueViolationError:
        await db.select_user(user_id=message.from_user.id)
    except Exception as ex:
        print(f"IsGuest:{ex}")

    user_id = message.from_user.first_name
    await message.reply(f"<b>👋🏻 Assalomu Aleykum {user_id} botimizga Xush kelipsiz!</b>")
    
@dp.message_handler(IsUser(), CommandStart(), state="*")
async def bot_start(message: types.Message):
    user = message.from_user
    username = message.from_user.username
    user_id = message.from_user.first_name
    await message.reply(f"<b>👋🏻 Assalomu Aleykum {user_id} botimizga Xush kelipsiz!</b>",reply_markup=kb.main())
from states.admin_state import RegisterState
from aiogram.dispatcher import FSMContext
import json
@dp.message_handler(content_types=types.ContentType.CONTACT,state=RegisterState.PhoneNumber)
async def phone_number(message: types.Message,state: FSMContext):
    id = message.contact.user_id
    phone_usm = message.contact.phone_number
    phone_num = phone_usm.replace("+", "")
    with open('data.json', 'r') as file:
        data = json.load(file)
    normal_price = data['price']['normal_price']
    premium_price = data['price']['premium_price']
    try:
        user = await db.is_user(user_id=int(message.from_user.id))
        if user:
            reffather_id = user[0]['ref_father']
            register = user[0]['register']
            if reffather_id and await db.is_user(user_id=int(reffather_id)):
                if message.from_user.is_premium:
                    await db.update_balance(user_id=int(user[0]['ref_father']),sum=int(premium_price))
                    await bot.send_message(chat_id=int(reffather_id),text=f"<b>🤑Sizga {message.from_user.first_name} tomonidan referal qo'shildi.\n\nSumma:{premium_price} so'm</b>")
                    await db.update_user_number(number=int(phone_num), user_id=int(message.from_user.id),register=True)
                else:
                    await db.update_balance(user_id=int(user[0]['ref_father']),sum=int(normal_price))
                    await bot.send_message(chat_id=int(reffather_id),text=f"<b>🤑Sizga {message.from_user.first_name} tomonidan referal qo'shildi.\n\nSumma:{normal_price} so'm</b>")
                    await db.update_user_number(number=int(phone_num), user_id=int(message.from_user.id),register=True)
            else:
                await db.update_user_number(number=int(phone_num), user_id=int(message.from_user.id),register=True)
        else:
            await db.add_user(name=message.from_user.first_name,username=message.from_user.username,user_id=int(message.from_user.id),number=int(phone_num),register=True)
        await message.answer(f"{message.from_user.first_name}, Tabriklayman botdan muvaffaqiyatli ro'yxatdan o'tdingiz\n\nBoshlash uchun <b>«🌟 Premium Olish»</b> tugmasini bosing", reply_markup=kb.main())
        await state.finish()
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0],text=f'Botda xatolik yuz berdi:{e}')
        await state.finish()
