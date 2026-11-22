from sqlalchemy.orm import Session
from datetime import datetime
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from functions import engine, Users, create_token


ph = PasswordHasher()


#A2
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


#A1
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