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


class Expenses(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.user_id"))
    title = Column(String)
    amount = Column(Float)
    category = Column(String)
    expense_date = Column(String)
    created_at = Column(String)

class User(Base):
    __tablename__ = "Users"
    user_id = Column[int](Integer,primary_key=True)
    user_name=Column[str](String)
    email=Column[str](String)
    password=Column[str](String)
    role=Column[str](String, default="user")


Base.metadata.create_all(engine)


#E1
def get_expenses(user_id):
    session = Session(engine)
    query = session.query(Expenses).filter(Expenses.user_id == user_id)
    response = []
    for expense in query.all():
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
    user = session.query(User).filter_by(email=email).first()
    if user is None:
        session.close()
        return False
    try :
        ph.verify(user.password,password)
       
    except VerifyMismatchError:
        session.close()
        return False 
    
    access_token = create_token(user_id=user.user_id,token_type="access",role=user.role)
    refresh_token= create_token(user_id=user.user_id,token_type="refresh",role=user.role)

    session.close()
    return {"access_token":access_token,"refresh_token":refresh_token}


def create_token(user_id,token_type,role):
    time = ACCESS_TOKEN_EXPIRY
    if token_type == "refresh":
        time = REFRESH_TOKEN_EXPIRY
    payload={
        "role":role,
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
def register_user(user_name :str, email: str, password: str, role: str):
    session = Session(engine)
    user_exists = session.query(User).filter_by(email = email).first()
    if user_exists is not None:
        session.close()
        return False

    try:
        hashed_password = ph.hash(password)
    except Exception:
        session.close()
        return False

    session.add(User(user_name=user_name, email=email, password=hashed_password, role=role))
    session.commit()
    session.close()
    return True



#A3
def refresh_access_token(refresh_token):

    payload = verify_token(refresh_token, token_type="refresh")

    if not payload:
        return None

    access_token = create_token(user_id=payload["user_id"], token_type="access", role=payload["role"])

    return access_token 