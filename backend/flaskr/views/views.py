import os
from datetime import datetime
from flask import request, send_from_directory
from ..models import db, User, UserSchema, Task, TaskSchema, Status
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename
from ..tasks import sumar, compresion_correo


UPLOAD_FOLDER = './'

user_Schema = UserSchema()
task_Schema = TaskSchema()


class VistaSignUp(Resource):
    #/api/auth/signup'
    #Metodo POST: añade un usuario a la DB
    #Se debe asegurar que el mail no tiene misma cuenta y contraseña ingresada es la misma    
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
                    return 'Nombre de usuario ya registrado', 409
            else: 
                return 'Correo ya registrado', 409
        else: 
            return 'Las contraseñas no coinciden', 409


class VistaLogIn(Resource):
    #/api/auth/login'
    #Metodo POST: revisa las credenciales y recupera token para hacer inicio de sesion exitoso
    def post(self):
        u_username = request.json["username"]
        u_password = request.json["password"]
        user = User.query.filter_by(username=u_username, password = u_password).all()
        if user:
                id_user = user[0].id
                token_de_acceso = create_access_token(id_user)
                # Llamado de tarea ascíncrona con Celery y Redis
                sumar.delay()
                compresion_correo()
                #
                return {'mensaje':'Inicio de sesión exitoso','token_de_acceso':token_de_acceso,'id_user':id_user}, 200
        else:
            return 'Correo o contraseña incorrectos', 401


class VistaTasksUser(Resource):
    @jwt_required()
    #/api/tasks
    #Metodo GET: recupera las tareas de un usuario
    def get(self):
        #Recuperar parametro order
        order = request.args.get('order')
        order = int(order) if order else 0
        #Recuperar parametro max
        max = request.args.get('max')
        max = int(max) if max else -1

        #Obtener tareas
        id_user = get_jwt_identity()
        user = User.query.get_or_404(id_user)
        tasks = user.tasks

        #tasks = Task.query.filter_by(user=id_user)
        if order == 0:
            tasks = tasks.order_by(Task.id)
        else:
            tasks = tasks.order_by(Task.id.desc())

        if max > -1:
            tasks = tasks.limit(max)

        return [task_Schema.dump(task) for task in tasks]

    
    @jwt_required()
    #/api/tasks
    #Metodo POST: añade un archivo y tarea de compresion a la DB
    def post(self):
        #Se revisa si se envió un archivo para comprimir
        if 'fileName' not in request.files:
            return 'No se envió un archivo para comprimir', 400
        
        file = request.files.get("fileName")

        if '/' in file.filename:
            return 'No se permiten subdirectorios', 400

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))  #app.config['UPLOAD_FOLDER']
        else:
            return 'No se envió un archivo para comprimir', 400
        
        print(get_jwt_identity())

        #Se genera la tarea con los datos del archivo
        new_Task = Task(fileName=filename, newFormat=request.form.get("newFormat"), 
                        status='UPLOADED', timeStamp=datetime.now(),
                        pathOriginal = UPLOAD_FOLDER, pathConverted = UPLOAD_FOLDER)
        id_user = get_jwt_identity()
        print(new_Task)
        user = User.query.get_or_404(id_user)
        user.tasks.append(new_Task)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'Error', 409

        return task_Schema.dump(new_Task)


class VistaTasks(Resource):
    @jwt_required()
    #/api/tasks/<int:id_task>
    #Metodo GET: recupera los datos de una tarea específica
    def get(self, id_task):
        task = Task.query.get_or_404(id_task)
        id_user = get_jwt_identity()
        if id_user == task.user:
            return task_Schema.dump(Task.query.get_or_404(id_task))
        else: 
            return 'No tiene autorizacion para consultar esta tarea', 400
    
    
    @jwt_required()
    #/api/tasks/<int:id_task>
    #Metodo DELETE: eliminar el archivo (original y el convertido), solo si estado es procesado
    def delete(self, id_task):
        task = Task.query.get_or_404(id_task)
        id_user = get_jwt_identity()
        filename = task.fileName
        new_filename = filename.rsplit('.', 1)[0] + '.' + task.newFormat.name
        
        #Se verifica que el archivo pertenezca a ese usuario
        if id_user != task.user:
            return "Usted no tiene permisos para ver esta tarea", 400
        else:
            if task.status == Status.PROCESSED: 
                #Se revisa si el archivo existe
                if os.path.isfile(os.path.join(task.pathOriginal, filename)) and os.path.isfile(os.path.join(task.pathConverted, new_filename)):
                    #Eliminar archivos
                    os.remove(os.path.join(task.pathOriginal, filename))
                    os.remove(os.path.join(task.pathConverted, new_filename))

                    #Eliminar task de DB
                    db.session.delete(task)
                    db.session.commit()
                    return 'Archivo eliminado', 204 
                else:
                    return "El archivo no existe", 400
            else: 
                return "El archivo no esta procesado", 400

    
class VistaFiles(Resource):
    @jwt_required()
    #Metodo GET: recupera un archivo
    #/api/files/<filename>
    def get(self, filename):
        id_user = get_jwt_identity()

        #Se retorna el archivo si este existe
        if os.path.isfile(os.path.join(UPLOAD_FOLDER, filename)):
            #Se verifica que el archivo pertenezca a ese usuario
            if db.session.query(Task.id).filter_by(user=id_user, fileName = filename).first() is None:
                return "Usted no tiene permisos para descargar el archivo", 400
            else:    
                return send_from_directory(os.path.join(UPLOAD_FOLDER), filename, as_attachment=True)
        else:
            return "El archivo no existe", 400    