from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum
from datetime import datetime
from sqlalchemy.orm import configure_mappers

db = SQLAlchemy()


class FileType(enum.Enum):
    ZIP = '.zip'
    SEVENZIP = '.7z'
    TARBZ2 = '.tar.bz2'

class Status(enum.Enum):
    UPLOADED = 1
    PROCESSED = 2


class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fileName = db.Column(db.String(128), nullable = False)
    newFormat = db.Column(db.Enum(FileType), nullable = False)
    status = db.Column(db.Enum(Status), nullable = False)
    #Falta definir
    timeStamp = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    pathOriginal = db.Column(db.String(128), nullable = False)
    pathConverted = db.Column(db.String(128), nullable = False)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(128), unique=True, nullable = False)
    password = db.Column(db.String(128), nullable = False)
    tasks = db.relationship('Task', cascade='all, delete, delete-orphan', lazy='dynamic')

configure_mappers()

class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}


class TaskSchema(SQLAlchemyAutoSchema):
    newFormat = EnumADiccionario(attribute=("newFormat"))
    status = EnumADiccionario(attribute=("status"))
    class Meta:
        model = Task
        include_relationships = True
        load_instance = True

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True