from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import date
import jwt
import E1_2

app = FastAPI(
    title="Expense Tracker API",
    description="Track your personal expenses"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins={"http://localhost:5173", "http://127.0.0.1:5173"},
    allow_methods={"*"},
    allow_headers={"*"},
)

SECRET_KEY = "expense-tracker-secret-key-change-before-deploy"
ALGORITHM = "HS256"


def authorize(token):
    try:
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or Expired access token")

    if payload.get("token_type") != "access":
        raise HTTPException(status_code=401, detail="Invalid or Expired access token")
    return payload


class ExpenseCreate(BaseModel):
    title: str = Field(min_length=1)
    amount: float = Field(gt=0)
    category: str = Field(min_length=1)
    expense_date: date


#E1
@app.get("/expenses")
def expenses(token=Header(None)):
    payload = authorize(token)
    return E1_2.get_expenses(user_id=payload["user_id"])


#E2
@app.post("/expenses", status_code=201)
def create_expense(data: ExpenseCreate, token=Header(None)):
    payload = authorize(token)
    return E1_2.add_expense(payload["user_id"], data.title, data.amount, data.category, str(data.expense_date))