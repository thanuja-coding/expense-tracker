from sqlalchemy import Integer, String, Float, Column, create_engine, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime,timedelta , timezone
import jwt


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