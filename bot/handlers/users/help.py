from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp,bot


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam")
    
    await message.answer("\n".join(text))


@dp.chat_join_request_handler()
async def echo(message: types.Message):
    msg = f"{message.chat.full_name} qo'shilish so'rovingiz tasdiqlandi✅"
    await bot.send_message(message.from_user.id, msg)
    await bot.approve_chat_join_request(message.chat.id, message.from_user.id)
