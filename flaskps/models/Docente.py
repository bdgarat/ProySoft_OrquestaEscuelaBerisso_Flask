from datetime import datetime

class Docente(object):
    
    db = None

    def __init__(self, apellido, nombre, fecha_nac, localidad_id, domicilio, genero_id, tipo_doc_id, numero, tel):
        self.apellido = apellido
        self.nombre = nombre
        self.fecha_nac = fecha_nac
        self.localidad_id = localidad_id
        self.domicilio = domicilio
        self.genero_id = genero_id
        self.tipo_doc_id = tipo_doc_id
        self.numero = numero
        self.tel = tel
        
        
    # RECUPERAR TODOS LOS DOCENTES
    @classmethod
    def all(self):
        sql = 'SELECT * FROM docente where borrado_logico = 0'
        cursor = self.db.cursor()
        cursor.execute(sql)

        return cursor.fetchall()
    
    
    # RECUPERAR UN DOCENTE DADO UN ID
    @classmethod
    def get_docente(self, id):
        sql = 'SELECT * FROM docente where borrado_logico = 0 and id = %s'
        cursor = self.db.cursor()
        cursor.execute(sql, (id))

        return cursor.fetchone()
    
    
    # INSERTAR docente
    @classmethod
    def insert(self, docente):
        sql = """
            INSERT INTO docente (apellido, nombre, fecha_nac, localidad_id, domicilio, genero_id, tipo_doc_id, numero, tel)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor = self.db.cursor()
        cursor.execute(sql, (
                             docente.apellido, 
                             docente.nombre, 
                             docente.fecha_nac, 
                             docente.localidad_id,
                             docente.domicilio, 
                             docente.genero_id, 
                             docente.tipo_doc_id, 
                             docente.numero, 
                             docente.tel))
        self.db.commit()

        return True
    
    # RECUPERAR TODOS LOS docenteS POR TERMINO DE BUSQUEDA
    @classmethod
    def get_docentes(self, termino = None):
        params = []
        sql = """
            SELECT * FROM docente
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
    
    # RECUPERAR TODOS LOS docenteS POR TERMINO DE BUSQUEDA POR ROL Y PAGINADOS
    @classmethod
    def get_docentes_paginados(self, limit, offset = 1, termino = None):
        
        sql = """
            SELECT * FROM docente
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