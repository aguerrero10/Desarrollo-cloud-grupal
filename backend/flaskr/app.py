from flaskr import create_app
from flask_restful import Api
from .modelos import db
from .vistas import VistaSignIn, VistaLogIn, VistaTarea, VistaTareasUsuario
from .vistas import VistaUsuarios, VistaTareas
from flask_cors import CORS
import logging
from flask_jwt_extended import JWTManager


app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaUsuarios, '/usuarios') #
api.add_resource(VistaTareas, '/tareas') #
api.add_resource(VistaSignIn, '/api/auth/signup')#Modificado -- JIA
api.add_resource(VistaLogIn, '/api/auth/login')#Modificado -- JIA
api.add_resource(VistaTareasUsuario, '/usuario/<int:id_usuario>/tareas')
api.add_resource(VistaTarea, '/tarea/<int:id_tarea>')

#Inicializar la instancia de JWTManager para manejo de tokens
jwt = JWTManager(app)

#Pequeño metodo para que en la aplicación para debuggear
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.StreamHandler()])