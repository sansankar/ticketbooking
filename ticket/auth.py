from typing import NamedTuple
import jwt
from flask import request,current_app,jsonify
from werkzeug import datastructures
from .model import userModel
from functools import wraps

def jwtVerify(func):
   @wraps(func)
   def decorator(*args, **kwargs):

      token = None

      if 'Authorization' in request.headers:
         token = request.headers['Authorization']

      if not token:
          result={'message': 'A valid token is missing'}
          return result,401
      
      data= verify(token)
      if "status_code" in data:
             del data['status_code']
             return data,401
      return func(data,*args, **kwargs)
        
   return decorator

def verify(token):
 try:
    decode=jwt.decode(token, "Happy@123", algorithms=["HS256"])
    validCheck=userModel.query.filter_by(email=decode['userName']).first()
    
    if validCheck is not None:
       return {"userId":decode['userId'],"userName":decode['userName']} 
    
    else:
       result={"message":"Token Not Valid!!"}
       result['status_code']=401
       return result

 except jwt.DecodeError:
    result={"message":"Invalid token"}
    result['status_code']=401
    return result

 except jwt.ExpiredSignatureError:
    result={"message":"Token Expired!!"}
    result['status_code']=401
    return result