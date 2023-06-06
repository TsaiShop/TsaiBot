from peewee import *
from settings.settings import DATABASE, USER, PASSWORD, HOST, PORT


db = PostgresqlDatabase(
    database=DATABASE,
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    autorollback=True,
    autoconnect=True,
)


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db


class BankAccounts(BaseModel):
    login = CharField(max_length=100)
    password = CharField(max_length=100)
    email = CharField(max_length=100)
    mail_pass = CharField(max_length=100)
    user_agent = CharField(max_length=300)
    status = BooleanField(default=False)
    active = DateTimeField()

    class Meta:
        db_table = 'bank_accounts'


class Courses(BaseModel):
    variable = CharField(max_length=50, null=True)
    value = FloatField(default=0.0)
    percent = FloatField(default=0.0)

    class Meta:
        db_table = 'courses'


class DeleteMessage(BaseModel):
    chat_id = BigIntegerField()
    message_id = CharField(max_length=200)

    class Meta:
        db_table = 'delete_message'


class DeleteMenu(BaseModel):
    chat_id = BigIntegerField()
    message_id = CharField(max_length=200)

    class Meta:
        db_table = 'delete_menu'


class TechnicalBreaks(BaseModel):
    variable = CharField(max_length=100, null=True)
    start_time = TimeField()
    end_time = TimeField()

    class Meta:
        db_table = 'technical_breaks'


class BankRub(BaseModel):
    merchant_id = CharField(max_length=100)
    api_key = CharField(max_length=100)
    pan = BigIntegerField()
    exp_month = IntegerField()
    exp_year = IntegerField()
    cvc2 = IntegerField()
    bank = CharField(max_length=20)
    status = BooleanField(default=False)
    active = DateTimeField()

    class Meta:
        db_table = 'bank_rub'


class RubStatistics(BaseModel):
    created_at = DateField()
    get_amount = FloatField(default=0.0)
    give_thb = FloatField(default=0.0)
    bought = FloatField(default=0.0)
    result = FloatField(default=0.0)
    percent = FloatField(default=0.0)

    class Meta:
        db_table = 'rub_statistics'


class AutoPayouts(BaseModel):
    created_at = DateField()
    start_balance = FloatField(default=0.0)
    amount = FloatField(default=0.0)
    qrcode = FloatField(default=0.0)
    transfer = FloatField(default=0.0)
    deposit = FloatField(default=0.0)
    end_balance = FloatField(default=0.0)

    class Meta:
        db_table = 'auto_payouts'


class ManualPayouts(BaseModel):
    created_at = DateField()
    start_balance = FloatField(default=0.0)
    amount = FloatField(default=0.0)
    qrcode = FloatField(default=0.0)
    transfer = FloatField(default=0.0)
    deposit = FloatField(default=0.0)
    end_balance = FloatField(default=0.0)

    class Meta:
        db_table = 'manual_payouts'


class Users(BaseModel):
    user_id = BigIntegerField()
    username = CharField(max_length=150, null=True)
    created_at = DateTimeField(null=True)
    email = CharField(max_length=150, null=True)
    code = CharField(max_length=100, null=True)
    active = BooleanField(default=False)
    balance = FloatField(default=0.0)
    ref_balance = FloatField(default=0.0)
    friend = BigIntegerField(null=True)
    link = CharField(max_length=100, null=True)
    referrals = IntegerField(default=0)
    percent = FloatField(default=0.0)
    lang = CharField(max_length=10, default='EN')

    class Meta:
        db_table = 'users'


class Deposit(BaseModel):
    order = CharField(max_length=20, null=True)
    user = ForeignKeyField(Users, related_name='deposit', on_delete='CASCADE')
    username = CharField(max_length=150, null=True)
    created_at = DateTimeField()
    usdt = CharField(max_length=50)
    amount = FloatField(default=0.0)
    thb_amount = FloatField(default=0.0)
    status = CharField(max_length=50, default='waiting for the payment ⏱')
    header_account = CharField(max_length=150, null=True)
    sub_account = CharField(max_length=150, null=True)

    class Meta:
        db_table = 'deposit'


class PayQR(BaseModel):
    order = CharField(max_length=20, null=True)
    user = ForeignKeyField(Users, related_name='pay_qr', on_delete='CASCADE')
    username = CharField(max_length=150, null=True)
    created_at = DateTimeField(null=True)
    operator_at = DateTimeField(null=True)
    ended_at = DateTimeField(null=True)
    amount = FloatField(null=True)
    qr_code = CharField(max_length=100, null=True)
    cheque = CharField(max_length=100, null=True)
    status = BooleanField(default=False)
    sending = BooleanField(default=False)
    auto = BooleanField(default=False)
    bank_account = ForeignKeyField(BankAccounts, related_name='pay_qr_bank_account', null=True, on_delete='CASCADE')
    mobile = BooleanField(default=False)
    approve = BooleanField(default=False)

    class Meta:
        db_table = 'pay_qr'


class PayBank(BaseModel):
    order = CharField(max_length=20, null=True)
    user = ForeignKeyField(Users, related_name='pay_bank', on_delete='CASCADE')
    username = CharField(max_length=150, null=True)
    created_at = DateTimeField(null=True)
    operator_at = DateTimeField(null=True)
    ended_at = DateTimeField(null=True)
    bank = CharField(max_length=50, null=True)
    amount = FloatField(null=True)
    address = TextField(null=True)
    cheque = CharField(max_length=100, null=True)
    status = BooleanField(default=False)
    sending = BooleanField(default=False)
    auto = BooleanField(default=False)
    bank_account = ForeignKeyField(BankAccounts, related_name='pay_bank_account', null=True, on_delete='CASCADE')
    mobile = BooleanField(default=False)
    approve = BooleanField(default=False)

    class Meta:
        db_table = 'pay_bank'


class DepositsRub(BaseModel):
    order = BigIntegerField()
    user = ForeignKeyField(Users, related_name='deposit_rub', on_delete='CASCADE')
    username = CharField(max_length=150, null=True)
    created_at = DateTimeField(null=True)
    bank = CharField(max_length=50, null=True)
    amount = FloatField(default=0.0)
    thb_amount = FloatField(default=0.0)
    full_name = CharField(max_length=100)
    destination_card = CharField(max_length=50, null=True)
    status = CharField(max_length=50, default='waiting for the payment ⏱')
    bank_rub = ForeignKeyField(BankRub, related_name='deposit_bank_rub', on_delete='CASCADE')

    class Meta:
        db_table = 'deposit_rub'


class Limits(BaseModel):
    user = ForeignKeyField(Users, related_name='limits_user', on_delete='CASCADE')
    pay = CharField(max_length=30)
    created_at = DateField()
    amount = FloatField(default=0.0)

    class Meta:
        db_table = 'limits'


class LinkValues(BaseModel):
    text = CharField(max_length=30)
    count = IntegerField(default=0)

    class Meta:
        db_table = 'link_values'
