from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_button():
    button = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=True)
    movie_catalog = KeyboardButton('Каталогом фильмов')
    user_management = KeyboardButton('Управление пользователями')
    statistics_and_analytics = KeyboardButton('Статистика и аналитика')
    return button.add(movie_catalog, user_management, statistics_and_analytics)


def movie_button():
    button = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=True)
    add_amovie = KeyboardButton('Добавить фильм')
    edit_amovie = KeyboardButton('Редактировать фильм')
    delete = KeyboardButton('Удалить фильм')
    back_button = KeyboardButton('Назад')
    return button.add(add_amovie, edit_amovie, delete, back_button)


def users_management_button():
    button = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=True)
    view_all_users = KeyboardButton('Просмотреть всех пользователей')
    block_user = KeyboardButton('Заблокировать пользователя')
    unblock_user = KeyboardButton('Разблокировать пользователя')
    back_button = KeyboardButton('Назад')
    return button.add(view_all_users, block_user, unblock_user, back_button)


def exit_button():
    button = ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True)
    back_button = KeyboardButton('Назад')
    return button.add(back_button)
