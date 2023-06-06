import string
import random
from datetime import datetime, timedelta
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from handlers.echo import delete_message
from keyboards import key_text
from keyboards.keyboards import balance_keyboard
from loader import bot, exception_state_decorator, values
from settings import constants
from database.models import *


def generate_alphanum_random_string(length) -> str:
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.sample(letters_and_digits, length))


@exception_state_decorator
async def current_rate_handler(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - обраатывает нажатие на кнопку current_rate
    :param state: FSMContext
    :param message: Message
    :return: None
    """
    if await state.get_state():
        await state.finish()
    user = Users.get_or_none(Users.user_id == message.from_user.id)
    if user.username != message.from_user.username:
        user.username = message.from_user.username
        user.save()
    await delete_message(message.from_user.id)
    await message.delete()
    currency = Courses.get(Courses.variable == 'Покупка')
    rub_currency = Courses.get(Courses.variable == 'Курс RUB')
    current_date = datetime.today() + timedelta(hours=4)
    str_date = current_date.strftime('%d.%m.%Y %H:%M')
    bot_message = await bot.send_message(
        message.from_user.id, constants.CURRENT_RATE[user.lang].format(
            str_date, currency.value,
            round(currency.value / (100 + currency.percent) * (100 + (currency.percent + 0.5)), 3),
            round(currency.value / (100 + currency.percent) * (100 + (currency.percent + 0.75)), 3),
            round(currency.value / (100 + currency.percent) * (100 + (currency.percent + 1)), 3),
            rub_currency.value,
            round(rub_currency.value / (100 + rub_currency.percent) * (100 + (rub_currency.percent - 0.5)), 3),
            round(rub_currency.value / (100 + rub_currency.percent) * (100 + (rub_currency.percent - 0.75)), 3),
            round(rub_currency.value / (100 + rub_currency.percent) * (100 + (rub_currency.percent - 1)), 3),
        ),
        reply_markup=await balance_keyboard(user.lang)
    )
    DeleteMessage(chat_id=message.from_user.id, message_id=str(bot_message.message_id)).save()


@exception_state_decorator
async def my_balance_handler(message: types.CallbackQuery, state: FSMContext) -> None:
    """
    Хэндлер - обарбатывает нажатие на кнопку my_balance
    :param state: FSMContext
    :param message: Message
    :return: None
    """
    if await state.get_state():
        await state.finish()
    user = Users.get_or_none(Users.user_id == message.from_user.id)
    if user:
        if user.username != message.from_user.username:
            user.username = message.from_user.username
            user.save()
        await delete_message(message.from_user.id)
        cur_date = (datetime.today() + timedelta(hours=4)).date()
        qr_limit = Courses.get_or_none(Courses.variable == 'QR payment').percent
        bank_limit = Courses.get_or_none(Courses.variable == 'Bank Transfer').percent
        prom_limit = Courses.get_or_none(Courses.variable == 'PromtPay').percent
        qr_user = Limits.get_or_none(Limits.pay == 'QR payment', Limits.user == user.id)
        if qr_user:
            if qr_user.created_at != cur_date:
                qr_user.amount = 0
                qr_user.save()
                qr_temp = qr_limit
            else:
                qr_temp = qr_limit - qr_user.amount
        else:
            qr_temp = qr_limit
        bank_user = Limits.get_or_none(Limits.pay == 'Bank Transfer', Limits.user == user.id)
        if bank_user:
            if bank_user.created_at != cur_date:
                bank_user.amount = 0
                bank_user.save()
                bank_temp = bank_limit
            else:
                bank_temp = bank_limit - bank_user.amount
        else:
            bank_temp = bank_limit
        prom_user = Limits.get_or_none(Limits.pay == 'PromtPay', Limits.user == user.id)
        if prom_user:
            if prom_user.created_at != cur_date:
                prom_user.amount = 0
                prom_user.save()
                prom_temp = prom_limit
            else:
                prom_temp = prom_limit - prom_user.amount
        else:
            prom_temp = prom_limit
        bot_message = await bot.send_message(
            message.from_user.id,
            constants.BALANCE[user.lang].format(
                message.from_user.id, round(user.balance, 2), round(user.ref_balance, 2),
                cur_date.strftime('%d.%m.%Y'), qr_temp, bank_temp, prom_temp
            ),
            reply_markup=await balance_keyboard(user.lang)
        )
        DeleteMessage(chat_id=message.from_user.id, message_id=str(bot_message.message_id)).save()


def register_short_command_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(current_rate_handler, Text(values(key_text.CURRENT_RATE)), state='*')
    dp.register_callback_query_handler(my_balance_handler, Text(values(key_text.MY_BALANCE)), state='*')
