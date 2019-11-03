from datetime import datetime

class Estudiante(object):
    
    db = None

    def __init__(self, email, apellido, nombre, fecha_nac, localidad_id, nivel_id, domicilio, genero_id, escuela_id, tipo_doc_id, numero, tel, barrio_id):
        self.email = email
        self.apellido = apellido
        self.nombre = nombre
        self.fecha_nac = fecha_nac
        self.localidad_id = localidad_id
        self.nivel_id = nivel_id
        self.domicilio = domicilio
        self.genero_id = genero_id
        self.escuela_id = escuela_id
        self.tipo_doc_id = tipo_doc_id
        self.numero = numero
        self.tel = tel
        self.barrio_id = barrio_id
        
        
    # RECUPERAR TODOS LOS ESTUDIANTES
    @classmethod
    def all(self):
        sql = 'SELECT * FROM estudiante where borrado_logico = 0'
        cursor = self.db.cursor()
        cursor.execute(sql)

        return cursor.fetchall()
    
    
    # RECUPERAR UN ESTUDIANTE DADO UN ID
    @classmethod
    def get_estudiante(self, id):
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
            INSERT INTO estudiante (email, apellido, nombre, fecha_nac, localidad_id, nivel_id, domicilio, genero_id, escuela_id, tipo_doc_id, numero, tel, barrio_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor = self.db.cursor()
        cursor.execute(sql, (estudiante.email,
                             estudiante.apellido, 
                             estudiante.nombre, 
                             estudiante.fecha_nac, 
                             estudiante.localidad_id, 
                             estudiante.nivel_id, 
                             estudiante.domicilio, 
                             estudiante.genero_id, 
                             estudiante.escuela_id,
                             estudiante.tipo_doc_id, 
                             estudiante.numero, 
                             estudiante.tel, 
                             estudiante.barrio_id))
        self.db.commit()

        return True
    
    # RECUPERAR TODOS LOS ESTUDIANTES POR TERMINO DE BUSQUEDA
    @classmethod
    def get_estudiantes(self, termino = None):
        params = []
        sql = """
            SELECT * FROM estudiante
            WHERE borrado_logico = 0
        """
        if termino != None:
            termino = '%'+termino+'%'
            sql = sql + """ AND (nombre LIKE %s OR apellido LIKE %s) """
            params.append(termino)
            params.append(termino)

        cursor = self.db.cursor()
        cursor.execute(sql, params)

        return cursor.fetchall()
    
    # RECUPERAR TODOS LOS ESTUDIANTES POR TERMINO DE BUSQUEDA POR ROL Y PAGINADOS
    @classmethod
    def get_estudiantes_paginados(self, limit, offset = 1, termino = None):
        
        sql = """
            SELECT * FROM estudiante
            WHERE borrado_logico = 0
            """

        if termino != None:
            termino = '%'+termino+'%'
            sql = sql + """ AND (nombre LIKE %s OR apellido LIKE %s)"""
            
        sql = sql + """
                    LIMIT %s OFFSET %s
                    """

        if termino != None:
            params = (termino,termino, limit, offset)
        else:
            params = (limit, offset)

        cursor = self.db.cursor()
        cursor.execute(sql, params)

        return cursor.fetchall()