import { useState } from "react";

/**
 * AddExpense Component
 * ---------------------
 * Form to add a new expense.
 * Sends POST request to backend and updates parent state.
 *
 * Props:
 * - token (string): JWT token for authentication
 * - onNewExpense (function): Callback to add new expense to frontend state
 */

export default function AddExpense({ token, onNewExpense }) {
  const [title, setTitle] = useState("");
  const [amount, setAmount] = useState("");
  const [category, setCategory] = useState("");
  const [error, setError] = useState("");

  /**
   * handleSubmit
   * -----------------
   * Sends POST request to create a new expense.
   * Clears form and updates parent state on success.
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await fetch("http://127.0.0.1:8000/expenses", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ title, amount: parseFloat(amount), category }),
      });

      if (!res.ok) throw new Error("Failed to add expense");
      const newExpense = await res.json();

      // Add new expense to parent state
      onNewExpense(newExpense);

      // Clear form
      setTitle("");
      setAmount("");
      setCategory("");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="add-expense">
      <h2>Add Expense</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Title:</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Amount:</label>
          <input
            type="number"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            step="0.01"
            required
          />
        </div>
        <div>
          <label>Category:</label>
          <input
            type="text"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            required
          />
        </div>
        <button type="submit">Add</button>
      </form>
    </div>
  );
}
