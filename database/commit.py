from database.operations import User, Movie


async def create_user(telegram_id: int, username: str):
    data = User.get_data(str(telegram_id))
    if not data:
        User.create_data(telegram_id=str(telegram_id), username=username)
        return True
    else:
        return False


def get_users():
    return User.get_data()


def create_movie(post_id: int, file_id: str, caption: str) -> int:
    data = Movie.get_movie(file_id)
    if not data:
        Movie.create_data(post_id, file_id, caption)
        return post_id
    else:
        return data.get('post_id', None)


def get_movie(post_id: int):
    data = Movie.get_data(post_id)
    if data:
        return [data['file_id'], data['caption']]
    else:
        return False
