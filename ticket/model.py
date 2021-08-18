from operator import imod
from flask import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy()


class userModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String())
    lastName = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    mobilenumber = db.Column(db.String)
    password = db.Column(db.String())
    booking_id = db.relationship('booking', backref='users', lazy=True)

    def __init__(self, firstName, lastName, email, mobilenumber, password):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.mobilenumber = mobilenumber
        self.password = password

    def __repr__(self):
        return f"<user {self.id} {self.firstName} {self.email} {self.password}>"


class booking(db.Model):

    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    bookingDate = db.Column(db.Date)
    busName=db.Column(db.String())
    bookingNumber = db.Column(db.Integer, default=datetime.now().strftime("%f"))
    fromTo=db.Column(db.String())
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, bookingDate, busName,userId,fromTo):
        self.bookingDate = bookingDate
        self.busName = busName
        self.userId=userId
        self.fromTo=fromTo
       
    def __repr__(self):
        return f'<booking: {self.bookingNumber} {self.fromTo} {self.busName} {self.bookingDate}>'



