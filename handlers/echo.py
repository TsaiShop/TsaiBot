"""
Файл - содержит хэндлер для отлова сообщений вне сценария
"""
from aiogram import Dispatcher, types
from loader import logger, bot, exception_decorator
from database.models import *


async def delete_message(user_id: int) -> None:
    """
    Функция - обрабатывает удаление сообщений
    :param user_id: int
    :return: None
    """
    try:
        message = DeleteMessage.select().where(DeleteMessage.chat_id == user_id)
        if len(message):
            for mess in message:
                if '&' in mess.message_id:
                    mes_ids = mess.message_id.split('&')
                    for elem in mes_ids:
                        try:
                            await bot.delete_message(chat_id=mess.chat_id, message_id=int(elem))
                        except Exception:
                            pass
                else:
                    try:
                        await bot.delete_message(chat_id=mess.chat_id, message_id=int(mess.message_id))
                    except Exception:
                        pass
                try:
                    mess.delete_instance()
                except Exception:
                    pass
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def delete_menu(user_id: int) -> None:
    """
    Функция - обрабатывает удаление сообщений меню
    :param user_id: int
    :return: None
    """
    try:
        mess = DeleteMenu.get_or_none(DeleteMenu.chat_id == user_id)
        if mess:
            try:
                await bot.delete_message(chat_id=mess.chat_id, message_id=int(mess.message_id))
            except Exception:
                pass
            try:
                mess.delete_instance()
            except Exception:
                pass
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


@exception_decorator
async def echo_handler(message: types.Message) -> None:
    """
    Хэндлер - оповещает бота о некорректной команде (Эхо)
    :param message: Message
    :return: None
    """
    await message.delete()


def register_echo_handlers(dp: Dispatcher) -> None:
    """
    Функция - регистрирует все хэндлеры файла echo.py
    :param dp: Dispatcher
    :return: None
    """
    dp.register_message_handler(echo_handler)
