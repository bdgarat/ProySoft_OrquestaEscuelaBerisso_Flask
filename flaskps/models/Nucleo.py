class Nucleo(object):
    
    db = None   
    
    # RECUPERAR TODOS LOS NUCLEOS
    @classmethod
    def all(self):
        sql = """
            SELECT * FROM nucleo
        """
        cursor = self.db.cursor()
        cursor.execute(sql)

        return cursor.fetchall()