import os
import sqlite3

DATABASE = os.getcwd()+'/databases/database.db'
TABLE = "Baka"

class Mitai:
    def __init__(self):
        self.conn = None

        try:
            self.conn = sqlite3.connect(DATABASE)
        except sqlite3.Error as e:
            print(e)
        self.cursor = self.conn.cursor()


        self._create_table()

    def close(self):
        self.conn.close()
        del self

    def _create_table(self):
        query = f"""CREATE TABLE IF NOT EXISTS {TABLE} (user BIGINT, pat INT, track INT, vtrack INT)"""
        self.cursor.execute(query)
        self.conn.commit()


    
    def _get_user_info(self, user_id):
        query = f"SELECT * FROM {TABLE} WHERE user = ?"
        self.cursor.execute(query, (user_id,))
        info = self.cursor.fetchall()
        if info:
            self.pat = info[0][1]
            self.track = info[0][2]
            return self.pat, self.track
        else:
            print("Monke4")
            self._create_new_user(user_id = user_id)
            self._get_user_info(user_id=user_id)

    def _get_vc(self, user_id):
        print("monke")
        query = f"SELECT * FROM {TABLE} WHERE user = ?"
        self.cursor.execute(query, (user_id,))
        info = self.cursor.fetchall()
        if info:
            print("monke2")
            self.vtrack = info[0][3]
            return self.vtrack
        else:
            print("Monke3")
            self._create_new_user(user_id = user_id)
            self._get_user_info(user_id=user_id)

    def _create_new_user(self, user_id):
        try:
            query = f"""INSERT INTO {TABLE} VALUES (?, ?, ?, ?)"""
            self.cursor.execute(query, (user_id, 0, 0, 0,))
            self.conn.commit()
        except sqlite3.Error:
            pass
    
    def update_value(self, user, column, value):
        query = f"UPDATE {TABLE} SET {column} = ? WHERE user = ?"
        self.cursor.execute(query, (value, user,))
        self.conn.commit()

    def reset(self):
        query1 = f"SELECT user FROM {TABLE}"
        self.cursor.execute(query1)
        users = self.cursor.fetchall()
        user_count = 0
        for user in users:
            query = f"UPDATE {TABLE} SET track = ? WHERE user = ?"
            self.cursor.execute(query, (0, user[user_count],))
            info = self.cursor.fetchall()
            if info:
                print(info)
    
    def get_all_pats(self):
        query = f"SELECT user FROM {TABLE} WHERE pat = 1"
        self.cursor.execute(query)
        info = self.cursor.fetchall()
        return info
