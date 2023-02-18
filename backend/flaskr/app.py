from flaskr import create_app
from flask_restful import Api
from .modelos import db
from .vistas import VistaSignIn, VistaLogIn, VistaTarea, VistaTareasUsuario
from .vistas import VistaUsuarios, VistaTareas
from flask_cors import CORS

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaUsuarios, '/usuarios') #
api.add_resource(VistaTareas, '/tareas') #
api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaLogIn, '/login')
api.add_resource(VistaTareasUsuario, '/usuario/<int:id_usuario>/tareas')
api.add_resource(VistaTarea, '/tarea/<int:id_tarea>')