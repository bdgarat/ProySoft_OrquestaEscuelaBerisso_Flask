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
        
    # RECUPERAR TODOS LOS USUARIOS
    @classmethod
    def all(self):
        sql = 'SELECT * FROM usuario where borrado_logico = 0'
        cursor = self.db.cursor()
        cursor.execute(sql)

        return cursor.fetchall()
    
    
    # RECUPERAR UN USUARIO DADO UN ID
    
    @classmethod
    def get_user(self, id):
        sql = 'SELECT * FROM usuario where borrado_logico = 0 and id = %s'
        cursor = self.db.cursor()
        cursor.execute(sql, (id))

        return cursor.fetchone()

    # RECUPERAR TODOS LOS USUARIOS POR ROL
    @classmethod
    def get_usuarios_por_rol(self, rol, termino = None):
        sql = """
            SELECT u.id, u.username FROM usuario u
            INNER JOIN usuario_tiene_rol ur ON (u.id = ur.usuario_id)
            INNER JOIN rol r ON (ur.rol_id = r.id)
            WHERE r.nombre = %s AND u.borrado_logico = 0
        """
        if termino != None:
            termino = '%'+termino+'%'
            sql = sql + """ AND u.username LIKE %s """
        
        if termino != None:
            params = (rol, termino)
        else:
            params = (rol)

        cursor = self.db.cursor()
        cursor.execute(sql, params)

        return cursor.fetchall()
    
    # RECUPERAR TODOS LOS USUARIOS POR ROL Y PAGINADOS
    @classmethod
    def get_usuarios_por_rol_paginados(self, rol, limit, offset = 1, termino = None):
        
        sql = """
            SELECT u.id, u.email, u.username, u.first_name, u.last_name, u.activo FROM usuario u
            INNER JOIN usuario_tiene_rol ur ON (u.id = ur.usuario_id)
            INNER JOIN rol r ON (ur.rol_id = r.id)
            WHERE r.nombre = %s AND u.borrado_logico = 0 
            """

        if termino != None:
            termino = '%'+termino+'%'
            sql = sql + """ AND u.username LIKE %s """

        sql = sql + """
                    LIMIT %s OFFSET %s
                    """

        if termino != None:
            params = (rol, termino, limit, offset)
        else:
            params = (rol, limit, offset)

        cursor = self.db.cursor()
        cursor.execute(sql, params)

        return cursor.fetchall()


     # ENOCONTRAR USUARIO DADO UN EMAIL Y CONTRASEÑA
    
    @classmethod
    def find_by_email_and_pass(self, email, password):
        sql = """
            SELECT * FROM usuario u
            WHERE u.email = %s AND u.password = %s
        """

        cursor = self.db.cursor()
        cursor.execute(sql, (email, password))

        return cursor.fetchone()
    
    # VER SI EXISTE UN USUARIO SEGUN UN USERNAME
    
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
    

    # INSERTAR USUARIO
    
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
    
    # AGREGAR ROL A UN USUARIO
    
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
    
    
    # ACTIVAR / DESACTIVAR UN USUARIO
    @classmethod
    def activar(self, id_usuario):
        cursor = self.db.cursor()
        
        sql = """
            UPDATE usuario 
            SET activo = not activo
            WHERE id = %s
        """

        cursor.execute(sql, (id_usuario))
        self.db.commit()

        return True

   