from datetime import datetime

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from sqlalchemy import (Column,DateTime,Integer,String,create_engine,)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, declarative_base


DB_PATH = "expenses.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.now)


Base.metadata.create_all(engine)

password_hasher = PasswordHasher()

def register_user(username, email, password):
    session = Session(engine)

    try:
        user = Users(username=username,email=email,hashed_password=password_hasher.hash(password),)
        session.add(user)

        try:
            session.commit()
            session.refresh(user)
        except IntegrityError:
            session.rollback()
            return None

        return {"id": user.id,"username": user.username,"email": user.email,"created_at": user.created_at.isoformat(),     }
    finally:
        session.close()


def login_user(email, password):
    session = Session(engine)

    try:
        user = session.query(Users).filter(Users.email == email).first()

        if user is None:
            return None

        try:
            password_hasher.verify(user.hashed_password, password)
        except VerificationError:
            return None

        return {"id": user.id,"username": user.username, "email": user.email, }
    finally:
        session.close()