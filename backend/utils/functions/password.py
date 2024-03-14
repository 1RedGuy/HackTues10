import re
from random import randint
from bcrypt import hashpw, gensalt, checkpw

def verify_password(password: str) -> bool:
    return (
        len(password) >= 8 
        and any(c.isupper() for c in password) 
        and any(c.isdigit() for c in password) 
        and re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>\/?]', password)
        and not any(pattern in password.lower() for pattern in ["123456", "password", "qwerty", "12345678"])
    )

def hash_password(passsword):
    return hashpw(passsword.encode('utf-8'), gensalt()).decode('utf-8')

def check_password(password, hashed_password):
    return checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_password():
    return str(randint(100000, 999999))
    