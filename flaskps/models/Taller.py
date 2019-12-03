

class Taller(object):
    
    db = None   
    
    # RECUPERAR TODOS LOS TALLERES DADO UN ID DE CICLO
    @classmethod
    def get_talleres_ciclo(self, id_ciclo):
        sql = ''
        cursor = self.db.cursor()
        cursor.execute(sql, (id_ciclo))

        return cursor.fetchall()
    

    # RECUPERAR TALLER
    @classmethod
    def get_taller(self, id_taller):
        sql = """SELECT * FROM taller
               WHERE id = %s"""
        cursor = self.db.cursor()
        cursor.execute(sql, (id_taller))

        return cursor.fetchall()

    # OBTENER INFORMACION DE TALLER
    @classmethod
    def get_taller_show(self, id_taller, id_ciclo):
        sql = """
            SELECT t.id, t.nombre, t.nombre_corto
            FROM taller t
            INNER JOIN ciclo_lectivo_taller clt ON (clt.taller_id = t.id)
            WHERE clt.taller_id = %s
            AND clt.ciclo_lectivo_id = %s
        """
        cursor = self.db.cursor()
        cursor.execute(sql, (id_taller, id_ciclo))

        return cursor.fetchone()

    @classmethod    
    def get_estudiantes_show(self, id_taller, id_ciclo):
        sql = """
            SELECT e.apellido, e.nombre, e.tel, esc.nombre AS escuela, b.nombre AS barrio
            FROM estudiante_taller et
            INNER JOIN estudiante e ON (et.estudiante_id = e.id)
            INNER JOIN escuela esc ON (esc.id = e.escuela_id)
            INNER JOIN barrio b ON (b.id = e.barrio_id)
            WHERE et.taller_id = %s
            AND et.ciclo_lectivo_id = %s
        """
        cursor = self.db.cursor()
        cursor.execute(sql, (id_taller, id_ciclo))
        return cursor.fetchall()
    
    @classmethod
    def get_docentes_show(self, id_taller, id_ciclo):
        sql = """
            SELECT d.apellido, d.nombre, d.tel, d.domicilio
            FROM docente_responsable_taller dt
            INNER JOIN docente d ON (dt.docente_id = d.id)
            WHERE dt.taller_id = %s
            AND dt.ciclo_lectivo_id = %s
        """
        cursor = self.db.cursor()
        cursor.execute(sql, (id_taller, id_ciclo))
        return cursor.fetchall()
    

    # RECUPERAR TODOS LOS CICLOS LECTIVOS POR TERMINO DE BUSQUEDA
    @classmethod
    def get_talleres_por_ciclo(self, id_ciclo, termino = None):
        params = []
        sql = """
                SELECT * FROM ciclo_lectivo_taller c 
                INNER JOIN taller t 
                ON c.taller_id = t.id 
                WHERE ciclo_lectivo_id = %s
            """
            
        params.append(id_ciclo)
        
        if termino != None:
            termino = '%'+termino+'%'
            sql = sql + """ AND (t.nombre LIKE %s OR t.nombre_corto LIKE %s) """
            params.append(termino)
            params.append(termino)
         
        cursor = self.db.cursor()
        cursor.execute(sql, params)

        return cursor.fetchall()

    # RECUPERAR TODOS LOS CICLOS LECTIVOS POR TERMINO DE BUSQUEDA
    @classmethod
    def get_talleres(self, termino = None):
        params = []
        sql = """
                SELECT * FROM taller t 
            """
            
        
        if termino != None:
            termino = '%'+termino+'%'
            sql = sql + """ WHERE (t.nombre LIKE %s OR t.nombre_corto LIKE %s) """
            params.append(termino)
            params.append(termino)
         
        cursor = self.db.cursor()
        cursor.execute(sql, params)

        return cursor.fetchall()

    # RECUPERAR TODOS LOS CICLOS LECTIVOS POR TERMINO DE BUSQUEDA Y PAGINADOS
    @classmethod
    def get_talleres_paginados(self, limit, offset = 1, termino = None):

        sql = """
                SELECT * FROM taller t
        """
        
        if termino != None:
            termino = '%'+termino+'%'
            sql = sql + """ WHERE (t.nombre LIKE %s OR t.nombre_corto LIKE %s) """

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
    
    # RECUPERAR TODOS LOS CICLOS LECTIVOS POR TERMINO DE BUSQUEDA Y PAGINADOS
    @classmethod
    def get_talleres_por_ciclo_paginados(self, limit, id_ciclo, offset = 1, termino = None):

        sql = """
                SELECT * FROM ciclo_lectivo_taller c 
                INNER JOIN taller t 
                ON c.taller_id = t.id 
                WHERE ciclo_lectivo_id = %s
        """
        
        if termino != None:
            termino = '%'+termino+'%'
            sql = sql + """ AND (t.nombre LIKE %s OR t.nombre_corto LIKE %s) """

        sql = sql + """
                    LIMIT %s OFFSET %s
                    """

        if termino != None:
            params = (id_ciclo, termino, termino, limit, offset)
        else:
            params = (id_ciclo, limit, offset)

        cursor = self.db.cursor()
        cursor.execute(sql, params)

        return cursor.fetchall()



    # INSERTAR DOCENTE EN UN TALLER DEL CICLO LECTIVO
    @classmethod
    def insertar_docente_en_taller(self, id_ciclo, id_taller, id_docente):
        sql = """
            INSERT INTO docente_responsable_taller (ciclo_lectivo_id, taller_id, docente_id)
            VALUES (%s, %s, %s)
        """

        cursor = self.db.cursor()
        cursor.execute(sql, (
                             id_ciclo,
                             id_taller,
                             id_docente ))
        self.db.commit()

        return True


    # INSERTAR ESTUDIANTE EN UN TALLER DEL CICLO LECTIVO
    @classmethod
    def insertar_estudiante_en_taller(self, id_ciclo, id_taller, id_estudiante):
        sql = """
            INSERT INTO estudiante_taller (ciclo_lectivo_id, taller_id, estudiante_id)
            VALUES (%s, %s, %s)
        """

        cursor = self.db.cursor()
        cursor.execute(sql, (
                             id_ciclo,
                             id_taller,
                             id_estudiante ))
        self.db.commit()

        return True

    # INSERTAR TALLER EN UN CICLO LECTIVO
    @classmethod
    def insertar_taller_en_ciclo_lectivo(self, id_ciclo, id_taller):
        sql = """
            INSERT INTO ciclo_lectivo_taller (ciclo_lectivo_id, taller_id)
            VALUES (%s, %s)
        """

        cursor = self.db.cursor()
        cursor.execute(sql, (
                             id_ciclo,
                             id_taller ))
        self.db.commit()

        return True

    # EXISTE ESTUDIANTE EN UN TALLER DEL CICLO LECTIVO
    @classmethod
    def existe_docente_en_taller(self, id_ciclo, id_taller, id_docente):
        sql = """
            SELECT * FROM docente_responsable_taller drt
            WHERE drt.ciclo_lectivo_id = %s AND drt.taller_id = %s AND drt.docente_id = %s
        """

        cursor = self.db.cursor()
        cursor.execute(sql, (
                             id_ciclo,
                             id_taller,
                             id_docente ))
        self.db.commit()

        return cursor.fetchall()

    # EXISTE ESTUDIANTE EN UN TALLER DEL CICLO LECTIVO
    @classmethod
    def existe_estudiante_en_taller(self, id_ciclo, id_taller, id_estudiante):
        sql = """
            SELECT * FROM estudiante_taller et
            WHERE et.ciclo_lectivo_id = %s AND et.taller_id = %s AND et.estudiante_id = %s
        """

        cursor = self.db.cursor()
        cursor.execute(sql, (
                             id_ciclo,
                             id_taller,
                             id_estudiante ))
        self.db.commit()

        return cursor.fetchall()


    # EXISTE TALLER EN UN CICLO LECTIVO
    @classmethod
    def existe_taller_en_ciclo_lectivo(self, id_ciclo, id_taller):
        sql = """
            SELECT * FROM ciclo_lectivo_taller clt
            WHERE clt.taller_id = %s AND clt.ciclo_lectivo_id = %s
        """

        cursor = self.db.cursor()
        cursor.execute(sql, (
                             id_taller,
                             id_ciclo ))
        self.db.commit()

        return cursor.fetchall()

    # ELIMINAR
    # ELIMINAR ESTUDIANTE DEL TALLER Y CICLO
    @classmethod
    def eliminar_estudiante_en_taller(self, id_ciclo, id_taller, id_estudiante):
        sql = """
            DELETE FROM estudiante_taller
            WHERE ciclo_lectivo_id = %s AND taller_id = %s AND estudiante_id = %s
        """

        cursor = self.db.cursor()
        ok= cursor.execute(sql, (
                             id_ciclo,
                             id_taller,
                             id_estudiante ))
        self.db.commit()

        return ok
    
    # ELIMINAR ESTUDIANTE DEL TALLER Y CICLO
    @classmethod
    def eliminar_docente_en_taller(self, id_ciclo, id_taller, id_docente):
        sql = """
            DELETE FROM docente_responsable_taller
            WHERE ciclo_lectivo_id = %s AND taller_id = %s AND docente_id = %s
        """

        cursor = self.db.cursor()
        ok= cursor.execute(sql, (
                             id_ciclo,
                             id_taller,
                             id_docente ))
        self.db.commit()

        return ok
    
    # ELIMINAR TALLER EN CICLO
    @classmethod
    def eliminar_taller_en_ciclo_lectivo(self, id_ciclo, id_taller):
        cursor = self.db.cursor()
        # Primero elimino a los docentes responsables
        sql = """
            DELETE FROM docente_responsable_taller
            WHERE ciclo_lectivo_id = %s AND taller_id = %s
        """
        ok= cursor.execute(sql, (id_ciclo, id_taller))
        self.db.commit()
        # Elimino a los estudiantes inscritos
        sql = """
            DELETE FROM estudiante_taller
            WHERE ciclo_lectivo_id = %s AND taller_id = %s
        """
        ok= cursor.execute(sql, (id_ciclo, id_taller))
        self.db.commit()

        # Elimino el taller del ciclo
        sql = """
            DELETE FROM ciclo_lectivo_taller
            WHERE ciclo_lectivo_id = %s AND taller_id = %s
        """
        ok= cursor.execute(sql, (id_ciclo, id_taller))
        self.db.commit()

        return ok

    
    # ESTUDIANTES POR TALLER+CICLO
    @classmethod
    def estudiantes_ciclo_taller(self, id_ciclo, id_taller):
        sql = """
            SELECT estudiante_id
            FROM estudiante_taller
            WHERE ciclo_lectivo_id = %s
            AND taller_id = %s  
        """
        cursor = self.db.cursor()
        cursor.execute(sql, (id_ciclo, id_taller))
        
        res = cursor.fetchall()
        lista = []
        for l in res:
            lista.append( (l['estudiante_id']))
        
        return lista
    
    # DOCENTE POR TALLER+CICLO
    @classmethod
    def docentes_ciclo_taller(self, id_ciclo, id_taller):
        sql = """
            SELECT docente_id
            FROM docente_responsable_taller
            WHERE ciclo_lectivo_id = %s
            AND taller_id = %s  
        """
        cursor = self.db.cursor()
        cursor.execute(sql, (id_ciclo, id_taller))
        
        res = cursor.fetchall()
        lista = []
        for l in res:
            lista.append( (l['docente_id']))
        
        return lista
    
    # DOCENTE POR TALLER+CICLO DEVOLVIENDO EL ITERABLE
    @classmethod
    def get_docentes_ciclo_taller(self, id_ciclo, id_taller):
        sql = """
            SELECT d.id, d.nombre, d.apellido
            FROM docente_responsable_taller drt
            INNER JOIN docente d ON drt.docente_id = d.id
            WHERE ciclo_lectivo_id = %s
            AND taller_id = %s  
        """
        cursor = self.db.cursor()
        cursor.execute(sql, (id_ciclo, id_taller))
        res = cursor.fetchall()
        lista = []
        for l in res:
            lista.append( (l['id'], l['apellido'].upper()+ " "+l['nombre'].upper()) )
          
        return lista

    # TALLERES POR CICLO
    @classmethod
    def talleres_ciclo(self, id_ciclo):
        sql = """
            SELECT taller_id
            FROM ciclo_lectivo_taller
            WHERE ciclo_lectivo_id = %s
        """
        cursor = self.db.cursor()
        cursor.execute(sql, (id_ciclo))
        
        res = cursor.fetchall()
        lista = []
        for l in res:
            lista.append( (l['taller_id']))
        
        return lista
    
    # AGREGAR HORARIO A CICLO + TALLER + PROFE + NUCLEO + HORARIO + DIA
    @classmethod
    def agregar_horario(self, id_ciclo, id_taller, id_docente, id_nucleo, hora_inicio, hora_fin, dia):
        sql = """
            INSERT INTO taller_docente_nucleo_horario(id_docente, id_nucleo, id_taller, id_ciclo, hora_inicio, hora_fin, dia)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor = self.db.cursor()
        ok = cursor.execute(sql, (id_ciclo, id_taller, id_docente, id_nucleo, hora_inicio, hora_fin, dia))
        
        self.db.commit()
        return ok
    
    # CHEQUEO SI EXISTE UN CICLO + TALLER + PROFE + NUCLEO + HORARIO + DIA
    @classmethod
    def existe_horario(self, id_ciclo, id_taller, id_docente, id_nucleo, hora_inicio, hora_fin, dia):
        sql = """
            SELECT *
            FROM taller_docente_nucleo_horario
            WHERE (id_docente = %s AND id_nucleo = %s AND id_taller = %s AND id_ciclo = %s AND hora_inicio = %s AND hora_fin = %s AND dia = %s)
        """
        cursor = self.db.cursor()
        cursor.execute(sql, (id_ciclo, id_taller, id_docente, id_nucleo, hora_inicio, hora_fin, dia))
        
        self.db.commit()
        return cursor.fetchall()
    
    
    # CHEQUEO SI UN TALLER PARA UN CICLO TIENE DOCENTE(S) ASIGNADO(S)
    @classmethod
    def tiene_docente(self, id_ciclo, id_taller):
        sql = """
            SELECT *
            FROM docente_responsable_taller
            WHERE (ciclo_lectivo_id = %s AND taller_id = %s)
        """
        cursor = self.db.cursor()
        cursor.execute(sql, (id_ciclo, id_taller))
        
        self.db.commit()
        return cursor.fetchall()