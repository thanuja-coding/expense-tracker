from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import functions

password_hasher = PasswordHasher()

# A1 - Register user
def register_user(username, email, password):
    session = Session(functions.engine)

    try:
        user = functions.Users( username=username,email=email,hashed_password=password_hasher.hash(password),)
        session.add(user)
        try:
            session.commit()
            session.refresh(user)
        except IntegrityError:
            session.rollback()
            return None

        return { "id": user.id,"username": user.username,"email": user.email,"created_at": str(user.created_at), }

    finally:
        session.close()

# A2 - Login user
def login_user(email, password):
    session = Session(functions.engine)

    try:
        user = session.query(functions.Users).filter(
            functions.Users.email == email
        ).first()
        if user is None:
            return None
        try:
            password_hasher.verify(user.hashed_password, password)
        except VerificationError:
            return None

        return {"id": user.id,"username": user.username,"email": user.email,}
    finally:
        session.close()


