from flask import request
from sqlalchemy import select
from database.index import get_by_val, get_students_subjects
from database.index import create_new_record

def GetByModel(model):
    return request.environ.get(model)

def GetMySubjects():
    ri_profile = request.environ.get(ri_profile)
    if ri_profile["role"] == "teacher":
        return get_by_val("subject", "teacher_id", ri_profile["id"])
    return get_students_subjects(ri_profile["id"])
    
def AttachStudents(subject_id):
    students = request.environ.get("request_body")
    for student in students:
        create_new_record("student_to_subject", {"student_id": student["student_id"], "subject_id": subject_id})
    return True, 201
        
