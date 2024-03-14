import jwt, os, datetime

def generate_token(payload):
    return jwt.encode({**payload, "exp": datetime.datetime.now() + datetime.timedelta(minutes=30)}, os.getenv('SECRET_KEY'), algorithm='HS256')

def verify_token(token):
    return jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])

