from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from database import Student, Grade, Teacher, Group, Subject  

# 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1(session: Session):
    return (
        session.query(Student.name, func.avg(Grade.value).label("average_grade"))
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.value).desc())
        .limit(5)
        .all()
    )

# 2. Знайти студента із найвищим середнім балом з певного предмета.
def select_2(session: Session, subject_id: int):
    return (
        session.query(Student.name, func.avg(Grade.value).label("average_grade"))
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.value).desc())
        .first()
    )

# 3. Знайти середній бал у групах з певного предмета.
def select_3(session: Session, subject_id: int):
    return (
        session.query(Group.name, func.avg(Grade.value).label("average_grade"))
        .join(Student)
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id)
        .all()
    )

# 4. Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4(session: Session):
    return session.query(func.avg(Grade.value).label("average_grade")).scalar()

# 5. Знайти які курси читає певний викладач.
def select_5(session: Session, teacher_id: int):
    subjects = session.query(
        Teacher.name.label('teacher_name'),
        Subject.name.label('subject_name')
    ).join(Subject, Subject.teacher_id == Teacher.id)\
     .filter(Teacher.id == teacher_id)\
     .order_by(Subject.name)\
     .all()

    return subjects

# 6. Знайти список студентів у певній групі.
def select_6(session: Session, group_id: int):
    return (
        session.query(Student.name)
        .filter(Student.group_id == group_id)
        .all()
    )

# 7. Знайти оцінки студентів у окремій групі з певного предмета.
def select_7(session: Session, group_id: int, subject_id: int):
    return (
        session.query(Student.name, Grade.value)
        .join(Grade)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .all()
    )

# 8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(session: Session, teacher_id: int):
    return (
        session.query(func.avg(Grade.value).label("average_grade"))
        .join(Subject)
        .filter(Subject.teacher_id == teacher_id)
        .scalar()
    )

# 9. Знайти список курсів, які відвідує певний студент.
def select_9(session: Session, student_id: int):
    return (
        session.query(Subject.name)
        .join(Grade)
        .filter(Grade.student_id == student_id)
        .group_by(Subject.id)
        .all()
    )


# 10. Список курсів, які певному студенту читає певний викладач.
def select_10(session: Session, student_id: int, teacher_id: int):
    return (
        session.query(Subject.name)
        .join(Grade)
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .group_by(Subject.id)
        .all()
    )