from datetime import datetime, timedelta
import jwt
import os
from dotenv import load_dotenv
from functools import wraps
from flask import request,jsonify

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

# encoding the token used for access to different endpoints 
def encode_token(user_id, role_names):
  payload= {
    'exp': datetime.now() + timedelta(days=1,hours=1),
    'iat': datetime.now(),
    'sub': user_id,
    'roles': role_names
  }
  
  token = jwt.encode(payload,SECRET_KEY,algorithm='HS256')
  return token

# checking the token if its valid or not 
def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = None
    if 'Authorization' in request.headers:
      try:
        token = request.headers['Authorization'].split(" ")[1]
        print("Token:", token)
        payload = jwt.decode(token,SECRET_KEY, algorithms="HS256")
      except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired', 'error': 'Unauthorized'}), 401
      except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token', 'error': 'Unauthorized'}), 401
    if not token:
      return jsonify({'message': 'Authentication Token is missing','error': 'Unauthorized'}), 401
    return f(*args,**kwargs)
  return decorated

# checking if the user has the role required to enter the endpoint
def role_required(role):
  def decorator(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
      token = None
      if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
      if not token:
        return jsonify({'message': 'Token is missing'}),401
      try:
        payload = jwt.decode(token,SECRET_KEY, algorithms="HS256")
      except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
      except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401
      roles = payload["roles"]
      
      if role not in roles:
        return jsonify({'message': 'User does not have the required role'}), 403
      
      return f(*args, **kwargs)
    return decorated_function
  return decorator
  
      