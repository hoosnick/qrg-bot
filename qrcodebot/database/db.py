from contextlib import closing
from sqlite3 import connect
from loguru import logger

import pydantic


class User(pydantic.BaseModel):
    id: int
    name: str
    style: int


class DataBase:
    def __init__(self):
        self.initialize()

    def initialize(self):
        with closing(connect("data.db")) as conn:
            with closing(conn.cursor()) as cursor:
                query = """
                CREATE TABLE IF NOT EXISTS Users(
                    user_id INT,
                    user_name TEXT,
                    user_design INTEGER DEFAULT 1
                )"""
                cursor.execute(query)
                conn.commit()

    def new_user(self, user_id: int, user_name: str):
        with closing(connect("data.db")) as conn:
            with closing(conn.cursor()) as cursor:
                q = 'SELECT * FROM `Users` WHERE `user_id` = ?'
                n = cursor.execute(q, (user_id,)).fetchall()

                if bool(len(n)):
                    return

                query = "INSERT INTO Users(user_id, user_name) VALUES(?,?)"
                cursor.execute(query, (user_id, user_name,))
                conn.commit()

    def update_name(self, user_id: int, new_name: str):
        with closing(connect("data.db")) as conn:
            with closing(conn.cursor()) as cursor:
                user = self.get_user(user_id)
                if user.name == new_name:
                    return

                q = "UPDATE `Users` SET `user_name` = (?) WHERE `user_id` = (?)"
                cursor.execute(q, (new_name, user_id,))
                conn.commit()

    def update_style(self, user_id: int, new_style: int):
        with closing(connect("data.db")) as conn:
            with closing(conn.cursor()) as cursor:
                user = self.get_user(user_id)
                if user.style == new_style:
                    return

                q = "UPDATE `Users` SET `user_design` = (?) WHERE `user_id` = (?)"
                cursor.execute(q, (new_style, user_id,))
                conn.commit()

    def get_user(self, user_id: int) -> User:
        with closing(connect("data.db")) as conn:
            with closing(conn.cursor()) as cursor:
                q = 'SELECT * FROM `Users` WHERE `user_id` = ?'
                result = cursor.execute(q, (user_id,)).fetchone()

                return User(
                    id=result[0],
                    name=result[1],
                    style=result[2]
                )
