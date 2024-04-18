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
    password: Mapped[str] = mapped_column(String(150))
    role: Mapped[str] = mapped_column(String(30))
    name: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"Profile(id={self.id}, name={self.name})"
    
class ProfileSchema(SQLAlchemySchema):
    class Meta:
        model = Profile
        load_instance = True

    id = auto_field() 
    email = auto_field()
    password = auto_field() 
    role = auto_field() 
    name = auto_field() 


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

class Student_to_Subject(Base):
    __tablename__ = "student_to_subject"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id : Mapped[int] = mapped_column(ForeignKey("profile.id"))
    subject_id : Mapped[int] = mapped_column(ForeignKey("subject.id"))

class Post(Base):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(500))
    title: Mapped[str] = mapped_column(String(50))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id"))

class PostsSchema(SQLAlchemySchema):
    class Meta:
        model = Post
        load_instance = True

    url = auto_field()
    title = auto_field()


    
