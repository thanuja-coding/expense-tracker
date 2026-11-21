import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

import E_3_4


app = FastAPI(
    title="Expense Tracker API",
    description="Register and log in to your account",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins={"http://localhost:5173", "http://127.0.0.1:5173"},
    allow_methods={"*"},
    allow_headers={"*"},
)

SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "local-development-key-change-before-deploy",
)
ALGORITHM = "HS256"


def create_access_token(data):
    token_data = data.copy()
    token_data["exp"] = datetime.now(timezone.utc) + timedelta(minutes=30)
    token_data["type"] = "access"

    return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data):
    token_data = data.copy()
    token_data["exp"] = datetime.now(timezone.utc) + timedelta(days=7)
    token_data["type"] = "refresh"

    return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# A Register
@app.post("/register", status_code=201)
def register(user: UserRegister):
    if not user.username.strip() or not user.password.strip():
        raise HTTPException(
            status_code=422,
            detail="Username and password cannot be empty", )
    response = E_3_4.register_user(
        user.username.strip(),
        str(user.email).lower(),
        user.password,)

    if response is None:
        raise HTTPException(
            status_code=409,
            detail="Email address is already registered",)
    return response

#  Login
@app.post("/login")
def login(user: UserLogin):
    user_data = E_3_4.login_user(
        str(user.email).lower(),
        user.password,)

    if user_data is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password", )

    token_data = {
        "id": user_data["id"],
        "username": user_data["username"],
        "email": user_data["email"],
    }

    return {
        "access_token": create_access_token(token_data),
        "refresh_token": create_refresh_token(token_data),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)