from loader import db,dp,bot
from aiogram import types
from keyboards.default.menu import *
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(f"<b>Bo'limni tanlang:</b>",reply_markup=kb.main())