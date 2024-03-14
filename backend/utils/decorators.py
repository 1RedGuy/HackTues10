
from utils.errors.ValidationError import ValidationError
from utils.errors.AuthorizationError import AuthorizationError
from utils.errors.ForbiddenAccessError import ForbiddenAccessError 
from utils.errors.AuthenticationError import AuthenticationError
from flask import request, jsonify
from functools import wraps
from utils.functions.password import verify_password
from utils.functions.email import verify_email
from utils.functions.token import verify_token
from database.index import create_new_record, get_by_id, get_by_val
from utils.errors.NotFound import NotFoundError

def HandleResponse(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		try: 
			if request.method != "GET" and request.method != "DELETE":
				request.environ.update({"request_body": request.get_json()})

			(output, status_code) = func(*args, **kwargs)
			return jsonify({"response": output}), status_code
		
		except ValidationError as error:    
			return jsonify({"Validation Error": str(error)}), 400
		except Exception as error:
			return jsonify({"Exception Error": str(error)}), 500
	return wrapper

def ValidateRequest(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		request_body = request.environ.get("request_body")
		if not request_body:
			raise ValidationError("Request body is empty")
		return func(*args, **kwargs)
	return wrapper

def ValidateSignUp(func):
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

def Create(model):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			request_body = request.environ.get("request_body")
			if type(request_body) == type([]):
				res = []
				for record in request_body:
					res.append(create_new_record(model, record))
				request.environ.update({model+"s": res})
				return func(*args, **kwargs)
			res = create_new_record(model, request_body)
			request.environ.update({model: res})
			return func(*args, **kwargs)
		return wrapper
	return decorator

def VerifyToken(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		token = request.headers.get("Authorization")
		if not token:
			raise AuthenticationError("No token provided")
		
		token = token.split("Bearer ")[1]

		profile_id = verify_token(token)["profileId"]
		profile = get_by_id("profile", profile_id)
		request.environ.update({"ri_profile": profile})
		return func(*args, **kwargs)
	return wrapper

def VerifyRole(role):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			user_role = request.environ.get("ri_profile")["role"]
			if user_role != role:
				raise AuthorizationError("Unauthorized")
			return func(*args, **kwargs)
		return wrapper
	return decorator	

def SignUpAccess(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		try:
			profile = get_by_val("profile", "id", 1)
		except:
			return func(*args, **kwargs)
		
		if profile:
			raise ForbiddenAccessError("Signing up is not allowed. Admin already exists.")
	return wrapper

def GetBy(model_name, by, loc):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			if loc == "args":
				docs = get_by_val(model_name, by, request.args.get(by))
			else:
				docs = get_by_val(model_name, "id", kwargs[by + "_id"])
			
			request.environ.update({model_name + "s": docs})
			return func(*args, **kwargs)
		return wrapper
	return decorator
				
def Exists(model_name):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			element_id = kwargs.get(model_name+"_id")
			element = get_by_id(model_name, element_id)
			request.environ.update({model_name: element})
			return func(*args, **kwargs)
		return wrapper 
	return decorator


			
