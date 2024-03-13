from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from database.dbmodels import Profile, Subject, Students_to_Subject, ProfileSchema, SubjectSchema

engine = create_engine("mysql+mysqld://guest@%:123456@localhost:3306/db_name")

def create_new_record(model_name, model_dict):
    pass
