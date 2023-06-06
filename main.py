"""Файл для запуска бота. Содержит в себе все регистраторы приложения"""
from aiogram import Dispatcher
from loader import dp
from aiogram.utils import executor
from handlers import start, short_command, echo, history


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        []
    )


start.register_start_handlers(dp)
short_command.register_short_command_handlers(dp)
history.register_history_handlers(dp)
echo.register_echo_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=set_default_commands, skip_updates=True)
