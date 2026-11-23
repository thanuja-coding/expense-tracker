import { useState, useEffect } from "react";

const API_URL = "http://127.0.0.1:8001";

// Show error messages from the backend as text
function errorText(data) {
    if (typeof data.detail === "string") return data.detail;
    return data.detail[0].msg;
}

// Call a protected endpoint. If the token expired, refresh it and try again.
async function authFetch(path, options = {}) {
    options.headers = { ...options.headers, token: localStorage.getItem("access_token") };
    let response = await fetch(API_URL + path, options);

    if (response.status === 401) {
        const refresh = await fetch(API_URL + "/refresh", {
            method: "POST",
            headers: { "refresh-token": localStorage.getItem("refresh_token") || "" }
        });
        if (refresh.ok) {
            const data = await refresh.json();
            localStorage.setItem("access_token", data.access_token);
            options.headers.token = data.access_token;
            response = await fetch(API_URL + path, options);
        }
    }
    return response;
}

function App() {
    const [page, setPage] = useState(localStorage.getItem("access_token") ? "expenses" : "login");
    const [userName, setUserName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [expenses, setExpenses] = useState([]);
    const [title, setTitle] = useState("");
    const [amount, setAmount] = useState("");
    const [category, setCategory] = useState("");
    const [expenseDate, setExpenseDate] = useState("");
    const [message, setMessage] = useState("");

    async function register() {
        const response = await fetch(API_URL + "/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_name: userName, email: email, password: password })
        });
        const data = await response.json();
        if (response.ok) {
            setMessage("Registered! Please login.");
            setPage("login");
        } else {
            setMessage(errorText(data));
        }
    }

    async function login() {
        const response = await fetch(API_URL + "/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: email, password: password })
        });
        const data = await response.json();
        if (response.ok) {
            localStorage.setItem("access_token", data.access_token);
            localStorage.setItem("refresh_token", data.refresh_token);
            setMessage("");
            setPage("expenses");
        } else {
            setMessage(errorText(data));
        }
    }

    async function loadExpenses() {
        const response = await authFetch("/expenses");
        const data = await response.json();
        if (response.ok) {
            setExpenses(data);
        } else {
            logout();
        }
    }

    async function addExpense() {
        const response = await authFetch("/expenses", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title: title, amount: Number(amount), category: category, expense_date: expenseDate })
        });
        const data = await response.json();
        if (response.ok) {
            setMessage("Expense added!");
            loadExpenses();
        } else {
            setMessage(errorText(data));
        }
    }

    function logout() {
        localStorage.clear();
        setExpenses([]);
        setPage("login");
    }

    useEffect(() => {
        if (page === "expenses") loadExpenses();
    }, [page]);

    if (page === "register") {
        return (
            <div className="form-box">
                <h2>Register</h2>
                <input placeholder="Username" onChange={(e) => setUserName(e.target.value)} />
                <input placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
                <input placeholder="Password" type="password" onChange={(e) => setPassword(e.target.value)} />
                <button onClick={register}>Register</button>
                <p>{message}</p>
                <span onClick={() => { setMessage(""); setPage("login"); }}>Go to Login</span>
            </div>
        );
    }

    if (page === "login") {
        return (
            <div className="form-box">
                <h2>Login</h2>
                <input placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
                <input placeholder="Password" type="password" onChange={(e) => setPassword(e.target.value)} />
                <button onClick={login}>Login</button>
                <p>{message}</p>
                <span onClick={() => { setMessage(""); setPage("register"); }}>Go to Register</span>
            </div>
        );
    }

    return (
        <div className="dashboard">
            <h2>My Expenses</h2>
            <button onClick={logout}>Logout</button>

            <h3>Add Expense</h3>
            <input placeholder="Title" onChange={(e) => setTitle(e.target.value)} />
            <input placeholder="Amount" type="number" onChange={(e) => setAmount(e.target.value)} />
            <input placeholder="Category" onChange={(e) => setCategory(e.target.value)} />
            <input type="date" onChange={(e) => setExpenseDate(e.target.value)} />
            <button onClick={addExpense}>Add</button>
            <p>{message}</p>

            {expenses.length === 0 && <p>No expenses found.</p>}

            {expenses.map((expense) => (
                <div className="expense-card" key={expense.id}>
                    <h3>{expense.title}</h3>
                    <p>Amount: {expense.amount}</p>
                    <p>Category: {expense.category}</p>
                    <p>Date: {expense.expense_date}</p>
                </div>
            ))}
        </div>
    );
}

export default App;
