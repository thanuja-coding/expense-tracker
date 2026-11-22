from fastapi import FastAPI , HTTPException , Header , Body
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel , Field
from datetime import date
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
    payload = functions.verify_token(token=token, token_type="access")
    if not payload:
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

@app.post("/login")
def login(email=Body(),password=Body()):
    token=functions.verify_login(email=email,password=password)
    if not token :
        raise HTTPException(status_code=401,detail="Invalid email or password")
    return token

@app.post("/register")
def register_user(username=Body(),email=Body(),password=Body()):
    if functions.register_user(username=username,email=email,password=password):
        return {"message":"user registered successfully"}
    raise HTTPException(status_code=400,detail="User already exists")