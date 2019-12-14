class Asistencia(object):
    
    db = None
    
    
    # obtener los talleres con el profe, horario, dia y nucleo
    @classmethod
    def get_talleres_con_profesor(self, termino=None):
        params = []
        sql = """SELECT d.nombre as nombre_docente, 
                        d.apellido,
                        d.id as id_docente, 
                        t.nombre as nombre_taller, 
                        t.id as id_taller, 
                        c.fecha_ini, 
                        c.semestre,
                        c.id as id_ciclo, 
                        n.id as id_nucleo, 
                        n.nombre as nombre_nucleo, 
                        tdnh.hora_inicio, 
                        tdnh.hora_fin, 
                        dia
                FROM taller_docente_nucleo_horario tdnh
                INNER JOIN docente d ON d.id = tdnh.id_docente
                INNER JOIN nucleo n ON n.id = tdnh.id_nucleo
                INNER JOIN ciclo_lectivo c ON c.id = tdnh.id_ciclo
                INNER JOIN taller t ON t.id = tdnh.id_taller"""
                
        if termino != None:
            termino = '%'+termino+'%'
            sql = sql + """ WHERE (t.nombre LIKE %s OR t.nombre_corto LIKE %s) """
            params.append(termino)
            params.append(termino)
         
        cursor = self.db.cursor()
        cursor.execute(sql, params)

        return cursor.fetchall()
    
    # obtener los talleres con el profe, horario, dia y nucleo paginados
    @classmethod
    def get_talleres_con_profesor_paginados(self, limit, offset = 1, termino = None):
        params = []
        sql = """SELECT d.nombre as nombre_docente, 
                        d.apellido,
                        d.id as id_docente, 
                        t.nombre as nombre_taller, 
                        t.id as id_taller, 
                        c.fecha_ini, 
                        c.semestre,
                        c.id as id_ciclo, 
                        n.id as id_nucleo, 
                        n.nombre as nombre_nucleo, 
                        tdnh.hora_inicio, 
                        tdnh.hora_fin, 
                        dia
                FROM taller_docente_nucleo_horario tdnh
                INNER JOIN docente d ON d.id = tdnh.id_docente
                INNER JOIN nucleo n ON n.id = tdnh.id_nucleo
                INNER JOIN ciclo_lectivo c ON c.id = tdnh.id_ciclo
                INNER JOIN taller t ON t.id = tdnh.id_taller"""
                
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
    
    @classmethod
    def get_alumnos_por_taller_y_ciclo(self, ciclo, taller):
        sql = """SELECT *
                FROM estudiante_taller et
                INNER JOIN estudiante e ON et.estudiante_id = e.id
                WHERE et.ciclo_lectivo_id = %s AND et.taller_id = %s"""
                
    
        cursor = self.db.cursor()
        cursor.execute(sql, (ciclo, taller))

        return cursor.fetchall()
    
    
    @classmethod
    def pasar(self, ciclo, taller, id_alumno, fecha, estado):
        sql = """
            INSERT INTO asistencia_estudiante_taller (estudiante_id, ciclo_lectivo_id, taller_id, fecha, estado)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        if estado == 1:
            estado = 'PRESENTE'
        else:
            estado = 'AUSENTE'

        cursor = self.db.cursor()
        cursor.execute(sql, ( id_alumno,
                             ciclo, 
                             taller, 
                             fecha, 
                             estado ))
        self.db.commit()

        return True
    
    @classmethod
    def existe(self, ciclo, taller, id_alumno, fecha, estado):
        if estado == 1:
            estado = 'PRESENTE'
        else:
            estado = 'AUSENTE'
        
        sql = """
            SELECT *
            FROM asistencia_estudiante_taller
            WHERE estudiante_id = %s AND taller_id = %s AND ciclo_lectivo_id=%s AND fecha = %s AND estado = %s
        """

        cursor = self.db.cursor()
        cursor.execute(sql, ( id_alumno,
                             taller, 
                             ciclo, 
                             fecha, 
                             estado  ))
        self.db.commit()

        return cursor.fetchall()
    
    @classmethod
    def hay_que_actualizar(self, ciclo, taller, id_alumno, fecha, estado):
        if estado == 1:
            estado = 'PRESENTE'
        else:
            estado = 'AUSENTE'
            
        sql = """
            SELECT *
            FROM asistencia_estudiante_taller
            WHERE estudiante_id = %s AND taller_id = %s AND ciclo_lectivo_id = %s AND fecha = %s AND estado != %s
        """

        cursor = self.db.cursor()
        cursor.execute(sql, ( id_alumno,
                             taller, 
                             ciclo, 
                             fecha, 
                             estado
                               ))
        self.db.commit()

        return cursor.fetchall()
    
    @classmethod
    def get_alumnos_con_asistencia(self, ciclo, taller, fecha):
        sql = """
            SELECT estudiante_id
            FROM asistencia_estudiante_taller
            WHERE taller_id = %s AND ciclo_lectivo_id=%s AND fecha = %s
        """

        cursor = self.db.cursor()
        cursor.execute(sql, (taller, 
                             ciclo, 
                             fecha  ))
        self.db.commit()

        ids = []
        for alu in cursor.fetchall():
            ids.append(alu['estudiante_id'])
        
        return ids
    
    @classmethod
    def actualizar(self, ciclo, taller, id_estudiante, fecha, estado):
        sql = """
            UPDATE asistencia_estudiante_taller 
            SET estado = %s
            WHERE estudiante_id = %s AND ciclo_lectivo_id = %s AND taller_id = %s AND fecha = %s
        """
        
        if estado == 1:
            estado_aux = 'PRESENTE'
        else:
            estado_aux = 'AUSENTE'

        print(estado_aux)
        cursor = self.db.cursor()
        cursor.execute(sql, ( estado_aux,
                             id_estudiante, 
                             ciclo, 
                             taller, 
                             fecha ))
        self.db.commit()

        return True