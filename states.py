from aiogram.dispatcher.filters.state import State, StatesGroup


class AdvertisementState(StatesGroup):
    waiting_for_ad = State()


class AddMovieState(StatesGroup):
    media = State()
    media_id = State()


class DeleteMovieState(StatesGroup):
    post_id = State()


class MovieState(StatesGroup):
    waiting_for_movie_code = State()
