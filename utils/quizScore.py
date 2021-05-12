import os
import sqlite3

DATABASE = os.getcwd()+'/databases/database.db'
TABLE = "Quiz"

class QuizScoreDB:
    def __init__(self, bot, guild):
        self.bot = bot
        self.guild = guild

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
        query = f"""CREATE TABLE IF NOT EXISTS {TABLE} (id BIGINT, user BIGINT, quiz TEXT, score BIGINT)"""
        self.cursor.execute(query)
        self.conn.commit()


    
    def _get_user_score(self, user_id):
        query = f"SELECT * FROM {TABLE} WHERE id = ? and user = ?"
        self.cursor.execute(query, (self.guild.id, user_id,))
        info = self.cursor.fetchall()
        if info:
            self.quiz = info[0][2]
            self.score = info[0][3]
            return self.quiz, self.score
        else:
            self._create_new_user(user_id = user_id)
            self._get_user_score(user_id=user_id)

    def _create_new_user(self, user_id):
        try:
            query = f"""INSERT INTO {TABLE} VALUES (?, ?, ?, ?)"""
            self.cursor.execute(query, (self.guild.id, user_id, 'spelling bee', 0))
            self.conn.commit()
        except sqlite3.Error:
            pass
    
    def update_value(self, column, value):
        query = f"UPDATE {TABLE} SET {column} = ? WHERE id = ?"
        self.cursor.execute(query, (f"{value}", self.guild.id))
        self.conn.commit()