from datetime import datetime

class Estudiante(object):
    
    db = None

    def __init__(self, apellido, nombre, fecha_nac, localidad_id, nivel_id, domicilio, genero_id, escuela_id, tipo_doc_id, numero, tel, barrio_id):
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
    
    
    # INSERTAR ESTUDIANTE
    @classmethod
    def insert(self, estudiante):
        sql = """
            INSERT INTO estudiante (apellido, nombre, fecha_nac, localidad_id, nivel_id, domicilio, genero_id, escuela_id, tipo_doc_id, numero, tel, barrio_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor = self.db.cursor()
        cursor.execute(sql, (
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
    
    
    # EDITAR ESTUDIANTE
    @classmethod
    def editar(self, id_estudiante, apellido, nombre, fecha_nac, localidad_id,nivel_id,domicilio, genero_id, escuela_id,tipo_doc_id, numero, tel,barrio_id):
        
        sql = """
            UPDATE estudiante 
            SET apellido = %s, nombre = %s, fecha_nac = %s, localidad_id = %s, nivel_id = %s,domicilio = %s, genero_id = %s, escuela_id = %s,tipo_doc_id = %s, numero = %s, tel = %s,barrio_id = %s
            WHERE id = %s
        """

        cursor = self.db.cursor()
        cursor.execute(sql, ( apellido, nombre, fecha_nac, localidad_id, nivel_id, domicilio, genero_id, escuela_id, tipo_doc_id, numero, tel, barrio_id,id_estudiante))
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
    
    
    # ELIMINAR UN ESTUDIANTE
    @classmethod
    def eliminar(self, id_estudiante):
        cursor = self.db.cursor()
        
        sql = """
            UPDATE estudiante 
            SET borrado_logico = 1
            WHERE id = %s
        """

        o = cursor.execute(sql, (id_estudiante))
        self.db.commit()

        return o