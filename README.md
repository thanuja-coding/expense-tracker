
# Expense Tracker

## Problem Statement

Every month starts with a budget and ends with a question: "Where did all my money go?"

A coffee here, a cab ride there, a subscription you forgot about. Small expenses pile up quietly, and by the time you check your balance, it's too late to remember what you spent on. Notes apps get messy, spreadsheets get abandoned, and receipts get lost.

People don't need complicated finance software. They need a simple, private place to record what they spend and see it all clearly.

The challenge is simple: How can we give every user a secure, personal space to record their expenses and view them in one place, accessible only to them?


## 1. Who is doing what

Update your own row at every check-in.

| Day | Partner | What are you doing? |
|---|---|---|
| Day 1 | Thanuja | creating tables and backend setup |
| Day 1 |  |  |
| Day 1 | | |
| Day 2 |  |  |
| Day 2 |  |  |
| Day 2 |  |  |
| Day 3 |  |  |
| Day 3 |  |  |
| Day 3 |  |  |

## 2. Endpoint tracker
| # | Method | Path | Request Body | Success Code | Error Codes |
|---|---|---|---|---|---|
| A1 | POST | /auth/register | username, email, password | 201 | 409, 422 |
| A2 | POST | /auth/login | email, password | 200 | 401, 422 |
| A3 | POST | /auth/refresh | refresh_token | 200 | 401, 422 |
| E1 | GET | /expenses | NONE (Bearer access token) | 200 | 401 |
| E2 | POST | /expenses | title, amount, category, expense_date | 201 | 401, 422 |



## How to Run

Backend

Open a terminal and navigate to the backend folder:
cd backend

Install dependencies:
pip install -r requirements.txt

Start the FastAPI server:
python -m uvicorn main:app --reload --port 8001

Open the API documentation:
Swagger UI: http://127.0.0.1:8001/docs

Frontend



Docker

Build the image:
docker build -t expense-tracker ./backend

Run the container:
docker run -d -p 8001:8001 -v ./data:/app/data expense-tracker

Deployment

Live on AWS EC2: http://<EC2_PUBLIC_IP>:8001/docs

### Flow of the Project Presentation

->	Problem statement
->	Distribution of work
->	API contracts
->	Frontend Demo
->	Swagger
->	Docker & CI/CD
->	EC2 Deployment
->	File structure
->	Conclusion
->	Interesting findings
->	QNA