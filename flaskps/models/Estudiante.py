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
        sql = 'SELECT * FROM estudiante'
        cursor = self.db.cursor()
        cursor.execute(sql)

        return cursor.fetchall()
    
    
    # RECUPERAR UN ESTUDIANTE DADO UN ID
    @classmethod
    def get_estudiante(self, id):
        sql = 'SELECT * FROM estudiante WHERE id = %s'
        cursor = self.db.cursor()
        cursor.execute(sql, (id))

        return cursor.fetchone()
    
    # RECUPERAR ESTUDIANTE DADO UN ID CON INFORMACION
    @classmethod
    def get_estudiante_show(self, id):
        sql = """
            SELECT e.id, e.apellido, e.nombre, e.fecha_nac, e.domicilio, e.numero,
                    e.tel, g.nombre AS genero, n.nombre AS nivel, es.nombre AS escuela,
                    b.nombre AS barrio
            FROM estudiante e
            INNER JOIN genero g ON (g.id = e.genero_id)
            INNER JOIN nivel n ON (n.id = e.nivel_id)
            INNER JOIN escuela es ON (es.id = e.escuela_id)
            INNER JOIN barrio b ON (b.id = e.barrio_id)
            WHERE e.id = %s 
        """
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

        return cursor.lastrowid

    
    
    # EDITAR ESTUDIANTE
    @classmethod
    def editar(self, id_estudiante, apellido, nombre, fecha_nac, localidad_id,nivel_id,domicilio, genero_id, escuela_id,tipo_doc_id, numero, tel,barrio_id):
        
        sql = """
            UPDATE estudiante 
            SET apellido = %s, nombre = %s, fecha_nac = %s, localidad_id = %s, nivel_id = %s,domicilio = %s, genero_id = %s, escuela_id = %s,tipo_doc_id = %s, numero = %s, tel = %s,barrio_id = %s
            WHERE id = %s
        """

        ok = cursor = self.db.cursor()
        cursor.execute(sql, ( apellido, nombre, fecha_nac, localidad_id, nivel_id, domicilio, genero_id, escuela_id, tipo_doc_id, numero, tel, barrio_id,id_estudiante))
        self.db.commit()

        return ok

    # AGREGAR RELACION CON RESPONSABLE
    @classmethod 
    def agregar_responsable(self, id_responsable, id_estudiante, id_tipo_responsable ):
        cursor = self.db.cursor()

        sql = """
            INSERT INTO responsable_estudiante (responsable_id, estudiante_id, tipo_responsable_id)
            VALUES (%s, %s, %s)
        """
        
        cursor.execute(sql, ( id_responsable, id_estudiante, id_tipo_responsable ))
        self.db.commit()
        
        return True

    # MODIFICAR RESPONSABLE
    @classmethod
    def editar_responsable(self, id_responsable, id_estudiante, id_tipo_responsable ):
        cursor = self.db.cursor()

        sql = """
            UPDATE responsable_estudiante 
            SET responsable_id = %s, tipo_responsable_id = %s
            WHERE estudiante_id = %s
        """
        
        cursor.execute(sql, ( id_responsable, id_tipo_responsable, id_estudiante ))
        self.db.commit()
        
        return True

    
    # OBTENER RESPONSABLE
    @classmethod
    def get_responsable(self, id_estudiante):

        sql = """
            SELECT r.id, r.apellido, r.nombre, r.fecha_nac, r.tel, re.tipo_responsable_id, tr.nombre AS tipo_responsable 
            FROM responsable r
            INNER JOIN responsable_estudiante re ON (r.id = re.responsable_id)
            INNER JOIN estudiante e ON (re.estudiante_id = e.id)
            INNER JOIN tipo_responsable tr ON (re.tipo_responsable_id = tr.id)
            WHERE e.id = %s
        """
        cursor = self.db.cursor()
        cursor.execute(sql, ( id_estudiante ))
        return cursor.fetchone()
    

    # RECUPERAR TODOS LOS ESTUDIANTES POR TERMINO DE BUSQUEDA
    @classmethod
    def get_estudiantes(self, termino = None):
        params = []
        sql = """
            SELECT * FROM estudiante
        """
        if termino != None:
            termino = '%'+termino+'%'
            sql = sql + """ WHERE (nombre LIKE %s OR apellido LIKE %s) """
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
    
    
    # ELIMINAR UN ESTUDIANTE
    @classmethod
    def eliminar(self, id_estudiante):
        cursor = self.db.cursor()
        
        sql = """
            DELETE FROM estudiante 
            WHERE id = %s
        """

        ok = cursor.execute(sql, (id_estudiante))
        self.db.commit()

        return ok

    # OBTENER RESPONSABLES
    @classmethod
    def get_responsables_select(self):
        
        sql = """
            SELECT id, apellido, nombre FROM responsable
        """

        cursor = self.db.cursor()
        cursor.execute(sql)

        res = cursor.fetchall()
        lista = []
        for l in res:
            lista.append( (l['id'], l['nombre'] + ' ' + l['apellido']) )
        return lista

    # ACTIVAR / DESACTIVAR UN ESTUDIANTE
    @classmethod
    def activar(self, id_estudiante):
        cursor = self.db.cursor()
        
        sql = """
            UPDATE estudiante 
            SET borrado_logico = not borrado_logico
            WHERE id = %s
        """

        ok = cursor.execute(sql, (id_estudiante))
        self.db.commit()

        return ok 