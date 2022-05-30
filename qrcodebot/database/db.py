import sqlite3


class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect('data.db', check_same_thread=False)
        self.cur = self.conn.cursor()

    def create(self):
        with self.conn:
            is_table_exists = self.cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='Users'",
            ).fetchone()
            if not is_table_exists:
                query = """CREATE TABLE IF NOT EXISTS Users(
                    user_id INT,
                    user_name TEXT,
                    user_design INTEGER DEFAULT 1)"""
                self.cur.execute(query)

    def new_user(self, user_id: int, user_name: str):
        with self.conn:
            n = self.cur.execute(
                'SELECT * FROM `Users` WHERE `user_id` = ?', (user_id,)
            ).fetchall()
            if bool(len(n)):
                return
            query = "INSERT INTO `Users` (`user_id`, `user_name`) VALUES(?,?)"
            return self.cur.execute(query, (user_id, user_name))

    def update_name(self, user_id: int, new_name: str):
        with self.conn:
            user = self.get_user(user_id)
            if user.name != new_name:
                query = "UPDATE `Users` SET `user_name` = (?) WHERE `user_id` = (?)"
                return self.cur.execute(query, (new_name, user_id))

    def update_style(self, user_id: int, new_style: int):
        with self.conn:
            user = self.get_user(user_id)
            if user.style != new_style:
                query = "UPDATE `Users` SET `user_design` = (?) WHERE `user_id` = (?)"
                return self.cur.execute(query, (new_style, user_id))

    def get_user(self, user_id: int):
        with self.conn:
            result = self.cur.execute(
                'SELECT * FROM `Users` WHERE `user_id` = ?', (user_id,)
            ).fetchone()

            return dotDict({
                'id': result[0],
                'name': result[1],
                'style': result[2],
            })


class dotDict:
    def __init__(self, new_dict: dict):
        self.dict = new_dict

    def __getattr__(self, val):
        return self.dict[val]
