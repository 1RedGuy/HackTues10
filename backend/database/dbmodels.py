from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

Base = declarative_base()

class Profile(Base):
    __tablename__ = "profile"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(30))
    role: Mapped[str] = mapped_column(String(30))
    username: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"Profile(id={self.id}, username={self.username})"
    
class ProfileSchema(SQLAlchemySchema):
    class Meta:
        model = Profile
        load_instance = True

    id = auto_field() 
    email = auto_field()
    password = auto_field() 
    role = auto_field() 
    username = auto_field() 


class Subject(Base):
    __tablename__ = "subject"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("profile.id"))

    def __repr__(self) -> str:
        return f"Subject(id={self.id}, name={self.name})"
     


class SubjectSchema(SQLAlchemySchema):
    class Meta:
        model = Subject
        load_instance = True
    
    id = auto_field()
    name = auto_field()

class Students_to_Subject(Base):
    __tablename__ = "students_to_subject"
    student_id = Mapped[int] = mapped_column(ForeignKey("profile.id"))
    subject_id = Mapped[int] = mapped_column(ForeignKey("subject.id"))




    
