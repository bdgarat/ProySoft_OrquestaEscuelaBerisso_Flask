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
        sql = """ SELECT i.id, i.nombre, i.numero_inventario, i.foto, ti.nombre AS tipo  
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
    
    # RECUPERAR TODOS LOS INSTRUMENTOS POR TERMINO DE BUSQUEDA
    @classmethod
    def get_instrumentos(self, termino = None):
        params = []
        sql = """
            SELECT i.id, i.nombre, i.numero_inventario, i.foto, ti.nombre AS tipo  
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
            SELECT i.id, i.nombre, i.numero_inventario, i.foto, ti.nombre AS tipo  
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