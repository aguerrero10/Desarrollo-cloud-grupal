from flask import request
from ..models import db, User, UserSchema, Task, TaskSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.exceptions import HTTPException



user_Schema = UserSchema()
task_Schema = TaskSchema()



class VistaLogIn(Resource):
#Recuperar token para hacer sesion de cuenta exitoso
#Modificado JIA
    def post(self):
        u_username = request.json["username"]
        u_password = request.json["password"]
        user = User.query.filter_by(username=u_username, password = u_password).all()
        if user:
                id_user = user[0].id
                token_de_acceso = create_access_token(id_user)
                return {'mensaje':'Inicio de sesión exitoso','token_de_acceso':token_de_acceso,'id_user':id_user}, 200
        else:
            return 'Correo o contraseña incorrectos', 401


class VistaSignUp(Resource):
    #Metodo POST: Añade un usuario a la DB
    # Se debe asegurar que el mail no tiene misma cuenta y contraseña ingresada es la misma    
    def post(self):
        u_username = request.json["username"]
        u_email=request.json["email"]
        u_password=request.json["password1"]
        u_conf_password = request.json["password2"]
        new_user = User(username=u_username, email=u_email,password=u_password)
        #Revision si confirmacion contraseña es la misma 
        if u_password == u_conf_password:
        #Se revisa si el correo esta asociado a una cuenta
            if db.session.query(User.email).filter_by(email=new_user.email).first() is None:
                if db.session.query(User.username).filter_by(username=new_user.username).first() is None:
                    db.session.add(new_user)
                    db.session.commit()
                    id_user = new_user.id
                    token_de_acceso = create_access_token(identity = id_user)
                    return {'mensaje':'usuario creado exitosamente','token_de_acceso':token_de_acceso,'id_user':id_user},201
                else:
                    return {'mensaje': 'Nombre de usuario ya registrado'}, 409
            else: 
                return {'mensaje': 'Correo ya registrado'}, 409
        else: 
            return {'mensaje':'Las contraseñas no coinciden'}, 409


class VistaTasksUser(Resource):
    @jwt_required()
    #/api/tasks -> Acá va la adición creo
    #Tiene que ser modificado de acuerdo a la entrega
    #El tiempo se lee acá o se manda de antes
    #Modificar
    def post(self):
        print(get_jwt_identity())
        new_Task = Task(fileName=request.json["fileName"], newFormat=request.json["newFormat"], 
                            status=request.json["status"], time=request.json["time"],
                            pathOriginal = request.json["pathOriginal"], pathConverted = request.json["pathConverted"])
        id_user = get_jwt_identity()
        print(new_Task)
        user = User.query.get_or_404(id_user)
        user.tasks.append(new_Task)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene una tarea con dicho nombre', 409

        return task_Schema.dump(new_Task)

    @jwt_required()
    #/api/tasks
    def get(self):
        id_user = get_jwt_identity()
        user = User.query.get_or_404(id_user)
        return [task_Schema.dump(ev) for ev in user.tasks]


class VistaTasks(Resource):
    #@jwt_required()
    #/api/tasks/<int:id_task>
    def get(self, id_task):
        return task_Schema.dump(Task.query.get_or_404(id_task))
    
    @jwt_required()
    #/api/tasks/<int:id_task>
    #Revisar metodo, solo lo puede hacer el usuario de la tarea
    def delete(self, id_task):
        task = Task.query.get_or_404(id_task)
        db.session.delete(task)
        db.session.commit()
        return '', 204