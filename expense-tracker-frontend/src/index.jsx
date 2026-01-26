/**
 * index.jsx
 *
 * Entry point for the React frontend application.
 *
 * Responsibilities:
 * 1. Import the main App component.
 * 2. Mount the React app into the root div in index.html.
 * 3. Wrap the app in React.StrictMode for highlighting potential problems.
 */

import React from "react"; // Import React library
import ReactDOM from "react-dom/client"; // Import ReactDOM for rendering
import App from "./App.jsx"; // Import main App component
import "./index.css"; // Optional: global CSS for the app

// Create a React root and mount the App component
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    {/* App is wrapped in StrictMode to enable additional checks during development */}
    <App />
  </React.StrictMode>,
);
