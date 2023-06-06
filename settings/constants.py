"""
Файл - для общей замены сообщений в боте
"""

"""start.py"""
LANGUAGE = '🇺🇸Please select the language\n🇷🇺Пожалуйста выберите язык'
WELCOME = {
    'EN': 'Hello!\nTsai is an automated QR payment service.\nCreate a wallet within a minute and pay via QR codes anywhere in Thailand',
    'RU': 'Приветствуем!\nTsai - автоматизированная платежная система\nПополните свой баланс крипто валютой или Рублями и оплачивайте покупки в Таиланде в один клик.'
}
CONTACTS = {
    'EN': 'Contacts:\nEmail: support@tsai.shop',
    'RU': 'Контакты:\nЭлектронная почта: support@tsai.shop',
}
HOW_ITS_WORK = {
    'EN': '<b>Buy anything in Thailand with TSAI</b>\n'
          'Villas, bikes, taxi, food, massage,\n'
          'shopping no Visa/MasterCard needed\n\n'
          '1. Deposit crypto or RUB in to your wallet\n'
          '2. Select payment method\n'
          '- QR payment\n'
          '- Bank transfer\n'
          '- Promptpay\n'
          '3. Pay with THB instantly\n\n'
          '❌No need to open a Thai bank account\n'
          '❌No KYC process\n\n'
          '🌐Works for citizens of any country\n\n'
          '<u>System maintenance every day:</u>\n'
          '- QR payment {} - {}\n'
          '- Bank transfer payment {} - {}',
    'RU': '<b>Оплачивайте все что угодно с помощью TSAI</b>\n'
          'Виллы, байки, такси, еду, массаж,\n'
          'совершайте любые покупки без карт.\n\n'
          '1. Пополните свой кошелек USDT или Рублями\n'
          '2. Выберите тип платежа\n'
          '- Оплата по QR коду\n'
          '- Перевод в банк Тайланда\n'
          '- Перевод Promptpay\n'
          '3. Оплачивайте покупки с Tsai мгновенно\n\n'
          '❌Не нужно открывать счет в Тайском банке\n'
          '❌Нет процесса KYC\n\n'
          '🌐Работает для граждан всех стран\n\n'
          '<u>Технический перерыв каждый день:</u>\n'
          '- Оплата по QR коду {} - {}\n'
          '- Оплата банковским переводом {} - {}'
}
CONTINUE = {
    'EN': '<b>Your UID: {}</b>\n\nUse it to contact support.',
    'RU': '<b>Ваш уникальный ID: {}</b>\n\nИспользуйте его для обращений в тех. Поддержку.'
}
LOGIN_MENU = {
    'EN': 'Deposit USDT or RUB and pay via QR codes anywhere In Thailand',
    'RU': 'Пополните баланс USDT или RUB и оплачивайте любые покупки с TSAI по всему Тайланду.',
}
SHARE = {
    'EN': 'Hello!\nTsai is an automated QR payment service.\n'
          'Create a wallet within a minute and pay via QR codes anywhere in Thailand\n\n<a href="https://t.me/tsaiqr_bot?start={}">Start Tsai bot</a>',
    'RU': 'Приветствуем!\nTsai - автоматизированная платежная система\n'
          'Пополните свой баланс крипто валютой или Рублями и оплачивайте покупки в Таиланде в один клик.\n\n<a href="https://t.me/tsaiqr_bot?start={}">Старт Tsai бот</a>'
}
SHARE_DESCR = {
    'EN': "👆👆👆 Share the message above and get <b>1%</b> cashback for each referrals deposit",
    'RU': "👆👆👆 Поделись сообщением выше и получай <b>1%</b> кешбека за каждый депозит реферала",
}

"""short_command.py"""
CURRENT_RATE = {
    'EN': '<b>Last rates update date time:</b> {}\n\n'
          '🇺🇸<b>USDT | THB: {}</b>\n\n'
          '🔹From 1000 USDT - <b>{}</b>\n'
          '🔹From 2000 USDT - <b>{}</b>\n'
          '🔹From 3000 USDT - <b>{}</b>\n\n'
          '🇷🇺<b>RUB | THB: {}</b>\n\n'
          '🔹From 70.000  rub - <b>{}</b>\n'
          '🔹From 150.000 rub - <b>{}</b>\n'
          '🔹From 250.000 rub - <b>{}</b>',
    'RU': '<b>Дата и время последнего обновления:</b> {}\n\n'
          '🇺🇸<b>USDT | THB: {}</b>\n\n'
          '🔹От 1000 USDT - <b>{}</b>\n'
          '🔹От 2000 USDT - <b>{}</b>\n'
          '🔹От 3000 USDT - <b>{}</b>\n\n'
          '🇷🇺<b>RUB | THB: {}</b>\n\n'
          '🔹От 70.000  руб - <b>{}</b>\n'
          '🔹От 150.000 руб - <b>{}</b>\n'
          '🔹От 250.000 руб - <b>{}</b>',
}
BALANCE = {
    'EN': '<b>Your UID: {}</b>\n\n'
          '💴Current balance <b>{}</b> THB\n\n'
          '🎯Referral balance <b>{}</b> THB\n\n'
          '<b>Available transactions limits for {}</b>\n'
          '🔹QR payment: {} THB\n'
          '🔹Bank transfer: {} THB\n'
          '🔹Promptpay: {} THB',
    'RU': '<b>Ваш уникальный ID: {}</b>\n\n'
          '💴Текущий баланс <b>{}</b> THB\n\n'
          '🎯Реферальный баланс <b>{}</b> THB\n\n'
          '<b>Лимит по операциям на {}</b>\n'
          '🔹Оплата по QR: {} THB\n'
          '🔹Банковский перевод: {} THB\n'
          '🔹Promptpay: {} THB'
}
MY_BALANCE = {
    'EN': 'Your current balance is <b>{}</b> THB',
    'RU': 'Ваш текущий баланс: <b>{}</b> THB',
}


"""history.py"""
HISTORY = {
    'EN': 'What kind of operation history do you want to see?',
    'RU': 'Выберите интересующий тип истории',
}
EMPTY_HISTORY = {
    'EN': "You haven't made any transactions yet",
    'RU': "Вы еще не совершили никаких транзакций",
}
TRUE_DEP_HISTORY = {
    'EN': '<b>Order number:</b> {}\n<b>Date:</b> {}\n<b>Token:</b> {}\n<b>Amount:</b> {} USDT\n<b>Deposited:</b> {} THB\n<b>Status:</b> {}',
    'RU': '<b>Номер заявки:</b> {}\n<b>Дата:</b> {}\n<b>Токен:</b> {}\n<b>Сумма:</b> {} USDT\n<b>Начислено:</b> {} THB\n<b>Статус:</b> {}',
}
RUB_DEP_HISTORY = {
    'EN': '<b>Order number:</b> {}\n<b>Date:</b> {}\n<b>Bank:</b> {}\n<b>Amount:</b> {} RUB\n<b>Deposited:</b> {} THB\n<b>Status:</b> {}',
    'RU': '<b>Номер заявки:</b> {}\n\n<b>Дата:</b> {}\n<b>Банк:</b> {}\n<b>Сумма пополнения:</b> {} RUB\n<b>THB к зачислению:</b> {} THB\n<b>Статус:</b> {}',
}
FALSE_DEP_HISTORY = {
    'EN': '<b>Order number:</b> {}\n<b>Date:</b> {}\n<b>Token:</b> {}\n<b>Status:</b> {}',
    'RU': '<b>Номер заявки:</b> {}\n<b>Дата:</b> {}\n<b>Токен:</b> {}\n<b>Статус:</b> {}',
}
QR_HISTORY = {
    'EN': '<b>Order number:</b> {}\n<b>Date:</b> {}\n<b>Amount:</b> {}',
    'RU': '<b>Номер заявки:</b> {}\n<b>Дата:</b> {}\n<b>Сумма:</b> {}',
}
BANK_HISTORY = {
    'EN': '<b>Order number:</b> {}\n<b>Date:</b> {}\n<b>Bank:</b> {}\n<b>Amount:</b> {}\n<b>Address:</b> {}',
    'RU': '<b>Номер заявки:</b> {}\n<b>Дата:</b> {}\n<b>Банк:</b> {}\n<b>Сумма:</b> {}\n<b>Адрес:</b> {}',
}
