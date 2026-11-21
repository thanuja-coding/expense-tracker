import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

import functions


app = FastAPI(
    title="Expense Tracker API",
    description="Register and log in to your account",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = os.getenv("JWT_SECRET_KEY","local-development-key-change-before-deploy",)
ALGORITHM = "HS256"


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


@app.post("/register", status_code=201)
def register(user: UserRegister):
    if not user.username.strip() or not user.password.strip():
        raise HTTPException(status_code=422,detail="Username and password cannot be empty",)

    response = functions.register_user(
        username=user.username.strip(),
        email=str(user.email).lower(),
        password=user.password,
    )

    if response is None:
        raise HTTPException(status_code=409,detail="Email address is already registered", )

    return response


@app.post("/login")
def login(user: UserLogin):
    user_data = functions.login_user(email=str(user.email).lower(),  password=user.password,)

    if user_data is None:
        raise HTTPException(status_code=401,detail="Invalid email or password",)

    token = jwt.encode(
        {"id": user_data["id"],"sub": str(user_data["id"]), "type": "access","exp": datetime.now(timezone.utc) + timedelta(minutes=30),},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return { "access_token": token,"token_type": "bearer","user": user_data,}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)