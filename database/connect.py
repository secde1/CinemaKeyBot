import psycopg2
from psycopg2.extras import DictCursor

conn = psycopg2.connect(
    database='moviedb',
    user='postgres',
    password='5719',
    host='localhost',
    port='5432',
    cursor_factory=DictCursor
)
cur = conn.cursor()


def startup_table():
    user = """CREATE TABLE IF NOT EXISTS users(
    id BIGSERIAL PRIMARY KEY,
    username varchar(69),
    user_id varchar(69) unique,
    created_at timestamp default now()
    )"""

    movie = """
    CREATE TABLE IF NOT EXISTS movies(
        id BIGSERIAL PRIMARY KEY,
        post_id int not null,
        file_id varchar(800) not null,
        caption text,
        created_at timestamp default now()
    )
    """
    cur.execute(user)
    cur.execute(movie)
    conn.commit()
