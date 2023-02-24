from flaskr import create_app
from flask_restful import Api
from .models import db
from .views import VistaSignUp, VistaLogIn, VistaTasks, VistaTasksUser, VistaFiles
from flask_cors import CORS
import logging
from flask_jwt_extended import JWTManager
from apscheduler.schedulers.background import BackgroundScheduler


app = create_app('default')
app_context = app.app_context()
app_context.push()

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

