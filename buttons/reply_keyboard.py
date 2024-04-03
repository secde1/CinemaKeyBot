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
    return button.add(add_amovie, edit_amovie, delete)


def exit_button():
    btn = ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True)
    return btn.add("❌")
