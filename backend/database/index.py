from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from database.dbmodels import Profile, Subject, Students_to_Subject, ProfileSchema, SubjectSchema
from utils.errors.NotFound import NotFoundError
import os

engine = create_engine(os.getenv("DATABASE_URI"), echo=True)

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

        if stmt:
            for res in stmt:
                if res:
                    scalars.append(schemas[model_name]().dump(session.scalars(res)))
                else:
                    raise NotFoundError("There is no such a record!")
        else:
            raise NotFoundError("There is no such a record!")
        return scalars
    
def get_by_id(model_name, id):
    return get_by_val(model_name,"id", id)[0]


def change_record(model_name, id, model_dict):
    with Session(engine) as session:

        stmt = session.query(models[model_name]).filter(getattr(models[model_name], "id") == id).limit(1) 
        if stmt:
            for item in model_dict.items():
                stmt = stmt.update({item[0]: item[1]})

            session.commit()
        else:
            raise NotFoundError(f"There is no such {model_name}!")
    return 


