class Configuracion(object):
    
    db = None
     
    def __init__(self, titulo, descripcion, contacto, paginacion, sitio_habilitado):
        self.titulo = titulo
        self.descripcion = descripcion
        self.paginacion = paginacion
        self.contacto = contacto
        self.sitio_habilitado = sitio_habilitado
        
    @classmethod
    def get_config(self):
        sql = """
            SELECT * FROM config
        """

        cursor = self.db.cursor()
        cursor.execute(sql)
        
        config_actual = cursor.fetchone()

        return config_actual
    
    @classmethod
    def set_config(self, config):
        sql = """
            UPDATE config
            SET titulo = %s, descripcion = %s, contacto=%s, paginacion = %s, sitio_habilitado = %s
            WHERE id=1
        """
        cursor = self.db.cursor()
        cursor.execute(sql, (config.titulo, config.descripcion, config.contacto, config.paginacion, config.sitio_habilitado))
        self.db.commit()
        
        config_actual = cursor.fetchone()
       
        return config_actual
    
    
    @classmethod
    def get_sitio_habilitado(self):
        
        sql = """
            SELECT sitio_habilitado
            FROM config
            WHERE id = 1
        """
        
        cursor = self.db.cursor()
        cursor.execute(sql)
        return cursor.fetchone()
    
    @classmethod
    def get_paginacion(self):
        
        sql = """
            SELECT paginacion
            FROM config
            WHERE id = 1
        """
        
        cursor = self.db.cursor()
        cursor.execute(sql)
        return cursor.fetchone()