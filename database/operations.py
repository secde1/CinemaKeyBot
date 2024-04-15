from psycopg2.extras import DictCursor

from database.connect import cur, conn


class User:
    @staticmethod
    def get_data(telegram_id: str):
        cur.execute('SELECT * FROM users WHERE user_id = %s', (telegram_id,))
        return cur.fetchone()

    @staticmethod
    def create_data(telegram_id: str, username: str):
        # Исправлен порядок параметров в соответствии с таблицей в БД
        cur.execute('INSERT INTO users (user_id, username) VALUES (%s, %s)', (telegram_id, username))
        conn.commit()

    @staticmethod
    def get_all():
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute('SELECT user_id, username FROM users')
            return cur.fetchall()


class Movie:
    @staticmethod
    def create_data(post_id: int, file_id: str, caption: str):
        query = 'INSERT INTO movies (post_id, file_id, caption) VALUES (%s, %s, %s)'
        cur.execute(query, (post_id, file_id, caption))
        conn.commit()

    @staticmethod
    def get_all_movies():
        query = 'SELECT * FROM movies'
        cur.execute(query)
        return cur.fetchall()

    @staticmethod
    def get_data(post_id: int):
        query = 'SELECT * FROM movies WHERE post_id = %s'
        cur.execute(query, (post_id,))
        return cur.fetchone()

    @staticmethod
    def get_movie(file_id: str):
        query = 'SELECT * FROM movies WHERE file_id = %s'
        cur.execute(query, (file_id,))
        return cur.fetchone()

    @staticmethod
    def get_movie_count():
        query = 'SELECT * FROM movies'
        cur.execute(query)
        return cur.fetchone()[0]

    @staticmethod
    def get_popular_movies(limit=5):
        query = 'SELECT * FROM movies ORDER BY views DESC LIMIT %s'
        cur.execute(query, (limit,))
        return cur.fetchall()

    @staticmethod
    def delete_movie(post_id: int):
        try:
            query = 'DELETE FROM movies WHERE post_id = %s'
            cur.execute(query, (post_id,))
            conn.commit()
            return "Фильм успешно удален."
        except Exception as e:
            print(f"Ошибка при удалении фильма: {e}")
            return "Ошибка при удалении фильма."
