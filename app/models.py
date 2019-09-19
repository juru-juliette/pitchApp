from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager
from flask_login import UserMixin
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    password_hash = db.Column(db.String(255))
    bio = db.Column(db.String(255))
   
    def __repr__(self):
        return f'User {self.username}'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# class Pitch(db.Model):
#     __tablename__ = 'pitches'

#     id = db.Column(db.Integer,primary_key = True)
#     name = db.Column(db.String(255))
#     users = db.relationship('User',backref = 'pitch',lazy="dynamic")
#     user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
#     def __repr__(self):
#         return f'User {self.name}'