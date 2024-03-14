from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from database.dbmodels import Profile, Subject, Students_to_Subject, ProfileSchema, SubjectSchema

engine = create_engine("mysql+mysqld://guest@%:123456@localhost:3306/db_name")

models = {"profile": Profile, "subject":Subject, "student_to_subject":Students_to_Subject}
schemas = {"profile": ProfileSchema, "subject": SubjectSchema}

def create_new_record(model_name, model_dict):
    with Session(engine) as session:
        models[model_name].__table__.create(bind=engine, checkfirst=True)
        new_record = models[model_name](**model_dict)

        session.add(new_record)
        session.commit()
    
    return schemas[model_name]().dump(new_record)

def get_by_val(model_name, by, val):
    with Session(engine) as session:
        models[model_name].__table__.create(bind=engine, checkfirst=True)

        stmt = select(models[model_name]).where(getattr(models[model_name], by) == val)

        scalars = []

        for res in stmt:
            
            scalars.append(schemas[model_name]().dump(session.scalars(res)))

        return scalars
    
def get_by_id(model_name):
    return get_by_val(model_name,"id", 0)

