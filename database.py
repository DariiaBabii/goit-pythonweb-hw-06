from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    DateTime,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Student(Base):

    __tablename__ = 'student'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("group.id", ondelete="CASCADE"), nullable=False)
    group = relationship("Group", back_populates='student')
    grade = relationship("Grade", back_populates="student", cascade="all, delete-orphan")

class Group(Base):

    __tablename__ = 'group'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    students = relationship(
        "Student", back_populates="group", cascade="all, delete-orphan"
    )

class Teacher(Base):

    __tablename__ = "teacher"
    id = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = mapped_column(String, nullable=False)
    subjects = relationship("Subject", back_populates="teacher")

class Subject(Base):
    __tablename__ = 'subject'


    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    teacher_id: Mapped[int] = mapped_column(Integer, ForeignKey("teacher.id", ondelete="SET NULL"))
    
    teacher = relationship("Teacher", back_populates="subject")
    grades = relationship("Grade", back_populates="subject", cascade="all, delete-orphan")

    
class Grade(Base):

    __tablename__ = 'grade'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    value: Mapped[int] = mapped_column(Integer, nullable=False)  
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("student.id", ondelete="CASCADE"), nullable=False)
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subject.id", ondelete="CASCADE"), nullable=False)
    date_received: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    
    student = relationship("Student", back_populates="grade")
    subject = relationship("Subject", back_populates="grades")