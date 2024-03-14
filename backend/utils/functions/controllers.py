from flask import request

def GetByModel(model):
    return request.environ.get(model)