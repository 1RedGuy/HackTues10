
from errors.ValidationError import ValidationError
from flask import request, jsonify
from functools import wraps
from functions.password import verify_password
from functions.email import verify_email
from functions.token import generate_token, verify_token

def HandleResponse():
  def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
          try: 
            request.environ.update({"request_body": request.get_json()})

            (output, status_code) = func(*args, **kwargs)
            return jsonify({"response": output}), status_code
          
          except ValidationError as error:    
            return jsonify({"Validation Error": str(error)}), 400
          except Exception as error:
            return jsonify({"Exception Error": str(error)}), 500
      return wrapper
  return decorator

def ValidateRequest():
  def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
          request_body = request.environ.get("request_body")
          if not request_body:
            raise ValidationError("Request body is empty")
          return func(*args, **kwargs)
      return wrapper
  return decorator

def ValidateSignUp():
  def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
          credentials = request.environ.get("request_body")                        
          if credentials["password"] != credentials["confirm_password"]:
            raise ValidationError("Passwords do not match")
          if verify_email(credentials["email"]) == False:
            raise ValidationError("Invalid email")
          if verify_password(credentials["password"]) == False:
            raise ValidationError("Invalid password")
          return func(*args, **kwargs)
      return wrapper
  return decorator