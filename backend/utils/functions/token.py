import jwt, os, datetime

def generate_token(payload):
    return jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256', expires_delta=datetime.timedelta(days=1))

def verify_token(token):
    return jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])

