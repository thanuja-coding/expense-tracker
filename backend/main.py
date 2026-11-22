from fastapi import FastAPI , HTTPException , Header
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel , Field
from datetime import date
import jwt
import functions


app = FastAPI(
    title = "Expense Tracker API",
    description="Register, login and manage your personal expenses",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173" , "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def authorize(token):
    try:
        payload = jwt.decode(jwt=token, key="SECRETCODE", algorithms=["HS256"])
    except:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    return payload


class ExpenseCreate(BaseModel):
    title: str = Field(min_length=1)
    amount: float = Field(gt=0)
    category: str = Field(min_length=1)
    expense_date: date

#E1
@app.get("/expenses")
def expenses(token = Header(None)):
    payload = authorize(token)
    return functions.get_expenses(user_id=payload["user_id"])

#E2
@app.post("/expenses")
def add_expense(expense: ExpenseCreate , token = Header(None)):
    payload = authorize(token)
    return functions.add_expense(user_id=payload["user_id"] , title=expense.title , amount=expense.amount , category=expense.category , expense_date=str(expense.expense_date))