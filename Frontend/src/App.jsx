import { useState, useEffect } from 'react';

const API_URL = "http://127.0.0.1:8001";

function App() {
    const [page, setPage] = useState("login");

    const [userName, setUserName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const [expenses, setExpenses] = useState([]);

    const [title, setTitle] = useState("");
    const [amount, setAmount] = useState("");
    const [category, setCategory] = useState("");
    const [expenseDate, setExpenseDate] = useState("");

    const [message, setMessage] = useState("");

    const token = localStorage.getItem("access_token");

    // Register
    async function register() {
        const response = await fetch(`${API_URL}/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_name: userName,
                email: email,
                password: password,
                role: "user"
            })
        });

        const data = await response.json();

        if (response.ok) {
            setMessage("Registration successful. Please login.");
            setPage("login");
        } else {
            setMessage(data.detail);
        }
    }

    // Login
    async function login() {
        const response = await fetch(`${API_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem("access_token", data.access_token);
            localStorage.setItem("refresh_token", data.refresh_token);

            setPage("expenses");
            loadExpenses(data.access_token);
        } else {
            setMessage(data.detail);
        }
    }

    // Get Expenses
    async function loadExpenses(accessToken = token) {
        const response = await fetch(`${API_URL}/expenses`, {
            method: "GET",
            headers: {
                "token": accessToken
            }
        });

        const data = await response.json();

        if (response.ok) {
            setExpenses(data);
        } else {
            setMessage(data.detail);
        }
    }

    // Add Expense
    async function addExpense() {
        const response = await fetch(`${API_URL}/expenses`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "token": token
            },
            body: JSON.stringify({
                title: title,
                amount: Number(amount),
                category: category,
                expense_date: expenseDate
            })
        });

        const data = await response.json();

        if (response.ok) {
            setTitle("");
            setAmount("");
            setCategory("");
            setExpenseDate("");
            setMessage("Expense added successfully!");

            loadExpenses();
        } else {
            setMessage(data.detail);
        }
    }

    // Logout
    function logout() {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");

        setExpenses([]);
        setPage("login");
        setMessage("");
    }

    useEffect(() => {
        if (token) {
            setPage("expenses");
            loadExpenses(token);
        }
    }, []);

    return (
        <div className="container">

            {page === "login" && (
                <div className="form-box">
                    <h1>Expense Tracker</h1>
                    <h2>Login</h2>

                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />

                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />

                    <button onClick={login}>Login</button>

                    <p>
                        Don't have an account?
                        <span onClick={() => {
                            setMessage("");
                            setPage("register");
                        }}>
                            Register
                        </span>
                    </p>

                    <p className="message">{message}</p>
                </div>
            )}

            {page === "register" && (
                <div className="form-box">
                    <h1>Expense Tracker</h1>
                    <h2>Register</h2>

                    <input
                        type="text"
                        placeholder="Username"
                        value={userName}
                        onChange={(e) => setUserName(e.target.value)}
                    />

                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />

                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />

                    <button onClick={register}>Create Account</button>

                    <p>
                        Already have an account?
                        <span onClick={() => {
                            setMessage("");
                            setPage("login");
                        }}>
                            Login
                        </span>
                    </p>

                    <p className="message">{message}</p>
                </div>
            )}

            {page === "expenses" && (
                <div className="dashboard">

                    <div className="top-bar">
                        <h1>Expense Tracker</h1>
                        <button onClick={logout}>Logout</button>
                    </div>

                    <h2>Add Expense</h2>

                    <div className="expense-form">

                        <input
                            type="text"
                            placeholder="Expense title"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                        />

                        <input
                            type="number"
                            placeholder="Amount"
                            value={amount}
                            onChange={(e) => setAmount(e.target.value)}
                        />

                        <input
                            type="text"
                            placeholder="Category"
                            value={category}
                            onChange={(e) => setCategory(e.target.value)}
                        />

                        <input
                            type="date"
                            value={expenseDate}
                            onChange={(e) => setExpenseDate(e.target.value)}
                        />

                        <button onClick={addExpense}>Add Expense</button>

                    </div>

                    <p className="message">{message}</p>

                    <h2>My Expenses</h2>

                    <button onClick={() => loadExpenses()}>
                        Refresh Expenses
                    </button>

                    <div className="expense-list">

                        {expenses.length === 0 ? (
                            <p>No expenses found.</p>
                        ) : (
                            expenses.map((expense) => (
                                <div className="expense-card" key={expense.id}>
                                    <h3>{expense.title}</h3>
                                    <p>Amount: ₹{expense.amount}</p>
                                    <p>Category: {expense.category}</p>
                                    <p>Date: {expense.expense_date}</p>
                                </div>
                            ))
                        )}

                    </div>

                </div>
            )}

        </div>
    );
}

export default App;