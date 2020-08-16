import os
from sqlalchemy import Column, String, Integer, create_engine, Date, Float
from datetime import date
from flask_sqlalchemy import SQLAlchemy
import json


database_name = "postgres"
os.environ['DATABASE_URL'] = "postgres://{}/{}".format("postgres:1234@localhost:5432", database_name)

#os.environ['DATABASE_URL'] = "postgres://eofhptjcntmjrc:4d8b31f8724ee1080f7a9d554ebe3f1f7168351169fa2cb4e400365e832e5e71@ec2-3-222-150-253.compute-1.amazonaws.com:5432/dros2klg10jhm"
database_path = os.environ['DATABASE_URL']


db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    # binds a flask application and a SQLAlchemy service
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    # drops the database tables and starts fresh
    db.drop_all()
    db.create_all()
    new_records()


def new_records():
    # create new records "test"
    new_actor = (Actor(
        name='Ward ahmed',
        gender='Female',
        age=100
    ))

    new_movie = (Movie(
        title='ward ahmad new movie',
        release_date=date.today()
    ))

    new_actor.insert()
    new_movie.insert()
    db.session.commit()

# Actor Model


class Actor(db.Model):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }


# Movies Model
class Movie(db.Model):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }
