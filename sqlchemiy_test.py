from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from bcrypt import hashpw, gensalt, checkpw

# SQLAlchemy base class
Base = declarative_base()

# Database engine (SQLite misolida)
DATABASE_URL = "sqlite:///university.db"
engine = create_engine(DATABASE_URL, echo=False)

# Session yaratish
Session = sessionmaker(bind=engine)
session = Session()

# User modeli
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    def check_password(self, password):
        return checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

# Student modeli
class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))
    email = Column(String(120), unique=True, nullable=False)
    major = Column(String(80))
    
    group = relationship("Group", back_populates="students")

# Group modeli
class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    
    students = relationship("Student", back_populates="group")

# Organization modeli
class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True, nullable=False)
    contact_email = Column(String(120))

# Student_Organization modeli
class StudentOrganization(Base):
    __tablename__ = 'student_organization'

    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'), primary_key=True)
    
    student = relationship("Student", back_populates="organizations")
    organization = relationship("Organization", back_populates="students")

# Organization - Student reverse relationship
Organization.students = relationship("StudentOrganization", back_populates="organization")
Student.organizations = relationship("StudentOrganization", back_populates="student")


# Jadvalni yaratish
Base.metadata.create_all(engine)

# CRUD operatsiyalarini amalga oshirish
def create_user(username, email, password):
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    session.add(new_user)
    session.commit()
    print(f"User {username} created!")

def create_student(first_name, last_name, email, major, group_name):
    group = session.query(Group).filter_by(name=group_name).first()
    if not group:
        print(f"Group {group_name} not found!")
        return
    new_student = Student(first_name=first_name, last_name=last_name, email=email, major=major, group=group)
    session.add(new_student)
    session.commit()
    print(f"Student {first_name} {last_name} created!")

def create_group(group_name):
    new_group = Group(name=group_name)
    session.add(new_group)
    session.commit()
    print(f"Group {group_name} created!")

def create_organization(name, contact_email):
    new_org = Organization(name=name, contact_email=contact_email)
    session.add(new_org)
    session.commit()
    print(f"Organization {name} created!")

def assign_student_to_organization(student_email, org_name):
    student = session.query(Student).filter_by(email=student_email).first()
    organization = session.query(Organization).filter_by(name=org_name).first()
    if student and organization:
        student_org = StudentOrganization(student_id=student.id, organization_id=organization.id)
        session.add(student_org)
        session.commit()
        print(f"Student {student.first_name} {student.last_name} assigned to {organization.name}")
    else:
        print(f"Student or Organization not found.")

def delete_user(username):
    user = session.query(User).filter_by(username=username).first()
    if user:
        session.delete(user)
        session.commit()
        print(f"User {username} deleted!")
    else:
        print(f"User {username} not found.")

def update_student_major(email, new_major):
    student = session.query(Student).filter_by(email=email).first()
    if student:
        student.major = new_major
        session.commit()
        print(f"Student {student.first_name} {student.last_name} major updated to {new_major}")
    else:
        print(f"Student with email {email} not found.")

def view_students_in_group(group_name):
    group = session.query(Group).filter_by(name=group_name).first()
    if group:
        students = group.students
        if students:
            print(f"Students in group {group_name}:")
            for student in students:
                print(f"{student.first_name} {student.last_name} - {student.major}")
        else:
            print(f"No students in group {group_name}.")
    else:
        print(f"Group {group_name} not found.")

# Konsolda ishlovchi dastur misol
if __name__ == "__main__":
    # Yangi foydalanuvchi yaratish
    create_user("john_doe", "john@example.com", "password123")

    # Yangi guruh yaratish
    create_group("Informatika 2024")

    # Yangi talaba yaratish
    create_student("John", "Doe", "john_doe@example.com", "Computer Science", "Informatika 2024")

    # Yangi tashkilot yaratish
    create_organization("Google", "contact@google.com")

    # Talabani tashkilotga qo'shish
    assign_student_to_organization("john_doe@example.com", "Google")

    # Talabaning o'qish yo'nalishini yangilash
    update_student_major("john_doe@example.com", "Data Science")

    # Guruhdagi talabalarni ko'rish
    view_students_in_group("Informatika 2024")

    # Foydalanuvchini o'chirish
    delete_user("john_doe")
