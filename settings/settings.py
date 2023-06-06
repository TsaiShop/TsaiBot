"""
Файл содержащий Token бота и данные для подключения к БД

sudo apt-get install zbar-tools
"""

import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Файл .env.example отсутствует')
else:
    load_dotenv()

"""Токен бота"""
TOKEN = os.environ.get('TOKEN')

"""База данных"""
DATABASE = os.environ.get('DATABASE')
USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD')
HOST = os.environ.get('HOST')
PORT = os.environ.get('PORT')

"""Поддержка"""
SUPPORT = os.environ.get('SUPPORT')
CHANNEL = os.environ.get('CHANNEL')
BOT_NAME = os.environ.get('BOT_NAME')

"""Контакты"""
TELEGRAM = os.environ.get('BOT_NAME')
TELEGRAM_CHANNEL = os.environ.get('BOT_NAME')
WEB_SITE = os.environ.get('BOT_NAME')
INSTAGRAM = os.environ.get('BOT_NAME')
FACEBOOK = os.environ.get('BOT_NAME')
