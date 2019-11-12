

class Informacion(object):

    db = None 

    # RECUPERAR TODOS 
    @classmethod
    def all(self, tabla):
        sql = 'SELECT * FROM ' + tabla
        cursor = self.db.cursor()
        cursor.execute(sql)

        res = cursor.fetchall()
        lista = []
        for l in res:
            lista.append( (l['id'], l['nombre']) )
        
        return lista

    # RECUPERAR NOMBRE DADO UN ID Y UNA TABLA
    @classmethod
    def get_nombre(self, tabla, id):
        sql = 'SELECT * FROM ' + tabla
        sql = sql + """ WHERE id = %s """
        cursor = self.db.cursor()
        cursor.execute(sql, (id))

        res = cursor.fetchone()
        return res['nombre']