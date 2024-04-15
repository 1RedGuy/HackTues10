from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import Session
from database.dbmodels import Profile, Subject, Student_to_Subject, ProfileSchema, SubjectSchema, Posts, PostsSchema
from utils.errors.NotFound import NotFoundError
import os

engine = create_engine(os.getenv("DATABASE_URI"), echo=True)

models = {"profile": Profile, "subject":Subject, "student_to_subject":Student_to_Subject, "posts": Posts}
schemas = {"profile": ProfileSchema, "subject": SubjectSchema, "student_to_subject": SubjectSchema, "posts": PostsSchema}

def create_new_record(model_name, model_dict, seraialize=True):
    with Session(engine) as session:
        models[model_name].__table__.create(bind=engine, checkfirst=True)
        print(model_dict)
        new_record = models[model_name](**model_dict)

        session.add(new_record)
        session.commit()

        if seraialize:
            return schemas[model_name]().dump(new_record)

def get_by_val(model_name, by=None, val=None, assertive=True):
    with Session(engine) as session:
        models[model_name].__table__.create(bind=engine, checkfirst=True)
        if by == None and val==None:
            stmt = select(models[model_name])
        else:
            stmt = select(models[model_name]).where(getattr(models[model_name], by) == val)

        dumped_scalars = []

        exists = session.scalar(stmt.limit(1))

        print(assertive)

        if exists:
            for res in session.scalars(stmt):
                dumped_scalars.append(schemas[model_name]().dump(res))
        else:
            if assertive:
                raise NotFoundError(f"There is no such {model_name}!")
            return []
        return dumped_scalars
    
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

def delete_record(model_name, id):
    with Session(engine) as session:
        stmt = delete(models[model_name]).where(getattr(models[model_name], "id") == id)
        session.commit()

def get_students_subjects(student_id):
    with Session(engine) as session:
        stmt = select(Student_to_Subject).where(Student_to_Subject.student_id == student_id).join(Subject, Subject.id == Student_to_Subject.subject_id)
        scalars = []

        for res in session.scalars(stmt):
            scalars.append(SubjectSchema().dump(session.scalar(res)))

        return scalars
