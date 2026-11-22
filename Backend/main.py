import os
from datetime import date, datetime, timedelta, timezone
import jwt
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr

import functions

app = FastAPI(
    title="Expense Tracker API",
    description="Register, login and manage your personal expenses",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
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
    role: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


def authorize(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


class ExpenseCreate(BaseModel):
    title: str = Field(min_length=1)
    amount: float = Field(gt=0)
    category: str = Field(min_length=1)
    expense_date: date


@app.post("/register", status_code=201)
def register(user: UserRegister):
    if not user.username.strip() or not user.password.strip():
        raise HTTPException(
            status_code=422,
            detail="Username and password cannot be empty",
        )
    response = functions.register_user(
    user.username.strip(),
    str(user.email).lower(),
    user.password,
    user.role
)

    if response is None:
        raise HTTPException(status_code=409,detail="Email address is already registered", )
    return response


@app.post("/login")
def login(user: UserLogin):
    user_data = functions.login_user(str(user.email).lower(), user.password)
    if user_data is None:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token_data = { "id": user_data["id"],"username": user_data["username"],"email": user_data["email"],"role": user_data["role"],}

    return {
        "access_token": create_access_token(token_data),
        "refresh_token": create_refresh_token(token_data),
    }


@app.get("/expenses")
def expenses(token=Header(None)):
    payload = authorize(token)
    return functions.get_expenses(user_id=payload["id"])


@app.post("/expenses")
def add_expense(expense: ExpenseCreate, token=Header(None)):
    payload = authorize(token)
    return functions.add_expense( user_id=payload["id"], title=expense.title,  amount=expense.amount,  category=expense.category,expense_date=str(expense.expense_date),)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("Main:app", host="0.0.0.0", port=8001, reload=True)