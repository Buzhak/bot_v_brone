import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject
from aiogram.types import CallbackQuery, Message, InputFile
from contextlib import suppress
from dotenv import load_dotenv

from data import DATA, MAIN_MENU
import keyboards

load_dotenv()

bot = Bot(token=os.getenv('TOKEN'), parse_mode='HTML')
dp = Dispatcher()

async def print_photo(message: Message):
    photo = 'AgACAgIAAxkBAAIHz2YR29clFUjcc-ak-Ay_2hmyPKn4AALa1TEbn_ORSGEYR3prCoGNAQADAgADeQADNAQ'
    await message.answer_photo(photo)


# =====================================START=====================================
@dp.message(Command('start'))
async def start(message: Message):
    await print_photo(message)
    await message.answer('<b>Selectaţi o limbă / Выберите язык</b>', reply_markup=keyboards.language_inline_kb(DATA.keys()))

@dp.message()
async def change_lanuage(message: Message):
    await print_photo(message)
    await message.answer('<b>Selectaţi o limbă / Выберите язык</b>', reply_markup=keyboards.language_inline_kb(DATA.keys()))

@dp.message(F.photo)
async def photo_hendler(message: Message):
    photo_data = message.photo[-1]
    print(photo_data)

@dp.callback_query(keyboards.Language.filter(F.language.in_(DATA.keys())))
async def start_hendler(query: CallbackQuery, callback_data: keyboards.Language):
    await main_menu(query.message, callback_data.language)


# =====================================MAIN MENU=====================================
async def main_menu(message: Message, language):
    title = DATA[language]['main_menu']['title']
    menu = DATA[language]['main_menu']['menu']
    await print_photo(message)
    await message.answer(text=title, reply_markup=keyboards.menu_inline_kb(menu, 'change_lanuage', language))

@dp.callback_query(keyboards.Menu.filter(F.menu_item == 'change_lanuage'))
async def back_main_menu_hendler(query: CallbackQuery, callback_data: keyboards.Menu):
    await change_lanuage(query.message)

@dp.callback_query(keyboards.Menu.filter(F.menu_item.in_(MAIN_MENU)))
async def back_main_menu_hendler(query: CallbackQuery, callback_data: keyboards.Menu):
        await menu(query.message, callback_data)



# =====================================Universal menu=====================================

async def menu(message: Message, data):
    title = DATA[data.language][data.menu_item]['title']
    menu = DATA[data.language][data.menu_item]['menu']
    await print_photo(message)
    await message.answer(title, reply_markup=keyboards.menu_inline_kb(menu, 'main_menu', data.language))

# =====================================About=====================================

@dp.callback_query(keyboards.Menu.filter(F.menu_item == 'main_menu'))
async def about_hendler(query: CallbackQuery, callback_data: keyboards.Menu):
    await main_menu(query.message, callback_data.language)


# =====================================Contacts=====================================

@dp.callback_query(keyboards.Menu.filter(F.menu_item == 'main_menu'))
async def contacts_hendler(query: CallbackQuery, callback_data: keyboards.Menu):
    await main_menu(query.message, callback_data.language)

@dp.callback_query(keyboards.Menu.filter(F.menu_item == 'center'))
async def contacts_hendler(query: CallbackQuery, callback_data: keyboards.Menu):
    await contact_info(query.message, callback_data)

async def contact_info(message: Message, data):
    title = DATA[data.language][data.menu_item]['title']
    menu = DATA[data.language][data.menu_item]['menu']
    lat = DATA[data.language][data.menu_item]['lat']
    lon = DATA[data.language][data.menu_item]['lon']
    await message.answer_location(latitude=lat, longitude=lon)
    await message.answer(title, reply_markup=keyboards.menu_inline_kb(menu, 'main_menu', data.language))
    


# =====================================MAIN=====================================
async def main():
    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())