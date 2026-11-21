from datetime import datetime

from sqlalchemy import (CheckConstraint,Column, Date,DateTime, Float, ForeignKey,  Integer,   String,   create_engine,)
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
    __table_args__ = (CheckConstraint("amount > 0"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    amount = Column(Float)
    category = Column(String)
    expense_date = Column(Date)
    created_at = Column(DateTime, default=datetime.now)

Base.metadata.create_all(engine)