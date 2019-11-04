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
    
    # RECUPERAR LOS PERMISOS DE UN USUARIO DADO UN ID ROL
    @classmethod
    def get_permisos(self, id_rol):
        sql = """
                SELECT p.nombre 
                FROM rol r
                INNER JOIN rol_tiene_permiso rp ON (r.id = rp.rol_id)
                INNER JOIN permiso p ON (p.id = rp.permiso_id) 
                WHERE r.id = %s
            """
        cursor = self.db.cursor()
        cursor.execute(sql, (id_rol))

        return cursor.fetchall()



    # RECUPERAR TODOS LOS USUARIOS
    @classmethod
    def get_usuarios(self, rol = '0', termino = '', activo = None, inactivo = None):
        
        params = []
        
        sql = """
            SELECT u.id, u.username FROM usuario u
            INNER JOIN usuario_tiene_rol ur ON (u.id = ur.usuario_id)
            INNER JOIN rol r ON (ur.rol_id = r.id)
            WHERE u.borrado_logico = 0
        """

        if rol != '0':
            sql = sql + """
                AND r.nombre = %s 
            """
            params.append(rol)

        if termino != '' and termino != None:
            termino = '%'+termino+'%'
            sql = sql + """ AND u.username LIKE %s """
            params.append(termino)
            
        if not (activo != None and inactivo != None):                
            if activo != None:
                sql = sql + """ AND u.activo = true """
                
            if inactivo != None:
                sql = sql + """ AND u.activo = false """

        cursor = self.db.cursor()   
        if len(params):
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        return cursor.fetchall()
    
    # RECUPERAR TODOS LOS USUARIOS POR ROL Y PAGINADOS
    @classmethod
    def get_usuarios_paginados(self, limit, offset = 1, rol = '0', termino = '', activo = None, inactivo = None):
        
        params = []
        sql = """
            SELECT u.id, u.email, u.username, u.first_name, u.last_name, u.activo FROM usuario u
            INNER JOIN usuario_tiene_rol ur ON (u.id = ur.usuario_id)
            INNER JOIN rol r ON (ur.rol_id = r.id)
            WHERE  u.borrado_logico = 0 
            """

        if rol != '0':
            sql = sql + """
                AND r.nombre = %s 
            """
            params.append(rol)

        if termino != '' and termino != None:
            termino = '%'+termino+'%'
            sql = sql + """ AND u.username LIKE %s """
            params.append(termino)
            
        if not (activo != None and inactivo != None):
            
            if activo != None:
                sql = sql + """ AND u.activo = true """
                
            if inactivo != None:
                sql = sql + """ AND u.activo = false """

        sql = sql + """
                    LIMIT %s OFFSET %s
                    """

        params.append(limit)
        params.append(offset)

        cursor = self.db.cursor()
        cursor.execute(sql, params)

        return cursor.fetchall()


    # ENOCONTRAR USUARIO DADO UN EMAIL Y CONTRASEÑA
    @classmethod
    def find_by_email_and_pass(self, email, password):
        sql = """
            SELECT u.id, u.email, u.password, u.username, u.first_name, u.last_name, r.id AS id_rol, r.nombre AS nombre_rol
            FROM usuario u
            INNER JOIN usuario_tiene_rol ur ON (u.id = ur.usuario_id)
            INNER JOIN rol r ON (ur.rol_id = r.id)
            WHERE u.email = %s AND u.password = %s
        """

        cursor = self.db.cursor()
        cursor.execute(sql, (email, password))

        return cursor.fetchall()
    
    
    # OBTENER ROLES DE UN USUARIO DADO UN ID
    @classmethod
    def get_roles(self, id_usuario):
        sql = """
            SELECT r.nombre
            FROM rol r
            INNER JOIN usuario_tiene_rol ur ON (r.id = ur.rol_id)
            INNER JOIN usuario u ON (ur.usuario_id = u.id)
            WHERE u.id = %s
        """
        cursor = self.db.cursor()
        cursor.execute(sql, (id_usuario))

        return cursor.fetchall()

    # OBTENER ROLES DE LA DB
    @classmethod
    def all_roles(self):
        sql = """
            SELECT r.nombre
            FROM rol r
        """
        cursor = self.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

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
            SELECT *
            FROM usuario_tiene_rol
            WHERE usuario_id = %s AND rol_id = %s
        """
        cursor.execute(sql, (id_usuario, id_rol))
        existe = cursor.fetchone()
        
        if existe:
            return False

        sql = """
            INSERT INTO usuario_tiene_rol (usuario_id, rol_id)
            VALUES (%s, %s)
        """
        cursor.execute(sql, (id_usuario, id_rol))

        self.db.commit()

        return True
    
    # QUITAR ROL A UN USUARIO
    @classmethod
    def quitar_rol(self, rol, usuario):
        
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
            DELETE 
            FROM usuario_tiene_rol 
            WHERE usuario_id = %s AND rol_id = %s
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
    
    
    # EDITAR UN USUARIO
    @classmethod
    def editar(self, id_usuario, email, username, first_name, last_name):
        cursor = self.db.cursor()
        
        updated_at = datetime.now()
        
        sql = """
            UPDATE usuario 
            SET email = %s, username = %s, first_name = %s, last_name = %s, updated_at = %s
            WHERE id = %s
        """

        o = cursor.execute(sql, (email, username, first_name, last_name, updated_at, id_usuario))
        self.db.commit()

        return o
    
    
    # ELIMINAR UN USUARIO
    @classmethod
    def eliminar(self, id_usuario):
        cursor = self.db.cursor()
        
        updated_at = datetime.now()
        
        sql = """
            UPDATE usuario 
            SET borrado_logico = 1, updated_at = %s
            WHERE id = %s
        """

        o = cursor.execute(sql, (updated_at, id_usuario))
        self.db.commit()

        return o
    
    
    #   CHEQUEO SI TENGO UN PERMISO
    @classmethod
    def tengo_permiso_registrar(self, permisos):
        if (( 'estudiante_new' in permisos) or ( 'preceptor_new' in permisos) or ( 'docente_new' in permisos) or ( 'admin_new' in permisos) ):
            return True
        return False 
    
    
    # CHEQUEO SI TENGO ALGUN PERMISO PARA REGISTRAR USUARIOS
    @classmethod
    def tengo_permiso(self, permisos, permiso):
        if ( permiso ) not in permisos:
            return False
        return True

   