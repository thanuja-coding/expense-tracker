import { useState } from "react";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    const response = await fetch("http://127.0.0.1:8001/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (response.ok) {
      localStorage.setItem("access_token", data.access_token);
      setMessage("Login successful");
    } else {
      setMessage(data.detail);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Login</h2>
      <input placeholder="Email" type="email" onChange={(e) => setEmail(e.target.value)} required />
      <input placeholder="Password" type="password" onChange={(e) => setPassword(e.target.value)} required />
      <button type="submit">Login</button>
      <p>{message}</p>
    </form>
  );
}

export default Login;