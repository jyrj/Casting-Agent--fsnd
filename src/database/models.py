import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

#database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "postgres://postgres:@localhost:5432/movies"

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
    db.app = app
    db.init_app(app)

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

'''
Movies
a persistent movies entity with title and release date as attributes, extends the base SQLAlchemy Model
'''

class Movie(db.Model):
    __tablename__= "movies"

    id = Column(Integer(), primary_key=True)
    title = Column(String(80), unique=True)
    release_date =  Column(db.DateTime())
    #connection with other model

    def movies_model(self):
        return{
            "id": self.id,
            "title": self.title,
            "release date": self.release_date
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            movie = Movie(title=req_title, release_date=release date)
            movie.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movie(title=req_title, release_date=release date)
            movie.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            movie.title = '<New Name>''
            movie.update()
    '''
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.movies_model())

class Actors(db.Model):
    __tablename__="actors"
    
    id = Column(Integer(), primary_key=True)
    name = Column(String(80))
    age = Column(Integer())
    gender = Column(String(26))
    
    #backref