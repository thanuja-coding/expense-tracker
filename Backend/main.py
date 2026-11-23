from fastapi import FastAPI , HTTPException , Header , Body
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel , Field
from datetime import date
import functions


app = FastAPI(
    title = "Expense Tracker API",
    description="Register, login and manage your personal expenses",
)
ROLES = ["admin", "user"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173" , "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def authorize(token, allowed_roles):
    payload = functions.verify_token(token=token, token_type="access")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    if payload["role"] not in allowed_roles:
        raise HTTPException(status_code=403, detail="You do not have permission to do this")
    return payload


class ExpenseCreate(BaseModel):
    title: str = Field(min_length=1)
    amount: float = Field(gt=0)
    category: str = Field(min_length=1)
    expense_date: date

#E1
@app.get("/expenses")
def expenses(token = Header(None)):
    payload = authorize(token, ["admin", "user"])
    return functions.get_expenses(user_id=payload["user_id"])

#E2
@app.post("/expenses")
def add_expense(expense: ExpenseCreate , token = Header(None)):
    payload = authorize(token, ["admin", "user"])
    return functions.add_expense(user_id=payload["user_id"] , title=expense.title , amount=expense.amount , category=expense.category , expense_date=str(expense.expense_date))

@app.post("/login")
def login(email=Body(),password=Body()):
    token=functions.verify_login(email=email,password=password)
    if not token :
        raise HTTPException(status_code=401,detail="Invalid email or password")
    return token

@app.post("/refresh")
def refresh(refresh_token=Header(None)):
    payload = functions.verify_token(token=refresh_token,token_type="refresh")
    if not payload:
        raise HTTPException(status_code=401,detail="Invalid or Expired refresh token")

    access_token = functions.create_token(user_id=payload["user_id"],token_type="access",role=payload["role"])
    return {"access_token":access_token}

@app.post("/register")
def register_user(user_name=Body(),email=Body(),password=Body(),role=Body("user")):
    if role not in ROLES:
        raise HTTPException(status_code=400,detail="Role must be admin or user")
    if functions.register_user(user_name=user_name,email=email,password=password,role=role):
        return {"message":"user registered successfully"}
    raise HTTPException(status_code=400,detail="User already exists")