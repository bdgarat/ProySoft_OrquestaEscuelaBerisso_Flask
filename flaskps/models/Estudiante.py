from datetime import datetime

class Estudiante(object):
    
    db = None

    def __init__(self, email, first_name, last_name, birth_date):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.birth_date = birth_date
        
        
    # RECUPERAR TODOS LOS ESTUDIANTES
    @classmethod
    def all(self):
        sql = 'SELECT * FROM estudiante where borrado_logico = 0'
        cursor = self.db.cursor()
        cursor.execute(sql)

        return cursor.fetchall()
    
    
    # RECUPERAR UN ESTUDIANTE DADO UN ID
    @classmethod
    def get_user(self, id):
        sql = 'SELECT * FROM estudiante where borrado_logico = 0 and id = %s'
        cursor = self.db.cursor()
        cursor.execute(sql, (id))

        return cursor.fetchone()
    
    # VER SI EXISTE UN ESTUDIANTE SEGUN UN EMAIL
    @classmethod
    def existe(self, email):
        sql = """
            SELECT * FROM estudiante
            WHERE email = %s
        """

        cursor = self.db.cursor()
        cursor.execute(sql, (email))
        
        if cursor.fetchone():
            return True

        return False
    
    
    # INSERTAR ESTUDIANTE
    @classmethod
    def insert(self, estudiante):
        sql = """
            INSERT INTO estudiante (email, updated_at, created_at, first_name, last_name, birth_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor = self.db.cursor()
        cursor.execute(sql, (estudiante.email,
                             estudiante.updated_at, 
                             estudiante.created_at, 
                             estudiante.first_name, 
                             estudiante.last_name,
                             estudiante.birth_date))
        self.db.commit()

        return True