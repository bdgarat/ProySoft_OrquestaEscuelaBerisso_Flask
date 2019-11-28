

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