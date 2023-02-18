from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum

db = SQLAlchemy()


class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(128))
    extension = db.Column(db.String(5))
    extension_final = db.Column(db.String(5))
    disponibilidad = db.Column(db.String(2))
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    email = db.Column(db.String(128))
    contrasena = db.Column(db.String(50))
    #tareas = db.relationship('Tarea', cascade='all, delete, delete-orphan')

class TareaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tarea
        include_relationships = True
        load_instance = True

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True