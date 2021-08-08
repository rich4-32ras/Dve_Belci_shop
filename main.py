# -*- coding: utf-8 -*-
# +--------- PROJECT INFO ----------+
# project name: Dve Belki TG shop
# coding by: S.semyon
# email: semyon.shilo@yandex.ru
# +---------------------------------+

import telebot
import mysql.connector
from telebot import types
# IMPORT FILE
import random
import config
import keyboards


bot = telebot.TeleBot(config.token_bot)

db = mysql.connector.connect(
    host='localhost',
    user=config.user,
    passwd=config.passwd,
    database=config.database
)
cursor = db.cursor()

print(f'status connect Telegram bot: {bot}')
print(f'status connect DataBase: {bot}')

user_data = {}
edit_catalog_data = {}


class User:
    def __init__(self, telegram_id):
        self.telegram_id = telegram_id
        self.first_name = ''
        self.number_phone = ''


class Edit_Catalog:
    try:
        def __int__(self, edit_category_id):
            self.edit_category_id = edit_category_id
            self.new_name_category = ''
    except Exception as e:
        print(f'ERROR Class {e}')

# class product:
#     def __int__(self):
#         self.name_categories = ''
#         self.description = ''
#         self.photo_id = ''
#         self.price = ''
#         self.product_id = ''
#         self.main_id = ''


@bot.message_handler(commands=['start'])
# /start handler message
def do_start(message):
    try:
        chat_id = message.chat.id
        telegram_id = message.from_user.id
        # add object to class
        user_data[telegram_id] = User(telegram_id)
        user = user_data[telegram_id]
        user.first_name = message.from_user.first_name
        # подключение к БД, проверка пользователя ( на регистрацию ), если нет регестрировать его
        sql = f"SELECT * FROM users WHERE user_id = {telegram_id}"
        cursor.execute(sql)
        exists_user = cursor.fetchone()
        if exists_user == None:
            sql = "INSERT INTO users (first_name, user_id, role) VALUES (%s, %s, %s)"
            val = (user.first_name, user.telegram_id, 'Пользователь')
            cursor.execute(sql, val)
            db.commit()
        print(message.from_user.id)

        bot.send_photo(chat_id=chat_id,
                       photo=open('main_menu_photo\\main_menu.png', 'rb'),
                       caption=f'Добро пожаловать {user.first_name}\n\nваш уникальный id: {user.telegram_id}',
                       )

        bot.send_message(chat_id=chat_id,
                         text='💬️   Главное меню',
                         reply_markup=keyboards.main_menu
                         )

    except Exception as e:
        chat_id = message.chat.id
        bot.send_message(
            chat_id=chat_id,
            text='Бот временно неработает',
        )
        print(f'ERROR by do_start: {e}')


@bot.message_handler(commands=['admin'])
def do_admin(message):
    chat_id = message.chat.id

    # TODO Проверка на доступ к админ панели

    bot.send_message(
        chat_id=chat_id,
        text='Добро пожаловать в админ меню',
        reply_markup=keyboards.admin_menu,
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    telegram_id = call.from_user.id
    first_user_name = call.from_user.first_name

    print(f'call_data: [{call.data}]')
    # Admin ------------------------------------------------------------------------------------------------------------
    if call.data == 'edit_catalog':
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text='📍Редактирование каталога',
            reply_markup=keyboards.edit_catalog_menu
        )
    elif call.data == 'create_catalog':
        msg = bot.send_message(
            chat_id=chat_id,
            text='Введите название новой категории: ',
            )
        bot.register_next_step_handler(msg, create_catalog)

    elif call.data == 'dell_catalog':
        chat_id = call.message.chat.id
        cursor.execute("SELECT * FROM catalog")
        rows = cursor.fetchall()
        string = ''
        for row in rows:
            string += f'{row[1]} -- ID: {row[2]}\n' + '-----' * 7 + '\n'
        msg = bot.send_message(
            chat_id=chat_id,
            text='Удаление категории:\n\n' + string + '\nВведите ID ! категории которую хотите удалить'
        )
        bot.register_next_step_handler(msg, dell_catalog)

    elif call.data == 'edit_catalog_name':
        chat_id = call.message.chat.id
        cursor.execute("SELECT * FROM catalog")
        rows = cursor.fetchall()
        string = ''
        for row in rows:
            string += f'{row[1]} -- ID: {row[2]}\n' + '-----' * 7 + '\n'
        msg = bot.send_message(
            chat_id=chat_id,
            text='изменение имени:\n\n' + string + '\nВведите ID ! категории которую хотите изменить'
        )
        bot.register_next_step_handler(msg, redactor_name_catalog)

    #  Client ----------------------------------------------------------------------------------------------------------
    elif call.data == 'profile':
        try:
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            user_info = [None] * 5
            for row in rows:
                if row[1] == telegram_id:
                    user_info = row
                    break

            exit_menu_key = types.InlineKeyboardMarkup(row_width=1)
            exit_menu_key.add(types.InlineKeyboardButton(text='❌ Выйти в меню', callback_data='exit_to_menu'))

            print(user_info)
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f'👤 Профиль\n{"-"*20}\n😀 Имя пользователя: {user_info[3]}\n📌 id пользователя: {user_info[1]}'
                     f'\n📞 Номер телефона: {user_info[2]}',
                reply_markup=exit_menu_key
            )
        except Exception as e:
            bot.send_message(
                chat_id=chat_id,
                text='Бот временно неработает',
            )
            print(f'ERROR by exit_to_menu: {e}')

    elif call.data == 'exit_to_menu':
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text='Главное Меню',
                reply_markup=keyboards.main_menu,
            )
        except Exception as e:
            chat_id = call.message.chat.id
            bot.send_message(
                chat_id=chat_id,
                text='Бот временно неработает',
            )
            print(f'ERROR by exit_to_menu: {e}')

    elif call.data == 'catalog':
        try:
            # выборка двнных для name и call_back ( клавиатуры для каталога )
            cursor.execute("SELECT * FROM catalog")
            rows = cursor.fetchall()
            menu_catalog_key = types.InlineKeyboardMarkup(row_width=1)
            # создание клавиатуры для catalog
            for row in rows:
                menu_catalog_key.add(types.InlineKeyboardButton(text=f'{row[1]}', callback_data=f'{row[2]}'))
            menu_catalog_key.add(types.InlineKeyboardButton(text='❌ Выйти в меню', callback_data='exit_to_menu'))

            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text='📍Каталог',
                reply_markup=menu_catalog_key
            )
        except Exception as e:
            chat_id = call.message.chat.id
            bot.send_message(
                chat_id=chat_id,
                text='Бот временно неработает',
            )
            print(f'ERROR by catalog: {e}')

    elif call.data in str(list_goods(call.message)):
        try:
            catalog_id = str(call.data)
            cursor.execute(f"SELECT * FROM products")
            rows = cursor.fetchall()
            menu_category_key = types.InlineKeyboardMarkup(row_width=1)

            for row in rows:
                if row[3] == catalog_id:
                    menu_category_key.add(types.InlineKeyboardButton(text=f'{row[1]}', callback_data=f'{row[2]}'))
            menu_category_key.add(types.InlineKeyboardButton(text='❌ Выйти в каталог', callback_data='catalog'))

            cursor.execute(f"SELECT * FROM catalog")
            rows = cursor.fetchall()
            catalog_name = ''

            for row in rows:
                if row[2] == catalog_id:
                    catalog_name = row[1]
                    break
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f'📍Категория: {catalog_name}',
                reply_markup=menu_category_key
            )

        except Exception as e:
            chat_id = call.message.chat.id
            bot.send_message(
                chat_id=chat_id,
                text='Бот временно неработает',
            )
            print(f'ERROR by generate product list: {e}')

    elif call.data in str(list_product(call.message)):
        product_id = str(call.data)

        cursor.execute(f"SELECT * FROM products")
        rows = cursor.fetchall()
        product_name = ''
        product_description = ''
        product_photo = ''
        product_price = ''

        for row in rows:
            if row[2] == product_id:
                product_name = row[1]
                product_description = row[4]
                product_price = row[5]
                product_photo = row[6]
                break

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f'📍Название: {product_name}\n\n📍Описание: {product_description}\n\n📍Цена: {product_price}',
            reply_markup=keyboards.menu_product_key
        )


# EDIT_CATALOG ---------------------------------------------------------------------------------------------------------
# create catalog
def create_catalog(message):
    chat_id = message.chat.id

    catalog_id = 'CTG' + str(random.randint(10000, 90000))

    name_category = message.text
    try:
        sql = "INSERT INTO catalog (catalog_name, catalog_id) VALUES (%s, %s)"
        val = (name_category, catalog_id)
        cursor.execute(sql, val)
        db.commit()

        bot.send_message(
            chat_id=chat_id,
            text='Внесены изменения',
        )
    except Exception as e:
        print(f'ERROR by create_catalog: {e}')


# DELL_CATALOG ---------------------------------------------------------------------------------------------------------
def dell_catalog(message):
    chat_id = message.chat.id
    dell_category_id = message.text
    try:
        sql = f"DELETE FROM catalog WHERE catalog_id = {dell_category_id}"
        cursor.execute(sql)
        db.commit()

        bot.send_message(
            chat_id=chat_id,
            text='Категория успешно удалена!'
        )
    except Exception as e:
        bot.send_message(
            chat_id=chat_id,
            text='Удаление неудалось!'
        )
        print(f'ERROR by dell_catalog: {e}')


# EDIT_NAME ------------------------------------------------------------------------------------------------------------
def redactor_name_catalog(message):
    try:
        chat_id = message.chat.id
        redact_category_num = message.text
        edit_catalog_data[redact_category_num] = Edit_Catalog()
        edit_catalog_name = edit_catalog_data[redact_category_num]
        edit_catalog_name.edit_category_id = redact_category_num
        msg = bot.send_message(
            chat_id=chat_id,
            text='Введите новое название: '
        )
        bot.register_next_step_handler(msg, redactor_name_catalog_2(message))
    except Exception as e:
        print(f'ERROR by redactor_name_catalog: {e}')


def redactor_name_catalog_2(message):
    try:
        edit_catalog_name = Edit_Catalog()
        chat_id = message.chat.id
        new_category_name = message.text

        edit_catalog_name.new_name_category = new_category_name
        print(edit_catalog_name.new_name_category, edit_catalog_name.edit_category_id)
        sql = f"""
            UPDATE category SET catalog_name = '{str(edit_catalog_name.new_name_category)}'
            WHERE catalog_id = '{str(edit_catalog_name.edit_category_id)}'
            """

        cursor.execute(sql)
        db.commit()
        bot.send_message(
            chat_id=chat_id,
            text='Название успешно изменино!'
        )
    except Exception as e:
        chat_id = message.chat.id
        bot.send_message(
            chat_id=chat_id,
            text='Название не изменино!'
        )
        print(f'ERROR by redactor_name_catalog_2: {e}')


# CREATE LIST CATALOG --------------------------------------------------------------------------------------------------
def list_goods(message):
    try:
        cursor.execute("SELECT * FROM catalog")
        row = cursor.fetchall()
        lst_goods = [(i[2]) for i in row]
        return lst_goods

    except Exception as e:
        chat_id = message.chat.id
        bot.send_message(
            chat_id=chat_id,
            text='Бот временно не работает'
        )
        print(f'ERROR by list_goods: {e}')


def list_product(message):
    try:
        cursor.execute("SELECT * FROM products")
        row = cursor.fetchall()
        lst_product = [(i[2]) for i in row]
        return lst_product

    except Exception as e:
        chat_id = message.chat.id
        bot.send_message(
            chat_id=chat_id,
            text='Бот временно не работает'
        )
        print(f'ERROR by list_goods: {e}')


# ADD PRODUCT TO CATALOG (def) -----------------------------------------------------------------------------------------
# STEP 1: SELECT CATALOG -----------------------------------------------------------------------------------------------
# def add_product():

# STEP 2: ADD PRODUCT NAME ---------------------------------------------------------------------------------------------
# def add_product_name():

# STEP 3: ADD PRODUCT DESCRIPTION --------------------------------------------------------------------------------------
# def add_product_description():

# STEP 4: ADD PRODUCT PRICE --------------------------------------------------------------------------------------------
# def add_product_price():

# STEP 5: ADD PRODUCT PHOTO --------------------------------------------------------------------------------------------
# def add_product_photo():

# STEP6: CHECK ADD PRODUCT ---------------------------------------------------------------------------------------------
# def check_add_product():

# STEP 7: FINISH ADD PRODUCT -------------------------------------------------------------------------------------------
# def finish_add_product():


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)
