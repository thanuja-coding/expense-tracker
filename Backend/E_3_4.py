from sqlalchemy.orm import Session
from datetime import datetime
from functions import engine, Expenses


#E1
def get_expenses(user_id):
    session = Session(engine)
    expenses = session.query(Expenses).filter(Expenses.user_id == user_id).all()
    response = []
    for expense in expenses:
        response.append({
            "id": expense.id,
            "title": expense.title,
            "amount": expense.amount,
            "category": expense.category,
            "expense_date": expense.expense_date,
            "created_at": expense.created_at
        })
    session.close()
    return response


#E2
def add_expense(user_id, title, amount, category, expense_date):
    session = Session(engine)
    new_expense = Expenses(
        user_id=user_id,
        title=title,
        amount=amount,
        category=category,
        expense_date=expense_date,
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    session.add(new_expense)
    session.commit()
    response = {
        "id": new_expense.id,
        "title": new_expense.title,
        "amount": new_expense.amount,
        "category": new_expense.category,
        "expense_date": new_expense.expense_date,
        "created_at": new_expense.created_at
    }
    session.close()
    return response