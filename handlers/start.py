"""
Файл с хэндлерами старт/хэлп и регистрация
"""

import re
from datetime import datetime, timedelta
from typing import Union
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from handlers.echo import delete_message, delete_menu
from keyboards import key_text
from keyboards.keyboards import user_menu_keyboard, back_keyboard, contacts_keyboard, menu_keyboard, language_keyboard
from loader import bot, exception_state_decorator, values
from database.models import *
from settings import constants


@exception_state_decorator
async def start_command(message: Union[types.Message, types.CallbackQuery], state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает команду /start. В зависимости от сценария выводит определенное меню.
    :param state: FSMContext
    :param message: Union[types.Message, types.CallbackQuery]
    :return: None
    """
    if await state.get_state():
        await state.finish()
    user = Users.get_or_none(Users.user_id == message.from_user.id)
    await delete_message(message.from_user.id)
    await delete_menu(message.from_user.id)
    if user is None:
        if isinstance(message, types.Message):
            if re.findall(r'\d+', message.text):
                friend = int(re.findall(r'\b\d+\b', message.text)[0])
                parent = Users.get_or_none(Users.user_id == friend)
                if parent:
                    parent.referrals += 1
                    parent.save()
                    Users(
                        user_id=message.from_user.id, created_at=datetime.today() + timedelta(hours=4), username=message.from_user.username,
                        friend=parent.user_id, active=False
                    ).save()
            elif " " in message.text:
                links = LinkValues.select()
                match_text = None
                if len(links) > 0:
                    text = message.text.split(' ')[1]
                    for link in links:
                        if link.text == text:
                            link.count += 1
                            link.save()
                            match_text = link.text
                Users(
                    user_id=message.from_user.id, created_at=datetime.today() + timedelta(hours=4), username=message.from_user.username, active=False,
                    link=match_text
                ).save()
            else:
                Users(
                    user_id=message.from_user.id, created_at=datetime.today() + timedelta(hours=4), username=message.from_user.username, active=False
                ).save()
        else:
            Users(
                user_id=message.from_user.id, created_at=datetime.today() + timedelta(hours=4), username=message.from_user.username, active=False
            ).save()
        bot_message = await bot.send_message(message.from_user.id, constants.LANGUAGE, reply_markup=await language_keyboard(False))
        DeleteMessage(chat_id=message.from_user.id, message_id=str(bot_message.message_id)).save()
    else:
        user = Users.get_or_none(Users.user_id == message.from_user.id)
        if user.username != message.from_user.username:
            user.username = message.from_user.username
            user.save()
        bot_message = await bot.send_photo(
            message.from_user.id, photo=open('media/banner1.png', 'rb'), reply_markup=await menu_keyboard(user.lang)
        )
        save_message = await bot.send_message(
            message.from_user.id, constants.LOGIN_MENU[user.lang], reply_markup=await user_menu_keyboard(user.lang)
        )
        DeleteMessage(chat_id=message.from_user.id, message_id=f'{save_message.message_id}').save()
        DeleteMenu(chat_id=message.from_user.id, message_id=f'{bot_message.message_id}').save()


@exception_state_decorator
async def language_handler(call: Union[types.CallbackQuery, types.Message], state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает нажатие на кнопку language
    :param call:CallbackQuery
    :param state:FSMContext
    :return:None
    """
    if await state.get_state():
        await state.finish()
    if isinstance(call, types.Message):
        await call.delete()
    user = Users.get_or_none(Users.user_id == call.from_user.id)
    await delete_message(call.from_user.id)
    bot_message = await bot.send_message(call.from_user.id, constants.LANGUAGE, reply_markup=await language_keyboard(lang=user.lang))
    DeleteMessage(chat_id=call.from_user.id, message_id=str(bot_message.message_id)).save()


@exception_state_decorator
async def set_language_handler(call: types.CallbackQuery, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает нажатие на один из языков. Устанавливает для пользователя новое значение языка
    :param state: FSMContext
    :param call: CallbackQuery
    :return: None
    """
    user = Users.get_or_none(Users.user_id == call.from_user.id)
    if user:
        user.lang = 'EN' if call.data == key_text.ENGLISH else 'RU'
        user.save()
    else:
        Users(user_id=call.from_user.id, created_at=datetime.today(), username=call.from_user.username, lang='EN' if call.data == key_text.ENGLISH else 'RU').save()
    await start_command(call, state)


@exception_state_decorator
async def how_its_work_handler(call: Union[types.CallbackQuery, types.Message], state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает нажатие на кнопку how_its_work
    :param state: FSMContext
    :param call: CallbackQuery,Message
    :return: None
    """
    if await state.get_state():
        await state.finish()
    user = Users.get_or_none(Users.user_id == call.from_user.id)
    await delete_message(call.from_user.id)
    if isinstance(call, types.Message):
        await call.delete()
    technical_qr = TechnicalBreaks.get_or_none(TechnicalBreaks.variable == 'pay_qr')
    technical_bank = TechnicalBreaks.get_or_none(TechnicalBreaks.variable == 'bank_transfer')
    bot_message = await bot.send_message(
        call.from_user.id,
        constants.HOW_ITS_WORK[user.lang].format(
            technical_qr.start_time.strftime('%H:%M'), technical_qr.end_time.strftime('%H:%M'),
            technical_bank.start_time.strftime('%H:%M'), technical_bank.end_time.strftime('%H:%M'),
        ),
        reply_markup=await back_keyboard(key_text.BACK_START, user.lang)
    )
    DeleteMessage(chat_id=call.from_user.id, message_id=str(bot_message.message_id)).save()


@exception_state_decorator
async def contacts_handler(call: Union[types.CallbackQuery, types.Message], state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает нажатие на кнопку contacts
    :param state: FSMContext
    :param call: CallbackQuery, Message
    :return: None
    """
    if await state.get_state():
        await state.finish()
    user = Users.get_or_none(Users.user_id == call.from_user.id)
    await delete_message(call.from_user.id)
    if isinstance(call, types.Message):
        await call.delete()
    bot_message = await bot.send_message(
        call.from_user.id, constants.CONTACTS[user.lang], reply_markup=await contacts_keyboard(user.lang)
    )
    DeleteMessage(chat_id=call.from_user.id, message_id=str(bot_message.message_id)).save()


@exception_state_decorator
async def share_handler(call: Union[types.CallbackQuery, types.Message], state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает нажатие на кнопку share
    :param state: FSMContext
    :param call: CallbackQuery, Message
    :return: None
    """
    if await state.get_state():
        await state.finish()
    user = Users.get_or_none(Users.user_id == call.from_user.id)
    await delete_message(call.from_user.id)
    if isinstance(call, types.Message):
        await call.delete()
    bot_message = await bot.send_message(call.from_user.id, constants.SHARE[user.lang].format(call.from_user.id), disable_web_page_preview=True)
    save_message = await bot.send_message(
        call.from_user.id, constants.SHARE_DESCR[user.lang], reply_markup=await back_keyboard(key_text.BACK_START, user.lang)
    )
    DeleteMessage(chat_id=call.from_user.id, message_id=f"{bot_message.message_id}&{save_message.message_id}").save()


def register_start_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(start_command, commands=['start'], state='*')
    dp.register_callback_query_handler(start_command, Text(key_text.BACK_START), state='*')
    dp.register_callback_query_handler(how_its_work_handler, Text(values(key_text.HOW_ITS_WORK)), state='*')
    dp.register_message_handler(how_its_work_handler, Text(values(key_text.HOW_ITS_WORK)), state='*')
    dp.register_callback_query_handler(share_handler, Text(values(key_text.SHARE)), state='*')
    dp.register_message_handler(share_handler, Text(values(key_text.SHARE)), state='*')
    dp.register_callback_query_handler(contacts_handler, Text(values(key_text.CONTACTS)), state='*')
    dp.register_message_handler(contacts_handler, Text(values(key_text.CONTACTS)), state='*')
    dp.register_message_handler(language_handler, Text(values(key_text.LANGUAGE)), state='*')
    dp.register_callback_query_handler(language_handler, Text(values(key_text.LANGUAGE)), state='*')
    dp.register_callback_query_handler(set_language_handler, Text([key_text.ENGLISH, key_text.RUSSIAN]), state='*')
