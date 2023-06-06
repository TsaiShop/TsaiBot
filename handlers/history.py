from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from handlers.echo import delete_message
from keyboards import key_text
from keyboards.keyboards import history_keyboard, history_back_keyboard, history_paginate_keyboard
from loader import bot, exception_decorator, values
from settings import constants
from database.models import *


@exception_decorator
async def history_handler(call: types.CallbackQuery) -> None:
    """
    Хэндлер - обарбатывает нажатие на кнопку history
    :param call: CallbackQuery
    :return: None
    """
    await delete_message(call.from_user.id)
    user = Users.get_or_none(Users.user_id == call.from_user.id)
    if user.username != call.from_user.username:
        user.username = call.from_user.username
        user.save()
    bot_message = await bot.send_message(
        call.from_user.id, constants.HISTORY[user.lang], reply_markup=await history_keyboard(user.lang)
    )
    DeleteMessage(chat_id=call.from_user.id, message_id=str(bot_message.message_id)).save()


@exception_decorator
async def dep_history_handler(call: types.CallbackQuery) -> None:
    """
    Хэндлер - обрабатывает нажатие на кнопку dep_history
    :param call: CallbackQuery
    :return: None
    """
    await delete_message(call.from_user.id)
    user = Users.get(Users.user_id == call.from_user.id)
    count = Deposit.select().where(Deposit.status != 'waiting for payment', Deposit.user == user.id).count()
    if count > 0:
        dep = Deposit.select().where(
            Deposit.status != 'waiting for payment', Deposit.user == user.id).order_by(Deposit.created_at.desc()).paginate(1, 1)
        str_date = dep[0].created_at.strftime('%d.%m.%Y %H:%M')
        if user.lang == 'EN':
            status = dep[0].status
        else:
            if dep[0].status == 'waiting for deposit ⏱':
                status = 'Ожидание депозита ⏱'
            elif dep[0].status == 'cancel ❌':
                status = 'Отменен ❌'
            elif dep[0].status == 'error':
                status = 'Ошибка'
            else:
                status = 'Успешный ✅'
        if dep[0].amount == 0.0:
            template = constants.FALSE_DEP_HISTORY[user.lang].format(
                dep[0].id, str_date, dep[0].usdt, status
            )
        else:
            template = constants.TRUE_DEP_HISTORY[user.lang].format(
                dep[0].id, str_date, dep[0].usdt, dep[0].amount, dep[0].thb_amount, status
            )
        bot_message = await bot.send_message(
            call.from_user.id, template, reply_markup=await history_paginate_keyboard('pag_dep', 1, count, user.lang)
        )
        DeleteMessage(chat_id=call.from_user.id, message_id=str(bot_message.message_id)).save()
    else:
        bot_message = await bot.send_message(
            call.from_user.id, constants.EMPTY_HISTORY[user.lang], reply_markup=await history_back_keyboard(key_text.HISTORY[user.lang], user.lang)
        )
        DeleteMessage(chat_id=call.from_user.id, message_id=str(bot_message.message_id)).save()


@exception_decorator
async def dep_history_paginate_handler(call: types.CallbackQuery) -> None:
    """
    Хэндлер - обрабатывает нажатие на кнопку pag_dep, пагинацию
    :param call: CallbackQuery
    :return: None
    """
    num_page = int(call.data.split('&')[1])
    await delete_message(call.from_user.id)
    user = Users.get(Users.user_id == call.from_user.id)
    count = Deposit.select().where(Deposit.status != 'waiting for payment', Deposit.user == user.id).count()
    dep = Deposit.select().where(
        Deposit.status != 'waiting for payment', Deposit.user == user.id).order_by(Deposit.created_at.desc()).paginate(num_page, 1)
    str_date = dep[0].created_at.strftime('%d.%m.%Y %H:%M')
    if user.lang == 'EN':
        status = dep[0].status
    else:
        if dep[0].status == 'waiting for deposit ⏱':
            status = 'Ожидание депозита ⏱'
        elif dep[0].status == 'cancel ❌':
            status = 'Отменен ❌'
        elif dep[0].status == 'error':
            status = 'Ошибка'
        else:
            status = 'Успешный ✅'
    if dep[0].amount == 0.0:
        template = constants.FALSE_DEP_HISTORY[user.lang].format(
            dep[0].id, str_date, dep[0].usdt, status
        )
    else:
        template = constants.TRUE_DEP_HISTORY[user.lang].format(
            dep[0].id, str_date, dep[0].usdt, dep[0].amount, dep[0].thb_amount, status
        )
    bot_message = await bot.send_message(
        call.from_user.id, template, reply_markup=await history_paginate_keyboard('pag_dep', num_page, count, user.lang)
    )
    DeleteMessage(chat_id=call.from_user.id, message_id=str(bot_message.message_id)).save()


@exception_decorator
async def qr_history_handler(call: types.CallbackQuery) -> None:
    """
    Хэндлер - обрабатывает нажатие на кнопку qr_history
    :param call: CallbackQuery
    :return: None
    """
    await delete_message(call.from_user.id)
    user = Users.get(Users.user_id == call.from_user.id)
    count = PayQR.select().where(PayQR.status == True, PayQR.user == user.id).count()
    if count > 0:
        pay = PayQR.select().where(PayQR.status == True, PayQR.user == user.id).order_by(PayQR.created_at.desc()).paginate(1, 1)
        str_date = pay[0].created_at.strftime('%d.%m.%Y %H:%M')
        template = constants.QR_HISTORY[user.lang].format(pay[0].id, str_date, pay[0].amount)
        bot_message = await bot.send_photo(
            call.from_user.id, photo=open(f'../thai/media/{pay[0].cheque}', 'rb'), caption=template,
            reply_markup=await history_paginate_keyboard('pag_qr', 1, count, user.lang)
        )
        DeleteMessage(chat_id=call.from_user.id, message_id=str(bot_message.message_id)).save()
    else:
        bot_message = await bot.send_message(
            call.from_user.id, constants.EMPTY_HISTORY[user.lang], reply_markup=await history_back_keyboard(key_text.HISTORY[user.lang], user.lang)
        )
        DeleteMessage(chat_id=call.from_user.id, message_id=str(bot_message.message_id)).save()


@exception_decorator
async def qr_history_paginate_handler(call: types.CallbackQuery) -> None:
    """
    Хэндлер - обрабатывает нажатие на кнопку pag_qr, пагинацию
    :param call: CallbackQuery
    :return: None
    """
    num_page = int(call.data.split('&')[1])
    await delete_message(call.from_user.id)
    user = Users.get(Users.user_id == call.from_user.id)
    count = PayQR.select().where(PayQR.status == True, PayQR.user == user.id).count()
    pay = PayQR.select().where(PayQR.status == True, PayQR.user == user.id).order_by(PayQR.created_at.desc()).paginate(num_page, 1)
    str_date = pay[0].created_at.strftime('%d.%m.%Y %H:%M')
    template = constants.QR_HISTORY[user.lang].format(pay[0].id, str_date, pay[0].amount)
    bot_message = await bot.send_photo(
        call.from_user.id, photo=open(f'../thai/media/{pay[0].cheque}', 'rb'), caption=template,
        reply_markup=await history_paginate_keyboard('pag_qr', num_page, count, user.lang)
    )
    DeleteMessage(chat_id=call.from_user.id, message_id=str(bot_message.message_id)).save()


@exception_decorator
async def bank_history_handler(call: types.CallbackQuery) -> None:
    """
    Хэндлер - обрабатывает нажатие на кнопку bank_history
    :param call: CallbackQuery
    :return: None
    """
    await delete_message(call.from_user.id)
    user = Users.get(Users.user_id == call.from_user.id)
    count = PayBank.select().where(PayBank.status == True, PayBank.user == user.id).count()
    if count > 0:
        pay = PayBank.select().where(PayBank.status == True, PayBank.user == user.id).order_by(PayBank.created_at.desc()).paginate(1, 1)
        str_date = pay[0].created_at.strftime('%d.%m.%Y %H:%M')
        template = constants.BANK_HISTORY[user.lang].format(pay[0].id, str_date, pay[0].bank, pay[0].amount, pay[0].address)
        bot_message = await bot.send_photo(
            call.from_user.id, photo=open(f'../thai/media/{pay[0].cheque}', 'rb'), caption=template,
            reply_markup=await history_paginate_keyboard('pag_bank', 1, count, user.lang)
        )
        DeleteMessage(chat_id=call.from_user.id, message_id=str(bot_message.message_id)).save()
    else:
        bot_message = await bot.send_message(
            call.from_user.id, constants.EMPTY_HISTORY[user.lang], reply_markup=await history_back_keyboard(key_text.HISTORY[user.lang], user.lang)
        )
        DeleteMessage(chat_id=call.from_user.id, message_id=str(bot_message.message_id)).save()


@exception_decorator
async def bank_history_paginate_handler(call: types.CallbackQuery) -> None:
    """
    Хэндлер - обрабатывает нажатие на кнопку bank_history
    :param call: CallbackQuery
    :return: None
    """
    num_page = int(call.data.split('&')[1])
    await delete_message(call.from_user.id)
    user = Users.get(Users.user_id == call.from_user.id)
    count = PayBank.select().where(PayBank.status == True, PayBank.user == user.id).count()
    pay = PayBank.select().where(PayBank.status == True, PayBank.user == user.id).order_by(PayBank.created_at.desc()).paginate(num_page, 1)
    str_date = pay[0].created_at.strftime('%d.%m.%Y %H:%M')
    template = constants.BANK_HISTORY[user.lang].format(pay[0].id, str_date, pay[0].bank, pay[0].amount, pay[0].address)
    bot_message = await bot.send_photo(
        call.from_user.id, photo=open(f'../thai/media/{pay[0].cheque}', 'rb'), caption=template,
        reply_markup=await history_paginate_keyboard('pag_bank', num_page, count, user.lang)
    )
    DeleteMessage(chat_id=call.from_user.id, message_id=str(bot_message.message_id)).save()


@exception_decorator
async def rub_dep_history_handler(call: types.CallbackQuery) -> None:
    """
    Хэндлер - обрабатывает нажатие на кнопку rub_dep_history
    :param call: CallbackQuery
    :return: None
    """
    await delete_message(call.from_user.id)
    user = Users.get(Users.user_id == call.from_user.id)
    count = DepositsRub.select().where(DepositsRub.status != 'waiting for payment', DepositsRub.user == user.id).count()
    if count > 0:
        dep = DepositsRub.select().where(
            DepositsRub.status != 'waiting for payment', DepositsRub.user == user.id).order_by(DepositsRub.created_at.desc()).paginate(1, 1)
        str_date = dep[0].created_at.strftime('%d.%m.%Y %H:%M')
        if user.lang == 'EN':
            bank = 'Sberbank' if dep[0].bank == 'Sber' else 'Tinkoff'
        else:
            bank = 'Сбербанк' if dep[0].bank == 'Sber' else 'Тинькофф'
        if user.lang == 'EN':
            status = dep[0].status
        else:
            if dep[0].status == 'waiting for deposit ⏱':
                status = 'Ожидание депозита ⏱'
            elif dep[0].status == 'cancel ❌':
                status = 'Отменен ❌'
            elif dep[0].status == 'error':
                status = 'Ошибка'
            else:
                status = 'Успешный ✅'
        template = constants.RUB_DEP_HISTORY[user.lang].format(
            dep[0].order, str_date, bank, dep[0].amount, dep[0].thb_amount, status
        )
        bot_message = await bot.send_message(
            call.from_user.id, template, reply_markup=await history_paginate_keyboard('rub_pag_dep', 1, count, user.lang)
        )
        DeleteMessage(chat_id=call.from_user.id, message_id=str(bot_message.message_id)).save()
    else:
        bot_message = await bot.send_message(
            call.from_user.id, constants.EMPTY_HISTORY[user.lang], reply_markup=await history_back_keyboard(key_text.HISTORY[user.lang], user.lang)
        )
        DeleteMessage(chat_id=call.from_user.id, message_id=str(bot_message.message_id)).save()


@exception_decorator
async def rub_dep_history_paginate_handler(call: types.CallbackQuery) -> None:
    """
    Хэндлер - обрабатывает нажатие на кнопку rub_pag_dep, пагинацию
    :param call: CallbackQuery
    :return: None
    """
    num_page = int(call.data.split('&')[1])
    await delete_message(call.from_user.id)
    user = Users.get(Users.user_id == call.from_user.id)
    count = DepositsRub.select().where(DepositsRub.status != 'waiting for payment', DepositsRub.user == user.id).count()
    dep = DepositsRub.select().where(
        DepositsRub.status != 'waiting for payment', DepositsRub.user == user.id).order_by(DepositsRub.created_at.desc()).paginate(num_page, 1)
    str_date = dep[0].created_at.strftime('%d.%m.%Y %H:%M')
    if user.lang == 'EN':
        bank = 'Sberbank' if dep[0].bank == 'Sber' else 'Tinkoff'
    else:
        bank = 'Сбербанк' if dep[0].bank == 'Sber' else 'Тинькофф'
    if user.lang == 'EN':
        status = dep[0].status
    else:
        if dep[0].status == 'waiting for deposit ⏱':
            status = 'Ожидание депозита ⏱'
        elif dep[0].status == 'cancel ❌':
            status = 'Отменен ❌'
        elif dep[0].status == 'error':
            status = 'Ошибка'
        else:
            status = 'Успешный ✅'
    template = constants.RUB_DEP_HISTORY[user.lang].format(
        dep[0].order, str_date, bank, dep[0].amount, dep[0].thb_amount, status
    )
    bot_message = await bot.send_message(
        call.from_user.id, template, reply_markup=await history_paginate_keyboard('rub_pag_dep', num_page, count, user.lang)
    )
    DeleteMessage(chat_id=call.from_user.id, message_id=str(bot_message.message_id)).save()


def register_history_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(history_handler, Text(values(key_text.HISTORY)), state=None)
    dp.register_callback_query_handler(dep_history_handler, Text(values(key_text.HISTORY_DEP)), state=None)
    dp.register_callback_query_handler(rub_dep_history_handler, Text(values(key_text.HISTORY_RUB)), state=None)
    dp.register_callback_query_handler(qr_history_handler, Text(values(key_text.HISTORY_QR)), state=None)
    dp.register_callback_query_handler(bank_history_handler, Text(values(key_text.HISTORY_BANK)), state=None)
    dp.register_callback_query_handler(dep_history_paginate_handler, Text(startswith='pag_dep'), state=None)
    dp.register_callback_query_handler(rub_dep_history_paginate_handler, Text(startswith='rub_pag_dep'), state=None)
    dp.register_callback_query_handler(qr_history_paginate_handler, Text(startswith='pag_qr'), state=None)
    dp.register_callback_query_handler(bank_history_paginate_handler, Text(startswith='pag_bank'), state=None)
