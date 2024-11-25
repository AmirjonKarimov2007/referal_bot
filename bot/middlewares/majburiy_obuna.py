from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.tekshirish import tekshir
from loader import bot, db
from filters import IsUser, IsSuperAdmin, IsGuest
from filters.admins import IsAdmin


async def kanallar():
    royxat = []
    ights = await db.select_channels()

    for x in ights:
        royxat.append(x[1])
    return royxat

class Asosiy(BaseMiddleware):
    async def on_pre_process_update(self, xabar: types.Update, data: dict):
        if xabar.message:
            if xabar.message.pinned_message:
                pass
            if xabar.message.chat.type in ["group", "supergroup"]:
                return
            user_id = xabar.message.from_user.id
            username = xabar.message.from_user.username
            first_name = xabar.message.from_user.first_name
            matn = "<b>🤖 Botdan Foydalanish uchun ro'yxatdan o'tishingiz kerak. \n\nIltimos telefon raqamingizni \"Raqamni yuborish\" tugmasi orqali yuboring.!</b>"
            user_info = await db.select_user(user_id=int(user_id))
            argument = xabar.message.get_args()
            if user_info:
               pass
            else:
                if argument:
                    if await db.is_user(user_id=int(argument)) and argument.isdigit() and int(argument) > 10:
                        try:
                            await db.add_user(user_id=user_id, username=username, name=first_name, ref_father=int(argument))
                        except Exception as e:
                            await bot.send_message(chat_id=ADMINS[0], text=f'Botda xatolik yuz berdi: majburiy_obuna:{e}')
                else:
                    try:
                        await db.add_user(user_id=int(user_id), username=username, name=first_name)
                    except asyncpg.exceptions.UniqueViolationError:
                        await db.select_user(user_id=int(user_id))   
               
        elif xabar.callback_query:
            user_id = xabar.callback_query.from_user.id
        else:
            return
      
        matn = "<b>🤖 Botdan Foydalanish uchun kanallarga a'zo bo'lib. \n\n\"✅ Tekshirish\" tugmasini bosing!</b>"
        royxat = []
        dastlabki = True

        for k in await kanallar():
            holat = await tekshir(user_id=user_id, kanal_id=k)
            dastlabki *= holat
            kanals = await bot.get_chat(k)
            if not holat:
                link = await kanals.export_invite_link()
                button = [InlineKeyboardButton(text=f"{kanals.title}", url=f"{link}")]
                royxat.append(button)
        royxat.append([InlineKeyboardButton(text="✅ Tekshirish", callback_data="start")])
        if not dastlabki:
            if xabar.callback_query:
                data = xabar.callback_query.data
                if data=='start':
                    await xabar.callback_query.message.delete()
                    
            await bot.send_message(chat_id=user_id, text=matn, disable_web_page_preview=True,
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=royxat))
            raise CancelHandler()

from keyboards.default.menu import *
import asyncpg
from data.config import ADMINS
from states.admin_state import RegisterState
from aiogram.dispatcher import FSMContext
from loader import dp
class CheckPhoneNumber(BaseMiddleware):
    async def on_pre_process_update(self, xabar: types.Update, data: dict):
        if xabar.message:
            user_id = xabar.message.from_user.id
            username = xabar.message.from_user.username
            first_name = xabar.message.from_user.first_name
            content_type = xabar.message.content_type
            if xabar.message.chat.type in ["group", "supergroup"]:
                return
            if content_type == 'contact':
                return 
            if xabar.message.pinned_message:
                pass
            if str(xabar.message.chat.id).startswith('-'):
                return


        elif xabar.callback_query:
            if str(xabar.callback_query.message.chat.id).startswith('-'):
                return

            user_id = xabar.callback_query.from_user.id
            username = xabar.callback_query.from_user.username
            first_name = xabar.callback_query.from_user.first_name
            data = xabar.callback_query.data
            if data=='start':
                await xabar.callback_query.message.delete()
            
        else:
            return
        
        bot_username = await  bot.get_me()
        bot_username = bot_username.username
        if bot_username == username:
            return
        

        user_state = await dp.current_state(user=user_id).get_state()
        matn = "<b>🤖 Botdan Foydalanish uchun ro'yxatdan o'tishingiz kerak. \n\nIltimos telefon raqamingizni \"Raqamni yuborish\" tugmasi orqali yuboring.!</b>"
        user_info = await db.select_user(user_id=int(user_id))
        if user_info:
            user = user_info[0]
            register = user['register']
            number = user['number']
            
            if number is None and bot_username!=username:
                await bot.send_message(chat_id=user_id, text=matn, reply_markup=kb.contact())
                await dp.current_state(user=user_id).set_state(RegisterState.PhoneNumber)
            else:
                return
        else:
            if xabar.message and bot_username!=username:
                argument = xabar.message.get_args()
                if argument:
                    if argument.isdigit() and int(argument) > 10 and await db.is_user(user_id=int(argument)):
                        try:
                            rfather = await db.is_user(user_id=int(argument))
                            ffather_name = rfather[0]['name']
                            ffather_username = rfather[0]['username']
                            await db.add_user(user_id=user_id, username=username, name=first_name, ref_father=int(argument))
                            await bot.send_message(
                                chat_id=user_id, 
                                text=f"<b>👋🏻 Assalomu Aleykum {first_name}, botimizga Tashrif buyurganingizdan xursandmiz kelipsiz!\n\nSizni <a href='t.me/{ffather_username}'>{xabar.message.from_user.full_name}</a> taklif qildi.</b>", 
                                reply_markup=kb.contact()
                            )
                        except Exception as e:
                            await bot.send_message(chat_id=ADMINS[0], text=f'Botda xatolik yuz berdi: {e}')
                else:
                    
                    try:
                        await db.add_user(user_id=int(user_id), username=username, name=first_name)
                    except asyncpg.exceptions.UniqueViolationError:
                        await db.select_user(user_id=int(user_id))
            await dp.current_state(user=user_id).set_state(RegisterState.PhoneNumber)
            
        raise CancelHandler()