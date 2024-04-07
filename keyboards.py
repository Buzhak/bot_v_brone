from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from data import BACK

class Language(CallbackData, prefix='menu'):
    language: str

class Menu(CallbackData, prefix='menu'):
    menu_item: str
    language: str

def language_inline_kb(items: list):
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.add(InlineKeyboardButton(text=item, callback_data=Language(language=item).pack()))
    return builder.as_markup()

def menu_inline_kb(items: dict, prev: str, language: str):
    builder = InlineKeyboardBuilder()
    builder.max_width = 3
    if len(items) > 0:
        for k,v in items.items():
            builder.add(InlineKeyboardButton(text=v, callback_data=Menu(menu_item=k, language=language).pack()))
    builder.row(InlineKeyboardButton(text=BACK[language], callback_data=Menu(menu_item=prev, language=language).pack()))
    return builder.as_markup()
