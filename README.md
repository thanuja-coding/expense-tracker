# Expense Tracker

## Problem Statement

Every month starts with a budget and ends with a question: “Where did all my money go?”

A coffee here, a cab ride there, a subscription you forgot about. Small expenses pile up quietly, and by the time you check your balance, it’s too late to remember what you spent on. Notes apps get messy, spreadsheets get abandoned, and receipts get lost.

People don’t need complicated finance software. They need a simple, private place to record what they spend and see it all clearly.

The challenge is simple: How can we give every user a secure, personal space to record their expenses and view them in one place, accessible only to them?

## 1. Who Is Doing What

Update your own row at every check-in.

| Day | Partner | What are you doing? |
|---|---|---|
| Day 1 | Thammiksha | Creating tables and backend setup |
| Day 1 | Thammiksha | done with backend endpoints       |
| Day 1 |Thammiksha  |  implemening the frontend         |
| Day 2 |  |  |
| Day 2 |  |  |
| Day 2 |  |  |
| Day 3 |  |  |
| Day 3 |  |  |
| Day 3 |  |  |

## 2. Endpoint Tracker

| # | Method | Path | Request Body | Success Code | Error Codes |
|---|---|---|---|---:|---|
| A1 | POST | `/auth/register` | username, email, password | 201 | 409, 422 |
| A2 | POST | `/auth/login` | email, password | 200 | 401, 422 |
| A3 | POST | `/auth/refresh` | refresh_token | 200 | 401, 422 |
| E1 | GET | `/expenses` | None; Bearer access token | 200 | 401 |
| E2 | POST | `/expenses` | title, amount, category, expense_date | 201 | 401, 422 |

Currently implemented: A1 and A2.

## How to Run

### Backend

From the project folder, open a terminal and run:

cd Backend
pip install fastapi uvicorn sqlalchemy argon2-cffi PyJWT email-validator
python -m uvicorn main:app --reload --port 8001