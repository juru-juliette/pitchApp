from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager
from flask_login import UserMixin

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    pass_secure = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pitch = db.relationship('Pitch', backref='user', lazy='dynamic')
    @property
    def password(self):
            raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
            self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
            return check_password_hash(self.pass_secure,password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()
    def __repr__(self):
        return f'User {self.username}'
    
class Pitch(db.Model):
    __tablename__ = 'pitches'

    id = db.Column(db.Integer,primary_key = True)
    post = db.Column(db.String(255))
    category = db.Column(db.String(255))
    upvotes = db.relationship('Upvote', backref = 'pitch', lazy = 'dynamic')
    downvotes = db.relationship('Downvote', backref = 'pitch', lazy = 'dynamic')
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    @classmethod
    def get_pitches(cls, id):
        pitches = Pitch.query.order_by(pitch_id=id).post().all()
        return pitches

    def __repr__(self):
        return f'Pitch {self.post}'
    
#     comment = db.relationship("Comment", backref="pitches", lazy = "dynamic")
class category (db.Model):
    __tablename__ = 'category'
    id = db.column(db.Integer,primary_key = True)
    category = db.Column(db.String(255))
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



