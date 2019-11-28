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
        sql = 'SELECT * FROM ciclo_lectivo WHERE borrado_logico = 0'
        cursor = self.db.cursor()
        cursor.execute(sql)

        return cursor.fetchall()
    
    
    # RECUPERAR UN CICLO LECTIVO DADO UN ID
    @classmethod
    def get_ciclo_lectivo(self, id):
        sql = 'SELECT * FROM ciclo_lectivo where borrado_logico = 0 and id = %s'
        cursor = self.db.cursor()
        cursor.execute(sql, (id))

        return cursor.fetchone()
    
    
    # INSERTAR CICLO LECTIVO
    @classmethod
    def insert(self, ciclo_lectivo):
        sql = """
            INSERT INTO ciclo_lectivo (fecha_ini, fecha_fin, semestre, borrado_logico)
            VALUES (%s, %s, %s, 0)
        """

        cursor = self.db.cursor()
        cursor.execute(sql, (
                             ciclo_lectivo.fecha_ini, 
                             ciclo_lectivo.fecha_fin, 
                             ciclo_lectivo.semestre ))
        self.db.commit()

        return True


    # RECUPERAR TODOS LOS CICLOS LECTIVOS POR TERMINO DE BUSQUEDA
    @classmethod
    def get_ciclos_lectivos(self, termino = None):
        params = []
        sql = """
                SELECT *
                FROM ciclo_lectivo
                WHERE borrado_logico = 0
            """
        if termino != None:
            termino = '%'+termino+'%'
            sql = sql + """ AND (YEAR(fecha_ini) LIKE %s OR YEAR(fecha_fin) LIKE %s) """
            params.append(termino)
            params.append(termino)

        sql = sql + """ ORDER BY YEAR(fecha_ini) desc"""
         
        cursor = self.db.cursor()
        cursor.execute(sql, params)

        return cursor.fetchall()
    
    # RECUPERAR TODOS LOS CICLOS LECTIVOS POR TERMINO DE BUSQUEDA Y PAGINADOS
    @classmethod
    def get_ciclos_lectivos_paginados(self, limit, offset = 1, termino = None):
        
        sql = """
                SELECT *
                FROM ciclo_lectivo c
                WHERE borrado_logico = 0
        """
        if termino != None:
            termino = '%'+termino+'%'
            sql = sql + """ AND (YEAR(fecha_ini) LIKE %s OR YEAR(fecha_fin) LIKE %s) """
        
        sql = sql + """ ORDER BY YEAR(fecha_ini) desc"""
        sql = sql + """
                    LIMIT %s OFFSET %s
                    """

        if termino != None:
            params = (termino, termino, limit, offset)
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


    @classmethod
    def existe(self, semestre, año):
        cursor = self.db.cursor()
        
        sql = """ SELECT id
            FROM ciclo_lectivo
            WHERE semestre = %s
            AND YEAR(fecha_ini) like %s """
            
        cursor = self.db.cursor()
        cursor.execute(sql, (semestre, año))
        return cursor.fetchone()
    
    @classmethod
    def se_superponen(self, fecha_inicio_semestre):
        cursor = self.db.cursor()
        
        año = fecha_inicio_semestre.year
        
        sql = """ SELECT fecha_fin
            FROM ciclo_lectivo
            WHERE semestre = 1
            AND YEAR(fecha_ini) like %s """
            
        cursor = self.db.cursor()
        cursor.execute(sql, (año))
        fecha_fin = cursor.fetchone()['fecha_fin']
        
        return fecha_fin > fecha_inicio_semestre


    # INSERTAR CICLO LECTIVO
    @classmethod
    def insert(self, ciclo_lectivo):
        sql = """
            INSERT INTO ciclo_lectivo (fecha_ini, fecha_fin, semestre, borrado_logico)
            VALUES (%s, %s, %s, 0)
        """

        cursor = self.db.cursor()
        cursor.execute(sql, (
                             ciclo_lectivo.fecha_ini, 
                             ciclo_lectivo.fecha_fin, 
                             ciclo_lectivo.semestre ))
        self.db.commit()

        return True
