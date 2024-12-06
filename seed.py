from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
from faker import Faker
from database import Base, Student, Group, Teacher, Subject, Grade
import atexit

faker = Faker()

engine = create_engine('postgresql://DBpostgres:azsxdc@localhost:5432/postgres')
Session = sessionmaker(bind=engine)
session = Session()

def close_session():
    session.close()

atexit.register(close_session)

def seed_data():
    groups = [Group(name=f"Group {i+1}") for i in range(3)]
    session.add_all(groups)
    session.commit()

    teachers = [Teacher(name=faker.name()) for _ in range(5)]
    session.add_all(teachers)
    session.commit()

    subjects = [
        Subject(name=f"Subject {i+1}", teacher=random.choice(teachers))
        for i in range(8)
    ]
    session.add_all(subjects)
    session.commit()

    students = [
        Student(name=faker.name(), group=random.choice(groups))
        for _ in range(50)
    ]
    session.add_all(students)
    session.commit()

    for student in students:
        for subject in subjects:
            for _ in range(random.randint(5, 20)):
                grade = Grade(
                    student=student,
                    subject=subject,
                    grade=round(random.uniform(2.0, 5.0), 2),
                    date_received=faker.date_time_this_year(),
                )
                session.add(grade)
    session.commit()

if __name__ == "__main__":
    Base.metadata.create_all(engine) 
    seed_data()
    print("Database seeded successfully!")
