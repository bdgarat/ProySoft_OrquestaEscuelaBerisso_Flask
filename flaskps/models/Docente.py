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
        sql = 'SELECT * FROM docente'
        cursor = self.db.cursor()
        cursor.execute(sql)

        return cursor.fetchall()
    
    
    # RECUPERAR UN DOCENTE DADO UN ID
    @classmethod
    def get_docente(self, id):
        sql = 'SELECT * FROM docente where id = %s'
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
        """
        if termino != None:
            termino = '%'+termino+'%'
            sql = sql + """ WHERE (nombre LIKE %s OR apellido LIKE %s) """
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
            """

        if termino != None:
            termino = '%'+termino+'%'
            sql = sql + """ WHERE (nombre LIKE %s OR apellido LIKE %s)"""
            
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
    
    # RECUPERAR DOCENTE DADO UN ID CON INFORMACION
    @classmethod
    def get_docente_show(self, id):
        sql = """
            SELECT d.id, d.apellido, d.nombre, d.fecha_nac, d.domicilio, d.numero,
                    d.tel, g.nombre AS genero
            FROM docente d
            INNER JOIN genero g ON (g.id = d.genero_id)
            WHERE d.id = %s 
        """
        cursor = self.db.cursor()
        cursor.execute(sql, (id))
        return cursor.fetchone()


    # ELIMINAR UN DOCENTE
    @classmethod
    def eliminar(self, id_docente):
        cursor = self.db.cursor()
        
        sql = """
            DELETE FROM docente
            WHERE id = %s
        """

        ok = cursor.execute(sql, (id_docente))
        self.db.commit()

        return ok

    # ACTIVAR / DESACTIVAR UN DOCENTE
    @classmethod
    def activar(self, id_docente):
        cursor = self.db.cursor()
        
        sql = """
            UPDATE docente 
            SET borrado_logico = not borrado_logico
            WHERE id = %s
        """

        ok = cursor.execute(sql, (id_docente))
        self.db.commit()

        return ok
    
    # EDITAR UN DOCENTE
    @classmethod
    def editar(self, id_docente, apellido, nombre, fecha_nac, localidad_id,domicilio, genero_id,tipo_doc_id, numero, tel):
        
        sql = """
            UPDATE docente 
            SET apellido = %s, nombre = %s, fecha_nac = %s, localidad_id = %s, domicilio = %s, genero_id = %s, tipo_doc_id = %s, numero = %s, tel = %s
            WHERE id = %s
        """

        cursor = self.db.cursor()
        ok = cursor.execute(sql, ( apellido, nombre, fecha_nac, localidad_id, domicilio, genero_id, tipo_doc_id, numero, tel,id_docente))
        self.db.commit()

        return ok
    
    # VER SI EXISTE TIPO_DOC+NUM
    @classmethod
    def existe_doc(self, tipo_doc_id, numero):
        sql = """
            SELECT id
            FROM docente
            WHERE tipo_doc_id = %s
            AND numero = %s
        """
        cursor = self.db.cursor()
        cursor.execute(sql, (tipo_doc_id, numero))
        return cursor.fetchone()