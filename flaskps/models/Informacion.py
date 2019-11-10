

class Informacion(object):

    db = None 

    # RECUPERAR TODOS LOS BARRIOS
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
