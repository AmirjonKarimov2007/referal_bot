from keyboards.inline.main_menu_super_admin import edit_premium_prices
import re
import time
import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#Dasturchi @Mrgayratov kanla @Kingsofpy
from filters import IsSuperAdmin
from keyboards.inline.main_menu_super_admin import main_menu_for_super_admin, back_to_main_menu
from loader import dp, db, bot
from states.admin_state import SuperAdminState
from middlewares.MediaGroup import AlbumMiddleware
from keyboards.inline.main_menu_super_admin import settings_menu_for_super_admin,back_settings

# ADMIN TAYORLASH VA CHIQARISH QISMI UCHUN
@dp.callback_query_handler(IsSuperAdmin(), text="add_admin", state="*")
async def add_admin(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text("Yangi adminni chat IDsini yuboring...\n"
                                 "🆔 Admin ID raqamini olish uchun @userinfobot ga /start bosishini ayting",
                                 reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_ADD_ADMIN.set()

@dp.message_handler(IsSuperAdmin(), state=SuperAdminState.SUPER_ADMIN_ADD_ADMIN)
async def add_admin_method(message: types.Message, state: FSMContext):
    admin_id =message.text
    await state.update_data({"admin_id": admin_id})
    await message.answer("👨🏻‍💻 Yangi admin ismini yuborin",
                                 reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_ADD_FULLNAME.set()
#Dasturchi @Mrgayratov kanla @Kingsofpy

@dp.message_handler(IsSuperAdmin(), state=SuperAdminState.SUPER_ADMIN_ADD_FULLNAME)
async def add_admin_method(message: types.Message,state: FSMContext):
    try:
        royxat = await db.select_admins()
        full_name = message.text
        await state.update_data({"full_name": full_name})
        malumot = await state.get_data()
        # Dasturchi @Mrgayratov kanla @Kingsofpy
        adminid = malumot.get("admin_id")
        full_name = malumot.get("full_name")
        try:
            if adminid not in royxat:
                await db.add_admin(user_id=int(adminid), full_name=full_name)
                await bot.send_message(chat_id=adminid,text="tabriklaymiz siz botimizda adminlik huquqini qolgan kiritidingiz /start bosing.")
                await message.answer("✅ Yangi admin muvaffaqiyatli qo'shildi!", reply_markup=main_menu_for_super_admin)
                await state.finish()

        except Exception as e:
            await message.answer("Adminni qo'shishda muammo yuz berdi.Admin botga start bosganligi yoki botni bloklamganligiga ishonch hozil qiling.")
            await state.finish()

    except Exception as e:
        await message.answer("❌ Xatolik yuz berdi!", reply_markup=main_menu_for_super_admin)
        await state.finish()

@dp.callback_query_handler(IsSuperAdmin(), text="del_admin", state="*")
async def show_admins(call: types.CallbackQuery):

    await call.answer(cache_time=2)
    admins = await db.select_all_admins()
    buttons = InlineKeyboardMarkup(row_width=1)
    for admin in admins:
        buttons.insert(InlineKeyboardButton(text=f"{admin[2]}", callback_data=f"admin:{admin[1]}"))
    # Dasturchi @Mrgayratov kanla @Kingsofpy
    buttons.add(InlineKeyboardButton(text="➕ Admin qo'shish", callback_data="add_admin"))
    buttons.insert(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main_menu"))
    await call.message.edit_text(text="👤 Adminlar", reply_markup=buttons)
    
#Dasturchi @Mrgayratov kanla @Kingsofpy
@dp.callback_query_handler(IsSuperAdmin(), text_contains="admin:", state="*")
async def del_admin_method(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    data = call.data.rsplit(":")
    admin = await db.select_all_admin(user_id=int(data[1]))
    for data in admin:
        text = f"Sizning ma'lumotlaringiz\n\n"
        text += f"<i>👤 Admin ismi :</i> <b>{data[2]}\n</b>"
        text += f"<i>🆔 Admin ID raqami :</i> <b>{data[1]}</b>"
        buttons = InlineKeyboardMarkup(row_width=1)

        buttons.insert(InlineKeyboardButton(text="❌ Admindan bo'shatish", callback_data=f"deladm:{data[1]}"))
        buttons.insert(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admins"))

        await call.message.edit_text(text=text, reply_markup=buttons)

@dp.callback_query_handler(IsSuperAdmin(), text_contains="deladm:", state="*")
async def del_admin_method(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    data = call.data.rsplit(":")
    delete_orders = await db.delete_admin(admin_id=int(data[1]))
    await bot.send_message(chat_id=data[1],
                           text="Sizdan adminlik huquqi olindi")

    await call.answer("🗑 Admin o'chirildi !",show_alert=True)
    await call.message.edit_text("✅ Admin muvaffaqiyatli o'chirildi!", reply_markup=main_menu_for_super_admin)


# ADMIN TAYORLASH VA CHIQARISH QISMI UCHUN

# MAJBURIY OBUNA SOZLASH UCHUN
@dp.callback_query_handler(text = "add_channel")
async def add_channel(call: types.CallbackQuery):
    await SuperAdminState.SUPER_ADMIN_ADD_CHANNEL.set()
    await call.message.edit_text(text="<i><b>📛 Kanal usernamesini yoki ID sini kiriting: </b></i>")
    await call.message.edit_reply_markup(reply_markup=back_to_main_menu)


@dp.message_handler(IsSuperAdmin(),state=SuperAdminState.SUPER_ADMIN_ADD_CHANNEL)
async def add_channel(message: types.Message, state: FSMContext):
    matn = message.text
    if matn.isdigit() or matn.startswith("@") or matn.startswith("-"):
        try:
            if await db.check_channel(channel=message.text):
                await message.answer("<i>❌Bu kanal qo'shilgan! Boshqa kanal qo'shing!</i>", reply_markup=back_to_main_menu)
            else:
                try:
                    deeellll = await bot.send_message(chat_id=message.text, text=".")
                    await bot.delete_message(chat_id=message.text, message_id=deeellll.message_id)
                    try:
                        await db.add_channel(channel=message.text)
                    except:
                        pass
                    await message.answer("<i><b>Channel succesfully added ✅</b></i>")
                    await message.answer("<i>Siz admin panelidasiz. 🧑‍💻</i>", reply_markup=main_menu_for_super_admin)
                    await state.finish()
                except:
                    await message.reply("""<i><b>
Bu kanalda admin emasman!⚙️
Yoki siz kiritgan username ga ega kanal mavjud emas! ❌
Kanalga admin qilib qaytadan urinib ko'ring yoki to'g'ri username kiriting.🔁
                    </b></i>""", reply_markup=back_to_main_menu)
        except Exception as err:
            await message.answer(f"Xatolik ketdi: {err}")
            await state.finish()
    else:
        await message.answer("Xato kiritdingiz.", reply_markup=back_to_main_menu)

@dp.callback_query_handler(text="del_channel")
async def channel_list(call: types.CallbackQuery):
    royxat = await db.select_channels()
    text = "🔰 Kanallar ro'yxati:\n\n"
    son = 0
    for o in royxat:
        son +=1
        text += f"{son}. {o[1]}\n💠 Username: {o[1]}\n\n"
    await call.message.edit_text(text=text)
    admins =await db.select_all_channels()
    buttons = InlineKeyboardMarkup(row_width=2)
    for admin in admins:
        buttons.insert(InlineKeyboardButton(text=f"{admin[1]}", callback_data=f"delchanel:{admin[1]}"))

    buttons.add(InlineKeyboardButton(text="➕ Kanal qo'shish", callback_data="add_channel"))
    buttons.insert(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main_menu"))
    await call.message.edit_text(text=text, reply_markup=buttons)

@dp.callback_query_handler(IsSuperAdmin(), text_contains="delchanel:", state="*")
async def del_admin_method(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    data = call.data.rsplit(":")
    delete_orders = await db.delete_channel(channel=data[1])
    await call.answer("🗑 Channel o'chirildi !",show_alert=True)
    await call.message.edit_text("✅ Kanal muvaffaqiyatli o'chirildi!", reply_markup=main_menu_for_super_admin)

# ADMINLARNI KORISH
@dp.callback_query_handler(text="admins")
async def channel_list(call: types.CallbackQuery):
    royxat = await db.select_admins()
    text = "🔰 Adminlar ro'yxati:\n\n"
    son = 0
    for o in royxat:
        son +=1
        text += f"{son}. {o[2]}\nID : {o[1]}💠 Ismi: {o[2]}\n\n"
    await call.message.edit_text(text=text)

    buttons = InlineKeyboardMarkup(row_width=1)
    buttons.insert(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main_menu"))
    await call.message.edit_text(text=text, reply_markup=buttons)
# ADMINLARNI KORISH

# STATISKA KORISH UCHUN
@dp.callback_query_handler(text="statistics")
async def stat(call : types.CallbackQuery):
    stat = await db.stat()
    await call.message.delete()

    stat = str(stat)

    datas = datetime.datetime.now()
    yil_oy_kun = (datetime.datetime.date(datetime.datetime.now()))
    soat_minut_sekund = f"{datas.hour}:{datas.minute}:{datas.second}"
    await call.message.answer(f"<b>👥 Bot foydalanuvchilari soni: {(stat)} nafar\n</b>"
                                f"<b>⏰ Soat: {soat_minut_sekund}\n</b>"
                                f"<b>📆 Sana: {yil_oy_kun}</b>",reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("◀️ Orqaga",callback_data="back_to_main_menu")))


# ADMINGA SEND FUNC
@dp.callback_query_handler(IsSuperAdmin(), text="send_message_to_admins", state="*")
async def send_advertisement(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text("Reklamani yuboring...\n"
                                 "Yoki bekor qilish tugmasini bosing", reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_SEND_MESSAGE_TO_ADMINS.set()

from asyncio import Semaphore, gather


@dp.message_handler(IsSuperAdmin(), state=SuperAdminState.SUPER_ADMIN_STATE_GET_ADVERTISEMENT,
                    content_types=types.ContentTypes.ANY)
async def send_advertisement_to_user(message: types.Message, state: FSMContext):
    users = await db.stat()
    user_list = await db.select_all_users()
    
    black_list = 0
    white_list = 0
    datas = datetime.datetime.now()
    boshlanish_vaqti = f"{datas.hour}:{datas.minute}:{datas.second}"

    start_msg = await message.answer(f"📢 Reklama jo'natish boshlandi...\n"
                                      f"📊 Foydalanuvchilar soni: {users} ta\n"
                                      f"🕒 Kuting...\n")

    semaphore = Semaphore(20)  # Har bir vaqtda 20 ta xabar yuborish bilan cheklov
    errors = []

    async def send_message(user_id):
        nonlocal black_list, white_list
        async with semaphore:
            try:
                await bot.copy_message(chat_id=user_id, from_chat_id=message.chat.id,
                                       message_id=message.message_id, reply_markup=message.reply_markup)
                white_list += 1
            except Exception as e:
                black_list += 1
                errors.append((user_id, str(e)))

    # Foydalanuvchilarga parallel xabar yuborish
    tasks = [send_message(user['user_id']) for user in user_list]
    await gather(*tasks)

    data = datetime.datetime.now()
    tugash_vaqti = f"{data.hour}:{data.minute}:{data.second}"
    
    text = (f'<b>✅ Reklama muvaffaqiyatli yuborildi!</b>\n\n'
            f'<b>⏰ Boshlangan vaqt: {boshlanish_vaqti}</b>\n'
            f'<b>👥 Yuborilgan foydalanuvchilar soni: {white_list}</b>\n'
            f'<b>🚫 Yuborilmagan foydalanuvchilar soni: {black_list}</b>\n'
            f'<b>🏁 Tugash vaqti: {tugash_vaqti}</b>\n')

    await bot.delete_message(chat_id=start_msg.chat.id, message_id=start_msg.message_id)
    await message.answer(text, reply_markup=main_menu_for_super_admin)
    await state.finish()

# ====================Foydalanuvchliar uchun SEND SUNC  ============================
@dp.callback_query_handler(IsSuperAdmin(), text="send_advertisement", state="*")
async def send_advertisement(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text("Reklamani yuboring...\n"
                                 "Yoki bekor qilish tugmasini bosing", reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_STATE_GET_ADVERTISEMENT.set()


@dp.message_handler(IsSuperAdmin(), state=SuperAdminState.SUPER_ADMIN_STATE_GET_ADVERTISEMENT,
                    content_types=types.ContentTypes.ANY)
async def send_advertisement_to_user(message: types.Message, state: FSMContext):
    users = await db.stat()
    users = str(users)
    black_list = 0
    white_list = 0
    datas = datetime.datetime.now()
    boshlanish_vaqti = f"{datas.hour}:{datas.minute}:{datas.second}"
    start_msg = await message.answer(f"📢 Reklama jo'natish boshlandi...\n"
                         f"📊 Foydalanuvchilar soni: {users} ta\n"
                         f"🕒 Kuting...\n")
    user = await db.select_all_users()
    for i in user:
        user_id = i['user_id']
        try:
            msg = await bot.copy_message(chat_id=user_id, from_chat_id=message.chat.id,
                                            message_id=message.message_id,reply_markup=message.reply_markup)
            white_list += 1
            time.sleep(0.3)
        except Exception as e:
            black_list += 1
    data = datetime.datetime.now()

    tugash_vaqti = f"{data.hour}:{data.minute}:{data.second}"
    text = f'<b>✅ Reklama muvaffaqiyatli yuborildi!</b>\n\n'
    text += f'<b>⏰Reklama yuborishning boshlangan vaqt: {boshlanish_vaqti}</b>\n'
    text += f"<b>👥 Reklama yuborilgan foydalanuchilar soni:{white_list}</b>\n"
    text += f"<b>🚫Reklama yuborilmagan foydalanuvchilar soni:{black_list}</b>\n"
    text += f'<b>🏁Reklama yuborishning tugash vaqt: {tugash_vaqti}</b>\n'
    await bot.delete_message(chat_id=start_msg.chat.id,message_id=start_msg.message_id)
    await message.answer(text, reply_markup=main_menu_for_super_admin)
    await state.finish()


# ==================== Foydalanuvchliar uchun SEND SUNC TUGADI ============================


#<><><><> ===================Post qo'shish=====================<><><><>
@dp.callback_query_handler(IsSuperAdmin(), text="add_post", state="*")
async def add_post(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text("rasm va textdan iborat post yuboring...\n"
                                 "Yoki Orqaga tugmasini bosing", reply_markup=back_to_main_menu)
    
    await SuperAdminState.SUPER_ADMIN_ADD_POST.set()

from typing import List, Union
# @dp.message_handler(IsSuperAdmin(),state=SuperAdminState.SUPER_ADMIN_ADD_POST,
#                     content_types=types.ContentTypes.ANY)
# @dp.message_handler(is_media_group=True, content_types=types.ContentType.ANY)
# async def add_post_to_social(message: types.Message,state: FSMContext):

#     file = message.content_type
#     niamdir = message.content_type
#     users =  await db.stat()
#     admin_id = message.from_user.id
#     caption = message.caption
    
#     caption_entities = message.caption_entities
#     urls = []

#     for caption_entry in caption_entities:
#         if caption_entry.type == 'text_link':
#             urls.append(caption_entry.url)
#     users = str(users)
#     for x in users:
#         user = await db.select_all_users()
#         for i in user:
#             user_id = i['user_id']
#             try:
#                 await bot.copy_message(
#                     chat_id=user_id,
#                     from_chat_id=message.from_user.id,
#                     message_id=message.message_id,
#                     reply_markup=message.reply_markup
#                 )

#                 time.sleep(0.5)
#             except Exception as e:
#                 await bot.send_message(admin_id, e)

#         # await message.answer("✅ Reklama muvaffaqiyatli yuborildi!", reply_markup=main_menu_for_super_admin)
    
#     channels = await db.channel_stat()
#     channels = str(channels)

#     for y in channels:

#         await message.answer(f"📢 Reklama jo'natish boshlandi...\n"
#                              f"📊 Foydalanuvchilar soni: {x} ta\n"
#                              f"📌 Kanallar soni: {y} ta\n"
#                              f"🕒 Kuting...\n")
#         channels = await db.select_all_channels()
#         for i in channels:
#             channel=i['channel']
#             channel_info = await bot.get_chat(channel)
#             channel = channel_info.id
#             try:
#                 await bot.copy_message(chat_id=channel, from_chat_id=admin_id,
#                                        message_id= message.message_id,reply_markup=message.reply_markup, parse_mode=types.ParseMode.HTML)
                
                
#                 time.sleep(0.5)
#             except Exception as e:
#                 await bot.send_message(admin_id,e)
#         await message.answer("✅ Reklama muvaffaqiyatli yuborildi!", reply_markup=main_menu_for_super_admin)
# # =================== ADD POST ON INSTAGRAM =================================
#         file_type = message.content_type
#         if file_type=='photo':
#             photo = message.photo[-1]
#             file_id = photo.file_id
#             caption = f"\n{message.caption}\n"
#             rasm = await upload_instagram(content_type=file_type,file_id=file_id,photo=photo,caption=caption)


#     await state.finish()


#Media group uchun handler yozdim
async def handle_albums(message: types.Message, album: List[types.Message]):
    """This handler will receive a complete album of any type."""
    media_group = types.MediaGroup()

    for obj in album:
        if obj.photo:
            file_id = obj.photo[-1].file_id
        else:
            file_id = obj[obj.content_type].file_id

        try:
            # We can also add a caption to each file by specifying `"caption": "text"`
            media_group.attach({"media": file_id, "type": obj.content_type})
        except ValueError:
            return await message.answer("This type of album is not supported by aiogram.")

    await message.answer_media_group(media_group)

# Bot Edit Section
@dp.callback_query_handler(IsSuperAdmin(),text='settings',state='*')
async def settings(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text("<b>✏️Nimani o'zgartirmoqchisiz</b>",reply_markup=settings_menu_for_super_admin)


def get_telegram_ids(url):
    pattern = r"https?://t\.me/c/(\d+)/(\d+)"
    match = re.match(pattern, url)
    if match:
        chat_id = match.group(1)
        message_id = match.group(2)
        return f"-100{chat_id}", message_id
    return None, None


# Premium olish uchun handlerlar


# @dp.callback_query_handler(IsSuperAdmin(),text='edit_premium')
# async def edit_premium(call: types.CallbackQuery):
#     await call.answer(cache_time=1)
#     await call.message.edit_text('🟪Premium Olish potini o\'zgartirish uchun,post kanaldan linkini olib menga  yuboring.',reply_markup=back_to_main_menu)
#     await SuperAdminState.SUPER_ADMIN_UPDATE_PREMIUM.set()
# import json
# @dp.message_handler(IsSuperAdmin(),content_types=types.ContentType.TEXT,state=SuperAdminState.SUPER_ADMIN_UPDATE_PREMIUM)
# async def edit__premium(message: types.Message,state:FSMContext):
#     url = message.text
#     channel_id, message_id = get_telegram_ids(url)
       
#     if channel_id and message_id:
#         with open('data.json', 'r') as file:
#             data = json.load(file) 
    
#         if data['primum_post']['message_id'] and data['primum_post']['from_chat_id']:
#             data['primum_post']['message_id']= message_id
#             data['primum_post']['from_chat_id']= channel_id
#             with open('data.json', 'w') as file:
#                 json.dump(data, file, indent=4)
#             await message.answer(text='<b>✅Premium Posti yangilandi</b>',reply_markup=main_menu_for_super_admin)
#             await state.finish()

#         else:
#             await message.answer(text='<b>❌Premium Posti yangilanmadi</b>',reply_markup=main_menu_for_super_admin)
#             await state.finish()
#     else:
#         await message.answer("<b>❌Bot kanalga adminligiga va kanal maxfiy ekanligiga ishonch hosil qiling.</b>",reply_markup=main_menu_for_super_admin)
#         await state.finish()

# Narx uchun handler
@dp.callback_query_handler(IsSuperAdmin(),text='edit_narx')
async def edit_premium(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('📣Premium Narxlari uchun postni kanalga olib menga linkini yuboring.',reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_UPDATE_PREMIUM_PRICE.set()

@dp.message_handler(IsSuperAdmin(),content_types=types.ContentType.TEXT,state=SuperAdminState.SUPER_ADMIN_UPDATE_PREMIUM_PRICE)
async def edit__premium(message: types.Message,state:FSMContext):
    url = message.text
    channel_id, message_id = get_telegram_ids(url)
       
    if channel_id and message_id:
        with open('data.json', 'r') as file:
            data = json.load(file) 
    
        if data['premium_price']['message_id'] and data['premium_price']['from_chat_id']:
            data['premium_price']['message_id']= message_id
            data['premium_price']['from_chat_id']= channel_id
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
            await message.answer(text='<b>✅Premium Narxlari yangilandi</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()

        else:
            await message.answer(text='<b>❌Premium Narxlari yangilanmadi</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()
    else:
        await message.answer("<b>❌Bot kanalga adminligiga va kanal maxfiy ekanligiga ishonch hosil qiling.</b>",reply_markup=main_menu_for_super_admin)
        await state.finish()
    
# Qo'llanma uchun handler


@dp.callback_query_handler(IsSuperAdmin(),text='edit_qollanma')
async def edirt_qollanma(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('📄Qo\'llanma  uchun postni kanalga olib menga linkini yuboring.',reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_UPDATE_QOLLANMA.set()

import json
@dp.message_handler(IsSuperAdmin(),content_types=types.ContentType.TEXT,state=SuperAdminState.SUPER_ADMIN_UPDATE_QOLLANMA)
async def edirt__qollanma(message: types.Message,state:FSMContext):
    url = message.text
    channel_id, message_id = get_telegram_ids(url)
       
    if channel_id and message_id:
        with open('data.json', 'r') as file:
            data = json.load(file) 
    
        if data['get_qollanma']['message_id'] and data['get_qollanma']['from_chat_id']:
            data['get_qollanma']['message_id']= message_id
            data['get_qollanma']['from_chat_id']= channel_id
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
            await message.answer(text='<b>✅Qo\'llanma  yangilandi!</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()

        else:
            await message.answer(text='<b>❌Qo\'llanma  yangilanmadi!</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()
    else:
        await message.answer("<b>❌Bot kanalga adminligiga va kanal maxfiy ekanligiga ishonch hosil qiling.</b>",reply_markup=main_menu_for_super_admin)
        await state.finish()




# <><><><><><><<><><><><><<><<<<>><<><>><<>><><<>><<><><><><><><><><><><>
# ADMIN UCHUN HANDLERLAR

@dp.callback_query_handler(IsSuperAdmin(),text='edit_admin')
async def edirt_administator(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('🧑‍💻Adminni uchun postni kanalga olib menga linkini yuboring.',reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_UPDATE_ADMINS.set()

@dp.message_handler(IsSuperAdmin(),content_types=types.ContentType.TEXT,state=SuperAdminState.SUPER_ADMIN_UPDATE_ADMINS)
async def edirt__administator(message: types.Message,state:FSMContext):
    url = message.text
    channel_id, message_id = get_telegram_ids(url)
       
    if channel_id and message_id:
        with open('data.json', 'r') as file:
            data = json.load(file) 
    
        if data['administator']['message_id'] and data['administator']['from_chat_id']:
            data['administator']['message_id']= message_id
            data['administator']['from_chat_id']= channel_id
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
            await message.answer(text='<b>✅Adminni post yangilandi!</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()

        else:
            await message.answer(text='<b>❌✅Admin post  yangilanmadi!</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()
    else:
        await message.answer("<b>❌Bot kanalga adminligiga va kanal maxfiy ekanligiga ishonch hosil qiling.</b>",reply_markup=main_menu_for_super_admin)
        await state.finish()




# Start uchun handlerlar


@dp.callback_query_handler(IsSuperAdmin(),text='edit_starts')
async def edirt_starts(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('🌟Stars uchun postni kanalga olib menga linkini yuboring.',reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_UPDATE_STARS.set()

@dp.message_handler(IsSuperAdmin(),content_types=types.ContentType.TEXT,state=SuperAdminState.SUPER_ADMIN_UPDATE_STARS)
async def edirt__starts(message: types.Message,state:FSMContext):
    url = message.text
    channel_id, message_id = get_telegram_ids(url)
    if channel_id and message_id:
        with open('data.json', 'r') as file:
            data = json.load(file) 
        if data['get_stars']['message_id'] and data['get_stars']['from_chat_id']:
            data['get_stars']['message_id']= message_id
            data['get_stars']['from_chat_id']= channel_id
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
            await message.answer(text='<b>✅Stars  posti yangilandi!</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()

        else:
            await message.answer(text='<b>❌Stars posti yangilanmadi!</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()
    else:
        await message.answer("<b>❌Bot kanalga adminligiga va kanal maxfiy ekanligiga ishonch hosil qiling.</b>",reply_markup=main_menu_for_super_admin)
        await state.finish()




# Referalning Qiymatini o'zgartirish
from keyboards.inline.main_menu_super_admin import edit_price_button
@dp.callback_query_handler(IsSuperAdmin(),text='edit_ref_sum')
async def edirt_starts(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Qaysi narxni o\'zgartirmoqchisiz?',reply_markup=edit_price_button)


@dp.callback_query_handler(IsSuperAdmin(),text='edit_price_normal')
async def edit_price_normal(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    
    await call.message.edit_text('💴Oddiy Referal Narxini menga yuboring va uni joriy qilaman.\n\nEtibor bering faqat raqamlardan tashkil topsin va va belgilardan iborat bo\'lmasin',reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_UPDATE_REF_SUM_NORMAL.set()

@dp.message_handler(IsSuperAdmin(),content_types=types.ContentType.TEXT,state=SuperAdminState.SUPER_ADMIN_UPDATE_REF_SUM_NORMAL)
async def edit_price__normal(message: types.Message,state:FSMContext):
    ref_sum = message.text
    if ref_sum and ref_sum.isdigit():
        with open('data.json', 'r') as file:
            data = json.load(file) 
        if data['price']['normal_price']:
            data['price']['normal_price'] = ref_sum
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
            await message.answer(text='<b>✅Normal Referal Summasi yangilandi!</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()

        else:
            await message.answer(text='<b>❌Normal Referal Summasiyangilanmadi!</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()
    else:
        await message.answer("<b>❌Bot kanalga adminligiga va kanal maxfiy ekanligiga ishonch hosil qiling.</b>",reply_markup=main_menu_for_super_admin)
        await state.finish()

@dp.callback_query_handler(IsSuperAdmin(),text='edit_price_premium')
async def edit_price_premium(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('💎Premium Referal Narxini menga yuboring va uni joriy qilaman.\n\nEtibor bering faqat raqamlardan tashkil topsin va va belgilardan iborat bo\'lmasin',reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_UPDATE_REF_SUM_PREMIUM.set()

@dp.message_handler(IsSuperAdmin(),content_types=types.ContentType.TEXT,state=SuperAdminState.SUPER_ADMIN_UPDATE_REF_SUM_PREMIUM)
async def edit_price__premium(message: types.Message,state:FSMContext):

    ref_sum = message.text
    if ref_sum and ref_sum.isdigit():
        with open('data.json', 'r') as file:
            data = json.load(file) 
        if data['price']['premium_price']:
            data['price']['premium_price'] = ref_sum
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
            await message.answer(text='<b>✅Premium Referal Summasi yangilandi!</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()

        else:
            await message.answer(text='<b>❌Premium  Referal Summasi yangilanmadi!</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()
    else:
        await message.answer("<b>❌Bot kanalga adminligiga va kanal maxfiy ekanligiga ishonch hosil qiling.</b>",reply_markup=main_menu_for_super_admin)
        await state.finish()


# Premium narxlarini o'zgartirish
@dp.callback_query_handler(IsSuperAdmin(),text='edit_premium_prices')
async def edit_primium_prices(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Qaysi Premium Tarigini o\'zgartirmoqchisiz?',reply_markup=edit_premium_prices())
    


@dp.callback_query_handler(IsSuperAdmin(),text_contains='premium_edit')
async def edit_premium__price(call: types.CallbackQuery,state: FSMContext):
    await state.finish()    
    await call.answer(cache_time=1)
    dataa = call.data.rsplit(":")
    premium_package = dataa[1]
    if premium_package:
        await state.update_data({'package':premium_package})
        await call.message.edit_text('💎Premium Narxini menga yuboring va uni joriy qilaman.\n\nEtibor bering faqat raqamlardan tashkil topsin va va belgilardan iborat bo\'lmasin',reply_markup=back_to_main_menu)
        await SuperAdminState.SUPER_ADMIN_UPDATE_SUM_PREMIUM_MONTH.set()

@dp.message_handler(IsSuperAdmin(),content_types=types.ContentType.TEXT,state=SuperAdminState.SUPER_ADMIN_UPDATE_SUM_PREMIUM_MONTH)
async def change_premium(message: types.Message,state:FSMContext):
    package_data = await state.get_data()
    price = message.text
    if price and price.isdigit():
        package = package_data.get('package')
        with open('data.json','r') as file:
            data = json.load(file)
        if package and package:
            data['premium_prices'][package]=price
            with open('data.json', 'w') as file:
                    json.dump(data, file, indent=4)
            await message.answer(text=f'<b>✅{package.title()} Premium  Summasi yangilandi!</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()
        else:
            await message.answer(text='<b>❌Premium  Referal Summasi yangilanmadi!</b>',reply_markup=main_menu_for_super_admin)
            await state.finish()
    else:
        await message.answer("<b>❌Bot kanalga adminligiga va kanal maxfiy ekanligiga ishonch hosil qiling.</b>",reply_markup=main_menu_for_super_admin)
        await state.finish()



    
    















# Bosh menu
@dp.callback_query_handler(IsSuperAdmin(), text="back_to_main_menu", state="*")
async def back_to_main_menu_method(call: types.CallbackQuery,state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.edit_text(text="👨‍💻 Bosh menyu", reply_markup=main_menu_for_super_admin)
    await state.finish()

from typing import List

# ======== Media GRoup Handler ===============
@dp.message_handler(commands=['yordam'])
async def salom(message: types.Message):
    message_idd = await bot.send_message(chat_id='@urguttoday',text='.')
    time.sleep(2)
    await bot.delete_message(chat_id='@urguttoday',message_id=message_idd.message_id)