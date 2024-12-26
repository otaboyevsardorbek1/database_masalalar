# -*- coding: utf-8 -*-
import bcrypt
from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey, Table
)
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# Bazaviy modelni yaratish
Base = declarative_base()

# "Ko'p-ko'pga" munosabatni saqlash uchun ko‘prik jadval
user_roles_table = Table(
    'user_roles', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)

# Parolni xeshlash funksiyasi
def hash_password(password):
    """Parolni xeshlaydi."""
    salt = bcrypt.gensalt()  # Tasodifiy tuz (salt) generatsiya qiladi
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

# Parolni tekshirish funksiyasi
def check_password(hashed_password, plain_password):
    """Xeshlangan parolni foydalanuvchi paroli bilan solishtiradi."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

# Foydalanuvchilar jadvali
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Xeshlangan parolni saqlash
    roles = relationship('Role', secondary=user_roles_table, back_populates='users')

    # Parolni avtomatik xeshlash
    def set_password(self, plain_password):
        self.password = hash_password(plain_password).decode('utf-8')

    def check_password(self, plain_password):
        return check_password(self.password.encode('utf-8'), plain_password)

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"

# Rollar jadvali
class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    users = relationship('User', secondary=user_roles_table, back_populates='roles')

    def __repr__(self):
        return f"<Role(name={self.name})>"

# SQLite ma'lumotlar bazasini ulash
engine = create_engine('sqlite:///app.db')

# Jadvalni yaratish
Base.metadata.create_all(engine)

# Sessiya yaratish
Session = sessionmaker(bind=engine)
session = Session()

# Misol uchun foydalanuvchilar va rollarni qo‘shish
if __name__ == '__main__':
    # Rollarni yaratish
    admin_role = Role(name='admin', description='Administrator with full access')
    user_role = Role(name='user', description='Regular user with limited access')

    # Foydalanuvchini yaratish va parolni xeshlash
    user1 = User(username='john_doe', email='john@example.com')
    user1.set_password('super_secure_password')  # Parolni xeshlash
    user2 = User(username='jane_doe', email='jane@example.com')
    user2.set_password('another_secure_password')  # Parolni xeshlash

    # Rollarni ulash
    user1.roles.append(admin_role)
    user2.roles.append(user_role)

    # Ma'lumotlar bazasiga saqlash
    session.add_all([admin_role, user_role, user1, user2])
    session.commit()

    # Parolni tekshirish
    print(user1.check_password('super_secure_password'))  # True
    print(user1.check_password('wrong_password'))        # False

    # Natijani tekshirish
    users = session.query(User).all()
    for user in users:
        print(user)
        print("Roles:", [role.name for role in user.roles])
