/**
 * App.jsx
 *
 * Main App component.
 * Handles:
 * - User login/logout
 * - Fetching, adding, updating, and deleting expenses
 * - Showing Expense summary
 * - Passing token to child components
 * - Layout and spacing
 */

import { useEffect, useState } from "react";
import Login from "./Login";
import ExpenseForm from "./ExpenseForm";
import ExpenseList from "./ExpenseList";

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || null);
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(false);

  /** Login callback */
  const handleLogin = (jwtToken) => {
    setToken(jwtToken);
    localStorage.setItem("token", jwtToken);
  };

  /** Logout callback */
  const handleLogout = () => {
    setToken(null);
    localStorage.removeItem("token");
    setExpenses([]);
  };

  /** Fetch all expenses from backend */
  const fetchExpenses = async () => {
    if (!token) return;
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/expenses", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (!res.ok) {
        if (res.status === 401)
          throw new Error("Unauthorized. Please login again.");
        throw new Error("Failed to fetch expenses");
      }
      const data = await res.json();
      setExpenses(data);
    } catch (err) {
      alert(err.message);
      handleLogout();
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchExpenses();
  }, [token]);

  /** Add new expense */
  const handleAdd = (newExpense) => {
    setExpenses([...expenses, newExpense]);
  };

  /** Delete expense */
  const handleDelete = (id) => {
    setExpenses(expenses.filter((exp) => exp.id !== id));
  };

  /** Update expense */
  const handleUpdate = (updated) => {
    setExpenses(expenses.map((exp) => (exp.id === updated.id ? updated : exp)));
  };

  /** Calculate summary totals */
  const categoryTotals = expenses.reduce((acc, exp) => {
    acc[exp.category] = (acc[exp.category] || 0) + parseFloat(exp.amount);
    return acc;
  }, {});

  const totalAmount = expenses.reduce(
    (acc, exp) => acc + parseFloat(exp.amount),
    0,
  );

  /** Show login if not logged in */
  if (!token) {
    return (
      <div className="login-wrapper">
        <Login onLogin={handleLogin} />
      </div>
    );
  }

  return (
    <div className="app-container expenses-layout">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Expense Tracker</h1>
        <button
          onClick={handleLogout}
          className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
        >
          Logout
        </button>
      </div>

      {/* Expense form */}
      <ExpenseForm token={token} onAdd={handleAdd} />

      {/* Loading or Expense List */}
      {loading ? (
        <p className="mt-6 text-gray-500">Loading expenses...</p>
      ) : (
        <>
          <ExpenseList
            token={token}
            expenses={expenses}
            onDelete={handleDelete}
            onUpdate={handleUpdate}
          />

          {/* Summary */}
          {expenses.length > 0 && (
            <div className="mt-6 p-4 bg-gray-50 rounded-lg">
              <h2 className="font-bold mb-2">Summary</h2>
              <ul>
                {Object.entries(categoryTotals).map(([cat, amt]) => (
                  <li key={cat} className="flex justify-between">
                    <span>{cat}</span>
                    <span>${amt.toFixed(2)}</span>
                  </li>
                ))}
                <li className="flex justify-between font-bold border-t pt-2 mt-2">
                  <span>Total</span>
                  <span>${totalAmount.toFixed(2)}</span>
                </li>
              </ul>
            </div>
          )}
        </>
      )}
    </div>
  );
}
