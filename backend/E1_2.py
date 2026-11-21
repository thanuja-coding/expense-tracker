from sqlalchemy.orm import Session
import functions

#E1
def get_expenses(user_id):
    session = Session(functions.engine)
    expenses = session.query(functions.Expenses).filter(functions.Expenses.user_id == user_id).all()
    response = []
    for expense in expenses:
        temp_expense = {
            "id": expense.id,
            "title": expense.title,
            "amount": expense.amount,
            "category": expense.category,
            "expense_date": expense.expense_date,
            "created_at": str(expense.created_at)
        }
        response.append(temp_expense)

    session.close()
    return response

#E2
def add_expense(user_id, title, amount, category, expense_date):
    session = Session(functions.engine)
    expense = functions.Expenses(user_id=user_id, title=title, amount=amount, category=category, expense_date=expense_date)
    session.add(expense)
    session.commit()
    response = {
        "id": expense.id,
        "title": expense.title,
        "amount": expense.amount,
        "category": expense.category,
        "expense_date": expense.expense_date
    }
    session.close()
    return response