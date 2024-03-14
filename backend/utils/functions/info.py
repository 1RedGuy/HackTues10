from backend.index import get_by_val

def can_sign_up():
    profile = get_by_val("profile", "id", 1)
    return not profile 
    