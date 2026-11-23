import { useState } from "react";

function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("user");
  const [message, setMessage] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    const response = await fetch("http://127.0.0.1:8001/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password, role }),
    });

    const data = await response.json();

    if (response.ok) {
      setMessage("Registered successfully");
    } else {
      setMessage(data.detail);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Register</h2>

      <input
        placeholder="Username"
        onChange={(event) => setUsername(event.target.value)}
        required
      />

      <input
        placeholder="Email"
        type="email"
        onChange={(event) => setEmail(event.target.value)}
        required
      />

      <input
        placeholder="Password"
        type="password"
        onChange={(event) => setPassword(event.target.value)}
        required
      />

      <input
        placeholder="Role"
        value={role}
        onChange={(event) => setRole(event.target.value)}
        required
      />

      <button type="submit">Register</button>
      <p>{message}</p>
    </form>
  );
}

export default Register;