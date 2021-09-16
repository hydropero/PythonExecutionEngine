from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # id will auto increment apparently
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # func.now just grabs current date information
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # user in user.id references User class but in SQL they don't use the uppercase convention, go figure
    # user.id goes to that table and then references that table's primary key



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # must have 1 primary key
    email = db.Column(db.String(150), unique=True)
    # unique means no duplicates allowed in the column
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    # whenever a note is created add it's noteID here, it will amount to a list, this needs capital FACT why?? UNKNOWN