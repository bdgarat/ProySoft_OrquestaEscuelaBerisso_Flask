from datetime import datetime

class Usuario(object):
    
    db = None

    def __init__(self, email, username, password, first_name, last_name):
        self.email = email
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.activo = 1
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        

    @classmethod
    def all(self):
        sql = 'SELECT * FROM usuario'
        cursor = self.db.cursor()
        cursor.execute(sql)

        return cursor.fetchall()

    @classmethod
    def get_usuarios_por_rol(self, rol):
        sql = """
            SELECT u.id, u.email, u.first_name, u.last_name, u.activo FROM usuario u
            INNER JOIN usuario_tiene_rol ur ON (u.id = ur.usuario_id)
            INNER JOIN rol r ON (ur.rol_id = r.id)
            WHERE r.nombre = %s
        """
        
        cursor = self.db.cursor()
        cursor.execute(sql, (rol))

        return cursor.fetchall()


    @classmethod
    def insert(self, user):
        sql = """
            INSERT INTO usuario (email, username, password, activo, updated_at, created_at, first_name, last_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor = self.db.cursor()
        cursor.execute(sql, (user.email, 
                             user.username, 
                             user.password, 
                             user.activo, 
                             user.updated_at, 
                             user.created_at, 
                             user.first_name, 
                             user.last_name))
        self.db.commit()

        return True
    
    @classmethod
    def agregar_rol(self, rol, usuario):
        
        cursor = self.db.cursor()
        
        sql = """
            SELECT id FROM rol where nombre=%s
        """

        cursor.execute(sql, (rol))
        id_rol = cursor.fetchone()['id']
        
        sql = """
            SELECT id FROM usuario where username=%s
        """

        cursor.execute(sql, (usuario.username))
        id_usuario = cursor.fetchone()['id']
        
        sql = """
            INSERT INTO usuario_tiene_rol (usuario_id, rol_id)
            VALUES (%s, %s)
        """
        cursor.execute(sql, (id_usuario, id_rol))

        self.db.commit()

        return True

    @classmethod
    def find_by_email_and_pass(self, email, password):
        sql = """
            SELECT * FROM usuario u
            WHERE u.email = %s AND u.password = %s
        """

        cursor = self.db.cursor()
        cursor.execute(sql, (email, password))

        return cursor.fetchone()
    
    @classmethod
    def existe(self, username):
        sql = """
            SELECT * FROM usuario
            WHERE username = %s
        """

        cursor = self.db.cursor()
        cursor.execute(sql, (username))
        
        if cursor.fetchone():
            return True

        return False
    
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