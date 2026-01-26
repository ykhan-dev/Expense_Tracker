/**
 * ExpenseForm.jsx
 *
 * Form for adding a new expense.
 *
 * Props:
 * - token (string): JWT token for authenticated requests
 * - onAdd (function): Callback invoked after successful creation
 */

import { useState } from "react";

export default function ExpenseForm({ token, onAdd }) {
  // Local form state
  const [title, setTitle] = useState("");
  const [amount, setAmount] = useState("");
  const [category, setCategory] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  /**
   * Handle form submission (POST request)
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/expenses", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          title,
          category,
          amount: Number(amount), // ensure backend receives a number
        }),
      });

      if (!res.ok) {
        throw new Error("Failed to add expense");
      }

      const newExpense = await res.json();
      onAdd(newExpense);

      // Reset form
      setTitle("");
      setAmount("");
      setCategory("");
    } catch (err) {
      alert(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: "1.5rem" }}>
      <h2>Add Expense</h2>

      <input
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />

      <input
        placeholder="Category"
        value={category}
        onChange={(e) => setCategory(e.target.value)}
        required
      />

      <input
        type="number"
        step="0.01"
        placeholder="Amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        required
      />

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Adding..." : "Add"}
      </button>
    </form>
  );
}
