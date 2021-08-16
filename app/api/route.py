from sqlalchemy.exc import IntegrityError
from passlib.hash import sha256_crypt
from re import DEBUG
from flask import Blueprint

from flask import request
from ..model import userModel
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

api = Blueprint('api', __name__, url_prefix="/ticket")


@api.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            password = sha256_crypt.encrypt(data['password'])

            print(sha256_crypt.verify(data['password'], password))

            try:
                new_user = userModel(firstName=data['firstName'], lastName=data['lastName'],
                                     email=data['email'], mobilenumber=data['mobilenumber'], password=password)
                db.session.add(new_user)
                db.session.commit()
                print('..........', new_user, '...........')
                response = {
                    "message": f"user {new_user.firstName} has been created successfully."}

                return response
            except IntegrityError:
                return {"message": " Email already exists"}
        else:
            return {"error": "The request payload is not in JSON format"}


@api.route('/users', methods=['GET'])
def getUsers():
    users = userModel.query.all()
    results = [
        {
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email,
            "mobilenumber": user.mobilenumber
        } for user in users]

    return {"No.of.users": len(results), "users": results}


@api.route('/signin')
def signin():
    return "user sign in"
