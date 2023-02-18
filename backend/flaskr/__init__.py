from flask import Flask

def create_app(config_name):
    app = Flask(__name__)  
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tareas.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config['FLASK_RUN_PORT'] = 5001


    #Frase secreta JWT
    app.config['JWT_SECRET_KEY']='frase-secreta'

    return app