from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from buttons.reply_keyboard import admin_button, movie_button, exit_button, users_management_button
from config import TOKEN, ADMIN
from database.commit import create_user, get_movie, create_movie
from database.connect import startup_table
from database.operations import Movie, User

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
admin = ADMIN


@dp.message_handler(commands=['start'])
async def start(message: types.message):
    user_created = await create_user(message.from_user.id, message.from_user.username)
    if user_created:
        await message.answer(f"Привет! Добро пожаловать {message.from_user.username}"
                             f"Можете найти фил")
    else:
        pass


@dp.message_handler(commands=['adminPanel'])
async def admin_panel(message: types):
    if message.from_user.id in admin:
        await message.answer(f' Привет! {message.from_user.first_name} Добро пожаловать админ-панель!',
                             reply_markup=admin_button())
    else:
        await message.answer('У вас нет доступа на админ-панель', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(Text('Каталогом фильмов'))
async def admin_movie_catalog(message: types):
    if message.from_user.id in admin:
        await message.answer("Выберите каталога:", reply_markup=movie_button())
    else:
        pass


class AddMovieState(StatesGroup):
    media = State()
    media_id = State()


@dp.message_handler(Text('Добавить фильм'))
async def admin_add_amovie(message: types.Message):
    if message.from_user.id in admin:
        await AddMovieState.media.set()
        await message.answer("Можете отправить фильм", reply_markup=exit_button())
    else:
        pass


@dp.message_handler(state=AddMovieState.media, content_types=types.ContentType.ANY)
async def handle_video(msg: types.Message, state: FSMContext):
    try:
        if msg.text == "❌":
            await msg.answer("Загрузка фильма отменена", reply_markup=exit_button())
            await state.finish()
        else:
            async with state.proxy() as data:
                data['file_id'] = msg.video.file_id
                data['caption'] = msg.caption
            await AddMovieState.media_id.set()
            await msg.answer(text="Пожалуйста, введите ID для фильма: ", reply_markup=exit_button())
    except:
        await msg.answer("Пожалуйста, отправьте фильм!", reply_markup=exit_button())


@dp.message_handler(state=AddMovieState.media_id, content_types=types.ContentType.TEXT)
async def handle_media_id(msg: types.Message, state: FSMContext):
    post_id_text = msg.text.strip()
    try:
        post_id = int(post_id_text)
    except ValueError:

        await msg.answer("ID должен быть числом. Пожалуйста, отправьте число в качестве ID!",
                         reply_markup=exit_button())
        return

    if post_id_text == "❌":
        await msg.answer("Загрузка фильма отменена", reply_markup=movie_button())
        await state.finish()
        return
    movie_exists = get_movie(post_id)
    if not movie_exists:
        async with state.proxy() as data:
            create_movie(post_id=post_id, file_id=data['file_id'], caption=data['caption'])
            await msg.reply(f"Фильм сохранен в базе данных \nКод фильма: {post_id}", reply_markup=movie_button())
        await state.finish()
    else:
        await msg.reply("Фильм с таким ID уже существует.")


class DeleteMovieState(StatesGroup):
    post_id = State()


@dp.message_handler(Text('Удалить фильм'))
async def delete_movie(message: types.Message):
    if message.from_user.id in admin:
        await DeleteMovieState.post_id.set()
        await message.answer('Чтобы удалить фильм, отправьте ID фильма:', reply_markup=exit_button())
    else:
        await message.answer('У вас нет доступа к этой команде.')


@dp.message_handler(state=DeleteMovieState.post_id)
async def process_delete_movie(message: types.Message, state: FSMContext):
    if message.text == "❌":
        await message.answer('Удаление фильма отменено.', reply_markup=movie_button())
        await state.finish()
    else:
        response = Movie.delete_movie(int(message.text))
        await message.answer(response, reply_markup=movie_button())
        await state.finish()


@dp.message_handler(Text('Редактировать фильм'))
async def edit_movie(message: types.Message):
    # if message.from_user.id in admin:
    #     await message.answer('У вас нет доступа к этой команде.')
    #     return
    movies_count = Movie.get_movie_count()
    await message.answer(f"Всего фильмов в базе: {movies_count}")

    popular_movies = Movie.get_popular_movies(limit=5)
    response = "Самые популярные фильмы:\n\n"
    for movie in popular_movies:
        response += f"{movie['caption']} - Просмотры: {movie['views']}\n"
        await message.answer(response)


@dp.message_handler(Text('Управление пользователями'))
async def admin_user_management(message: types.Message):
    if message.from_user.id in admin:
        await message.answer("Выберите действие:", reply_markup=users_management_button())
    else:
        await message.answer("У вас нет доступа к этой команде.")


@dp.message_handler(Text('Просмотреть всех пользователей'))
async def user_management(message: types.Message):
    users_count = User.get_all()
    await message.answer(f"Количество пользователей: {len(users_count)}")


@dp.message_handler(Text('Заблокировать пользователя'))
async def block_user_management(message: types.Message):
    await message.answer('Эта команда ещё не реализована')


@dp.message_handler(Text('Разблокировать пользователя'))
async def unblock_user_management(message: types.Message):
    await message.answer('Эта команда ещё не реализована')


@dp.message_handler(Text('Статистика и аналитика'))
async def statistics_and_analytics(message: types.Message):
    await message.answer('Эта команда ещё не реализована')


@dp.message_handler(Text(equals="Назад"))
async def back_to_menu(message: types.Message, state: FSMContext):
    await state.finish()
    if message.from_user.id in admin:
        await message.answer("Вы вернулись в административное меню:", reply_markup=admin_button())
    else:
        pass


class MovieState(StatesGroup):
    waiting_for_movie_code = State()


@dp.message_handler(commands=['get_movie'], state="*")
async def command_get_movie(message: types.Message, state: FSMContext):
    await MovieState.waiting_for_movie_code.set()
    await message.reply("Пожалуйста, отправьте код фильма.")


@dp.message_handler(lambda message: message.text.isdigit(), state=MovieState.waiting_for_movie_code)
async def send_movie_by_code(message: types.Message, state: FSMContext):
    movie_data = get_movie(int(message.text))
    if movie_data:
        try:
            await bot.send_video(chat_id=message.from_user.id, video=movie_data[0],
                                 caption=f"{movie_data[1]}\n\n🤖 Наш бот: @piratsbot")
            await state.finish()
        except Exception as e:
            print(e)
            await message.reply("Произошла ошибка при отправке фильма. Пожалуйста, попробуйте позже.")
            await state.finish()
    else:
        await message.reply(f"Фильм с кодом {message.text} не найден")
        await state.finish()


async def startup(dp):
    startup_table()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=startup, skip_updates=True)
