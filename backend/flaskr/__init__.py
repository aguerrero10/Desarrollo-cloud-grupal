from flask import Flask
from datetime import timedelta
from celery import Celery, Task

mail_settings = {
    "MAIL_SERVER":"smtp.gmail.com",
    "MAIL_PORT":465,
    "MAIL_USE:TLS":False,
    "MAIL_USE_SSL":True,
    "MAIL_USERNAME":"desarrollo.cloud.2023@gmail.com",
    "MAIL_PASSWORD":"rihmnrlonrsxhrat",
    "MAIL_DEFAULT_SENDER":"desarrollo.cloud.2023@gmail.com"
}

def create_app(config_name):
    app = Flask(__name__)  
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tareas.db'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@10.128.0.2:5432/tareas'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@172.28.16.3:5432/tareas'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config['FLASK_RUN_PORT'] = 5001

    #Frase secreta JWT
    app.config['JWT_SECRET_KEY']='frase-secreta'
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    
    #Configuracion del correo
    app.config.update(mail_settings)

    return app
