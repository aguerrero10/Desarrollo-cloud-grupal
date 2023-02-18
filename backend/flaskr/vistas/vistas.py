from flask import request
from ..modelos import db, Usuario, UsuarioSchema, Tarea, TareaSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

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
    def post(self):
        u_email = request.json["email"]
        u_contrasena = request.json["contrasena"]
        usuario = Usuario.query.filter_by(email=u_email, contrasena = u_contrasena).first() #Modificado
        if usuario:
            #return 'Inicio de sesión exitoso', 200
            return usuario_schema.dump(usuario)
        else:
            return 'Correo o contraseña incorrectos', 401


class VistaSignIn(Resource):    
    def post(self):
        nuevo_usuario = Usuario(nombre=request.json["nombre"], email=request.json["email"], contrasena=request.json["contrasena"])
        db.session.add(nuevo_usuario)
        db.session.commit()
        return 'Usuario creado exitosamente', 201

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