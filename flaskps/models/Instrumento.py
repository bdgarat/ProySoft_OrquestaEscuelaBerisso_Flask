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
        print(cursor)
        return True