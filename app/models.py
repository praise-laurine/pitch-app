from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True, index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    pass_secure = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pitch = db.relationship('Pitch',backref='user', lazy='dynamic')
    comment = db.relationship('Comment', backref = 'user', lazy= 'dynamic')
    

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

        @password.setter
        def password(self, password):
            self.pass_secure = generate_password_hash(password)

        def verify_password(self, password):
            return check_password_hash(self.pass_secure,password)    

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))    



    def __repr__(self):
        return f'User {self.username}'

class Pitch(db.Model):
    __tablename__ = 'pitch'
    
    id = db.Column(db.Integer,primary_key = True)
    title =  db.Column(db.String(255)) 
    pitch_content = db.Column(db.String(255))
    author = db.Column(db.String(255))
    category = db.Column(db.String(255))
    upvote = db.Column(db.Integer)
    downvote = db.Column(db.Integer)
    published_at = db.Column(db.DateTime, default = datetime.utcnow)    
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    comment = db.relationship('Comment',backref = 'pitch',lazy="dynamic")

     def save_review(self):
        db.session.add(self)
        db.session.commit()

     @classmethod
     def get_reviews(cls,id):
        reviews = Review.query.filter_by(movie_id=id).all()
        return reviews
    


class Comment(db.Model):
    '''
    Comment class that define comment Objects
    '''
    __tablename__ = 'comment'

    id = db.Column(db.Integer,primary_key = True)
    body = db.Column(db.String(255))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitch.id'))
            
    published_at = db.Column(db.DateTime, default = datetime.utcnow)  

    def __repr__(self):
        return f'User {self.description}'

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'





