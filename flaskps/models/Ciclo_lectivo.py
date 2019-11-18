from datetime import datetime

class Ciclo_lectivo(object):
    
    db = None

    def __init__(self, fecha_ini, fecha_fin, semestre):
        self.fecha_ini = fecha_ini
        self.fecha_fin = fecha_fin
        self.semestre = semestre
        
        
    # RECUPERAR TODOS LOS CICLOS LECTIVOS
    @classmethod
    def all(self):
        sql = 'SELECT * FROM ciclo_lectivo WHERE WHERE borrado_logico = 0'
        cursor = self.db.cursor()
        cursor.execute(sql)

        return cursor.fetchall()
    
    
    # RECUPERAR UN CICLO LECTIVO DADO UN ID
    @classmethod
    def get_ciclo_lectivo(self, id):
        sql = 'SELECT * FROM ciclo_lectivo where WHERE borrado_logico = 0 AND id = %s'
        cursor = self.db.cursor()
        cursor.execute(sql, (id))

        return cursor.fetchone()
    
    
    # INSERTAR CICLO LECTIVO
    @classmethod
    def insert(self, ciclo_lectivo):
        sql = """
            INSERT INTO ciclo_lectivo (fecha_ini, fecha_fin, semestre)
            VALUES (%s, %s, %s)
        """

        cursor = self.db.cursor()
        cursor.execute(sql, (
                             ciclo_lectivo.fecha_ini, 
                             ciclo_lectivo.fecha_fin, 
                             ciclo_lectivo.semestre))
        self.db.commit()

        return True
    
    # EDITAR UN CICLO LECTIVO
    @classmethod
    def editar(self, id_ciclo_lectivo, fecha_ini, fecha_fin, semestre):
        
        sql = """
            UPDATE ciclo_lectivo 
            SET fecha_ini = %s, fecha_fin = %s, semestre = %s
            WHERE id = %s
        """

        cursor = self.db.cursor()
        ok = cursor.execute(sql, (fecha_ini, fecha_fin, semestre, id_ciclo_lectivo))
        self.db.commit()

        return ok

    # RECUPERAR TODOS LOS CICLOS LECTIVOS POR TERMINO DE BUSQUEDA
    @classmethod
    def get_ciclos_lectivos(self, termino = None):
        params = []
        sql = """
            SELECT * FROM ciclo_lectivo
            WHERE borrado_logico = 0
        """
        if termino != None:
            termino = '%'+termino+'%'
            sql = sql + """ AND (fecha_ini LIKE %s OR fecha_fin LIKE %s OR semestre LIKE %s) """
            params.append(termino)
            params.append(termino)
            params.append(termino)

        cursor = self.db.cursor()
        cursor.execute(sql, params)

        return cursor.fetchall()
    
    # RECUPERAR TODOS LOS CICLOS LECTIVOS POR TERMINO DE BUSQUEDA Y PAGINADOS
    @classmethod
    def get_ciclos_lectivos_paginados(self, limit, offset = 1, termino = None):
        
        sql = """
            SELECT * FROM ciclo_lectivo
            WHERE borrado_logico = 0
        """
        if termino != None:
            termino = '%'+termino+'%'
            sql = sql + """ AND (fecha_ini LIKE %s OR fecha_fin LIKE %s OR semestre LIKE %s) """
            
        sql = sql + """
                    LIMIT %s OFFSET %s
                    """

        if termino != None:
            params = (termino, termino, termino, limit, offset)
        else:
            params = (limit, offset)

        cursor = self.db.cursor()
        cursor.execute(sql, params)

        return cursor.fetchall()
    
    # ELIMINAR UN CICLO LECTIVO
    @classmethod
    def eliminar(self, id_ciclo_lectivo):
        cursor = self.db.cursor()
        
        sql = """
            UPDATE ciclo_lectivo 
            SET borrado_logico = 1
            WHERE id = %s
        """

        o = cursor.execute(sql, (id_ciclo_lectivo))
        self.db.commit()

        return o