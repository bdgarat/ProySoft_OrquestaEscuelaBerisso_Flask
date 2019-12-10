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