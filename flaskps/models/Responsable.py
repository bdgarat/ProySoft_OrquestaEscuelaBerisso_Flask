from datetime import datetime

class Responsable(object):
    
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
        
        
    # RECUPERAR TODOS LOS RESPONSABLES
    @classmethod
    def all(self):
        sql = 'SELECT * FROM responsable'
        cursor = self.db.cursor()
        cursor.execute(sql)

        return cursor.fetchall()
    
    
    # RECUPERAR UN RESPONSABLE DADO UN ID
    @classmethod
    def get_responsable(self, id):
        sql = 'SELECT * FROM docente where id = %s'
        cursor = self.db.cursor()
        cursor.execute(sql, (id))

        return cursor.fetchone()
    
    
    # INSERTAR RESPONSABLE
    @classmethod
    def insert(self, responsable):
        sql = """
            INSERT INTO responsable (apellido, nombre, fecha_nac, localidad_id, domicilio, genero_id, tipo_doc_id, numero, tel)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor = self.db.cursor()
        cursor.execute(sql, (
                             responsable.apellido, 
                             responsable.nombre, 
                             responsable.fecha_nac, 
                             responsable.localidad_id,
                             responsable.domicilio, 
                             responsable.genero_id, 
                             responsable.tipo_doc_id, 
                             responsable.numero, 
                             responsable.tel))
        self.db.commit()

        return True
    
    # RECUPERAR TODOS LOS RESPONSABLES POR TERMINO DE BUSQUEDA
    @classmethod
    def get_responsables(self, termino = None):
        params = []
        sql = """
            SELECT * FROM responsable
        """
        if termino != None:
            termino = '%'+termino+'%'
            sql = sql + """ AND (nombre LIKE %s OR apellido LIKE %s) """
            params.append(termino)
            params.append(termino)

        cursor = self.db.cursor()
        cursor.execute(sql, params)

        return cursor.fetchall()
    
    # RECUPERAR TODOS LOS RESPONSABLES POR TERMINO DE BUSQUEDA POR ROL Y PAGINADOS
    @classmethod
    def get_responsables_paginados(self, limit, offset = 1, termino = None):
        
        sql = """
            SELECT * FROM responsable
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
    
    
    # ELIMINAR UN RESPONSABLE
    @classmethod
    def eliminar(self, id_responsable):
        cursor = self.db.cursor()
        
        sql = """
            DELETE FROM responsable 
            WHERE id = %s
        """

        o = cursor.execute(sql, (id_responsable))
        self.db.commit()

        return o
    
    # EDITAR UN RESPONSABLE
    @classmethod
    def editar(self, id_responsable, apellido, nombre, fecha_nac, localidad_id,domicilio, genero_id,tipo_doc_id, numero, tel):
        
        sql = """
            UPDATE responsable 
            SET apellido = %s, nombre = %s, fecha_nac = %s, localidad_id = %s, domicilio = %s, genero_id = %s, tipo_doc_id = %s, numero = %s, tel = %s
            WHERE id = %s
        """

        cursor = self.db.cursor()
        ok = cursor.execute(sql, ( apellido, nombre, fecha_nac, localidad_id, domicilio, genero_id, tipo_doc_id, numero, tel,id_responsable))
        self.db.commit()

        return ok