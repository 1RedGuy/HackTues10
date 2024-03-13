import re

def verify_password(password: str) -> bool:
    return (
        len(password) >= 8 
        and any(c.isupper() for c in password) 
        and any(c.isdigit() for c in password) 
        and re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>\/?]', password)
        and not any(pattern in password.lower() for pattern in ["123456", "password", "qwerty", "12345678"])
    )