"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


# MODELS GO BELOW

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    first_name = db.Column(db.String(50),
                    nullable=False,
                    unique=False)

    last_name = db.Column(db.String(50),
                    nullable=False,
                    unique=False)

    image_url = db.Column(db.String(500),
                    nullable=True,
                    unique=False)
    

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
    title = db.Column(db.String(50),
                    nullable = False,
                    unique = True)
                
    content = db.Column(db.String(1000),
                    nullable=False,
                    unique = True)
    
    created_at = db.Column(db.DateTime,
                    nullable = False,
                    default = datetime.utcnow
                    )

# https://pypi.org/project/SQLAlchemy-Utc/
# https://www.postgresqltutorial.com/postgresql-timestamp/

    user_id = db.Column(
                    db.Integer,
                    db.ForeignKey('users.id'))


    user = db.relationship('User', backref='posts')
