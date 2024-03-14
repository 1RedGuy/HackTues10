from database.index import get_by_val
from utils.errors.NotFound import NotFoundError

def can_sign_up():
    try:
      get_by_val("profile", "id", 1)
      return False
    except NotFoundError:
      return True
    except Exception as error:
      raise error
    