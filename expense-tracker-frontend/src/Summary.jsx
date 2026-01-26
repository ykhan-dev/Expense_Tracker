/**
 * Summary Component
 * ---------------------
 * Displays a summary of expenses grouped by category.
 *
 * Props:
 * - expenses (array): Array of expense objects
 */

export default function Summary({ expenses }) {
  /**
   * calculateSummary
   * -----------------
   * Aggregates expenses by category and sums amounts.
   *
   * Returns:
   * - Object where keys are categories and values are total amounts
   */
  const calculateSummary = () => {
    const summary = {};
    expenses.forEach((exp) => {
      if (summary[exp.category]) {
        summary[exp.category] += exp.amount;
      } else {
        summary[exp.category] = exp.amount;
      }
    });
    return summary;
  };

  const summary = calculateSummary();

  return (
    <div className="summary">
      <h2>Summary by Category</h2>
      {Object.keys(summary).length === 0 ? (
        <p>No expenses to summarize.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Category</th>
              <th>Total Amount ($)</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(summary).map(([category, total]) => (
              <tr key={category}>
                <td>{category}</td>
                <td>{total.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
