/**
 * ExpenseList.jsx
 *
 * Displays a list of expenses with inline edit support.
 *
 * Supported fields (backend-safe):
 * - title
 * - category
 * - amount
 *
 * Features:
 * - Inline Edit / Save / Cancel
 * - Category colors
 * - Auth-safe PUT & DELETE
 * - Does NOT break summary, layout, or login
 */

import { useState } from "react";

export default function ExpenseList({ token, expenses, onDelete, onUpdate }) {
  /** Track which expense is being edited */
  const [editingId, setEditingId] = useState(null);

  /** Local edit form state */
  const [formData, setFormData] = useState({
    title: "",
    category: "",
    amount: "",
  });

  /** Category → color mapping */
  const categoryColors = {
    Food: "#10b981",
    Transport: "#3b82f6",
    Entertainment: "#8b5cf6",
    Utilities: "#f59e0b",
    Shopping: "#ec4899",
    Health: "#ef4444",
    Other: "#6b7280",
  };

  /** Start editing an expense */
  const startEdit = (exp) => {
    setEditingId(exp.id);
    setFormData({
      title: exp.title,
      category: exp.category,
      amount: exp.amount,
    });
  };

  /** Cancel editing */
  const cancelEdit = () => {
    setEditingId(null);
    setFormData({ title: "", category: "", amount: "" });
  };

  /** Save edited expense */
  const saveEdit = async (id) => {
    const res = await fetch(`http://127.0.0.1:8000/expenses/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        title: formData.title,
        category: formData.category,
        amount: formData.amount,
      }),
    });

    if (!res.ok) {
      alert("Failed to update expense");
      return;
    }

    const updatedExpense = await res.json();
    onUpdate(updatedExpense);
    cancelEdit();
  };

  /** Delete expense */
  const handleDelete = async (id) => {
    if (!confirm("Delete this expense?")) return;

    const res = await fetch(`http://127.0.0.1:8000/expenses/${id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (res.ok) {
      onDelete(id);
    } else {
      alert("Failed to delete expense");
    }
  };

  /** Empty state */
  if (expenses.length === 0) {
    return <p className="mt-6 text-gray-500">No expenses added yet.</p>;
  }

  return (
    <div className="mt-6">
      <table className="expense-table">
        <thead>
          <tr>
            <th>Title</th>
            <th>Category</th>
            <th>Amount ($)</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          {expenses.map((exp) => (
            <tr key={exp.id}>
              {editingId === exp.id ? (
                <>
                  <td>
                    <input
                      value={formData.title}
                      onChange={(e) =>
                        setFormData({ ...formData, title: e.target.value })
                      }
                    />
                  </td>

                  <td>
                    <input
                      value={formData.category}
                      onChange={(e) =>
                        setFormData({ ...formData, category: e.target.value })
                      }
                    />
                  </td>

                  <td>
                    <input
                      type="number"
                      value={formData.amount}
                      onChange={(e) =>
                        setFormData({ ...formData, amount: e.target.value })
                      }
                    />
                  </td>

                  <td>
                    <button
                      className="bg-green-500 text-white px-2 py-1 rounded"
                      onClick={() => saveEdit(exp.id)}
                    >
                      Save
                    </button>
                    <button
                      className="ml-2 bg-gray-400 text-white px-2 py-1 rounded"
                      onClick={cancelEdit}
                    >
                      Cancel
                    </button>
                  </td>
                </>
              ) : (
                <>
                  <td>{exp.title}</td>

                  <td>
                    <span
                      className="expense-category"
                      style={{
                        backgroundColor:
                          categoryColors[exp.category] || "#6b7280",
                      }}
                    >
                      {exp.category}
                    </span>
                  </td>

                  <td>${parseFloat(exp.amount).toFixed(2)}</td>

                  <td className="expense-actions">
                    <button
                      className="bg-yellow-400 hover:bg-yellow-500 text-white px-2 py-1 rounded"
                      onClick={() => startEdit(exp)}
                    >
                      Edit
                    </button>

                    <button
                      className="bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded ml-2"
                      onClick={() => handleDelete(exp.id)}
                    >
                      Delete
                    </button>
                  </td>
                </>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
