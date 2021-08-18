from sqlalchemy.exc import IntegrityError
from passlib.hash import sha256_crypt
from re import DEBUG
from flask import Blueprint

from flask import request
from ..model import userModel,booking,db
from ..auth import jwtVerify
from flask_sqlalchemy import SQLAlchemy

import jwt
import datetime

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

                return response,201
            except IntegrityError:
                return {"message": " Email already exists"}
        else:
            return {"error": "The request payload is not in JSON format"}


@api.route('/signin',methods=['POST'])
def signin():
    if request.method == 'POST':
        if request.is_json:
            
              data = request.get_json()
              users = userModel.query.filter_by(email=data['userName']).first()
              if users==None:
                  result={"message":"users not found"}
                  return result,404
              else:

                 pwdcheck=sha256_crypt.verify(data['password'],users.password)
                 if pwdcheck==True:
                     token = jwt.encode({'userId' :users.id ,'userName':users.email, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, "Happy@123", algorithm="HS256")
                     decode=jwt.decode(token, "Happy@123", algorithms=["HS256"])
                     print(decode)
                     result={"message":"login success", "authToken":token}
                     return result,200
                 else:
                     result={"message":"Entered password is Wrong!!"}
                     return result,403


@api.route('/booking', methods=['POST'])
@jwtVerify
def bookings(paramsData):
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            try:
               bookbus = booking(bookingDate=data['bookingDate'], busName=data['busName'],userId=paramsData['userId'],fromTo=data['fromTo'])
               db.session.add(bookbus)            
               db.session.commit()
               print(bookbus, '...........')
               response = {
                    "message": f" Booking Success and Your Booking ID: {bookbus.bookingNumber}"}

               return response,201
            except IntegrityError:
                result={"message": " user not exists"}
               
                return result,400
        else:
            return {"error": "The request payload is not in JSON format"}


@api.route('/users', methods=['GET'])
@jwtVerify
def getUsers(parmdata):
    print(parmdata,'.....')
    users = userModel.query.all()
    print(users)
    results = [
        {
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email,
            "mobilenumber": user.mobilenumber
        } for user in users]

    return {"No.of.users": len(results), "users": results}

@api.route('/users/<userId>', methods=['GET'])
@jwtVerify
def getUsersbooking(paramdata,userId):
   
    print(paramdata)
    users = booking.query.filter_by(userId=userId).all()

    results=[{
        "BookingId":userdata.bookingNumber,
        "FromTo":userdata.fromTo,
        "BookigDate":userdata.bookingDate
    } for userdata in users]
  
    return {"yourBookings":results}



            
              

          
              
