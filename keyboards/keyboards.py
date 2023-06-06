from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from keyboards import key_text
from settings import settings


async def language_keyboard(flag: bool = True, lang=None) -> InlineKeyboardMarkup:
    """
    Клавиатура выбора языка
    :return:
    """
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(key_text.ENGLISH, callback_data=key_text.ENGLISH),
        InlineKeyboardButton(key_text.RUSSIAN, callback_data=key_text.RUSSIAN),
    )
    if flag:
        return keyboard.add(InlineKeyboardButton(text=key_text.MENU[lang], callback_data=key_text.BACK_START))
    else:
        return keyboard


async def user_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    """
    Клавиатура верхнего меню зарегистрированного пользователя
    :return: InlineKeyboardMarkup
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    return keyboard.add(
        InlineKeyboardButton(text=key_text.MY_BALANCE[lang], callback_data=key_text.MY_BALANCE[lang]),
        InlineKeyboardButton(text=key_text.HISTORY[lang], callback_data=key_text.HISTORY[lang]),
    )


async def menu_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """
    Клавиатура нижнего меню зарегистрированного пользователя
    :return: ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    return keyboard.add(
        KeyboardButton(text=key_text.CONTACTS[lang]),
        KeyboardButton(text=key_text.CURRENT_RATE[lang]),
        KeyboardButton(text=key_text.HOW_ITS_WORK[lang]),
        KeyboardButton(text=key_text.SHARE[lang]),
        KeyboardButton(text=key_text.LANGUAGE[lang])
    )


async def contacts_keyboard(lang: str) -> InlineKeyboardMarkup:
    """
    Клавиатура меню контактов
    :return: InlineKeyboardMarkup
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    return keyboard.add(
        InlineKeyboardButton(text=key_text.TELEGRAM[lang], url=settings.TELEGRAM),
        InlineKeyboardButton(text=key_text.TELEGRAM_CHANNEL[lang], url=settings.TELEGRAM_CHANNEL),
        InlineKeyboardButton(text=key_text.WEB_SITE[lang], url=settings.WEB_SITE),
        InlineKeyboardButton(text=key_text.INSTAGRAM[lang], url=settings.INSTAGRAM),
        InlineKeyboardButton(text=key_text.FACEBOOK[lang], url=settings.FACEBOOK),
        InlineKeyboardButton(text=key_text.BACK[lang], callback_data=key_text.BACK_START),
    )


async def back_keyboard(key: str, lang: str) -> InlineKeyboardMarkup:
    """
    Клавиатура возврата. Принимает значение, для понимания, куда нужно возвращаться
    :param lang: str
    :param key: str
    :return: InlineKeyboardMarkup
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    return keyboard.add(
        InlineKeyboardButton(text=key_text.BACK[lang], callback_data=key)
    )


async def balance_keyboard(lang: str) -> InlineKeyboardMarkup:
    """
    Клавиатура меню баланса и текущего курса
    :return: InlineKeyboardMarkup
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    return keyboard.add(
        InlineKeyboardButton(text=key_text.BACK[lang], callback_data=key_text.BACK_START)
    )


async def history_back_keyboard(key: str, lang: str) -> InlineKeyboardMarkup:
    """
    Клавиатура возврата из меню истории
    :return: InlineKeyboardMarkup
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    return keyboard.add(
        InlineKeyboardButton(text=key_text.BACK[lang], callback_data=key),
        InlineKeyboardButton(text=key_text.MENU[lang], callback_data=key_text.BACK_START),
    )


async def history_keyboard(lang: str) -> InlineKeyboardMarkup:
    """
    Клавиатура меню Истории
    :return: InlineKeyboardMarkup
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    return keyboard.add(
        InlineKeyboardButton(text=key_text.HISTORY_DEP[lang], callback_data=key_text.HISTORY_DEP[lang]),
        InlineKeyboardButton(text=key_text.HISTORY_RUB[lang], callback_data=key_text.HISTORY_RUB[lang]),
        InlineKeyboardButton(text=key_text.HISTORY_QR[lang], callback_data=key_text.HISTORY_QR[lang]),
        InlineKeyboardButton(text=key_text.HISTORY_BANK[lang], callback_data=key_text.HISTORY_BANK[lang]),
        InlineKeyboardButton(text=key_text.MENU[lang], callback_data=key_text.BACK_START),
    )


async def history_paginate_keyboard(text: str, num_page: int, end: int, lang: str, start=1) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    if start == end:
        return keyboard.add(InlineKeyboardButton(key_text.MENU[lang], callback_data=key_text.BACK_START))
    elif num_page == start:
        left = end
        right = num_page + 1
    elif num_page == end:
        left = num_page - 1
        right = start
    else:
        left = num_page - 1
        right = num_page + 1
    return keyboard.add(
        InlineKeyboardButton(text='⬅️', callback_data=f"{text}&{left}"),
        InlineKeyboardButton(text='➡️', callback_data=f"{text}&{right}"),
        InlineKeyboardButton(key_text.BACK[lang], callback_data=key_text.HISTORY[lang]),
        InlineKeyboardButton(key_text.MENU[lang], callback_data=key_text.BACK_START)
    )
