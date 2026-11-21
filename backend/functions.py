from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base

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


class Expenses(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    amount = Column(Float)
    category = Column(String)
    expense_date = Column(String)
    created_at = Column(DateTime, default=datetime.now)


Base.metadata.create_all(engine)


