from telebot import types

# TODO Главное меню
# one_time_keyboard=True
main_menu = types.InlineKeyboardMarkup(row_width=3)
main_menu.add(
    types.InlineKeyboardButton(text='🛍Каталог', callback_data='catalog')
)
main_menu.add(
    types.InlineKeyboardButton(text='👤 Профиль', callback_data='profile'),
    types.InlineKeyboardButton(text='ℹ️ Информация', callback_data='info')
)
main_menu.add(
    types.InlineKeyboardButton(text='📦 Мои покупки', callback_data='purchases'),
    types.InlineKeyboardButton(text='🛒 Корзина', callback_data='basket')
)

# TODO Админ меню
admin_menu = types.InlineKeyboardMarkup(row_width=3)
admin_menu.add(types.InlineKeyboardButton(text='⚙ Редактировать каталог', callback_data='edit_catalog'))
admin_menu.add(types.InlineKeyboardButton(text='⚙ Редактировать продукты', callback_data='edit_products'))

# TODO Админ меню ( редактирование катлога)
edit_catalog_menu = types.InlineKeyboardMarkup(row_width=3)
edit_catalog_menu.add(
    types.InlineKeyboardButton(text='📝 Редактировать название', callback_data='edit_catalog_name')
)
edit_catalog_menu.add(
    types.InlineKeyboardButton(text='🗑 удалить каталог', callback_data='dell_catalog')
)
edit_catalog_menu.add(
    types.InlineKeyboardButton(text='⚙ создать каталог', callback_data='create_catalog')
)

# TODO Клавиатура для продуктов
menu_product_key = types.InlineKeyboardMarkup(row_width=1)
menu_product_key.add(types.InlineKeyboardButton(text='Купить', callback_data='catalog'))
menu_product_key.add(types.InlineKeyboardButton(text='Добавить в карзину', callback_data='catalog'))
menu_product_key.add(types.InlineKeyboardButton(text='❌ Выйти в каталог', callback_data='catalog'))
