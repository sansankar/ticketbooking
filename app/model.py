from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class userModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String())
    lastName = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    mobilenumber = db.Column(db.Text)
    password = db.Column(db.String())

    def __init__(self, firstName, lastName, email, mobilenumber, password):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.mobilenumber = mobilenumber
        self.password = password

    def __repr__(self):
        return f"<user {self.firstName}>"
