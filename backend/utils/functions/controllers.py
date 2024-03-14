from flask import request
from sqlalchemy import select
from database.index import get_by_val, get_students_subjects

def GetByModel(model):
    return request.environ.get(model)

def GetMySubjects():
    ri_profile = request.environ.get(ri_profile)
    if ri_profile["role"] == "teacher":
        return get_by_val("subject", "teacher_id", ri_profile["id"])
    return get_students_subjects(ri_profile["id"])
    