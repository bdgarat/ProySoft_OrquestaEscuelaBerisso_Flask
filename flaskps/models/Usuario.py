from datetime import datetime
from flask_login import UserMixin


class Usuario(object):
    
    db = None
    
    def __init__(self, email, username, password, first_name, last_name):
        self.email = email
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.activo = 1
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        

    @classmethod
    def all(self):
        sql = 'SELECT * FROM usuario'
        cursor = self.db.cursor()
        cursor.execute(sql)

        return cursor.fetchall()

    @classmethod
    def insert(self, user):
        sql = """
            INSERT INTO usuario (email, username, password, activo, updated_at, created_at, first_name, last_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor = self.db.cursor()
        cursor.execute(sql, (user.email, user.username, user.password, user.activo, user.updated_at, user.created_at, user.first_name, user.last_name))
        self.db.commit()

        return True

    # @classmethod
    # def find_by_email_and_pass(self, email, password):
    #     sql = """
    #         SELECT * FROM users AS u
    #         WHERE u.email = %s AND u.password = %s
    #     """

    #     cursor = self.db.cursor()
    #     cursor.execute(sql, (email, password))

    #     return cursor.fetchone()