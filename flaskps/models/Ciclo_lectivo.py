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

    # VER SI EXISTE EL CICLO LECTIVO Y TALLER
    @classmethod
    def existe(self, ciclo_lectivo, nombre_taller):
        cursor = self.db.cursor()
        
        sql = """
            SELECT id FROM ciclo_lectivo WHERE fecha_ini=%s AND fecha_fin=%s AND semestre=%s
        """

        cursor.execute(sql, (ciclo_lectivo.fecha_ini, ciclo_lectivo.fecha_fin, ciclo_lectivo.semestre))
        id_ciclo_lectivo = cursor.fetchone()['id']
        
        sql = """
            SELECT id FROM taller where nombre=%s
        """

        cursor.execute(sql, (taller.nombre))
        id_taller = cursor.fetchone()['id']
        
        sql = """
            SELECT *
            FROM ciclo_lectivo_taller
            WHERE ciclo_lectivo_id = %s AND taller_id = %s
        """
        cursor.execute(sql, (id_ciclo_lectivo, id_taller))
        existe = cursor.fetchone()
        
        if existe:
            return True

        
        return False

    # OBTENER TALLERES DE LA DB
    @classmethod
    def all_talleres(self):
        sql = """
            SELECT t.nombre
            FROM taller t
        """
        cursor = self.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()


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

    # RECUPERAR EL TALLER DE UN CICLO LECTIVO DADO UN ID CICLO LECTIVO
    @classmethod
    def get_taller(self, id_ciclo_lectivo):
        sql = """
                SELECT t.nombre 
                FROM ciclo_lectivo c
                INNER JOIN ciclo_lectivo_taller ct ON (c.id = ct.ciclo_lectivo_id)
                INNER JOIN taller t ON (t.id = ct.taller_id) 
                WHERE c.id = %s
            """
        cursor = self.db.cursor()
        cursor.execute(sql, (id_ciclo_lectivo))

        return cursor.fetchone()


    # RECUPERAR LOS DOCENTES DE UN CICLO LECTIVO DADO UN ID CICLO LECTIVO
    @classmethod
    def get_docentes(self, id_ciclo_lectivo):
        sql = """
                SELECT d.nombre AND d.apellido
                FROM ciclo_lectivo c
                INNER JOIN docente_responsable_taller drt ON (c.id = drt.ciclo_lectivo_id)
                INNER JOIN docente d ON (d.id = drt.docente_id) 
                WHERE c.id = %s
            """
        cursor = self.db.cursor()
        cursor.execute(sql, (id_ciclo_lectivo))

        return cursor.fetchall()


    # RECUPERAR LOS ESTUDIANTES DE UN CICLO LECTIVO DADO UN ID CICLO LECTIVO
    @classmethod
    def get_estudiantes(self, id_ciclo_lectivo):
        sql = """
                SELECT e.nombre AND e.apellido
                FROM ciclo_lectivo c
                INNER JOIN estudiante_taller aet ON (c.id = et.ciclo_lectivo_id)
                INNER JOIN estudiante e ON (e.id = et.estudiante_id) 
                WHERE c.id = %s
            """
        cursor = self.db.cursor()
        cursor.execute(sql, (id_ciclo_lectivo))

        return cursor.fetchall()

    # AGREGAR TALLER A UN CICLO LECTIVO
    @classmethod
    def agregar_taller(self, ciclo_lectivo, nombre_taller):
        
        cursor = self.db.cursor()
        
        sql = """
            SELECT id FROM ciclo_lectivo WHERE fecha_ini=%s AND fecha_fin=%s AND semestre=%s
        """

        cursor.execute(sql, (ciclo_lectivo.fecha_ini, ciclo_lectivo.fecha_fin, ciclo_lectivo.semestre))
        id_ciclo_lectivo = cursor.fetchone()['id']
        
        sql = """
            SELECT id FROM taller where nombre=%s
        """

        cursor.execute(sql, (nombre_taller))
        id_taller = cursor.fetchone()['id']
        
        sql = """
            SELECT *
            FROM ciclo_lectivo_taller
            WHERE ciclo_lectivo_id = %s AND taller_id = %s
        """
        cursor.execute(sql, (id_ciclo_lectivo, id_taller))
        existe = cursor.fetchone()
        
        if existe:
            return False

        sql = """
            INSERT INTO ciclo_lectivo_taller (taller_id, ciclo_lectivo_id)
            VALUES (%s, %s)
        """
        cursor.execute(sql, (id_taller, id_ciclo_lectivo))

        self.db.commit()

        return True
    
    # QUITAR TALLER DE UN CICLO LECTIVO
    @classmethod
    def quitar_taller(self, ciclo_lectivo, nombre_taller):
        
        cursor = self.db.cursor()
        
        sql = """
            SELECT id FROM ciclo_lectivo WHERE fecha_ini=%s AND fecha_fin=%s AND semestre=%s
        """

        cursor.execute(sql, (ciclo_lectivo.fecha_ini, ciclo_lectivo.fecha_fin, ciclo_lectivo.semestre))
        id_ciclo_lectivo = cursor.fetchone()['id']
        
        sql = """
            SELECT id FROM taller where nombre=%s
        """

        cursor.execute(sql, (nombre_taller))
        id_taller = cursor.fetchone()['id']
        
        sql = """
            DELETE 
            FROM ciclo_lectivo_taller 
            WHERE taller_id = %s AND ciclo_lectivo_id = %s
        """

        cursor.execute(sql, (id_taller, id_ciclo_lectivo))
        self.db.commit()

        return True

    # AGREGAR DOCENTE A UN TALLER
    @classmethod
    def agregar_docente(self, ciclo_lectivo, taller, docente):
        
        cursor = self.db.cursor()
        
        sql = """
            SELECT id FROM ciclo_lectivo WHERE fecha_ini=%s AND fecha_fin=%s AND semestre=%s
        """

        cursor.execute(sql, (ciclo_lectivo.fecha_ini, ciclo_lectivo.fecha_fin, ciclo_lectivo.semestre))
        id_ciclo_lectivo = cursor.fetchone()['id']
        
        sql = """
            SELECT id FROM docente where nombre=%s AND apellido=%s AND numero=%s
        """

        cursor.execute(sql, (docente.nombre, docente.apellido, docente.numero))
        id_docente = cursor.fetchone()['id']
        
        sql = """
            SELECT id FROM taller where nombre=%s AND nombre_corto=%s
        """

        cursor.execute(sql, (taller.nombre, taller.nombre_corto))
        id_taller = cursor.fetchone()['id']

        sql = """
            SELECT *
            FROM docente_responsable_taller
            WHERE ciclo_lectivo_id = %s AND taller_id = %s AND docente_id = %s
        """
        cursor.execute(sql, (id_ciclo_lectivo, id_taller, id_docente))
        existe = cursor.fetchone()
        
        if existe:
            return False

        sql = """
            INSERT INTO ciclo_lectivo_taller (taller_id, ciclo_lectivo_id, docente_id)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (id_taller, id_ciclo_lectivo, id_docente))

        self.db.commit()

        return True
    
    # QUITAR DOCENTE DE UN TALLER
    @classmethod
    def quitar_docente(self, ciclo_lectivo, taller, docente):
        
        cursor = self.db.cursor()
        
        sql = """
            SELECT id FROM ciclo_lectivo WHERE fecha_ini=%s AND fecha_fin=%s AND semestre=%s
        """

        cursor.execute(sql, (ciclo_lectivo.fecha_ini, ciclo_lectivo.fecha_fin, ciclo_lectivo.semestre))
        id_ciclo_lectivo = cursor.fetchone()['id']
        
        sql = """
            SELECT id FROM docente where nombre=%s AND apellido=%s AND numero=%s
        """

        cursor.execute(sql, (docente.nombre, docente.apellido, docente.numero))
        id_docente = cursor.fetchone()['id']
        
        sql = """
            SELECT id FROM taller where nombre=%s AND nombre_corto=%s
        """

        cursor.execute(sql, (taller.nombre, taller.nombre_corto))
        id_taller = cursor.fetchone()['id']
        
        sql = """
            DELETE 
            FROM docente_responsable_taller 
            WHERE taller_id = %s AND ciclo_lectivo_id = %s AND docente_id = %s
        """

        cursor.execute(sql, (id_taller, id_ciclo_lectivo, id_docente))
        self.db.commit()

        return True

    # AGREGAR ESTUDIANTE A UN TALLER
    @classmethod
    def agregar_estudiante(self, ciclo_lectivo, taller, estudiante):
        
        cursor = self.db.cursor()
        
        sql = """
            SELECT id FROM ciclo_lectivo WHERE fecha_ini=%s AND fecha_fin=%s AND semestre=%s
        """

        cursor.execute(sql, (ciclo_lectivo.fecha_ini, ciclo_lectivo.fecha_fin, ciclo_lectivo.semestre))
        id_ciclo_lectivo = cursor.fetchone()['id']
        
        sql = """
            SELECT id FROM estudiante where nombre=%s AND apellido=%s AND numero=%s
        """

        cursor.execute(sql, (estudiante.nombre, estudiante.apellido, estudiante.numero))
        id_estudiante = cursor.fetchone()['id']
        
        sql = """
            SELECT id FROM taller where nombre=%s AND nombre_corto=%s
        """

        cursor.execute(sql, (taller.nombre, taller.nombre_corto))
        id_taller = cursor.fetchone()['id']

        sql = """
            SELECT *
            FROM estudiante_taller
            WHERE ciclo_lectivo_id = %s AND taller_id = %s AND estudiante_id = %s
        """
        cursor.execute(sql, (id_ciclo_lectivo, id_taller, id_estudiante))
        existe = cursor.fetchone()
        
        if existe:
            return False

        sql = """
            INSERT INTO estudiante_taller (taller_id, ciclo_lectivo_id, estudiante_id)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (id_taller, id_ciclo_lectivo, id_estudiante))

        self.db.commit()

        return True
    
    # QUITAR ESTUDIANTE DE UN TALLER
    @classmethod
    def quitar_estudiante(self, ciclo_lectivo, taller, estudiante):
        
        cursor = self.db.cursor()
        
        sql = """
            SELECT id FROM ciclo_lectivo WHERE fecha_ini=%s AND fecha_fin=%s AND semestre=%s
        """

        cursor.execute(sql, (ciclo_lectivo.fecha_ini, ciclo_lectivo.fecha_fin, ciclo_lectivo.semestre))
        id_ciclo_lectivo = cursor.fetchone()['id']
        
        sql = """
            SELECT id FROM estudiante where nombre=%s AND apellido=%s AND numero=%s
        """

        cursor.execute(sql, (estudiante.nombre, estudiante.apellido, estudiante.numero))
        id_estudiante = cursor.fetchone()['id']
        
        sql = """
            SELECT id FROM taller where nombre=%s AND nombre_corto=%s
        """

        cursor.execute(sql, (taller.nombre, taller.nombre_corto))
        id_taller = cursor.fetchone()['id']
        
        sql = """
            DELETE 
            FROM estudiante_taller 
            WHERE taller_id = %s AND ciclo_lectivo_id = %s AND estudiante_id = %s
        """

        cursor.execute(sql, (id_taller, id_ciclo_lectivo, id_estudiante))
        self.db.commit()

        return True