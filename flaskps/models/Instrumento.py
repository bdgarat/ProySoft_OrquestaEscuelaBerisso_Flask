class Instrumento(object):
    
    db = None

    def __init__(self, nombre, numero_inventario, tipo_id, foto):
        self.nombre = nombre
        self.numero_inventario = numero_inventario
        self.tipo_id = tipo_id
        self.foto = foto

    # RECUPERAR TODOS LOS INSTRUMENTOS
    @classmethod
    def all(self):
        sql = """ SELECT i.id, i.nombre, i.numero_inventario, i.foto, ti.nombre AS tipo  
                  FROM instrumento i
                  INNER JOIN tipo_instrumento ti ON (ti.id = i.tipo_id)
        """
        cursor = self.db.cursor()
        cursor.execute(sql)

        return cursor.fetchall()

    # RECUPERAR UN INSTRUMENTO DADO UN ID
    @classmethod
    def get_instrumento(self, id):
        sql = """ SELECT i.id, i.nombre, i.numero_inventario, i.foto, i.tipo_id, ti.nombre AS tipo  
                  FROM instrumento i
                  INNER JOIN tipo_instrumento ti ON (ti.id = i.tipo_id)
                  WHERE i.id = %s
        """
        cursor = self.db.cursor()
        cursor.execute(sql, (id))

        return cursor.fetchone()

    # INSERTAR INSTRUMENTO
    @classmethod
    def insert(self, instrumento):
        sql = """
            INSERT INTO instrumento (nombre, numero_inventario,tipo_id, foto)
            VALUES (%s, %s, %s, %s)
        """

        cursor = self.db.cursor()
        cursor.execute(sql, (instrumento.nombre,
                             instrumento.numero_inventario,
                             instrumento.tipo_id,
                             instrumento.foto))
        
        self.db.commit()
        return True
    
    # EDITAR INSTRUMENTO
    @classmethod
    def editar(self, id_instrumento, nombre, numero_inventario, tipo_id, foto):
        print(foto=='')
        if foto == '':
            sql = """
                UPDATE instrumento 
                SET nombre = %s, numero_inventario = %s, tipo_id = %s
                WHERE id = %s
            """
            params=(nombre, numero_inventario, tipo_id, id_instrumento)
        else:
            sql = """
                UPDATE instrumento 
                SET nombre = %s, numero_inventario = %s, tipo_id = %s, foto = %s
                WHERE id = %s
            """
            params=(nombre, numero_inventario, tipo_id, foto, id_instrumento)

        ok = cursor = self.db.cursor()
        cursor.execute(sql, params)
        self.db.commit()

        return ok




    # RECUPERAR TODOS LOS INSTRUMENTOS POR TERMINO DE BUSQUEDA
    @classmethod
    def get_instrumentos(self, termino = None):
        params = []
        sql = """
            SELECT i.id  
            FROM instrumento i
            INNER JOIN tipo_instrumento ti ON (ti.id = i.tipo_id)
        """
        if termino != None:
            termino = '%'+termino+'%'
            sql = sql + """ WHERE (i.numero_inventario LIKE %s ) """
            params.append(termino)

        cursor = self.db.cursor()
        cursor.execute(sql, params)

        return cursor.fetchall()
    
    # RECUPERAR TODOS LOS INSTRUMENTOS POR TERMINO DE BUSQUEDA Y PAGINADOS
    @classmethod
    def get_instrumentos_paginados(self, limit, offset = 1, termino = None):
        
        sql = """
            SELECT i.id, i.nombre, i.numero_inventario, ti.nombre AS tipo  
            FROM instrumento i
            INNER JOIN tipo_instrumento ti ON (ti.id = i.tipo_id)
        """

        if termino != None:
            termino = '%'+termino+'%'
            sql = sql + """ WHERE (i.numero_inventario LIKE %s ) """
            
        sql = sql + """
                    LIMIT %s OFFSET %s
                    """

        if termino != None:
            params = (termino, limit, offset)
        else:
            params = (limit, offset)

        cursor = self.db.cursor()
        cursor.execute(sql, params)

        return cursor.fetchall()
    
    # VER SI EXISTE NUMERO DE INVENTARIO
    @classmethod
    def existe(self, numero_inventario):
        sql = """
            SELECT id
            FROM instrumento
            WHERE numero_inventario = %s
        """
        cursor = self.db.cursor()
        cursor.execute(sql, (numero_inventario))
        return cursor.fetchone()
    
    # ELIMINAR UN INSTRUMENTO
    @classmethod
    def eliminar(self, id_instrumento):
        cursor = self.db.cursor()
        
        sql = """
            DELETE FROM instrumento 
            WHERE id = %s
        """

        ok = cursor.execute(sql, (id_instrumento))
        self.db.commit()

        return ok
    