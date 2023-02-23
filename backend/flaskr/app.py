from flaskr import create_app
from flask_restful import Api
from .models import db
from .views import VistaSignUp, VistaLogIn, VistaTasks, VistaTasksUser, VistaFiles
from flask_cors import CORS
import logging
from flask_jwt_extended import JWTManager
from celery import Celery


app = create_app('default')

# Config Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6360/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6360/0'

app_context = app.app_context()
app_context.push()

# Creando el objeto Celery
celery = Celery(app, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# DB
db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaSignUp, '/api/auth/signup')
api.add_resource(VistaLogIn, '/api/auth/login')
api.add_resource(VistaTasks, '/api/tasks/<int:id_task>')
api.add_resource(VistaTasksUser, '/api/tasks')
api.add_resource(VistaFiles, '/api/files/<filename>')

#Inicializar la instancia de JWTManager para manejo de tokens
jwt = JWTManager(app)

#Pequeño metodo para que en la aplicación para debuggear
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.StreamHandler()])

@celery.task
def sumar(x,y):
    print('Se sumaron los números')
    return 1 + 2