from sqlalchemy import Integer, String, Float, Column, create_engine, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime,timedelta , timezone
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


ph = PasswordHasher()

DB_PATH = "expenses.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


ACCESS_TOKEN_EXPIRY = 15
REFRESH_TOKEN_EXPIRY = 7*24*60
SECRET_KEY ="SECRETCODE"
ALGORITHM = "HS256"


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    hashed_password = Column(String)
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


#E1
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

#E2
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


def verify_login(email,password):
    session = Session(engine)
    user = session.query(Users).filter_by(email=email).first()
    if user is None:
        session.close()
        return False
    try :
        ph.verify(user.hashed_password,password)

    except VerifyMismatchError:
        session.close()
        return False

    access_token = create_token(user_id=user.id,token_type="access")
    refresh_token= create_token(user_id=user.id,token_type="refresh")

    session.close()
    return {"access_token":access_token,"refresh_token":refresh_token}


def create_token(user_id,token_type):
    time = ACCESS_TOKEN_EXPIRY
    if token_type == "refresh":
        time = REFRESH_TOKEN_EXPIRY
    payload={
        "user_id":user_id,
        "token_type":token_type,
        "exp":datetime.now(timezone.utc)+timedelta(minutes=time)
    }
    token =jwt.encode(payload=payload,key=SECRET_KEY,algorithm=ALGORITHM)
    return token

def verify_token(token,token_type):
    try:
        payload = jwt.decode(jwt=token,key=SECRET_KEY,algorithms=[ALGORITHM])
    except:
        return False

    if payload ["token_type"] == token_type:
        return payload
    return False


#user
def register_user(username :str, email: str, password: str):
    session = Session(engine)
    user_exists = session.query(Users).filter_by(email = email).first()
    if user_exists is not None:
        session.close()
        return False

    try:
        hashed_password = ph.hash(password)
    except Exception:
        session.close()
        return False

    session.add(Users(username=username, email=email, hashed_password=hashed_password, created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    session.commit()
    session.close()
    return True