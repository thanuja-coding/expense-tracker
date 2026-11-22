from sqlalchemy import Integer, String, Float, Column, create_engine, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


password_hasher = PasswordHasher()

DB_PATH = "expenses.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    role = Column(String)  # add this
    created_at = Column(String)


class Expenses(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    amount = Column(Float)
    category = Column(String)
    expense_date = Column(String)
    created_at = Column(String)


Base.metadata.create_all(engine)

def get_expenses(user_id):
    session = Session(engine)
    expenses = session.query(Expenses).filter(Expenses.user_id == user_id).all()
    response = []
    for expense in expenses:
        response.append({
            "id": expense.id,
            "title": expense.title,
            "amount": expense.amount,
            "category": expense.category,
            "expense_date": expense.expense_date,
            "created_at": expense.created_at
        })
    session.close()
    return response

def add_expense(user_id, title, amount, category, expense_date):
    session = Session(engine)
    new_expense = Expenses(user_id=user_id, title=title, amount=amount, category=category, expense_date=expense_date, created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    session.add(new_expense)
    session.commit()
    response = {
        "id": new_expense.id,
        "title": new_expense.title,
        "amount": new_expense.amount,
        "category": new_expense.category,
        "expense_date": new_expense.expense_date,
        "created_at": new_expense.created_at
    }
    session.close()
    return response

def register_user(username, email, password, role):
    session = Session(engine)
    try:
        user = Users(  username=username,email=email, hashed_password=password_hasher.hash(password), role=role,created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        session.add(user)
        session.commit()
        session.refresh(user)

        return {  "id": user.id, "username": user.username,"email": user.email,"role": user.role,"created_at": str(user.created_at)  }

    except IntegrityError:
        session.rollback()
        return None

    finally:
        session.close()

def login_user(email, password):
    session = Session(engine)

    try:
        user = (  session.query(Users).filter(Users.email == email)
            .first()
        )
        if user is None:
            return None
        try:
            password_hasher.verify(user.hashed_password, password)
        except VerificationError:
            return None

        return {"id": user.id, "username": user.username, "email": user.email, "role": user.role }

    finally:
        session.close()
