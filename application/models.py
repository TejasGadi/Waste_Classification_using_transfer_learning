import flask
from application import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Document):
    user_id     =   db.IntField( unique=True )
    first_name  =   db.StringField( max_length=50 )
    last_name   =   db.StringField( max_length=50 )
    email       =   db.StringField( max_length=30, unique=True )
    password    =   db.StringField( )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)

class Contact(db.Document):
    email        =   db.StringField( max_length=88 )
    first        =   db.StringField( max_length=88 )
    subject      =   db.StringField( max_length=88 )
    message      =   db.StringField( max_length=88 )
