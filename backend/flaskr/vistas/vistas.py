from flask import request
from ..modelos import db, Usuario, UsuarioSchema, Tarea, TareaSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token
from sqlalchemy import select, exists



usuario_schema = UsuarioSchema()
tarea_schema = TareaSchema()

#----- Usuario -----
class VistaUsuarios(Resource):
    def get(self):
        return [usuario_schema.dump(usuario) for usuario in Usuario.query.all()]

#----- Tarea -----
class VistaTareas(Resource):
    def get(self):
        return [tarea_schema.dump(tarea) for tarea in Tarea.query.all()]


class VistaLogIn(Resource):
#Recuperar token para hacer sesion de cuenta exitoso
#Modificado JIA
    def post(self):
        u_email = request.json["email"]
        u_contrasena = request.json["contrasena"]
        usuario = Usuario.query.filter_by(email=u_email, contrasena = u_contrasena).all() #Modificado
        if usuario:
                token_de_acceso = create_access_token(identity=u_email)
                id_usuario = usuario[0].id
                return {'mensaje':'Inicio de sesión exitoso','token_de_acceso':token_de_acceso,'id_usuario':id_usuario}, 200
        else:
            return 'Correo o contraseña incorrectos', 401


class VistaSignIn(Resource):
    #Metodo POST: Añade un usuario a la DB
    # Se debe asegurar que el mail no tiene misma cuenta y contraseña ingresada es la misma    
    def post(self):
        u_nombre = request.json["nombre"]
        u_email=request.json["email"]
        u_contrasena=request.json["contrasena"]
        u_conf_contrasena = request.json["conf_constrena"]
        nuevo_usuario = Usuario(nombre=u_nombre, email=u_email,contrasena=u_contrasena)
        #Revision si confirmacion contraseña es la misma 
        if u_contrasena == u_conf_contrasena:
        #Se revisa si el correo esta asociado a una cuenta
            if db.session.query(Usuario.email).filter_by(email=nuevo_usuario.email).first() is None: 
                token_de_acceso = create_access_token(identity = request.json['email'])
                db.session.add(nuevo_usuario)
                db.session.commit()
                id_usuario = nuevo_usuario.id
                return {'mensaje':'usuario creado exitosamente','token de acceso':token_de_acceso,'id_usuario':id_usuario},201
            else: 
                return {'mensaje': 'Correo ya registrado'}, 409
        else: 
            return {'mensaje':'Las contraseñas no coinciden'}, 409


    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena",usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '',204


class VistaTareasUsuario(Resource):
    def post(self, id_usuario):
        nueva_tarea = Tarea(nombre=request.json["nombre"], extension=request.json["extension"], 
                            extension_final=request.json["extension_final"], disponibilidad=request.json["disponibilidad"])
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.tareas.append(nueva_tarea)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene una tarea con dicho nombre', 409

        return tarea_schema.dump(nueva_tarea)

    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return [tarea_schema.dump(ev) for ev in usuario.tareas]


class VistaTarea(Resource):
    def get(self, id_tarea):
        return tarea_schema.dump(Tarea.query.get_or_404(id_tarea))

    def put(self, id_tarea):
        tarea = Tarea.query.get_or_404(id_tarea)
        tarea.nombre = request.json.get("nombre", tarea.nombre)
        tarea.extension = request.json.get("extension", tarea.extension)
        tarea.extension_final = request.json.get("extension_final", tarea.extension_final)
        tarea.disponibilidad = request.json.get("disponibilidad", tarea.disponibilidad)
        db.session.commit()
        return tarea_schema.dump(tarea)

    def delete(self, id_tarea):
        tarea = Tarea.query.get_or_404(id_tarea)
        db.session.delete(tarea)
        db.session.commit()
        return '', 204