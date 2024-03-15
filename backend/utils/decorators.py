
from utils.errors.ValidationError import ValidationError
from utils.errors.AuthorizationError import AuthorizationError
from utils.errors.ForbiddenAccessError import ForbiddenAccessError 
from utils.errors.AuthenticationError import AuthenticationError
from flask import request, jsonify
from functools import wraps
from utils.functions.password import verify_password, check_password, hash_password, generate_password
from utils.functions.email import verify_email
from utils.functions.token import verify_token
from database.index import create_new_record, get_by_id, get_by_val
from utils.errors.NotFound import NotFoundError
from mail.index import Email_Service
from werkzeug.utils import secure_filename
import os
from utils.functions.allowed_file import allowed_file

def HandleResponse(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		# try: 
			
			(output, status_code) = func(*args, **kwargs)
			return jsonify({"response": output}), status_code
		
		# except ValidationError as error:    
		# 	return jsonify({"error": str(error)}), 400
		# except Exception as error:
		# 	return jsonify({"error": str(error)}), 500
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
		if len(credentials.values()) != 4:
			raise ValidationError("Invalid sign up")                      
		if credentials["password"] != credentials["confirm_password"]:
			raise ValidationError("Passwords do not match")
		if verify_email(credentials["email"]) == False:
			raise ValidationError("Invalid email")
		if verify_password(credentials["password"]) == False:
			raise ValidationError("Invalid password")
		if not credentials["name"]:
			raise ValidationError("Name is empty")
		
		del credentials["confirm_password"]
		credentials.update({"role": "admin"})
		credentials["password"] = hash_password(credentials["password"])

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
			get_by_val("profile", "id", 1)
			raise ForbiddenAccessError("Signing up is not allowed. Admin already exists.")
		except NotFoundError as error:
			return func(*args, **kwargs)
		except Exception as error:
			raise error
		
	return wrapper

def GetBy(model_name, by, loc, assertive=True, listed=True):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			print(loc)
			if loc == None and by == None:
				docs = get_by_val(model_name, assertive=assertive)
			if loc == "args":
				docs = get_by_val(model_name, by, request.args.get(by), assertive)
			elif loc == "body":
				docs = get_by_val(model_name, by, request.environ.get("request_body")[by], assertive)
			else:
				docs = get_by_val(model_name, "id", kwargs[by + "_id"], assertive)

			if not listed:
				request.environ.update({model_name: docs[0]})
				return func(*args, **kwargs)
			
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


def VerifyPassword(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		credentials = request.environ.get("request_body")
		profile = request.environ.get("profile")
		if check_password(credentials["password"], profile["password"]):
			return func(*args, **kwargs)
		else:
			raise AuthenticationError("Invalid password")
	return wrapper

def GeneratePassword(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		email_service = Email_Service()
		request_body = request.environ.get("request_body")
		for element in request_body:
			generated_password = generate_password()
			email_service = Email_Service()
			email_service.send_password(element["email"], generated_password)
			element.update({"password": hash_password(generated_password)})
		
		
		return func(*args, **kwargs)
	return wrapper

def ValidateBodyRoles(role):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			request_body = request.environ.get("request_body")
			for element in request_body:
				profile = get_by_id("profile",element[role + "_id"])
				if profile["role"] != role:
					raise ValidationError(f"Profile with id = {id} is not {role}")
			return func(*args, **kwargs)
		return wrapper
	return decorator

def StoreFile(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if 'files[]' not in request.files:
			raise NotFoundError("No file!")

		files = request.files.getlist('files[]')

		for file in files:
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.getcwd() + os.path.join("\\public", filename))
			else:
				raise NotFoundError("No file!")
		return func(*args, **kwargs)
	return wrapper
	
def GetJSONBody(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if request.method != "GET" and request.method != "DELETE":
			body = request.get_json()
			if body.get("list") != None:
				body = body["list"]
			request.environ.update({"request_body": body})
		return func(*args, **kwargs)
	return wrapper
